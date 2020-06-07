import random
import pandas
import numpy
from selection import tournament, roulette, uniform
from os import listdir
from os.path import isfile, join
import re
from pysat.formula import CNF
import tarfile

PATH = "./server/"


# ...............................................................................
def load_sat_problems(path=PATH+'sat_problems/'):
    return sorted([
        {"name": f.split('.')[0],
         "nv":int(re.findall("[0-9]+", f)[0]),
         "clauses":int(re.findall("[0-9]+", f)[1])}
        for f in listdir(path) if isfile(join(path, f))
    ], key=lambda x: x['nv'])

def get_sat_problem(name):
    path = PATH+'sat_problems/'+name+".tar.gz"
    tar = tarfile.open(path)

    f = tar.extractfile(random.choice(tar.getmembers()))
    content = f.read()

    formula = CNF(from_string=content.decode("utf-8"))
    formula.clauses = formula.clauses[:-2]

    return formula

# ...............................................................................
def load_tsp_problems(path=PATH+'tsp_problems/'):
    problems = []
    for f in listdir(path):
        with open(join(path, f)) as fp:
            name = fp.readline().split(' ')[1]
            optimum = int(fp.readline().split(' ')[1])
            line = fp.readline()
            points = []
            while line != 'EOF':
                points.append([float(line.strip().split()[1]),
                               float(line.strip().split()[2])])
                line = fp.readline()

        problems.append({
            "name": name,
            "optimum": optimum,
            "points": points
        })

    return problems

# ...............................................................................

# ISSUES WITH FITNESS DISTRIBUTION COMPUTATION OF SOME FUNCTIONS
def load_fe_problems():
    return [
        {"name": "Ackley", "minimize": True, "minimum": 4.440892098500626e-16,
            "maximum": None, "func": "f(x)="},
        {"name": "Dixonprice", "minimize": True,
            "minimum": 0, "maximum": None, "func": "f(x)="},
        {"name": "Ellipse", "minimize": True, "minimum": None,
            "maximum": None, "func": "f(x)="},
        {"name": "Griewank", "minimize": True,
            "minimum": 0, "maximum": None, "func": "f(x)="},
        {"name": "Levy", "minimize": True, "minimum": 0,
            "maximum": None, "func": "f(x)="},
        {"name": "Michalewicz", "minimize": True,
            "minimum": -1.87, "maximum": None, "func": "f(x)="},
        {"name": "Nesterov", "minimize": True,
            "minimum": None, "maximum": None, "func": "f(x)="},
        {"name": "Perm", "minimize": True, "minimum": 0,
            "maximum": None, "func": "f(x)="},
        {"name": "Powell", "minimize": True, "minimum": 0,
            "maximum": None, "func": "f(x)="},
        {"name": "Powersum", "minimize": False,
            "minimum": None, "maximum": 388, "func": "f(x)="},
        {"name": "Rastrigin", "minimize": True,
            "minimum": 0, "maximum": None, "func": "f(x)="},
        {"name": "Rosenbrock", "minimize": True,
            "minimum": 0, "maximum": None, "func": "f(x)="},
        {"name": "Schwefel", "minimize": True,
            "minimum": 0, "maximum": None, "func": "f(x)="},
        {"name": "Sphere", "minimize": True, "minimum": 0,
            "maximum": None, "func": "f(x)="},
        # {"name": "Saddle", "minimize": True, "minimum": None,
        #     "maximum": None, "func": "f(x)="},
        # {"name": "Sum2", "minimize": True, "minimum": 0,
        #     "maximum": None, "func": "f(x)="},
        {"name": "Trid", "minimize": True, "minimum": -2,
            "maximum": None, "func": "f(x)="},
        # {"name": "Zakharov", "minimize": True,
        #     "minimum": 0, "maximum": None, "func": "f(x)="}
    ]


# ...............................................................................
# get attribute for algorithm from json data
def get_att(att, data):
    selections = {
        "Tournament": tournament,
        "Uniform": uniform,
        "Roulette": roulette
    }

    for x in data:
        if x['name'] == att:
            if att == "Selection type":
                return selections[x['value']]
            return x['value']
    return False

# ...............................................................................

# get minimum / maximum / mean fitness values for each generation
def get_min(df):
    df_min = df.groupby(df.columns[0]).min()
    return df_min.iloc[:, -1].tolist()


def get_mean(df):
    df_mean = df.groupby(df.columns[0]).mean()
    return df_mean.iloc[:, -1].tolist()


def get_max(df):
    df_max = df.groupby(df.columns[0]).max()
    return df_max.iloc[:, -1].tolist()

# ...............................................................................

# get optima reached by algortihm
def get_min_overall(df):
    return df.iloc[df.iloc[:, -1].idxmin()].tolist()


def get_max_overall(df):
    return df.iloc[df.iloc[:, -1].idxmax()].tolist()


# ...............................................................................
# normalize tsp coordinates to range
def normalize_coordinates(points, range, x=0, y=1):
    swapped = numpy.swapaxes(points, 0, 1)
    min_x, max_x = min(swapped[x]), max(swapped[x])
    min_y, max_y = min(swapped[y]), max(swapped[y])
    points = numpy.swapaxes(swapped, 0, 1).tolist()

    return [
        [(point[x]-min_x)/(max_x-min_x)*(abs(range[0])+abs(range[1]) - abs(range[0])),
         (point[y]-min_y)/(max_y-min_y)*(abs(range[0])+abs(range[1]) - abs(range[0]))]
        for point in points
    ]


# ...............................................................................
# get the fitness/brightness distribution of a generation
# if normalization boundaries are not given, compute from generation
def get_distribution(data, min_=None, max_=None):
    from scipy.stats import gaussian_kde
    from statistics import stdev

    values = [row[-1] for row in data]

    if values[1:] == values[:-1]:
        return [1 for _ in range(50)]

    if min_==None:
        min_ = min(values)
    if max_==None:
        max_ = max(values)

    eps = sum([val for val in values])
    min_ -= eps/4
    max_ += eps/4

    kde = gaussian_kde(values)
    return kde.evaluate(numpy.linspace(min_, max_, 50)).tolist()
 