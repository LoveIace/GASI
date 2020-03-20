import array
import random
from sympy import *

class Individual_TSP:
    def __init__(self, genotype_len):
        self.fitness = None
        self.genotype = []
        for i in range(genotype_len):
            self.genotype.append(i+1)
        shuffle(self.genotype)

class Individual_SLF:
    def __init__(self, genotype_len):
        self.fitness = None
        self.genotype = array.array('B', [0]) * genotype_len
        for i in range(genotype_len):
            if random.random() < 0.5:
                self.genotype[i] = 1

class Individual_HEF:
    def crossover(self, a, b):
        return [a[0], (a[1]+b[1])/2]

    def mutate(self):
        for i in range(len(self.genotype)):
            mutation_check = random.random()
            if mutation_check < 0.05:
               self.genotype[i][1] *= 1.1 
            elif mutation_check < 0.1:
                self.genotype[i][1] *= 0.9 

    def __init__(self, variables=None, start=None, stop=None, parent_A=None, parent_B=None, offspring=False, mutate=True):
        self.fitness = None
        self.genotype = []

        if offspring is True:
            self.genotype = list(map(lambda x, y: self.crossover(x, y), parent_A.genotype, parent_B.genotype))
            if mutate is True:
                self.mutate()
        else:
            for var in variables:
                self.genotype.append(
                        [var, random.uniform(start,stop)]
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
        print(curr, landing_spot)
        curr += i.fitness
        if curr >= landing_spot:
            return i

    print('ohnoooooooooooooooooooooooooooooooooooooooooooooooooo')

def tournament(population, tournament_size = 3):
    tournament = []
    for i in range(tournament_size):
        tournament.append(random.choice(population))
    
    max_fitness = float('-inf')
    for participant in tournament:
        if participant.fitness > max_fitness:
            max_fitness = participant.fitness
            victor = participant

    return victor


def main(pop_size, size):

    fn = sympify('-2*x**4 + 5*x**3')

    population = []
    for i in range(pop_size):
        population.append(Individual_HEF(fn.free_symbols, 0, 10))
    # for i in population:
        # print(i.genotype)

    counter = 0
    max_fitness = 0

    while(counter < 1000):   
        new_generation = []

        # evaluate fitness of each individual in current population 
        for i in population:
            i.fitness = fn.subs(i.genotype)
            if i.fitness is None:
                i.fitness = 0
            if max_fitness < i.fitness:
                best_sol = i
                max_fitness = i.fitness

        for i in population:
            # select parents for new offspring
            parent_A = tournament(population)
            parent_B = tournament(population)
            offspring = Individual_HEF(parent_A=parent_A, parent_B=parent_B, offspring=True)

            new_generation.append(offspring)

        population = new_generation.copy()
        counter+=1

    print(best_sol.genotype, best_sol.fitness)

main(30,10)