import time

# from zad2.problem import Problem
# from zad3.candidate_moves import CandidateMoves
# from zad3.lom import Lom


from problem import Problem
from candidate_moves import CandidateMoves
from lom import Lom

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
        # for i in range(2):
        #     cm = CandidateMoves(problem)
        #     cm.set_random(problem)
        #     #cm.visualise(False, "alg", "")
        #     start_time = time.time() * 1000
        #     cm.optimize()
        #     end_time = time.time() * 1000
        #     elapsed_time = end_time - start_time
        #     cm.visualise(False, "alg", "")
        #     results.append(cm.dist)
        #     times.append(elapsed_time)
        # problem.save_results("CandidateMoves", "NoStyle", results, times)


        for i in range(1):
            lom = Lom(problem)
            lom.set_random(problem)
            #lom.visualise(False, "alg", "")
            start_time = time.time() * 1000
            lom.optimize()
            end_time = time.time() * 1000
            elapsed_time = end_time - start_time
            #cm.visualise(False, "alg", "")
            results.append(cm.dist)
            lom.visualise(False, "alg", "")
            results.append(lom.dist)
            times.append(elapsed_time)
        problem.save_results("ListOfMoves", "NoStyle", results, times)


if __name__ == '__main__':
    main()
