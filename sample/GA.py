import array
import random
import re
import numpy as np
import sympy as sp
import pandas as pd

class Individual_TSP:
    def evaluate(self):
        tour_length = 0
        previous = self.genotype[0]
        for current in self.genotype:
            tour_length += self.distances[previous-1][current-1]
        self.fitness = -tour_length

    def solved(self):
        return False

    def mutate(self):
        mutation_check = random.random()
        if mutation_check < 0.5:
            # generate start and end of subtour to shift
            start = random.randrange(len(self.distances))
            end = random.randrange(len(self.distances))
            if start > end:
                start, end = end, start

            # slice subtour out of genotype
            cut = self.genotype[start:end+1]
            del self.genotype[start:end+1]

            # insert slice to newly generated spot
            start_new = random.randrange(len(self.distances))
            self.genotype[start_new:start_new] = cut
        elif mutation_check < 0.8:
            a = random.randrange(len(self.genotype))
            b = random.randrange(len(self.genotype))
            self.genotype[a], self.genotype[b] = self.genotype[b], self.genotype[a]

    def __init__(self, distances=[], parent_A=None, parent_B=None, offspring=False, mutate=True):
        self.fitness = None
        self.genotype = []
        self.distances = distances.copy()
        # crossover
        if offspring is True:
            self.distances += parent_A.distances.copy()
            # choose start and end points of section for crossover
            start = random.randrange(len(self.distances))
            end = random.randrange(len(self.distances))
            if start > end:
                start, end = end, start

            # genes from parent A
            from_A = parent_A.genotype[start:end+1]
            
            # genes from parent B
            for genome in parent_B.genotype:
                if genome not in from_A:
                    self.genotype.append(genome)

            # insert A genes into B genes
            self.genotype[start:start] = from_A

            if mutate is True:
                self.mutate()
        else:
            for i in range(len(distances)):
                self.genotype.append(i+1)
            shuffle(self.genotype)

class Individual_SLF:
    def solved(self):
        if self.CLAUSULE_COUNT == self.fitness:
            return True
        return False

    def evaluate(self):
        self.fitness = 0
        for clause in self.formula.split("∧"):
            for literal in clause.split("∨"):
                literal = literal.strip("() ")
                if literal[0] == '¬':
                    if self.genotype[literal[1]] is False:
                        self.fitness += 1
                        break
                elif self.genotype[literal] is True:
                    self.fitness += 1
                    break
        return

    def mutate(self):
        for i in range(len(self.genotype)):
            mutation_check = random.random()
            if mutation_check < 0.025:
                self.genotype[i][1] = not self.genotype[i][1]

    def __init__(self, formula=None, clausules=None, variables=None, parent_A=None, parent_B=None, offspring=False, mutate=True):
        self.fitness = None
        self.CLAUSULE_COUNT = clausules
        self.formula = formula

        if offspring is True:
            self.genotype = parent_A.genotype.copy()
            self.CLAUSULE_COUNT = parent_A.CLAUSULE_COUNT
            self.formula = parent_A.formula

            for var in self.genotype:
                if random.random() < 0.5:
                    self.genotype[var] = parent_A.genotype[var]
                else:
                    self.genotype[var] = parent_B.genotype[var]
            if mutate is True:
                self.mutate()       
        else:
            self.genotype = variables.copy()
            for var in self.genotype:
                if random.random() < 0.5:
                    self.genotype[var] = True

class Individual_HEF:
    def solved(self):
        return False

    def evaluate(self):
        self.fitness = self.problem.subs(self.genotype)

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

    def __init__(self, problem=None, variables=None, interval = (float('-inf'), float('inf')), parent_A=None, parent_B=None, offspring=False, mutate=True):
        self.fitness = None
        self.genotype = []
        self.interval = interval
        self.problem = problem

        if offspring is True:
            self.interval = parent_A.interval
            self.problem = parent_A.problem
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

def function_extreme(function, population_size = 100, generation_ceiling = 100, interval = (float('-inf'), float('inf'))):

    fn = sp.sympify(function)

    population = []
    for i in range(population_size):
        population.append(Individual_HEF(fn, fn.free_symbols, interval = interval))

    genetic_algo(population, population_size, generation_ceiling, tournament, Individual_HEF, out_path='documentation/hef_out.csv')
            
def satisfiability(formula, population_size = 100, generation_ceiling = 100):
    variables = {}
    for char in formula:
        if char.isalpha():
            variables[char] = False

    CLAUSULE_COUNT = formula.count("∧") + 1

    # create initial population
    population = []
    for i in range(population_size):
        population.append(Individual_SLF(formula, CLAUSULE_COUNT, variables))

    genetic_algo(population, population_size, generation_ceiling, roulette, Individual_SLF, out_path= 'documentation/slf_out.csv')

def add_entry(data, gen_num, genotype, fitness):
    entry = []
    entry.append(gen_num)
    for genome in genotype:
        if isinstance(genome,list):
            entry.append(genome[1])
        elif isinstance(genotype,dict):
            entry.append(genotype[genome])
        else:
            entry.append(genome)   
    entry.append(fitness)
    data.append(entry)

def columns(i):
    if isinstance(i.genotype,dict):
        return ['generation'] + list(i.genotype.keys()) + ['fitness']
    elif isinstance(i.genotype[0],list):
        return ['generation'] + list(i.problem.free_symbols) + ['fitness']
    else:
        numbers = []
        for x in range(len(i.distances)):
            numbers.append(x+1)
        return ['generation'] + numbers + ['fitness']

def genetic_algo(population, population_size, generation_ceiling, select, individual, elitism = True, out_path = False):
    generation_num = 1
    max_fitness = float('-inf')
    data = []
    best_sol = None

    while(generation_num <= generation_ceiling):   
            new_generation = []

            # evaluate fitness of each individual in current population, add to dataset
            for i in population:
                i.evaluate()
                add_entry(data, generation_num, i.genotype, i.fitness)

                if i.fitness is None:
                    continue
                if i.fitness > max_fitness:
                    best_sol = i
                    max_fitness = i.fitness
                if i.solved():
                    print("Solution found in", generation_num, "generations:", i.genotype)
                    return

            # select 2 parents, create offspring, repeat until new generation is complete
            for i in population:
                parent_A = select(population)
                parent_B = select(population)
                offspring = individual(parent_A=parent_A, parent_B=parent_B, offspring=True)

                new_generation.append(offspring)

            population = new_generation.copy()
            generation_num+=1

    if out_path is not False:
        print("Best solution found after",generation_ceiling,"generations:",best_sol.genotype, best_sol.fitness)
        print("Exporting dataset to", out_path,"...")
        df = pd.DataFrame(data) 
        df.to_csv(out_path, index=False, header=columns(best_sol)) 
        print("Dataset exported")

def travelling_salesman(distances, population_size = 100, generation_ceiling = 100):
    population = []

    for i in range(population_size):
        population.append(Individual_TSP(distances))

    genetic_algo(population, population_size, generation_ceiling, tournament, Individual_TSP, out_path='documentation/tsp_out.csv')

def generate_distance_matrix(size, max_distance):
    matrix = []
    for i in range(size):
        row = []
        for j in range(size-1):
            row.append(round(random.uniform(0, max_distance), 2))
        row.insert(i, 0)
        matrix.append(row)
    return matrix  

distance_matrix = generate_distance_matrix(500,10)  

# function_extreme('(x/40)**2 - (x/40)**3 - 10*(x/40)**4 + (y/40)**2 - (y/40)**3 - 10*(y/40)**4', interval = (-10, 10))
# satisfiability('a∧b∧c∧d∧e∧f∧g∧h∧i∧j∧k∧l∧m∧n∧o∧p∧q∧r∧s∧t∧u∧v∧w∧x∧y∧z∧A∧B∧C∧D∧E∧F∧G∧H∧I∧J∧K∧L∧M∧N∧O∧P∧Q∧R∧S∧T∧U∧V∧W∧X∧Y∧Z')
travelling_salesman(distance_matrix)



