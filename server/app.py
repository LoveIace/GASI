# -*- coding: utf-8 -*- 

import function_extreme as fe
import travelling_salesman as tsp
import satisfiability as sat
from optimization import genetic_algo, firefly_algo
from selection import tournament, roulette, uniform
import util
import util_tsp
import util_fe
import util_sat
import inspect
import cProfile
import pandas
import json
import sys
import time
import numpy
import pandas as pd
from flask import Flask, jsonify, request, Response, stream_with_context
from flask_cors import CORS


# configuration
# DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

#...............................................................................

# Load all problems at server startup
TSP_PROBLEMS = util.load_tsp_problems()
FE_PROBLEMS = util.load_fe_problems()
SAT_PROBLEMS = util.load_sat_problems()


#...............................................................................
@app.route('/tsp', methods=['GET', 'POST'])
def run_tsp():
    response_object = {'status':'success'}
    if request.method == 'GET':
        response_object['problems'] = TSP_PROBLEMS
        return response_object
    else:
        post_data = request.get_json()
        variables, problem = post_data['variables'], post_data['problem']

        towns, optimum = problem['points'], problem['optimum']
        tsp_problem = tsp.Travelling_Salesman(towns, optimum)

        if util.get_att("Algorithm", variables) == "genetic":
            df, _, gen = genetic_algo(tsp_problem, 
                                generation_ceiling=util.get_att("Generation ceiling", variables), 
                                population_size=util.get_att("Population size", variables), 
                                mutation_rate=util.get_att("Mutation rate", variables),
                                select=util.get_att("Selection type", variables),
                                elitism=util.get_att("Elitism", variables),
                                out_path=False)
        else:
            df, _, gen = firefly_algo(tsp_problem, 
                                iteration_ceiling=util.get_att("Iteration ceiling", variables), 
                                population_size=util.get_att("Population size", variables),
                                alpha=util.get_att("Alpha", variables),
                                beta=util.get_att("Beta", variables),
                                gamma=util.get_att("Gamma", variables),
                                out_path=False)
            
        best_solution = util.get_min_overall(df)
        response_object['labels'] = [i+1 for i in range(gen)]
        response_object['datasets'] = [
            {
            'data':util.get_max(df)
            },
            {
            'data':util.get_mean(df)
            },
            {
            'data':util.get_min(df)
            }
        ]
        route = best_solution[1:-1]
        normalized_towns = util.normalize_coordinates(towns, (0,10))
        response_object['route'] = [
            {'x':normalized_towns[int(i)-1][0], 'y':normalized_towns[int(i)-1][1]} 
            for i in route
        ] + [{'x':normalized_towns[0][0], 'y':normalized_towns[0][1]}]
        response_object['best_solution'] = best_solution[-1]

        return jsonify(response_object)

#...............................................................................
@app.route('/fe', methods=['GET', 'POST'])
def run_fe():
    response_object = {'status':'success'}
    if request.method == 'GET':
        response_object['problems'] = FE_PROBLEMS
        return response_object
    else:
        post_data = request.get_json()
        variables, problem = post_data['variables'], post_data['problem']

        minimize = util_fe.get_problem_att(problem, "minimize")
        fe_problem = fe.Function_Extreme(problem.lower(), 2, minimize=minimize)

        if util.get_att("Algorithm", variables) == "genetic":
            df, data, gen = genetic_algo(fe_problem, 
                                generation_ceiling=util.get_att("Generation ceiling", variables), 
                                population_size=util.get_att("Population size", variables), 
                                mutation_rate=util.get_att("Mutation rate", variables),
                                select=util.get_att("Selection type", variables),
                                elitism=util.get_att("Elitism", variables),
                                out_path=False)
        else:
            df, data, gen = firefly_algo(fe_problem, 
                                iteration_ceiling=util.get_att("Iteration ceiling", variables), 
                                population_size=util.get_att("Population size", variables),
                                alpha=util.get_att("Alpha", variables),
                                beta=util.get_att("Beta", variables),
                                gamma=util.get_att("Gamma", variables),
                                delta=util.get_att("Delta", variables),
                                out_path=False)
        min_value = util.get_min_overall(df)[-1]
        max_value = util.get_max_overall(df)[-1]
        best_solution = min_value if minimize else max_value
        response_object['labels'] = [i+1 for i in range(gen)]
        response_object['datasets'] = [
            {
            'data':util.get_max(df)
            },
            {
            'data':util.get_mean(df)
            },
            {
            'data':util.get_min(df)
            }
        ]
        size = util.get_att("Population size", variables)

        # point data for each individual
        response_object['points'] = []
        for i in range(gen-1):
            response_object['points'].append([])
            for j in range(size):
                response_object['points'][i].append({'x':data[i*size+j][1], 'y':data[i*size+j][2]})

        # fitness distribution for each generation
        response_object['distribution'] = []
        response_object['dist_labels'] = ["" for _ in range(50)]
        for i in range(gen-1):
            chunk = data[i*size:i*size+size]
            distribution = util.get_distribution(chunk)
            response_object['distribution'].append(distribution)
        
        response_object['best_solution'] = best_solution

        return jsonify(response_object)

#...............................................................................
@app.route('/sat', methods=['GET', 'POST'])
def run_sat():
    response_object = {'status':'success'}
    if request.method == 'GET':
        response_object['problems'] = SAT_PROBLEMS
        return response_object
    else:
        post_data = request.get_json()
        minimize=False
        variables, problem = post_data['variables'], post_data['problem']
        formula = util_sat.get_sat_problem('./sat_problems/'+problem)
        sat_problem = sat.Satisfiability(formula)
        df, data, gen = genetic_algo(   sat_problem, 
                                        generation_ceiling=util.get_att("Generation ceiling", variables), 
                                        population_size=util.get_att("Population size", variables), 
                                        mutation_rate=util.get_att("Mutation rate", variables),
                                        select=util.get_att("Selection type", variables),
                                        elitism=util.get_att("Elitism", variables),
                                        out_path=False)

        min_value = util.get_min_overall(df)[-1]
        max_value = util.get_max_overall(df)[-1]
        best_solution = min_value if minimize else max_value

        response_object['labels'] = [i+1 for i in range(gen)]
        response_object['datasets'] = [
            {
            'data':util.get_max(df)
            },
            {
            'data':util.get_mean(df)
            },
            {
            'data':util.get_min(df)
            }
        ]

        size = util.get_att("Population size", variables)
        # fitness distribution for each generation
        response_object['distribution'] = []
        response_object['dist_labels'] = ["" for _ in range(50)]
        for i in range(gen-1):
            chunk = data[i*size:i*size+size]
            distribution = util.get_distribution(chunk, min_value, max_value)
            response_object['distribution'].append(distribution)

        response_object['best_solution'] = int(best_solution)
        response_object['clauses'] = formula.clauses
        response_object['satisfiable'] = True if int(best_solution) >= sat_problem.clause_count else False


        return jsonify(response_object)

#...............................................................................
if __name__ == '__main__':
    app.run()