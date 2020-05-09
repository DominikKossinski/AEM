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
        min_path = None
        for i in range(1):
            print("MSLS", instance, i)
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
                min_path = msls.path
                msls.visualise(True, "MSLS_" + instance, str(min_msls), min_path)
        problem.save_results("MSLS", "", results, times)
        avg_time = np.mean(times)
        print("Avg time", avg_time)
        results = []
        min_ils1 = None
        min_path = None
        for i in range(5):
            print("ILS1", instance, i)
            ils1 = ILS1(problem, avg_time)
            ils1.optimize()
            if min_ils1 is None or min_ils1 > ils1.dist:
                if min_ils1 is not None:
                    os.remove("ILS1_" + instance + "_" + str(min_ils1) + ".png")
                min_ils1 = ils1.dist
                min_path = ils1.path
                msls.visualise(True, "ILS1_" + instance, str(min_ils1), min_path)
            results.append(ils1.dist)
        problem.save_results("ILS1", "", results)

if __name__ == '__main__':
    main()
