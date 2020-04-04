from init import *
from problem import Problem
from solution import Solution
from nodes import Nodes

from zad2.edges import Edges

VIS = True  # Visualise or not


def main():
    instances = ["kroA100"]  # , "kroB100"]
    styles = ["steep", "greedy"]

    # grid = list(zip(instances, styles))# + list(zip(instances, styles[::-1]))
    for instance in instances:
        problem = Problem(instance)
        for style in styles:
            # sol = Nodes(problem, style)
            # sol.set_random(problem)
            # if (not VIS): sol.visualise(False)
            # sol.optimize_neighbours()
            # if (not VIS): sol.visualise(False)

            ed = Edges(problem, style)
            ed.set_random(problem)
            if VIS: ed.visualise(False)
            ed.optimize()
            if VIS: ed.visualise(False)


if __name__ == '__main__':
    main()
