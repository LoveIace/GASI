import random
from optimization import genetic_algo, firefly_algo

def shuffle(list):
    for i in range(len(list)-1, 0, -1): 
        j = random.randint(0, i) 
        list[i], list[j] = list[j], list[i] 

def generate_distance_matrix(size, max_distance):
    matrix = []
    for i in range(size):
        row = []
        for j in range(i,size-1):
            row.append(j-i+1)
        row.insert(0, 0)
        for k in range(i):
            row.insert(0, k+1)
        matrix.append(row)
    return matrix

    # for i in range(size):
    #     row = []
    #     for j in range(size-1):
    #         row.append(round(random.uniform(0, max_distance), 2))
    #     row.insert(i, 0)
    #     matrix.append(row)
    # return matrix

class Individual:
    def __init__(self, length=0, parent_A=None, parent_B=None, mutation_rate=1):
        if not parent_A:
            self.length = length
            self.genotype = [
                i+1 for i in range(length)
            ]
            shuffle(self.genotype)
        else:
            self.length = parent_A.length
            # choose start and end points of section for crossover
            start = random.randrange(self.length)
            end = random.randrange(self.length)
            if start > end:
                start, end = end, start

            # genes from parent A
            from_A = parent_A.genotype[start:end+1]
            
            self.genotype = []
            # genes from parent B
            for genome in parent_B.genotype:
                if genome not in from_A:
                    self.genotype.append(genome)

            # insert A genes into B genes
            self.genotype[start:start] = from_A

            if random.random() < mutation_rate:
                self.mutate()

    def mutate(self):
        mutation_check = random.random()
        if mutation_check < 0.5:
            # generate start and end of subtour to mutate
            start = random.randrange(self.length)
            end = random.randrange(self.length)
            if start > end:
                start, end = end, start

            # slice subtour out of genotype
            cut = self.genotype[start:end+1]
            del self.genotype[start:end+1]

            if random.random() < 0.5:   
                # insert slice to newly generated spot
                start_new = random.randrange(self.length)
                self.genotype[start_new:start_new] = cut
            else:
                self.genotype[start:start] = cut[::-1]


        elif mutation_check < 0.8:
            a = random.randrange(self.length)
            b = random.randrange(self.length)
            self.genotype[a], self.genotype[b] = self.genotype[b], self.genotype[a]

    def values(self):
        return self.genotype

class Travelling_Salesman:
    def __init__(self, distance_matrix, optimum = None, minimize = False):
        self.distance_matrix = distance_matrix
        self.optimum = optimum
        self.minimize = minimize
        self.number_of_towns = len(distance_matrix)

    def population(self, population_size):
        return [
            Individual(self.number_of_towns)
            for _ in range(population_size)
        ]

    def is_solved(self, individual):
        if not self.optimum or self.optimum != individual.fitness:
            return False
        else:
            return True

    def evaluate(self, individual):
        tour_length = 0
        previous = individual.genotype[0]
        for current in individual.genotype:
            tour_length += self.distance_matrix[previous-1][current-1]
            previous = current
        individual.fitness = -tour_length if self.minimize else tour_length

    def offspring(self, parent_A, parent_B, mutation_rate):
        return Individual(parent_A=parent_A, parent_B=parent_B, mutation_rate=mutation_rate)

    def values(self):
        return [
            i+1 for i in range(self.number_of_towns)
        ]

distance_matrix = generate_distance_matrix(30,10)
problem = Travelling_Salesman(distance_matrix, minimize=True)
genetic_algo(problem, 100, 100)