import random
import copy
from numpy import exp
from optimization import genetic_algo, firefly_algo
from util_fe import Benchmark, clip
from util_tsp import euclidean_distance
from selection import uniform
from crossover import uniform_continuous_crossover

# ...............................................................................
# Firefly class of function extreme problem
class Firefly:
    def __init__(self, function):
        self.function = function
        self.brightness = 0

        # random position from function boundaries
        self.position = [
            random.uniform(function.bounds[0], function.bounds[1])
            for i in range(function.var_count)
        ]

    def distance(self, firefly):
        return euclidean_distance(self.position, firefly.position)

    # YANG firefly movement approach
    def move_towards(self, firefly, alpha, beta, gamma):
        self.position = [
            x + beta * exp(-gamma * self.distance(firefly)** 2) * (y - x) \
              + alpha * (random.uniform(-1, 1))
            for x, y in zip(self.position, firefly.position)
        ]

    # like move_towards but only random term
    def random_walk(self, alpha):
        self.position = [
            x + alpha * (random.uniform(-1, 1))
            for x in self.position
        ]

    # dataframe values
    def values(self):
        return [x for x in self.position] + [-self.brightness if self.function.minimize else self.brightness]

# ...............................................................................
# Individual class of function extreme problem
class Individual:
    def __init__(self, function=None):
        self.fitness = 0
        self.function = function
        self.genotype = [
            random.uniform(function.bounds[0], function.bounds[1])
            for i in range(function.var_count)
        ]

    def crossover(self, mate, mutation_rate):
        # create offspring
        offspring = copy.copy(self)
        offspring.genotype = uniform_continuous_crossover(a_genotype=self.genotype,
                                                          b_genotype=mate.genotype,
                                                          a_weight=self.fitness if self.fitness >= 0 else 1/self.fitness,
                                                          b_weight=mate.fitness if mate.fitness >= 0 else 1/mate.fitness
                                                          )

        # mutate offspring
        offspring.mutate(mutation_rate)

        return offspring

    # mutation function, clip to boundaries of function search area
    def mutate(self, mutation_rate):
        for i in range(len(self.genotype)):
            if random.random() < mutation_rate:
                self.genotype[i] *= random.choice([-1, 1]) * random.uniform(0.5, 1.5)
            self.genotype[i] = clip(
                self.function.bounds[0], self.function.bounds[1], self.genotype[i])

    def values(self):
        return [genome for genome in self.genotype] + [-self.fitness if self.function.minimize else self.fitness]

# ...............................................................................
# main problem class of function extreme problem
class Function_Extreme:
    def __init__(self, function, variable_num, minimize=False):
        # get function by name, set number of variables/dimensions
        self.function = Benchmark(function, variable_num)
        self.minimize = minimize

    # create population of fireflies
    def fireflies(self, population_size):
        return [
            Firefly(self.function)
            for _ in range(population_size)
        ]

    # create population of individuals
    def population(self, population_size):
        return [
            Individual(self.function)
            for _ in range(population_size)
        ]

    # evaluate firefly position / individual chromosome
    def evaluate(self, values):
        return -self.function.value(values) if self.minimize else self.function.value(values)

    # check for optimum reach
    def is_solved(self, value):
        if self.function.optimum is None:
            return False
        elif self.minimize:
            if -1 * self.function.optimum <= value:
                return True
        elif self.function.optimum <= value:
            return True

    # df column headers
    def df_headers(self):
        return [
            i+1 for i in range(self.function.var_count)
        ]
