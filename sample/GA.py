import array
import random

def shuffle(list):
    for i in range(len(list)-1, 0, -1): 
        j = random.randint(0, i) 
        list[i], list[j] = list[j], list[i] 

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
    def __init__(self, genotype_len, start, stop):
        self.fitness = None
        self.genotype = []
        for i in range(genotype_len):
            self.genotype.append(random.uniform(start,stop))


def main(pop_size, size):
    population = []
    for i in range(pop_size):
        population.append(Individual_HEF(size, 0, 100))
    for i in population:
        print(i.genotype)

main(30,10)