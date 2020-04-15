import random
import numpy
import sympy
import pandas
import copy
from optimization import genetic_algo, firefly_algo

class Firefly:
    def __init__(self, function, lower, upper, alpha, beta, beta_min, gamma, minimize):
        self.function = function
        self.lower = lower
        self.upper = upper
        self.alpha = alpha
        self.beta = beta
        self.beta_min = beta_min
        self.gamma = gamma
        self.minimize = minimize
        self.position = [
            [var_symbol, random.uniform(self.lower, self.upper)]
            for var_symbol in self.function.free_symbols
        ]
        self.update_brightness()

    def solved(self):
        return False

    def update_brightness(self):
        self.brightness = self.function.subs(self.position)
        if self.minimize:
            self.brightness *= -1

    def distance(self, firefly):
        sum = 0
        for i in range(len(self.position)):
            sum += (self.position[i][1] - firefly.position[i][1]) ** 2
        return sum**0.5

    def intensity(self, firefly):
        return self.brightness * numpy.exp(-self.gamma * self.distance(firefly) ** 2)

    def move_towards(self, firefly):
        for position, target in zip(self.position, firefly.position):
            position[1] += (self.beta - self.beta_min) * numpy.exp(-self.gamma * self.distance(firefly) ** 2) * (target[1] - position[1]) + self.alpha * (random.uniform(0, 1) - 0.5) + self.beta_min

    def random_walk(self):
        for coord in self.position:
            coord[1] += self.alpha * (random.uniform(0, 1) - 0.5)

    def values(self):
        return [coord[1] for coord in self.position]

class Individual:
    def __init__(self, function=None, lower=None, upper=None, parent_A=None, parent_B=None, mutation_rate=1):
        if not parent_A:
            self.lower = lower
            self.upper = upper
            self.genotype = [
                [var, random.uniform(lower, upper)]
                for var in function.free_symbols
            ]
        else:
            self.lower = parent_A.lower
            self.upper = parent_A.upper
            self.genotype = [
                [a[0], (a[1]+b[1])/2]
                for a, b in zip(parent_A.genotype, parent_B.genotype)
            ]
            if random.random() < mutation_rate:
                self.mutate()

    def mutate(self):
        mutated_gene = random.randrange(0, len(self.genotype))
        mutation_type = random.random()
        if mutation_type < 0.2:
            self.genotype[mutated_gene][1] *= -1
        elif mutation_type < 0.6:
            self.genotype[mutated_gene][1] = numpy.clip(self.lower, self.upper, self.genotype[mutated_gene][1]*1.2)
        else:
            self.genotype[mutated_gene][1] = numpy.clip(self.lower, self.upper, self.genotype[mutated_gene][1]*0.8)

    def values(self):
        return [genome[1] for genome in self.genotype]

class Function_Extreme:
    def __init__(self, function, lower, upper, optimum = None, minimize = False):
        self.function = sympy.sympify(function)
        self.lower = lower
        self.upper = upper
        self.optimum = optimum
        self.minimize = minimize

    def fireflies(self, population_size, alpha, beta, beta_min, gamma):
        return [
            Firefly(self.function, self.lower, self.upper, alpha, beta, beta_min, gamma, self.minimize)
            for _ in range(population_size)
        ]   

    def population(self, population_size):
        return [
            Individual(self.function, self.lower, self.upper)
            for _ in range(population_size)
        ]

    def evaluate(self, individual):
        individual.fitness = self.function.subs(individual.genotype)
        if self.minimize:
            individual.fitness *= -1

    def is_solved(self, individual):
        if not self.optimum or self.optimum != individual.fitness:
            return False
        else:
            return True

    def offspring(self, a, b, mutation_rate):
        return Individual(parent_A=a, parent_B=b, mutation_rate=mutation_rate)

    def values(self):
        return [
            variable for variable in self.function.free_symbols
        ]

# problem = Function_Extreme('-20*exp(-0.2*(0.5*(x**2+y**2))**0.5)-exp(0.5*(cos(2*3.14159*x)+cos(2*3.14159*y)))+2.71828+20', -5, 5, minimize=True)
# firefly_algo(problem)

# '-20*exp(-0.2*(0.5*(x**2+y**2))**0.5)-exp(0.5*(cos(2*pi*x+cos(2*pi*y)))) + e + 20'
# '(x/40)**2 - (x/40)**3 - 10*(x/40)**4 + (y/40)**2 - (y/40)**3 - 10*(y/40)**4'

# def ackley(X,Y):
#     a=20
#     b=0.2
#     c=2*numpy.pi
#     sum_sq_term = -a * numpy.exp(-b * numpy.sqrt(X*X + Y*Y) / 2)
#     cos_term = -numpy.exp((numpy.cos(c*X) + numpy.cos(c*Y)) / 2)
#     Z = a + numpy.exp(1) + sum_sq_term + cos_term
#     return Z

# print(ackley(0,0))

# for _ in range(100):
#     print(ackley(random.uniform(-5,5),random.uniform(-5,5)))
# print(ackley(0.0000000000,0.0000000000))

# fn = sympy.sympify('2.71828/10+x')
# print(fn.subs([['x',10]]))

print("yo"+1)