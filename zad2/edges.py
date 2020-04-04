import traceback

from init import *

from solution import Solution


class Edges(Solution):

    def __init__(self, problem, style):
        super(Edges, self).__init__(problem)
        print(self.p.vertices)
        self.style = style

    def calculate_delta(self, i, j):
        delta = 0
        delta -= self.p.distances[self.nodes[i - 1][0] - 1, self.nodes[i][0] - 1]
        delta -= self.p.distances[self.nodes[j][0] - 1, self.nodes[(j + 1) % 50][0] - 1]
        delta += self.p.distances[self.nodes[i - 1][0] - 1, self.nodes[j][0] - 1]
        delta += self.p.distances[self.nodes[i][0] - 1, self.nodes[(j + 1) % 50][0] - 1]
        return delta

    def optimize(self):
        if self.style == 'greedy':
            self.optimize_greedy()
        elif self.style == 'steep':
            self.optimize_steepest()

    def optimize_greedy(self):
        self.path = self.build_path(self.nodes)
        print("Start distance", self.path_distance(self.path))
        for a in range(100):
            for i in range(len(self.nodes)):
                for j in range(len(self.nodes)):
                    if i != j:
                        delta = self.calculate_delta(i, j)
                        if delta < 0:
                            rev = self.nodes[i:j + 1][::-1]
                            self.nodes[i:j + 1] = rev
                            self.path = self.build_path(self.nodes)
        self.path = self.build_path(self.nodes)
        print("End distance:", self.path_distance(self.path))

    def optimize_steepest(self):
        self.path = self.build_path(self.nodes)
        print("Start distance", self.path_distance(self.path))
        min_delta = 0
        for a in range(100):
            for i in range(len(self.nodes)):
                for j in range(i + 1, len(self.nodes) - 1):
                    delta = self.calculate_delta(i, j)
                    if delta < min_delta:
                        min_delta =  min_delta
                        rev = self.nodes[i:j + 1][::-1]
                        self.nodes[i:j + 1] = rev

        self.path = self.build_path(self.nodes)
        print("Current distance:", self.path_distance(self.path))
