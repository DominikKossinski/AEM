import time
import os
import numpy as np

from zad4.ILS1 import ILS1
from zad4.ILS2 import ILS2
from zad4.MSLS import MSLS
from zad4.problem import Problem


def main():
    vis = False
    instances = ["kroA200", "kroB200"]
    for instance in instances:
        problem = Problem(instance)

        #msls = MSLS(problem)
        results = []
        times = []
        min_msls = None
        min_path = None
        # for i in range(10):
        #     print("MSLS", instance, i)
        #     start_time = time.time() * 1000
        #     msls.optimize()
        #     end_time = time.time() * 1000
        #     elapsed_time = end_time - start_time
        #     results.append(msls.dist)
        #     times.append(elapsed_time)
        #     if min_msls is None or min_msls > msls.dist:
        #         if min_msls is not None:
        #             os.remove("MSLS_" + instance + "_" + str(min_msls) + ".png")
        #         min_msls = msls.dist
        #         min_path = msls.path
        #         msls.visualise(True, "MSLS_" + instance, str(min_msls), min_path)
        # problem.save_results("MSLS", "", results, times)
        # avg_time = np.mean(times)

        avg_time = 1300_000
        print("Avg time", avg_time)
        results = []
        iterations = []
        min_ils2 = None
        min_path = None
        for i in range(5):
            print("ILS2", instance, i)
            ils2 = ILS2(problem, avg_time)
            ils2.optimize()
            #if min_ils2 is None or min_ils2 > ils2.dist:
                # if min_ils2 is not None:
                #     os.remove("ILS2_" + instance + "_" + str(min_ils2) + ".png")
            min_ils2 = ils2.dist
            min_path = ils2.path.copy()
            ils2.visualise(True, "ILS2_" + instance, str(min_ils2), min_path)
            results.append(ils2.dist)
            iterations.append(ils2.iterations)
        problem.save_results("ILS2", "", results, times=iterations)

if __name__ == '__main__':
    main()
