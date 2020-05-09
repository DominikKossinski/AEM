import time
import os
import numpy as np

from zad4.ILS1 import ILS1
from zad4.MSLS import MSLS
from zad4.problem import Problem


def main():
    vis = False
    instances = ["kroA200", "kroB200"]
    for instance in instances:
        problem = Problem(instance)

        msls = MSLS(problem)
        results = []
        times = []
        min_msls = None
        for _ in range(10):
            start_time = time.time() * 1000
            msls.optimize()
            end_time = time.time() * 1000
            elapsed_time = end_time - start_time
            results.append(msls.dist)
            times.append(elapsed_time)
            if min_msls is None or min_msls > msls.dist:
                if min_msls is not None:
                    os.remove("MSLS_" + instance + "_" + str(min_msls) + ".png")
                min_msls = msls.dist
                msls.visualise(True, "MSLS_" + instance, str(min_msls))
        avg_time = np.mean(times)
        print("Avg time", avg_time)
        ils1 = ILS1(problem, avg_time)
        ils1.optimize()
        # problem.save_results("MSLS", "", results, times)

if __name__ == '__main__':
    main()
