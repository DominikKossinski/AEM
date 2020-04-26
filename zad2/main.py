from init import *
from problem import Problem
from solution import Solution
from nodes import Nodes

from zad2.edges import Edges

VIS = True  # Visualise or not


def main():
    instances = ["kroB100", "kroA100"]
    styles = ["greedy", "steep"]

    # grid = list(zip(instances, styles))# + list(zip(instances, styles[::-1]))
    for instance in instances:
        problem = Problem(instance)
        for style in styles:
            # results = []
            # for _ in range(1):
            #     sol = Nodes(problem, style)
            #     sol.set_random(problem)
            #     #if VIS: sol.visualise(False, "losowy")
            #     sol.optimize_neighbours()
            #     if VIS: sol.visualise(True, "nodes", style)
            #     results.append(sol.dist)
            # problem.save_results("nodes", style, results)
            results = []
            for _ in range(100):
                ed = Edges(problem, style)
                ed.set_random(problem)
                #if VIS: ed.visualise(False)
                ed.optimize()
                #if VIS: ed.visualise(True, "edges", style)
                results.append(ed.dist)
            problem.save_results("edges", style, results)


if __name__ == '__main__':
    main()
