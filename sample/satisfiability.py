import random
import re
from optimization import genetic_algo, firefly_algo

class Individual:
    def __init__(self, variables=None, parent_A=None, parent_B=None, mutation_rate=1):
        if not parent_A:
            self.genotype = variables.copy()
            for var in self.genotype:
                if random.random() < 0.5:
                    self.genotype[var] = True
        else:
            self.genotype = parent_A.genotype.copy()
            for var in self.genotype:
                if random.random() < 0.5:
                    self.genotype[var] = parent_A.genotype[var]
                else:
                    self.genotype[var] = parent_B.genotype[var]
            if random.random() < mutation_rate:
                self.mutate()       

    def mutate(self):
        mutated = random.choice(list(self.genotype.keys()))
        self.genotype[mutated] = not self.genotype[mutated]

    def values(self):
        return list(self.genotype.values())

class Satisfiability:
    def __init__(self, formula):
        self.formula = [
            [ literal.strip("() ") for literal in clause.split("∨")]
            for clause in formula.split("∧")
        ]
        self.clausule_count = len(self.formula)
        self.variables = {
            char:False
            for char in re.sub(r'\W+', '', formula)
        }

    def population(self, population_size):
        return [
            Individual(self.variables)
            for _ in range(population_size)
        ]

    def evaluate(self, individual):
        individual.fitness = 0 
        for clause in self.formula:
            clause_is_true = True
            for literal in clause:
                if literal[0] == '¬':
                    if individual.genotype[literal[1]]:
                        clause_is_true = False
                        continue
                elif not individual.genotype[literal]:
                    clause_is_true = False
                    continue
            if clause_is_true:
                individual.fitness += 1               

    def is_solved(self, individual):
        return True if self.clausule_count == individual.fitness else False

    def offspring(self, parent_A, parent_B, mutation_rate):
        return Individual(parent_A=parent_A, parent_B=parent_B, mutation_rate=mutation_rate)

    def values(self):
        return [
            variable for variable in self.variables
        ]

problem = Satisfiability('a∧b∧c∧d∧e∧f∧g∧h∧i∧j∧k∧l∧m∧n∧o∧p∧q∧r∧s∧t∧u∧v∧w∧x∧y∧z∧A∧B∧C∧D∧E∧F∧G∧H∧I∧J∧K∧L∧M∧N∧O∧P∧Q∧R∧S∧T∧U∧V∧W∧X∧Y∧Z')
genetic_algo(problem)