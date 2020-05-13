import random
from numpy import exp
from util_tsp import *
import copy
from crossover import pmx, k_point_pmx


# ...............................................................................
class Firefly:
    def __init__(self, matrix):
        self.matrix = matrix
        self.brightness = 0

        # random position
        self.position = [
            i+1 for i in range(len(matrix))
        ]
        shuffle(self.position, start=1)


    # determine distance from given firefly
    def distance(self, firefly):
        # swap distance
        return swap_distance(self.position, firefly.position)
        # hamming distance
        # return hamming_distance(self.position, firefly.position)

    # move towards firefly
    def move_towards(self, firefly, alpha, beta, gamma):
        distance = self.distance(firefly)

        k = beta * exp(-gamma * distance** 2) * distance
        k = int(k)

        # use k-opt if distance small enough, else fix k differences
        if 2 < k < 5:
            k_opt(self.position, k, self.matrix)
        else:
            k_fix(self.position, firefly.position, k)

        relocate(tour=self.position,
                 k=3,
                 shift=random.randrange(3),
                 invert=True)


    # random walk function for random local search
    def random_walk(self, alpha):
        """
        Different possible random walk functions

        # kchange(self.position, len(self.position)//3)
        # relocate(tour=self.position,
        #          k=random.randrange(len(self.position)),
        #          shift=random.randrange(len(self.position)),
        #          invert=True)
        """
        # relocate(tour=self.position,
        #          k=3,
        #          shift=random.randrange(3),
        #          invert=True)
        k_opt(self.position, 4, self.matrix)

    # data row values
    def values(self):
        return self.position + [math.ceil(1/self.brightness)]


# ...............................................................................
class Individual:
    def __init__(self, length=0):
        self.fitness = 0
        self.length = length

        self.genotype = [
            i+1 for i in range(length)
        ]
        shuffle(self.genotype, start=1)

    # PMX crossover
    def crossover(self, mate, mutation_rate):
        offspring = copy.copy(self)
        offspring.genotype = pmx(self.genotype,
                                 mate.genotype,
                                 1/self.fitness,
                                 1/mate.fitness
                                 )

        if random.random() < mutation_rate:
            offspring.mutate()

        return offspring

    # genetic mutation
    def mutate(self):
        relocate(tour=self.genotype,
                k=random.randrange(self.length),
                shift=random.randrange(self.length),
                invert=True)

    # data row values
    def values(self):
        return self.genotype + [1/self.fitness]


# ...............................................................................
class Travelling_Salesman:

    def __init__(self, towns, optimum=None):
        # list of town coordinates
        self.towns = towns
        # tour length
        self.length = len(towns)
        self.distance_matrix = distance_matrix_from_points(towns)
        # optimal tour length
        self.optimum = optimum

    # function for generating a population of fireflies
    def fireflies(self, population_size):
        return [
            Firefly(self.distance_matrix)
            for _ in range(population_size)
        ]

    # function for generating a population of individuals
    def population(self, population_size):
        return [
            Individual(self.length)
            for _ in range(population_size)
        ]

    # function for determining whether global optimum was reached
    def is_solved(self, value):
        if not self.optimum or 1/self.optimum > value:
            return False
        else:
            return True

    # function for solution evaluation
    def evaluate(self, values):
        return 1 / tour_length(values, self.distance_matrix)  

    # function returning dataframe header names
    def df_headers(self):
        return [
            i+1 for i in range(self.length)
        ]