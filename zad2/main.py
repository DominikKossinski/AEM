from init import *
from problem import Problem
from solution import Solution
from nodes import Nodes

VIS = True #Visualise or not

def main():
    instances = ["kroA100"]#, "kroB100"]
    styles = ["steep"]#, "greedy"]

    grid = list(zip(instances, styles))# + list(zip(instances, styles[::-1]))

    for instance, style in grid:
        problem = Problem(instance)
        sol = Nodes(problem, style)
        sol.set_random(problem)
        if(VIS): sol.visualise(False)
        sol.optimize_neighbours()
        if(VIS): sol.visualise(False)

if __name__ == '__main__':
    main()