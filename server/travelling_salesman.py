import random
import numpy
from optimization import genetic_algo, firefly_algo
import util_tsp
import math


# ...............................................................................
class Firefly:
    def __init__(self, matrix, alpha, beta, beta_min, gamma):
        self.matrix = matrix
        self.alpha = alpha              # random term coefficient
        self.beta = beta                # max travel distance coefficient
        self.beta_min = beta_min        # min travel distance coefficient
        self.gamma = gamma              # light absorption coefficient

        # random position
        self.position = [
            i+1 for i in range(len(matrix))
        ]
        util_tsp.shuffle(self.position, start=1)

        # update brightness
        self.update_brightness()

    # determine distance from given firefly
    def distance(self, firefly):
        # swap distance
        return util_tsp.swap_distance(self.position, firefly.position)

        # hamming distance
        # return util_tsp.hamming_distance(self.position, firefly.position)

    # calculate brightness based on tour length in current position
    def update_brightness(self):
        self.brightness = 1 / util_tsp.tour_length(self.position, self.matrix)

    # calculate intensity at distance 
    def intensity(self, min_brightness, firefly=None):
        if not firefly:
            return (self.brightness + abs(min_brightness)*1.1)
        else:
            return (self.brightness + abs(min_brightness)*1.1) * numpy.exp(-self.gamma * util_tsp.hamming_distance(self.position, firefly.position) ** 2)

    # move towards firefly
    def move_towards(self, firefly):
        distance = self.distance(firefly)
        k = random.randrange(2, distance+1) if distance >= 2 else 2

        # use k-opt if distance small enough, else fix k differences
        if distance < 7:
            util_tsp.k_opt(self.position, k, self.matrix)
        else:
            util_tsp.k_fix(self.position, firefly.position, distance//4)

    # random walk function for random local search
    def random_walk(self):
        """
        Different possible random walk functions

        # self.position = util_tsp.kchange(self.position, len(self.position)//3)
        # self.position = util_tsp.relocate(tour=self.position,
        #                                     k=random.randrange(len(self.position)),
        #                                     shift=random.randrange(len(self.position)),
        #                                     inverse=True)
        """
        util_tsp.k_opt(self.position, 4, self.matrix)

    # data row values
    def values(self):
        return self.position + [math.ceil(1/self.brightness)]


# ...............................................................................
class Individual:
    def __init__(self, length=0, parent_A=None, parent_B=None, mutation_rate=1):
        self.fitness = 0

        # constructor for initial population
        if not parent_A:
            self.length = length
            self.genotype = [
                i+1 for i in range(length)
            ]
            util_tsp.shuffle(self.genotype, start=1)

        # constructor for offspring - PMX crossover
        else:
            self.length = parent_A.length
            crossover_point = random.randrange(self.length)

            self.genotype = parent_B.genotype[:]
            for i in range(crossover_point):
                j = parent_B.genotype.index(parent_A.genotype[i])
                self.genotype[i], self.genotype[j] = self.genotype[j], self.genotype[i]

            if random.random() < mutation_rate:
                self.mutate()

    # genetic mutation
    def mutate(self):
        util_tsp.relocate(tour=self.genotype,
                          k=random.randrange(self.length),
                          shift=random.randrange(self.length),
                          inverse=True)

    # data row values
    def values(self):
        return self.genotype + [1/self.fitness]


# ...............................................................................
class Travelling_Salesman:

    def __init__(self, towns, optimum=None):
        # list of town coordinates
        self.towns = towns
        self.distance_matrix = util_tsp.distance_matrix_from_points(
            towns)  # distance matrix for given problem
        # optimal tour length
        self.optimum = optimum

    # function for generating a population of fireflies
    def fireflies(self, population_size, alpha, beta, beta_min, gamma):
        return [
            Firefly(self.distance_matrix, alpha, beta, beta_min, gamma)
            for _ in range(population_size)
        ]

    # function for generating a population of individuals
    def population(self, population_size):
        return [
            Individual(len(self.towns))
            for _ in range(population_size)
        ]

    # function for determining whether global optimum was reached
    def is_solved(self, individual):
        if not self.optimum or 1/self.optimum > individual.fitness:
            return False
        else:
            return True

    # function for fitness evaluation of GA individual
    def evaluate(self, individual):
        individual.fitness = 1 / \
            util_tsp.tour_length(individual.genotype, self.distance_matrix)

    # offspring creation
    def offspring(self, parent_A, parent_B, mutation_rate):
        return Individual(parent_A=parent_A, parent_B=parent_B, mutation_rate=mutation_rate)

    # function returning dataframe header names
    def df_headers(self):
        return [
            i+1 for i in range(len(self.towns))
        ]
