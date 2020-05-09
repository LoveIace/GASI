import random
import itertools
import math
from scipy.spatial.distance import squareform, pdist
import numpy as np

# GENERAL TSP FUNCTIONS:

# ...............................................................................
def to_perm(inv):
    pos = [0]*len(inv)
    for i in range(len(inv)-1,-1,-1):
        for m in range(i, len(inv)):
            if pos[m] >= inv[i]+1:
                pos[m] += 1
            pos[i] = inv[i]+1
    perm = [0]*len(inv)

    for i in range(len(inv)):
        perm[pos[i]-1] = i+1
    return perm

def to_inv(perm):
    inv = [0]*len(perm)
    for i in range(len(perm)):
        j = 0
        while perm[j] != i+1:
            if perm[j] > i+1:
                inv[i]+=1
            j+=1
    return inv

# ...............................................................................
def euclidean_distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2) if a!=b else 0

# ...............................................................................
# split tour into subtours based on list of edge indices to remove
def split_by_indices(tour, indices):
    return [
        tour[indices[i]:indices[i+1]] if i<len(indices)-1 else tour[indices[-1]:]+tour[:indices[0]]
        for i in range(len(indices))
    ]

# ...............................................................................
# compute tour length based on distance_matrix
def tour_length(tour, distance_matrix):
    tour_length = 0
    previous = tour[0]
    for current in tour:
        tour_length += distance_matrix[previous-1][current-1]
        previous = current

    return tour_length + distance_matrix[previous-1][tour[0]-1]





"""
.................................................................................
TSP tour mutations
.................................................................................

"""

# ...............................................................................
# TSP mutation - realign tour (cycling tour until first index fits)

# arguments:
# first - first value of resulting tour
def realign(tour, first=1):
    tour[:] = tour[tour.index(first):] + tour[:tour.index(first)]
    return tour[tour.index(first):] + tour[:tour.index(first)]


# ...............................................................................
# TSP mutation - relocate part of tour

# arguments:
# k - length of subtour to mutate
# shift - number to shift subtour by
# inverse - invert subtour
def relocate(tour, k, shift=0, inverse=False):
    start_index = random.randrange(len(tour))
    realign(tour, tour[start_index])
    tour[:] = tour[k:k+shift] + (tour[:k][::-1] if inverse else tour[:k]) + tour[k+shift:]
    realign(tour)

# ...............................................................................
# TSP mutation - fix k differences between tours
def k_fix(tour, better_tour, k):
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

# ...............................................................................
# TSP mutation - remove k edges, reconnect randomly
def k_change_random(tour, k):
    deleted = sorted(random.sample(range(len(tour)), k))
    subtours = split_by_indices(tour, deleted)
    subtours = [subtours[0]] + shuffle(subtours[1:])

    for sub in subtours:
        if random.random()<0.5:
            sub = sub[::-1]

    tour[:] = list(itertools.chain.from_iterable(subtours))
    realign(tour)

# ...............................................................................
def shuffle(list, start=0, end=-1):
    if end == -1:
        end = len(list)-1

    for i in range(end, start, -1): 
        j = random.randint(start, i) 
        list[i], list[j] = list[j], list[i] 
    return(list)


# ...............................................................................
def distance_matrix_from_points(points):
    np_points = np.array(points)
    dist_array = pdist(np_points)
    return squareform(dist_array).tolist()


# ...............................................................................
def all_permutations(elements):
    if len(elements) <=1:
        yield elements
    else:
        for perm in all_permutations(elements[1:]):
            for i in range(len(elements)):
                yield perm[:i] + elements[0:1] + perm[i:]


# ...............................................................................
# hamming distance of tours
def hamming_distance(tour_a, tour_b):
    distance=0
    for a, b in zip(tour_a, tour_b):
        if a!=b:
            distance+=1
    return distance


# ...............................................................................
# swap distance of tours / number of swaps to make tours equal
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

# ...............................................................................






"""
...............................................................................
K-opt Functions
...............................................................................

"""

def invert(tour, k):
    return tour[:k] + [tour[k][::-1]] + tour[k+1:]


# ...............................................................................
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

# ...............................................................................
def k_opt(tour, k, distance_matrix):
    # pick k random edges to delete from tour
    deleted = sorted(random.sample(range(len(tour)), k))

    # create list of subtours after deletion of k edges
    subtours = split_by_indices(tour, deleted)

    # create list permutations of subtours (first index fixed to avoid cyclic repetitions)
    permutations = [
        [subtours[0]]+perm
        for perm in all_permutations(subtours[1:])
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

    # modify original tour
    tour[:] = list(itertools.chain.from_iterable(best_opt))
    realign(tour)