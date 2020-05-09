import random
import numpy
import sympy
import pandas
import copy
import itertools
from optimization import genetic_algo, firefly_algo
import util_fe
from selection import uniform

class Firefly:
    def __init__(self, function, alpha, beta, beta_min, gamma, minimize):
        self.function = function
        self.alpha = alpha
        self.beta = beta
        self.beta_min = beta_min
        self.gamma = gamma
        self.minimize = minimize
        self.position = [
            random.uniform(function.bounds[0],function.bounds[1])
            for i in range(function.var_count)
        ]
        self.update_brightness()

    def solved(self):
        return False

    def update_brightness(self):
        self.brightness = self.function.value(self.position)
        if self.minimize:
            self.brightness *= -1

    def distance(self, firefly):
        sum = 0
        for i in range(len(self.position)):
            sum += (self.position[i] - firefly.position[i]) ** 2
        return sum**0.5

    def intensity(self, min_brightness, firefly = None):
        if not firefly:
            return (self.brightness + abs(min_brightness)*1.1)
        else:
            return (self.brightness + abs(min_brightness)*1.1) * numpy.exp(-self.gamma * self.distance(firefly) ** 2)

    def move_towards(self, firefly):
        self.position = [
            position + (self.beta - self.beta_min) * numpy.exp(-self.gamma * self.distance(firefly) ** 2) * (target - position) + self.alpha * (random.uniform(-1, 1)) + self.beta_min
            for position, target in zip(self.position, firefly.position)
        ]

    def random_walk(self):
        self.position = [
            coord + self.alpha * (random.uniform(-1, 1))
            for coord in self.position
        ]

    def values(self):
        return [coord for coord in self.position] + [-self.brightness if self.function.minimize else self.brightness]

class Individual:
    def __init__(self, function=None, parent_A=None, parent_B=None, mutation_rate=1):
        self.fitness = 0
        self.function = function
        if not parent_A:
            self.genotype = [
                random.uniform(function.bounds[0],function.bounds[1])
                for i in range(function.var_count)
            ]
        else:
            self.function = parent_A.function
            self.genotype = [
                (a+b)/2
                for a, b in zip(parent_A.genotype, parent_B.genotype)
            ]
            if random.random() < mutation_rate:
                self.mutate(mutation_rate)

    def mutate(self, mutation_rate):
        # index of gene to mutate
        for i in range(len(self.genotype)):
            if random.random() < mutation_rate:
                mutation_type = random.random()
                if mutation_type < 0.2:
                    self.genotype[i] *= -1
                elif mutation_type < 0.6:
                    self.genotype[i] = self.genotype[i]*1.2
                else:
                    orig = self.genotype[i]
                    self.genotype[i] = self.genotype[i]*0.8
                    if orig == self.genotype[i]:
                        self.genotype[i] = 0
            self.genotype[i] = util_fe.clip(self.function.bounds[0], self.function.bounds[1], self.genotype[i])

    def values(self):
        return [genome for genome in self.genotype] + [-self.fitness if self.function.minimize else self.fitness]

class Function_Extreme:
    def __init__(self, function, variable_num, minimize = False):
        self.function = util_fe.Benchmark(function, variable_num)
        self.minimize = minimize

    def fireflies(self, population_size, alpha, beta, beta_min, gamma):
        return [
            Firefly(self.function, alpha, beta, beta_min, gamma, self.minimize)
            for _ in range(population_size)
        ]   

    def population(self, population_size):
        return [
            Individual(self.function)
            for _ in range(population_size)
        ]

    def evaluate(self, individual):
        individual.fitness = self.function.value(individual.genotype)
        if self.minimize:
            individual.fitness *= -1  

    def is_solved(self, individual):
        if self.function.optimum is None:
            return False
        elif self.minimize:
            if -1 * self.function.optimum <= individual.fitness:
                return True
        elif self.function.optimum <= individual.fitness:
            return False

    def offspring(self, parent_A, parent_B, mutation_rate):
        return Individual(parent_A=parent_A, parent_B=parent_B, mutation_rate=mutation_rate)

    def df_headers(self):
        return [
            i+1 for i in range(self.function.var_count)
        ] 


