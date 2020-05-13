import random
import re
import copy
from optimization import genetic_algo, firefly_algo
from crossover import uniform_discrete_crossover

class Individual:
    def __init__(self, nv=0):
        self.fitness = 0
        self.genotype = [
            True if random.random() < 0.5 else False
            for _ in range(nv)
        ]

    def crossover(self, mate, mutation_rate):
        offspring = copy.copy(self)

        offspring.genotype = uniform_discrete_crossover(a_genotype=self.genotype,
                                                        b_genotype=mate.genotype,
                                                        a_weight=self.fitness,
                                                        b_weight=mate.fitness)
        if random.random() < mutation_rate:
            offspring.mutate()

        return offspring

    def mutate(self):
        to_mutate = random.sample(range(len(self.genotype)), random.randrange(1,4))
        for index in to_mutate:
            self.genotype[index] = not self.genotype[index]

    def values(self):
        return self.genotype + [self.fitness]

class Satisfiability:
    def __init__(self, formula):
        self.formula = formula
        self.clause_count = len(formula.clauses)

    def population(self, population_size):
        return [
            Individual(self.formula.nv)
            for _ in range(population_size)
        ]

    def evaluate(self, values):
        satisfied = 0
        for clause in self.formula.clauses:
            clause_is_true = False
            for literal in clause:
                if literal < 0:
                    if not values[abs(literal)-1]:
                        clause_is_true = True
                        break
                elif values[abs(literal)-1]:
                    clause_is_true = True
                    break
            if clause_is_true:
                satisfied += 1

        return satisfied              

    def is_solved(self, value):
        return True if self.clause_count == value else False

    def df_headers(self):
        return [
            i+1 for i in range(self.formula.nv)
        ]