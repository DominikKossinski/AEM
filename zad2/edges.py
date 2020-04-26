import sys
import traceback

from init import *

from solution import Solution
from random import randint


class Edges(Solution):

    def __init__(self, problem, style):
        super(Edges, self).__init__(problem)
        print(self.p.vertices)
        self.style = style

    def calculate_delta(self, i, j):
        delta = 0
        delta -= self.p.distances[self.nodes[i][0] - 1, self.nodes[(i + 1) % 50][0] - 1]
        # print("Odj: ", self.nodes[i][0] - 1, " ", self.nodes[(i + 1) % 50][0] - 1)

        delta -= self.p.distances[self.nodes[j - 1][0] - 1, self.nodes[j][0] - 1]
        # print("Odj: ", self.nodes[j - 1][0] - 1, " ", self.nodes[j][0] - 1)

        delta += self.p.distances[self.nodes[i][0] - 1, self.nodes[j - 1][0] - 1]
        # print("Dod: ", self.nodes[i][0] - 1, " ", self.nodes[j - 1][0] - 1)

        delta += self.p.distances[self.nodes[(i + 1) % 50][0] - 1, self.nodes[j][0] - 1]
        # print("Dod: ", self.nodes[(i + 1) % 50][0] - 1, " ", self.nodes[j][0] - 1)
        return delta

    def optimize(self):
        if self.style == 'greedy':
            print("Greedy")
            self.new_greedy()
        elif self.style == 'steep':
            self.new_steepest()

    def rotate(self, a=None):
        if a is None:
            a = randint(1, len(self.nodes))
        for i in range(a):
            x = self.nodes.pop()
            self.nodes.insert(0, x)

    def new_greedy(self):
        print("Start distance", self.path_distance(self.path))
        self.path = self.build_path(self.nodes)
        improved = True
        while improved:
            improved = False
            #self.rotate()
            for b in range(len(self.path)):
                self.rotate(1)
                for i in range(1, len(self.path) - 2):
                    for j in range(i + 1, len(self.path)):
                        if j - i == 1: continue
                        new_nodes = self.nodes[:]
                        new_nodes[i:j] = self.nodes[j - 1:i - 1:-1]
                        if self.path_distance(self.build_path(new_nodes)) < self.path_distance(self.path):
                            self.path = self.build_path(new_nodes)
                            self.nodes = new_nodes
                            improved = True

        self.path = self.build_path(self.nodes)
        self.dist = self.path_distance(self.path)
        print("End distance:", self.path_distance(self.path))

    def new_steepest(self):
        print("Start distance", self.path_distance(self.path))
        self.path = self.build_path(self.nodes)
        improved = True
        while improved:
            improved = False
            best_delta = 0
            best_nodes = None
            self.rotate()
            for b in range(len(self.path)):
                self.rotate(1)
                for i in range(1, len(self.path) - 2):
                    for j in range(i + 1, len(self.path)):
                        if j - i == 1: continue
                        new_nodes = self.nodes[:]
                        new_nodes[i:j] = self.nodes[j - 1:i - 1:-1]
                        new_dist = self.path_distance(self.build_path(new_nodes))
                        curr_dist = self.path_distance(self.path)
                        if new_dist < curr_dist:
                            if curr_dist - new_dist > best_delta:
                                best_nodes = new_nodes
                                best_delta = curr_dist - new_dist
                                #improved = True
            if best_delta > 0:
                self.path = self.build_path(best_nodes)
                self.nodes = best_nodes
                improved = True

        self.path = self.build_path(self.nodes)
        self.dist = self.path_distance(self.path)
        print("End distance:", self.path_distance(self.path))

    def optimize_greedy(self):
        self.path = self.build_path(self.nodes)
        print("Start distance", self.path_distance(self.path))
        found = True
        a = 0
        while found:
            print("\n\n\n\nA = ", a)
            a += 1
            found = False
            for i in range(len(self.nodes) - 1):
                for j in range(i + 2, len(self.nodes)):
                    if True:  # i != j and abs(i - j) > 1:
                        delta = self.calculate_delta(i, j)
                        if delta < 0:
                            print("Delta: ", delta)
                            # print(self.nodes)
                            prev_dist = self.path_distance(self.path)
                            rev = self.nodes[i + 1:j][::-1]
                            print("i = ", i, " j = ", j)
                            # print(rev)
                            self.nodes[i + 1:j] = rev
                            # print(self.nodes)
                            # exit(0)
                            found = True

                            self.path = self.build_path(self.nodes)
                            self.dist = self.path_distance(self.path)
                            print("Act dist:", self.dist)
                            if len(self.nodes) != 50:
                                exit(-50)

                            if self.dist - prev_dist != delta:
                                print("Delta error")
                                exit(-20)
                            break

        self.path = self.build_path(self.nodes)
        self.dist = self.path_distance(self.path)
        print("End distance:", self.path_distance(self.path))

    def optimize_steepest(self):
        self.path = self.build_path(self.nodes)
        print("Start distance", self.path_distance(self.path))
        min_delta = 0
        found = True
        while found:
            found = False
            for i in range(len(self.nodes) - 1):
                for j in range(i + 2, len(self.nodes)):
                    delta = self.calculate_delta(i, j)
                    if delta < min_delta:
                        min_delta = min_delta
                        rev = self.nodes[i + 1:j][::-1]
                        self.nodes[i + 1:j] = rev
                        found = True

        self.path = self.build_path(self.nodes)
        self.dist = self.path_distance(self.path)
        print("Current distance:", self.path_distance(self.path))
