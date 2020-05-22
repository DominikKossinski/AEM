from zad5.evolutionary_algorithm import EvolutionaryAlgorithm
from zad5.problem import Problem
import numpy as np
import random
if __name__ == '__main__':
    instances = ["kroA200", "kroB200"]

    random.seed(0)
    np.random.seed(0)
    for instance in instances:
        problem = Problem(instance)

        ea = EvolutionaryAlgorithm(problem, 130_000)
        ea.run()
