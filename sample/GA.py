import array
import random

# class Individual:
#     def __init__(self, genotype_len):
#         self.fitness = 0
#         self.genotype = array.array('B', [0]) * genotype_len

def shuffle(list):
    for i in range(len(list)-1, 0, -1): 
        j = random.randint(0, i + 1)  
        list[i], list[j] = list[j], list[i] 

class Individual_TSP:
    def __init__(self, number_of_cities):
        self.fitness = None
        self.genotype = []
        for i in range(number_of_cities):
            self.genotype.append(i+1)
        shuffle(self.genotype)

def main(size):
    test = Individual_TSP(size)
    print(test.genotype)

main(30)