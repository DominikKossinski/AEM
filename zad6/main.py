from zad6.GreedyLocalSearch import GreedyLocalSearch
from zad6.ProbabilityCounter import ProbabilityCounter
from zad6.problem import Problem

if __name__ == '__main__':
    instances = ["kroA200"]

    # random.seed(0)
    # np.random.seed(0)
    problem = Problem("kroA200")
    results = []
    nodes_lists = []
    for i in range(100):
        print("i =", i)
        gls = GreedyLocalSearch(problem)
        gls.run_algorithm()
        if i % 20 == 0:
            gls.visualise(False, "GLS_" + "kroA200", str(gls.dist), gls.path.copy())
        results.append(gls.dist)
        nodes_lists.append(gls.nodes)
    problem.save_results("GLS", "", results)
    probCounter = ProbabilityCounter(problem, nodes_lists, results, True)
