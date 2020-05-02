import random
import numpy
from optimization import genetic_algo, firefly_algo
import util_tsp
import math

class Firefly:
    def __init__(self, matrix, alpha, beta, beta_min, gamma):
        self.matrix = matrix
        self.alpha = alpha
        self.beta = beta
        self.beta_min = beta_min
        self.gamma = gamma
        self.position = [
                i+1 for i in range(len(matrix))
        ]
        util_tsp.shuffle(self.position, start=1)
        self.update_brightness()

    def distance(self, firefly):
        return util_tsp.hamming_distance(self.position, firefly.position)

    def update_brightness(self):
        self.brightness = 1 / util_tsp.length(self.position, self.matrix)
    
    def intensity(self, min_brightness, firefly = None):
        if not firefly:
            return (self.brightness + abs(min_brightness)*1.1)
        else:
            return (self.brightness + abs(min_brightness)*1.1) * numpy.exp(-self.gamma * util_tsp.hamming_distance(self.position, firefly.position) ** 2)

    def move_towards(self, firefly):
        distance = util_tsp.hamming_distance(self.position, firefly.position)
        k = random.randrange(2, distance+1) if distance >= 2 else 2

        if distance < 7:
            print("!!!!!!!")
            print(util_tsp.length(self.position, self.matrix))
            self.position = util_tsp.kopt(self.position, k, self.matrix)
            print(util_tsp.length(self.position, self.matrix))
        else:
            # self.position = util_tsp.relocate(self.position, k, inverse=True)
            util_tsp.fix_k(self.position, firefly.position, distance//5)

    def random_walk(self):
        # self.position = util_tsp.kchange(self.position, len(self.position)//3)
        self.position = util_tsp.relocate(self.position, random.randrange(len(self.position)), inverse=True)
        # self.position = util_tsp.kopt(self.position, 4, self.matrix)

    def values(self):
        return self.position + [math.ceil(1/self.brightness)]

class Individual:
    def __init__(self, length=0, parent_A=None, parent_B=None, mutation_rate=1):
        self.fitness = 0
        if not parent_A:
            self.length = length
            self.genotype = [
                i+1 for i in range(length)
            ]
            util_tsp.shuffle(self.genotype, start=1)
        else:
            self.length = parent_A.length
            self.genotype = []

            # choose start and end points of section for crossover
            left = random.randrange(self.length)
            right = random.randrange(self.length)

            if left < right:
                from_parent_B = parent_B.genotype[left:right]
            else:
                from_parent_B = parent_B.genotype[left:] + parent_B.genotype[:right]
            
            for gene in parent_A.genotype:
                if gene not in from_parent_B:
                    self.genotype.append(gene)
            
            self.genotype[left:left] = from_parent_B
            self.genotype = util_tsp.realign(self.genotype)
            
            if random.random() < mutation_rate:
                self.mutate()

    def mutate(self):
        self.genotype = util_tsp.relocate(tour=self.genotype, 
                                            k=random.randrange(self.length), 
                                            shift=random.randrange(self.length),
                                            inverse=bool(random.getrandbits(1)))

    def values(self):
        return self.genotype + [1/self.fitness]

class Travelling_Salesman:
    def __init__(self, towns, optimum = None, minimize = False):
        self.towns = towns
        self.distance_matrix = util_tsp.distance_matrix_from_points(towns)
        self.optimum = optimum
        self.minimize = minimize

    def fireflies(self, population_size, alpha, beta, beta_min, gamma):
        return [
            Firefly(self.towns, alpha, beta, beta_min, gamma)
            for _ in range(population_size)
        ]

    def population(self, population_size):
        return [
            Individual(len(self.towns))
            for _ in range(population_size)
        ]

    def is_solved(self, individual):
        if not self.optimum or 1/self.optimum > individual.fitness:
            return False
        else:
            return True

    def evaluate(self, individual):
        individual.fitness = 1 / util_tsp.length(individual.genotype, self.distance_matrix)

    def offspring(self, parent_A, parent_B, mutation_rate):
        return Individual(parent_A=parent_A, parent_B=parent_B, mutation_rate=mutation_rate)

    def values(self):
        return [
            i+1 for i in range(len(self.towns))
        ]