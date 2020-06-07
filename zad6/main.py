import tqdm

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
    print(f"Test{results}")
    for i in tqdm.trange(1000):
        gls = GreedyLocalSearch(problem)
        gls.run_algorithm()
        if i % 100 == 0:
            gls.visualise(True, "GLS_" + "kroA200", str(gls.dist), gls.path.copy())
        results.append(gls.dist)
        nodes_lists.append(gls.nodes)
    problem.save_results("GLS", "", results)
    probCounter = ProbabilityCounter(problem, nodes_lists, results, True)
