import tqdm

from zad6.GreedyLocalSearch import GreedyLocalSearch
from zad6.ProbabilityCounter import ProbabilityCounter
from zad6.problem import Problem

if __name__ == '__main__':
    instances = ["kroA100", "kroB100"]

    # random.seed(0)
    # np.random.seed(0)
    for instance in instances:
        problem = Problem(instance)
        results = []
        nodes_lists = []
        print(f"Test{results}")
        for i in tqdm.trange(3):
            gls = GreedyLocalSearch(problem)
            gls.run_algorithm()
            if i % 100 == 0:
                gls.visualise(True, "GLS_" + instance, str(gls.dist), gls.path.copy())
            results.append(gls.dist)
            nodes_lists.append(gls.nodes)
        problem.save_results("GLS", "", results)
        probCounter = ProbabilityCounter(problem, nodes_lists, results, instance, True)
