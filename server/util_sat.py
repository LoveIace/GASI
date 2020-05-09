from pysat.formula import CNF
import tarfile
import random

def get_sat_problem(path):
    tar = tarfile.open(path+".tar.gz", "r:gz")

    f = tar.extractfile(random.choice(tar.getmembers()))
    content = f.read()

    return CNF(from_string=content.decode("utf-8"))
