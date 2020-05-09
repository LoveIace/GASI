import ndtestfunc
import sympy
import sys
import util

class Benchmark():
    def __init__(self, fn, dim):
        self.minimize = get_problem_att(fn, 'minimize')
        if self.minimize:
            self.optimum = get_problem_att(fn, 'minimum')
        else:
            self.optimum = get_problem_att(fn, 'maximum')
        print(self.optimum)
        self.var_count = dim
        self.bounds = ndtestfunc.getbounds( fn, dim )
        self.name = fn
        self.value = ndtestfunc.getfuncs(fn)[0]


def clip(lower, upper, value):
    return lower if value < lower else upper if value > upper else value

def get_problem_att(name, att):
    problems = util.load_fe_problems()
    for problem in problems:
        if problem['name'].lower() == name.lower():
            return problem[att]
