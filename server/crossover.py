import random
import util_tsp

#...............................................................................
def uniform_discrete_crossover(a_genotype, b_genotype, a_weight = 1, b_weight = 1):
    return [
        a if random.random() < a_weight/(a_weight + b_weight) else b
        for a,b in zip(a_genotype, b_genotype)
    ]

#...............................................................................
def uniform_continuous_crossover(a_genotype, b_genotype, a_weight = 1, b_weight = 1):
    return [
        (a*a_weight+b*b_weight)/(a_weight+b_weight)
        for a,b in zip(a_genotype, b_genotype)
    ]

#...............................................................................
def k_point_crossover(a_genotype, b_genotype, k):
    length = len(a_genotype)
    if k >= length:
        k = length - 1

    crossover_points = sorted(random.sample(range(1,length), k)) + [length]

    result = a_genotype[:]
    from_b = False
    for point in crossover_points:
        if from_b:
            result[previous:point] = b_genotype[previous:point]
        from_b = not from_b
        previous = point

    return result

#...............................................................................
# partial match crossover
def pmx(a_genotype, b_genotype, a_weight=None, b_weight=None):
    length = len(a_genotype)

    if(a_weight == None):
        crossover_length = random.randrange(length)
    else:
        crossover_length = int((length / (a_weight + b_weight)) * a_weight)
    left = random.randrange(length)

    result = a_genotype[:]
    for i in range(crossover_length):
        a = (left+i)%length
        b = a_genotype.index(b_genotype[a])
        result[a], result[b] = result[b], result[a]

    return result

#...............................................................................
# k point version of partial match crossover
def k_point_pmx(a_genotype, b_genotype, k):
    length = len(a_genotype)
    crossover_points = sorted(random.sample(range(1,length), k)) + [length]

    result = a_genotype[:]
    prev=0
    from_b = True
    for point in crossover_points:
        if from_b:
            for i in range(prev, point):
                j = result.index(b_genotype[i])
                result[i], result[j] = result[j], result[i]
        from_b = not from_b
        prev = point
    return result