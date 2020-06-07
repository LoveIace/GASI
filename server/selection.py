import random
from statistics import stdev

# ...............................................................................
# util functions for uniform select
def find_closest(val1, val2, target):
    return val2[0] if target - val1[1] >= val2[1] - target else val1[0]

def get_index_of_closest(arr, target):
    n = len(arr)
    left = 0
    right = n - 1
    mid = 0

    if target >= arr[n - 1][1]:
        return arr[n - 1][0]
    if target <= arr[0][1]:
        return arr[0][0]

    while left < right:
        mid = (left + right) // 2 
        if target < arr[mid][1]:
            right = mid
        elif target > arr[mid][1]:
            left = mid + 1
        else:
            return arr[mid][0]

    if target < arr[mid][1]:
        return find_closest(arr[mid - 1], arr[mid], target)
    else:
        return find_closest(arr[mid], arr[mid + 1], target)

# ...............................................................................
# roulette selection, generator method
def roulette(population, pressure = 10):
    # get maximum/minimum fitness of generation
    min_bound = population[-1].fitness
    max_bound = population[0].fitness

    # compute circumference of normalized data
    circumference = 0
    pool = []
    for i in population:
        normalized_fitness = (((i.fitness - min_bound)/(max_bound - min_bound) + 1))**pressure
        circumference += normalized_fitness
        pool.append(normalized_fitness)

    # yield parents
    while True:
        landing_spot = random.uniform(0, circumference)

        curr = 0
        for index, value in enumerate(pool):
            curr+= value
            if curr>=landing_spot:
                yield population[index]
                break

# ...............................................................................
# tournament selection, generator method
def tournament(population):
    tournament_size = int(len(population) / 5)

    # yield parents
    while True:
        tournament = random.sample(population, tournament_size)
        yield max(tournament, key=lambda participant: participant.fitness)


# ...............................................................................
# uniform selection, generator method
def uniform(population):
    # create pool of fitness values
    pool = [
        (index, individual.fitness)
        for index, individual in enumerate(population)
    ]
    pool.sort(key=lambda x:x[1])

    # get min max
    fmin, fmax = pool[0][1], pool[-1][1]
    epsilon = stdev([i[1] for i in pool])

    # pick a random value, choose parent closest to said value
    while True:
        value = random.uniform(fmin-epsilon/2, fmax+epsilon/2)
        index = get_index_of_closest(pool, value)
        yield population[index]