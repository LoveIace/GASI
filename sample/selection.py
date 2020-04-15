import random

def roulette(population, min_val):
    circumference = sum(individual.fitness+min_val for individual in population)

    while True:
        landing_spot = random.uniform(0, circumference)

        curr = 0
        for individual in population:
            curr += individual.fitness + min_val
            if curr >= landing_spot:
                yield individual

def tournament(population, min_val):
    tournament_size = int(len(population) / 5)

    while True:
        tournament = [
            random.choice(population)
            for _ in range(tournament_size)
        ]
        yield max(tournament, key=lambda participant: participant.fitness)


