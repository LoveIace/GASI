import pandas
from selection import roulette, tournament, uniform
from operator import attrgetter
import json

def firefly_algo(problem, population_size = 20, iteration_ceiling = 50, alpha = 1.5, beta = 0.6, beta_min = 0.2, gamma = 0.005, out_path='documentation/FA_fe_out.csv'):   
    data = []
    iter_count = 0

    fireflies = problem.fireflies(population_size, alpha, beta, beta_min, gamma)
    min_brightness = min([firefly.brightness for firefly in fireflies])

    for firefly in fireflies:
        data.append([iter_count] + firefly.values())

    # iterate
    while(iter_count < iteration_ceiling):
        iter_count += 1
        for firefly in fireflies:
            moved = False
            for mate in fireflies:
                if firefly == mate:
                    continue
                if firefly.intensity(min_brightness) < mate.intensity(min_brightness, firefly):
                    firefly.move_towards(mate)
                    firefly.update_brightness()
                    if firefly.brightness < min_brightness:
                        min_brightness = firefly.brightness
                    moved = True
            data.append([iter_count] + firefly.values())
            if not moved:
                firefly.random_walk()

    if out_path is not False:
        print("Exporting dataset to", out_path,"...")
        df = pandas.DataFrame(data) 
        df.to_csv(out_path, index=False, header=['generation']+problem.values()+['fitness']) 
        print("Dataset exported")

    return pandas.DataFrame(data), data, iter_count

    

def genetic_algo(problem, population_size = 50, generation_ceiling = 25, select = tournament, mutation_rate = 1, elitism = True, out_path='../documentation/GA_fe_out.csv'):

    population = problem.population(population_size)
    generation_num = 0
    data = []
    best_solution = None
    max_overall = float('-inf')

    # iterate generations
    while(generation_num < generation_ceiling): 
        generation_num+=1
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

        if problem.is_solved(best_solution):
            print("Solution found in", generation_num, "generations:", individual.genotype)
            break

        # select 2 parents, create offspring, repeat until new generation is complete
        selector = select(population, min_val)
        new_generation = [
            problem.offspring(parent_A=next(selector), parent_B=next(selector), mutation_rate=mutation_rate)
            for _ in population
        ]
        if elitism:
            new_generation[0].genotype = best_solution.genotype[:]
        population = new_generation[:]

    if out_path is not False:
        print("Exporting dataset to", out_path,"...")
        df = pandas.DataFrame(data) 
        df.to_csv(out_path, index=False, header=['generation']+problem.df_headers()+['fitness']) 
        print("Dataset exported")

    return pandas.DataFrame(data), data, generation_num