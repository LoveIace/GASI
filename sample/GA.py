import array
import random
import re
import numpy as np
import sympy as sp
import pandas as pd

class Individual_TSP:
    def __init__(self, genotype_len):
        self.fitness = None
        self.genotype = []
        for i in range(genotype_len):
            self.genotype.append(i+1)
        shuffle(self.genotype)

class Individual_SLF:
    def __init__(self, variables=None, parent_A=None, parent_B=None, offspring = False):
        self.fitness = None

        if offspring is False:
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

class Individual_HEF:

    def crossover(self, a, b):
        return [a[0], (a[1]+b[1])/2]

    def mutate(self):
        for i in range(len(self.genotype)):
            mutation_check = random.random()
            if mutation_check < 0.05:
                self.genotype[i][1] *= -1
            elif mutation_check < 0.15:
                self.genotype[i][1] = np.clip(self.interval[0], self.interval[1], self.genotype[i][1]*1.1)
            elif mutation_check < 0.25:
                self.genotype[i][1] = np.clip(self.interval[0], self.interval[1], self.genotype[i][1]*0.9)

    def __init__(self, variables=None, interval = (float('-inf'), float('inf')), parent_A=None, parent_B=None, offspring=False, mutate=True):
        self.fitness = None
        self.genotype = []
        self.interval = interval

        if offspring is True:
            self.genotype = list(map(lambda x, y: self.crossover(x, y), parent_A.genotype, parent_B.genotype))
            if mutate is True:
                self.mutate()
        else:
            for var in variables:
                self.genotype.append(
                        [var, random.uniform(interval[0], interval[1])]
                    )    

def shuffle(list):
    for i in range(len(list)-1, 0, -1): 
        j = random.randint(0, i) 
        list[i], list[j] = list[j], list[i] 

def roulette(population):
    # finding circumference of the roulette wheel
    circumference = 0
    for i in population:
        circumference += i.fitness
    
    # establishing resulting landing spot of the roulette wheel
    landing_spot = random.uniform(0, circumference)

    # getting the winning individual
    curr = 0
    for i in population:
        curr += i.fitness
        if curr >= landing_spot:
            return i

def tournament(population, tournament_size = None):
    if tournament_size is None:
        tournament_size = int(len(population) / 5)

    tournament = []
    for i in range(tournament_size):
        tournament.append(random.choice(population))
    
    max_fitness = float('-inf')
    for participant in tournament:
        if participant.fitness > max_fitness:
            max_fitness = participant.fitness
            victor = participant

    return victor

def is_true(formula, values):
    fitness = 0
    for clause in formula.split("∧"):
        clause_truth_value = False
        for literal in clause.split("∨"):
            literal = literal.strip("() ")
            if literal[0] == '¬':
                if values[literal[1]] is False:
                    clause_truth_value = True
                    fitness += 1
                    break
            elif values[literal[0]] is True:
                clause_truth_value = True
                fitness += 1
                break
        if clause_truth_value is False:
            return fitness
    return fitness

def function_extreme(function, population_size = 100, generation_ceiling = 100, interval_searched = (-100, 100), interval_initial = (-100, 100)):

    fn = sp.sympify(function)

    population = []
    for i in range(population_size):
        population.append(Individual_HEF(fn.free_symbols, interval = interval_initial))

    generation_num = 1
    max_fitness = float('-inf')
    data = []

    # loop through generations
    while(generation_num <= generation_ceiling):   
        new_generation = []

        # evaluate fitness of each individual in current population, add to dataset
        for i in population:
            i.fitness = fn.subs(i.genotype)
            data.append([item for sublist in i.genotype for item in sublist] + [i.fitness, generation_num])

            if i.fitness is None:
                continue
            if i.fitness > max_fitness:
                best_sol = i
                max_fitness = i.fitness

        # select 2 parents, create offspring, repeat until new generation is complete
        for i in population:
            parent_A = tournament(population)
            parent_B = tournament(population)
            offspring = Individual_HEF(parent_A=parent_A, parent_B=parent_B, offspring=True, interval = interval_searched)

            new_generation.append(offspring)

        population = new_generation.copy()
        generation_num+=1

    # print best result
    print(best_sol.genotype, best_sol.fitness)
    df = pd.DataFrame(data) 

    df.to_csv('documentation/out.csv', index=False)  
            
def satisfiability(formula, population_size = 100, generation_ceiling = 100):
    variables = {}
    for char in formula:
        if char.isalpha():
            variables[char] = False

    CLAUSULE_COUNT = formula.count("∧") + 1
    population = []

    for i in range(population_size):
        population.append(Individual_SLF(variables))

    generation_num = 1

    while(generation_num <= generation_ceiling):  
        print(generation_num)

        for i in population:
            i.fitness = is_true(formula, i.genotype)
            if i.fitness == CLAUSULE_COUNT:
                print("Solution for",formula, "found in", generation_num, "generations:", i.genotype)
                return

        new_generation = []
        for i in population:
                parent_A = roulette(population)
                parent_B = roulette(population)
                offspring = Individual_SLF(parent_A=parent_A, parent_B=parent_B, offspring=True)

                new_generation.append(offspring)

        population = new_generation.copy()
        generation_num+=1
    
    


# function_extreme('(x/40)**2 - (x/40)**3 - 10*(x/40)**4 + (y/40)**2 - (y/40)**3 - 10*(y/40)**4', 100, 100, (-10, 10))
# ∨∧¬

satisfiability('a∧b∧c∧d∧e∧f∧g∧h∧i∧j∧k∧l∧m∧n∧o∧p∧q∧r∧s∧t∧u∧v', generation_ceiling=100)