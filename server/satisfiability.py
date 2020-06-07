import random
import re
import copy
from optimization import genetic_algo, firefly_algo
from crossover import uniform_discrete_crossover

# ...............................................................................
# GA individual class for satisfiability problem
class Individual:
    def __init__(self, nv=0):
        self.fitness = 0
        # pick random bools for each formula variable
        self.genotype = [
            True if random.random() < 0.5 else False
            for _ in range(nv)
        ]

    # crossover method
    def crossover(self, mate, mutation_rate):
        # create offspring
        offspring = copy.copy(self)
        # weighted uniform discrete crossover
        offspring.genotype = uniform_discrete_crossover(a_genotype=self.genotype,
                                                        b_genotype=mate.genotype,
                                                        a_weight=self.fitness,
                                                        b_weight=mate.fitness)
        # mutate offspring
        offspring.mutate(mutation_rate)

        return offspring

    def mutate(self, mutation_rate):
        # invert genes with probability of mutation_rate
        self.genotype = [
            not gene if random.random()<mutation_rate else gene
            for gene in self.genotype
        ]

    # dataframe values
    def values(self):
        return self.genotype + [self.fitness]


# ...............................................................................
# main problem class of satisfiability problem
class Satisfiability:
    def __init__(self, formula):
        self.formula = formula
        self.clause_count = len(formula.clauses)

    # create GA population
    def population(self, population_size):
        return [
            Individual(self.formula.nv)
            for _ in range(population_size)
        ]

    # evaluate values for formula
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

    # check if all satisfied
    def is_solved(self, value):
        return True if self.clause_count == value else False

    # df column headers
    def df_headers(self):
        return [
            i+1 for i in range(self.formula.nv)
        ]