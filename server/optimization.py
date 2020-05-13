import pandas
from selection import roulette, tournament, uniform
from numpy import exp
from copy import copy
    
def firefly_algo(problem, population_size = 20, iteration_ceiling = 50, alpha = 1.5, beta = 0.6, beta_min = 0.2, gamma = 0.005, delta=0.97, out_path='../documentation/FA_out.csv'):   
    data = []
    iter_count = 1

    fireflies = problem.fireflies(population_size)
    for firefly in fireflies:
        firefly.brightness = problem.evaluate(firefly.position)
        data.append([iter_count] + firefly.values())

    # find lowest brightness
    min_brightness = min(fireflies, key=lambda f: f.brightness).brightness

    # iterate
    while iter_count <= iteration_ceiling:
        for firefly in fireflies:
            moved = False
            for mate in fireflies:
                # don't compare to itself
                if firefly == mate:
                    continue
                # compute light intensity based on distance
                firefly_intensity = firefly.brightness + abs(min_brightness)
                mate_intensity = (mate.brightness + abs(min_brightness)) * exp(-gamma * firefly.distance(mate) ** 2)
                
                
                if firefly_intensity < mate_intensity:
                    # move firefly
                    firefly.move_towards(mate, alpha, beta, gamma)
                    # update brightness
                    firefly.brightness = problem.evaluate(firefly.position)
                    # update min_brightness
                    if firefly.brightness < min_brightness:
                        min_brightness = firefly.brightness
                    moved = True
            # if firefly hasn't moved, do random local search
            # if not moved:
            #     firefly.random_walk(alpha)

            data.append([iter_count] + firefly.values())

        best = max(fireflies, key=lambda f: f.brightness)
        if problem.is_solved(best.brightness):
            return
        best.random_walk(alpha)

        # update alpha value, increase iteration counter
        alpha *= delta
        iter_count += 1

    if out_path is not False:
        print("Exporting dataset to", out_path,"...")
        df = pandas.DataFrame(data) 
        df.to_csv(out_path, index=False, header=['generation']+problem.values()+['fitness']) 
        print("Dataset exported")

    return pandas.DataFrame(data), data, iter_count



def genetic_algo(problem, population_size = 50, generation_ceiling = 25, select = tournament, mutation_rate = 0.25, elitism = 0.02, out_path='../documentation/GA_out.csv'):

    population = problem.population(population_size)

    generation_num = 1
    data = []

    # iterate generations
    while generation_num <= generation_ceiling: 
        min_val = float('inf')
        print(generation_num)

        # evaluate fitness of each individual in current population, add to dataset
        for individual in population:
            individual.fitness = problem.evaluate(individual.genotype)
            data.append([generation_num] + individual.values())

            if individual.fitness is None:
                continue
            # move lower boundary
            if individual.fitness < min_val:
                min_val = individual.fitness

        # sort population by fitness
        population.sort(key=lambda individual: individual.fitness, reverse=True)

        # if population contains the problem solution break cycle
        if problem.is_solved(population[0].fitness):
            break

        # account for elitism
        new_generation = [
            copy(population[i])
            for i in range(int(elitism * population_size))
        ]

        # select 2 parents, create offspring, repeat until new generation is complete
        selector = select(population)
        while len(new_generation) < population_size:
            new_generation.append(
                next(selector).crossover(next(selector), mutation_rate)
            )

        # introduce new population
        population = new_generation[:]
        generation_num+=1

    if out_path is not False:
        print("Exporting dataset to", out_path,"...")
        df = pandas.DataFrame(data) 
        df.to_csv(out_path, index=False, header=['generation']+problem.df_headers()+['fitness']) 
        print("Dataset exported")

    return pandas.DataFrame(data), data, generation_num