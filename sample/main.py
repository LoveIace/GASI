import function_extreme as fe
import travelling_salesman as tsp
import satisfiability as sat
from optimization import genetic_algo, firefly_algo
import util_tsp
import inspect
import cProfile
import pandas

towns = util_tsp.benchmark()

tsp_problem = tsp.Travelling_Salesman(towns, minimize=True, optimum=27603)
# sat_problem = sat.Satisfiability('a∧b∧c∧d∧e∧f∧g∧h∧i∧j∧k∧l∧m∧n∧o∧p∧q∧r∧s∧t∧u∧v∧w∧x∧y∧z∧A∧B∧C∧D∧E∧F∧G∧H∧I∧J∧K∧L∧M∧N∧O∧P∧Q∧R∧S∧T∧U∧V∧W∧X∧Y∧Z')
# fe_problem = fe.Function_Extreme('(x/40)**2 - (x/40)**3 - 10*(x/40)**4 + (y/40)**2 - (y/40)**3 - 10*(y/40)**4', -10, 10)

# def find_best_parameters(tsp_problem):
#     for argument in inspect.getargspec(genetic_algo)[0]:
#         print(argument)

# find_best_parameters(tsp_problem)

points = pandas.DataFrame(tsp_problem.towns) 
points.to_csv('documentation/towns.csv', index=False, header=['x','y'])

genetic_algo(tsp_problem, generation_ceiling=100, population_size=100)
# cProfile.run('firefly_algo(tsp_problem, gamma=0, iteration_ceiling=100, population_size=100)')
# firefly_algo(tsp_problem, gamma=0, iteration_ceiling=100, population_size=100)