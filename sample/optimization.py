import pandas
from selection import roulette, tournament
from operator import attrgetter

def firefly_algo(problem, population_size = 20, iteration_ceiling = 50, alpha = 1.5, beta = 0.6, beta_min = 0.2, gamma = 0.005, out_path='documentation/FA_fe_out.csv'):   
    data = []
    iter_count = 0

    fireflies = problem.fireflies(population_size, alpha, beta, beta_min, gamma)
    min_brightness = min([firefly.brightness for firefly in fireflies])

    for firefly in fireflies:
        data.append([iter_count] + firefly.values())

    while(iter_count < iteration_ceiling):
        iter_count += 1
        print(iter_count)   
        for firefly in fireflies:
            for mate in fireflies:
                if firefly == mate:
                    continue
                # print("comparing:",firefly.intensity(min_brightness), "to", mate.intensity(min_brightness, firefly), "(",mate.intensity(min_brightness),")")
                if firefly.intensity(min_brightness) < mate.intensity(min_brightness, firefly):
                    firefly.move_towards(mate)
                    firefly.update_brightness()
                    if firefly.brightness < min_brightness:
                        min_brightness = firefly.brightness
            data.append([iter_count] + firefly.values())
        best = max(fireflies, key=attrgetter('brightness'))
        if best.brightness == problem.optimum:
            print("Solution found in", iter_count, "iterations:", best.brightness)
            return
        best.random_walk()

    if out_path is not False:
        print("Exporting dataset to", out_path,"...")
        df = pandas.DataFrame(data) 
        df.to_csv(out_path, index=False, header=['generation']+problem.values()+['fitness']) 
        print("Dataset exported")

def genetic_algo(problem, population_size = 50, generation_ceiling = 25, select = tournament, mutation_rate = 1, elitism = True, out_path='documentation/GA_fe_out.csv'):
    
    population = problem.population(population_size)
    generation_num = 1
    data = []
    best_solution = None
    max_overall = float('-inf')

    while(generation_num <= generation_ceiling): 
        print(generation_num) 
        min_val = float('inf')

        # evaluate fitness of each individual in current population, add to dataset
        for individual in population:
            problem.evaluate(individual)
            data.append([generation_num] + individual.values())

            if individual.fitness is None:
                continue
            if individual.fitness > max_overall:
                max_overall = individual.fitness
                best_solution = individual
            # move lower boundary
            if individual.fitness < min_val:
                min_val = individual.fitness

            if problem.is_solved(individual):
                print("Solution found in", generation_num, "generations:", individual.genotype)
                return

        # select 2 parents, create offspring, repeat until new generation is complete
        selector = select(population, min_val)
        new_generation = [
            problem.offspring(parent_A=next(selector), parent_B=next(selector), mutation_rate=mutation_rate)
            for _ in population
        ]
        if elitism:
            new_generation[0] = best_solution

        population = new_generation.copy()
        generation_num+=1

    if out_path is not False:
        print("Exporting dataset to", out_path,"...")
        df = pandas.DataFrame(data) 
        df.to_csv(out_path, index=False, header=['generation']+problem.values()+['fitness']) 
        print("Dataset exported")