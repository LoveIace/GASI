import pandas
from selection import roulette, tournament

def firefly_algo(problem, population_size = 10, iteration_ceiling = 30, alpha = 1, beta = 0.6, beta_min = 0.2, gamma = 0.05, out_path='documentation/FA_fe_out.csv'):   
    data = []
    iter_count = 0

    fireflies = problem.fireflies(population_size, alpha, beta, beta_min, gamma)
    for firefly in fireflies:
        data.append([iter_count] + firefly.values() + [firefly.brightness])

    while(iter_count < iteration_ceiling):
        iter_count += 1
        print(iter_count)
        best = None
        max_brightness = float('-inf')
        for firefly in fireflies:
            for mate in fireflies:
                if firefly == mate:
                    continue
                if firefly.brightness < mate.brightness:
                    firefly.move_towards(mate)
                    firefly.update_brightness()
                    if firefly.brightness > max_brightness:
                        best = firefly
                        max_brightness = firefly.brightness
            data.append([iter_count] + firefly.values() + [firefly.brightness])
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
        for i in population:
            problem.evaluate(i)
            # add_entry(data, generation_num, i.genotype, i.fitness)
            data.append([generation_num] + i.values() + [i.fitness])

            if i.fitness is None:
                continue
            if i.fitness > max_overall:
                max_overall = i.fitness
                best_solution = i
            # move lower boundary
            if i.fitness < min_val:
                min_val = i.fitness

            if problem.is_solved(i):
                print("Solution found in", generation_num, "generations:", i.genotype)
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

    print("Best solution found after",generation_ceiling,"generations:",best_solution.genotype, -best_solution.fitness if problem.minimize else best_solution.fitness)
    if out_path is not False:
        print("Exporting dataset to", out_path,"...")
        df = pandas.DataFrame(data) 
        df.to_csv(out_path, index=False, header=['generation']+problem.values()+['fitness']) 
        print("Dataset exported")