import random
import numpy as np

from zad6.solution import Solution


class Action:

    def __init__(self, v1, v2, action):
        self.v1 = v1
        self.v2 = v2
        self.action = action


class GreedyLocalSearch(Solution):

    def __init__(self, problem):
        super(GreedyLocalSearch, self).__init__(problem)
        self.v_indexes = list(map(lambda x: x[0], self.p.vertices))
        self.n = len(self.v_indexes)
        v = self.p.vertices.copy()
        random.shuffle(v)

        self.v_indexes = list(map(lambda x: x[0], self.p.vertices))
        self.nodes = list(map(lambda x: x[0], self.nodes))
        self.unused = list(map(lambda x: x[0], self.unused))
        self.set_random()

    def set_random(self):
        random.shuffle(self.v_indexes)
        self.nodes = self.v_indexes[:int(np.ceil(self.p.n / 2))]
        self.unused = self.v_indexes[int(np.ceil(self.p.n / 2)):]

    def optimize(self):
        best_solution = None
        best_distance = None
        for i in range(100):
            print(i)
            self.set_random()
            self.run_algorithm()
            if best_distance is None or best_distance > self.dist:
                print("Best")
                best_distance = self.dist
                best_solution = self.path
        self.path = best_solution
        self.dist = best_distance

    def swap_nodes(self, start, end, nodes):
        if start == end: return nodes
        new_nodes = nodes.copy()
        if start < end:
            new_nodes = nodes.copy()
            new_nodes[0:start] = nodes[0:start]
            new_nodes[start:end + 1] = nodes[start:end + 1][::-1]
            new_nodes[end + 1:] = nodes[end + 1:]
        else:
            new_nodes[:self.n - start] = nodes[start:][::-1]
            new_nodes[self.n - start + 1: self.n - end] = nodes[end + 1: start]
            new_nodes[self.n - end:] = nodes[:end + 1][::-1]

        return new_nodes

    def calc_outer_move(self, v1, v2):
        delta = 0
        if v1 not in self.nodes:
            temp = v1
            v1 = v2
            v2 = temp
        v1_ind = self.nodes.index(v1)
        pre = self.nodes[v1_ind - 1]
        aft = self.nodes[(v1_ind + 1) % (self.n // 2)]
        delta -= self.p.distances[pre - 1, v1 - 1]
        delta -= self.p.distances[v1 - 1, aft - 1]
        delta += self.p.distances[pre - 1, v2 - 1]
        delta += self.p.distances[v2 - 1, aft - 1]
        return delta

    def calc_swap_move(self, v1, v2):
        delta = 0
        v1_ind = self.nodes.index(v1)
        v2_ind = self.nodes.index(v2)
        if abs(v2_ind - v1_ind) == 0 or abs(v1_ind - v2_ind) == (self.n // 2) - 1:
            return 0

        if v2_ind < v1_ind == v2_ind + 1:
            return 0

        delta -= self.p.distances[v1 - 1, self.nodes[v1_ind - 1] - 1]
        delta -= self.p.distances[self.nodes[(v2_ind + 1) % (self.n // 2)] - 1, v2 - 1]

        delta += self.p.distances[v1 - 1, self.nodes[(v2_ind + 1) % (self.n // 2)] - 1]
        delta += self.p.distances[self.nodes[v1_ind - 1] - 1, v2 - 1]
        return delta

    def do_swap_move(self, v1, v2):
        v1_ind = self.nodes.index(v1)
        v2_ind = self.nodes.index(v2)
        self.nodes = self.swap_nodes(v1_ind, v2_ind, self.nodes)

    def do_outer_move(self, v1, v2):
        if v1 in self.nodes:
            v1_ind = self.nodes.index(v1)
            self.nodes[v1_ind] = v2
        else:
            v2_ind = self.nodes.index(v2)
            self.nodes[v2_ind] = v1

    def run_algorithm(self):
        self.unused = np.setdiff1d(np.arange(1, self.p.n + 1), self.nodes)
        self.path = self.build_path(self.nodes)
        # print("Start distance", self.path_distance(self.path))
        while True:
            best_action = None
            best_delta = 0
            for e, i in enumerate(self.nodes):
                for j in self.nodes[e + 1:]:
                    if i == j: continue
                    delta = self.calc_swap_move(i, j)
                    if delta < 0:
                        best_action = Action(i, j, "swap")
                        best_delta = delta
                        break
                if best_delta < 0:
                    break
                for j in self.unused:
                    if i == j: continue
                    delta = self.calc_outer_move(i, j)
                    if delta < 0:
                        best_action = Action(i, j, "outer")
                        best_delta = delta
                        break
                if best_delta < 0:
                    break
            if best_delta < 0:
                if best_action.action == "swap":
                    self.do_swap_move(best_action.v1, best_action.v2)
                else:
                    self.do_outer_move(best_action.v1, best_action.v2)
                    self.unused = np.setdiff1d(np.arange(1, self.p.n + 1), self.nodes)
                # self.path = self.build_path(self.nodes)
            else:
                break
        self.path = self.build_path(self.nodes)
        self.dist = self.path_distance(self.path)
        # print("End distance:", self.dist)
        # print("Path len:", len(np.unique(self.nodes)))
