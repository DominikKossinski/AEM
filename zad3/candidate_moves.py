from solution import Solution
import numpy as np

from edges import Edges, Action


class CandidateMoves(Edges):

    def __init__(self, problem):
        super(CandidateMoves, self).__init__(problem, "steepest")
        self.neighbours = []

    def find_five_nearest(self, vertex):
        dist = self.p.distances[vertex - 1]
        return np.argsort(dist)[1:6]


    def optimize(self):
        for i in self.v_indexes:
            self.neighbours.append(self.find_five_nearest(i))
        self.path = self.build_path(self.nodes)
        print("Start distance", self.path_distance(self.path))
        improved = True
        while improved:
            best_action = None
            best_delta = 0
            for i in self.v_indexes:
                candidates = self.neighbours[i - 1]
                for j in candidates:
                    if i == j: continue
                    if (i in self.nodes and j in self.unused) or (j in self.nodes and i in self.unused):
                        delta = self.calc_outer_move(i, j)
                        if delta < best_delta:
                            best_action = Action(i, j, "outer")
                            best_delta = delta
                    if i in self.nodes and j in self.nodes:
                        # print("Swap delta", self.calc_swap_move(i, j))
                        delta = self.calc_swap_move(i, j)
                        if delta < best_delta:
                            best_action = Action(i, j, "swap")
                            best_delta = delta
            if best_delta < 0:
                improved = True
                if best_action.action == "swap":
                    self.do_swap_move(best_action.v1, best_action.v2)
                else:
                    self.do_outer_move(best_action.v1, best_action.v2)
                self.path = self.build_path(self.nodes)
                #kself.visualise(False, "", "")
            else:
                break
        self.path = self.build_path(self.nodes)
        self.dist = self.path_distance(self.path)
        print("End distance:", self.dist)
