import time

from zad2.problem import Problem
from zad3.candidate_moves import CandidateMoves


def main():
    instances = ["kroA100", "kroB100"]
    for instance in instances:
        results = []
        times = []
        problem = Problem(instance)
        for i in range(50):
            cm = CandidateMoves(problem)
            cm.set_random(problem)
            #cm.visualise(False, "alg", "")
            start_time = time.time() * 1000
            cm.optimize()
            end_time = time.time() * 1000
            elapsed_time = end_time - start_time
            #cm.visualise(False, "alg", "")
            results.append(cm.dist)
            times.append(elapsed_time)
        problem.save_results("CandidateMoves", "NoStyle", results, times)


if __name__ == '__main__':
    main()
