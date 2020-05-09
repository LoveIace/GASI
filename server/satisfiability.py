import random
import re
from optimization import genetic_algo, firefly_algo

class Individual:
    def __init__(self, nv=0, parent_A=None, parent_B=None, mutation_rate=1):
        self.fitness = 0
        if not parent_A:
            self.genotype = [
                True if random.random() < 0.5 else False
                for _ in range(nv)
            ]

        else:
            self.genotype = [
                parent_A.genotype[i] if random.random() < 0.5 else parent_B.genotype[i]
                for i in range(len(parent_A.genotype))
            ]
            if random.random() < mutation_rate:
                self.mutate()       

    def mutate(self):
        to_mutate = random.sample(range(len(self.genotype)), random.randrange(1,4))
        for index in to_mutate:
            self.genotype[index] = not self.genotype[index]

    def values(self):
        return self.genotype + [self.fitness]

class Satisfiability:
    def __init__(self, formula):
        self.formula = formula
        self.clause_count = len(formula.clauses[:-2])

    def population(self, population_size):
        return [
            Individual(self.formula.nv)
            for _ in range(population_size)
        ]

    def evaluate(self, individual):
        individual.fitness = 0 
        for clause in self.formula.clauses[:-2]:
            clause_is_true = False
            for literal in clause:
                if literal < 0:
                    if not individual.genotype[abs(literal)-1]:
                        clause_is_true = True
                        break
                elif individual.genotype[abs(literal)-1]:
                    clause_is_true = True
                    break
            if clause_is_true:
                individual.fitness += 1               

    def is_solved(self, individual):
        return True if self.clause_count == individual.fitness else False

    def offspring(self, parent_A, parent_B, mutation_rate):
        return Individual(parent_A=parent_A, parent_B=parent_B, mutation_rate=mutation_rate)

    def df_headers(self):
        return [
            i+1 for i in range(self.formula.nv)
        ]