from init import *
from problem import Problem
from solution import Solution
from nodes import Nodes

def main():
    instances = ["kroA100"]#, "kroB100"]
    styles = ["steep"]#, "greedy"]

    grid = list(zip(instances, styles))# + list(zip(instances, styles[::-1]))

    for instance, style in grid:
        problem = Problem(instance)
        sol = Nodes(problem, style)
        sol.set_random(problem)
        # sol.visualise(False)
        sol.outside_move()

if __name__ == '__main__':
    main()