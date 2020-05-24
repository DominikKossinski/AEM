from zad5.evolutionary_algorithm import EvolutionaryAlgorithm
from zad5.problem import Problem
import numpy as np
import random

if __name__ == '__main__':
    instances = ["kroA200", "kroB200"]

    # random.seed(0)
    # np.random.seed(0)
    time = 1300_000
    for instance in instances:
        problem = Problem(instance)
        results = []
        iterations = []
        for i in range(1):
            ea = EvolutionaryAlgorithm(problem, time)
            ea.run()
            ea.visualise(True, "EA_" + instance, str(ea.dist), ea.path.copy())
            results.append(ea.dist)
            iterations.append(ea.iterations)
        problem.save_results("EA", "", results, times=iterations)
