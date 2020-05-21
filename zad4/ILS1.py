import time

from zad4.MSLS import MSLS
from zad4.solution import Solution
import numpy as np


class ILS1(MSLS):

    def __init__(self, problem, time):
        super(ILS1, self).__init__(problem)
        self.time = time
        self.set_random()
        self.neighbours = []
        self.iterations = 0

    def optimize(self):
        self.find_nearest()
        start_time = time.time() * 1000
        self.run_algorithm()
        best_dist = self.dist
        best_nodes = self.nodes.copy()
        iterations = 1
        while True:
            print("i =", iterations)
            self.perturbacja()
            self.run_algorithm()
            if best_dist > self.dist:
                print("New Best:", self.dist)
                best_dist = self.dist
                best_nodes = self.nodes.copy()
            current_time = time.time() * 1000
            if current_time - start_time > self.time - 10_000:
                break
            iterations += 1
        print("TotalTime:", current_time - start_time)
        self.path = self.build_path(best_nodes)
        self.dist = self.path_distance(self.path)
        self.iterations = iterations
        print("Best Dist: ", best_dist)

    def find_nearest(self):
        for i in self.v_indexes:
            self.neighbours.append(self.find_five_nearest(i))

    def find_five_nearest(self, vertex):
        dist = self.p.distances[vertex - 1]
        return np.argsort(dist)[1:6]


    def perturbacja(self):
        self.unused = np.setdiff1d(np.arange(1, self.p.n + 1), self.nodes)
        k = 5
        max_dist = 0
        max_ind = 0
        n = self.n // 2
        for e, i in enumerate(self.nodes):
            d = self.p.distances[i - 1, self.nodes[(e + 1) % n] - 1]
            if d > max_dist:
                max_dist = d
                max_ind = e
        max_dist = []
        for i in range(-2, 3):
            max_dist.append((max_ind, (max_ind + i) % n))
        # max_dist = []
        # n = self.n // 2
        # for e, i in enumerate(self.nodes):
        #     d = self.p.distances[i - 1, self.nodes[(e + 1) % n] - 1]
        #     if len(max_dist) < k:
        #         max_dist.append((d, e))
        #     elif max_dist[-1][0] < d:
        #         max_dist.append((d, e))
        #         max_dist.sort(key=lambda x: x[0], reverse=True)
        #         max_dist.pop()
        self.replace_to_random(max_dist, k)

    def replace_to_random(self, max_dists, k):
        random_indexes = np.arange(self.n // 2)
        np.random.shuffle(random_indexes)
        random_indexes = random_indexes[:k]
        for v_in, v_out in zip(max_dists, random_indexes):
            self.nodes[v_in[1]] = self.unused[v_out]


        n_u = len(np.unique(self.nodes))
        if n_u != 100:
            print(self.path)
            print(self.nodes)
            print("Unique", len(np.unique(self.nodes)))
        self.unused = np.setdiff1d(np.arange(1, self.p.n + 1), self.nodes)

