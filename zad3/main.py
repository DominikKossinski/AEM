import time

# from zad2.problem import Problem
# from zad3.candidate_moves import CandidateMoves
# from zad3.lom import Lom


from problem import Problem
from candidate_moves import CandidateMoves
from lom import Lom
from edges import Edges

def main():
    instances = ["kroA200", "kroB200"]
    for instance in instances:
        problem = Problem(instance)
      
        results = []
        times = []
        for i in range(100):
            print(i)
            cm = CandidateMoves(problem)
            cm.set_random(problem)
            #cm.visualise(False, "alg", "")
            start_time = time.time() * 1000
            cm.optimize()
            end_time = time.time() * 1000
            elapsed_time = end_time - start_time
            # cm.visualise(False, "alg", "")
            results.append(cm.dist)
            times.append(elapsed_time)
        problem.save_results("CandidateMoves", "NoStyle", results, times)

        results = []
        times = []
        for i in range(100):
            print(i)
            lom = Lom(problem)
            lom.set_random(problem)
            #lom.visualise(False, "alg", "")
            start_time = time.time() * 1000
            lom.optimize()
            end_time = time.time() * 1000
            elapsed_time = end_time - start_time
            # lom.visualise(False, "alg", "")
            results.append(lom.dist)
            times.append(elapsed_time)
        problem.save_results("ListOfMoves", "NoStyle", results, times)

        # results = []
        # times = []
        # for i in range(100):
        #     print(i)
        #     edg = Edges(problem, 'steep')
        #     edg.set_random(problem)
        #     #edg.visualise(False, "alg", "")
        #     start_time = time.time() * 1000
        #     edg.optimize()
        #     end_time = time.time() * 1000
        #     elapsed_time = end_time - start_time
        #     # edg.visualise(False, "alg", "")
        #     results.append(edg.dist)
        #     times.append(elapsed_time)
        # problem.save_results("Edges", "Steep", results, times)


if __name__ == '__main__':
    main()
