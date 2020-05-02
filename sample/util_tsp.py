import random
import itertools
import math

# GENERAL TSP FUNCTIONS:

def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2) if a!=b else 0

def benchmark(type=None):
    strong = "1 20833.3333 17100.0000 2 20900.0000 17066.6667 3 21300.0000 13016.6667 4 21600.0000 14150.0000 5 21600.0000 14966.6667 6 21600.0000 16500.0000 7 22183.3333 13133.3333 8 22583.3333 14300.0000 9 22683.3333 12716.6667 10 23616.6667 15866.6667 11 23700.0000 15933.3333 12 23883.3333 14533.3333 13 24166.6667 13250.0000 14 25149.1667 12365.8333 15 26133.3333 14500.0000 16 26150.0000 10550.0000 17 26283.3333 12766.6667 18 26433.3333 13433.3333 19 26550.0000 13850.0000 20 26733.3333 11683.3333 21 27026.1111 13051.9444 22 27096.1111 13415.8333 23 27153.6111 13203.3333 24 27166.6667 9833.3333 25 27233.3333 10450.0000 26 27233.3333 11783.3333 27 27266.6667 10383.3333 28 27433.3333 12400.0000 29 27462.5000 12992.2222"
    strong = strong.split(" ")

    if not type:
        return [
            [float(strong[3*i+1]), float(strong[3*i+2])]
            for i in range(29)
        ]

def split_by_indices(tour, indices):
    return [
        tour[indices[i]:indices[i+1]] if i<len(indices)-1 else tour[indices[-1]:]+tour[:indices[0]]
        for i in range(len(indices))
    ]

def length(tour, distance_matrix):
    tour_length = 0
    previous = tour[0]
    for current in tour:
        tour_length += distance_matrix[previous-1][current-1]
        previous = current

    return tour_length + distance_matrix[previous-1][tour[0]-1]

def realign(tour, first=1):
    return tour[tour.index(first):] + tour[:tour.index(first)]

def relocate(tour, k, shift=0, inverse=False):
    start_index = random.randrange(len(tour))
    tour = realign(tour, tour[start_index])
    tour = tour[k:k+shift] + (tour[:k][::-1] if inverse else tour[:k]) + tour[k+shift:]

    return realign(tour)

def fix_k(tour, better_tour, k):
    mismatches = [
        better_tour.index(y)
        for x, y in zip(tour, better_tour) if y != x
    ]
    for _ in range(k):
        a = random.choice(mismatches)
        b = tour.index(better_tour[a])

        tour[a], tour[b] = tour[b], tour[a]
        mismatches.remove(a)
        if better_tour[b] == tour[b]:
            mismatches.remove(b)
        if len(mismatches) == 0:
            return      
    return

def kchange(tour, k):
    deleted = sorted(random.sample(range(len(tour)), k))
    subtours = split_by_indices(tour, deleted)
    subtours = [subtours[0]] + shuffle(subtours[1:])

    for sub in subtours:
        if random.random()<0.5:
            sub = sub[::-1]
    tour = list(itertools.chain.from_iterable(subtours))
    return realign(tour)

def shuffle(list, start=0, end=-1):
    if end == -1:
        end = len(list)-1

    for i in range(end, start, -1): 
        j = random.randint(start, i) 
        list[i], list[j] = list[j], list[i] 
    return(list)

def distance_matrix_from_points(points):
    return [
        [distance(i, j) for j in points]
        for i in points
    ]

def generate_distance_matrix(size, max_distance=10, type='random'):
    matrix = []
    if type == 'random':
        for i in range(size):
            row = [
                round(random.uniform(0, max_distance), 2)
                for _ in range(size-1)
            ]
            row.insert(i, 0)
            matrix.append(row)
        return matrix

    elif type == 'line':
        for i in range(size):
            row = []
            for j in range(i,size-1):
                row.append(j-i+1)
            row.insert(0, 0)
            for k in range(i):
                row.insert(0, k+1)
            matrix.append(row)
        return matrix

def all_perms(elements):
    if len(elements) <=1:
        yield elements
    else:
        for perm in all_perms(elements[1:]):
            for i in range(len(elements)):
                # nb elements[0:1] works in both string and list contexts
                yield perm[:i] + elements[0:1] + perm[i:]

# PERMUTATION DISTANCE FUNCTIONS:

def hamming_distance(tour_a, tour_b):
    distance=0
    for a, b in zip(tour_a, tour_b):
        if a!=b:
            distance+=1
    return distance

def swap_distance(tour_a, tour_b):
    arr = [
        tour_b.index(tour_a[i])
        for i in range(len(tour_a))
    ]
    return min_swaps(arr)

def min_swaps(arr): 
    n = len(arr) 

    arrpos = [*enumerate(arr)] 
    arrpos.sort(key = lambda it:it[1]) 

    vis = {k:False for k in range(n)} 

    ans = 0
    for i in range(n): 
        if vis[i] or arrpos[i][0] == i: 
            continue

        cycle_size = 0
        j = i 
        while not vis[j]: 

            vis[j] = True
            j = arrpos[j][0] 
            cycle_size += 1
        if cycle_size > 0: 
            ans += (cycle_size - 1) 

    return ans 

# K-OPT FUNCTIONS:

def invert(tour, k):
    return tour[:k] + [tour[k][::-1]] + tour[k+1:]

def try_invert(tour, distance_matrix, total = 0, last = -1, k = 0):
    if k == len(tour):
        return tour, total + distance_matrix[last-1][tour[0][0]-1]
    curr = tour[k]
    if curr[0] == curr[-1]:
        return try_invert(tour, distance_matrix, total + distance_matrix[last-1][curr[0]-1], curr[-1], k+1)
    a_tour, a_len = try_invert(tour, distance_matrix, total + distance_matrix[last-1][curr[0]-1], curr[-1], k+1)
    b_tour, b_len = try_invert(invert(tour, k), distance_matrix, total + distance_matrix[last-1][curr[-1]-1], curr[0], k+1)
    if a_len > b_len:
        return b_tour, b_len
    else:
        return a_tour, a_len       

def kopt(tour, k, distance_matrix):
    # pick k random edges to delete from tour
    deleted = sorted(random.sample(range(len(tour)), k))

    # create list of subtours after deletion of k edges
    subtours = split_by_indices(tour, deleted)

    # create list permutations of subtours (first index fixed to avoid cyclic repetitions)
    permutations = [
        [subtours[0]]+perm
        for perm in all_perms(subtours[1:])
    ]

    min_len = float('inf')
    best_opt = None
    # for each permutation try inverting every possible combination of subtours
    for permutation in permutations:
        opt, opt_len = try_invert(permutation, distance_matrix)
        # find the best one
        if opt_len < min_len:
            min_len = opt_len
            best_opt = opt
    
    tour = list(itertools.chain.from_iterable(best_opt))

    return realign(tour)