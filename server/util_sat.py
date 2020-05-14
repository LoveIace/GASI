from pysat.formula import CNF
import tarfile
import random

def get_sat_problem(path):
    tar = tarfile.open(path)

    f = tar.extractfile(random.choice(tar.getmembers()))
    content = f.read()

    formula = CNF(from_string=content.decode("utf-8"))
    formula.clauses = formula.clauses[:-2]

    return formula
