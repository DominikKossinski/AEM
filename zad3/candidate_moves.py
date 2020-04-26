from solution import Solution
import numpy as np


class CandidateMoves(Solution):

    def __init__(self, problem):
        super(CandidateMoves, self).__init__(problem)
        self.find_five_nearest(0)
        # print([x for x in range(6)])
        # print(self.swap_nodes(0, 1, [x for x in range(6)]))
        # print(self.swap_nodes(4, 1, [x for x in range(6)]))
        # print(self.swap_nodes(1, 1, [x for x in range(6)]))
        # exit(0)

    def find_five_nearest(self, vertex):
        dist = self.p.distances[vertex]
        return np.argsort(dist)[1:6]

    def find_five_nearest_from_nodes(self, vertex):
        dist = self.p.distances[vertex]
        ind = np.argsort(dist)
        nearest = []
        indexes = list(map(lambda x: x[0] - 1, self.nodes))
        for i in ind:
            if i != vertex and i in indexes:
                nearest.append(indexes.index(i))
            if len(nearest) == 5:
                return nearest

    def swap_nodes(self, start, end, nodes):
        if start == end: return nodes
        new_nodes = []
        if start < end:
            for i in range(0, start):
                new_nodes.append(nodes[i])
            for i in range(end, start - 1, -1):
                new_nodes.append(nodes[i])
            for i in range(end + 1, len(nodes)):
                new_nodes.append(nodes[i])
        else:
            for i in range(start, len(nodes)):
                new_nodes.append(nodes[i])
            for i in range(end + 1, start):
                new_nodes.append(nodes[i])
            for i in range(end + 1):
                new_nodes.append(nodes[i])
        return new_nodes

    def optimize(self):

        print("Start distance", self.path_distance(self.path))
        self.path = self.build_path(self.nodes)

        improved = True
        while improved:
            improved = False
            for i in range(len(self.nodes)):
                # print(self.nodes)
                candidate = self.find_five_nearest_from_nodes(self.nodes[i][0] - 1)
                for j in candidate:
                    if abs(j - i) == 1: continue
                    new_nodes = self.swap_nodes(i, j, self.nodes)
                    # if j == 0: continue
                    # if i < j:
                    #     new_nodes = self.nodes[:]
                    #     new_nodes[i:j] = self.nodes[j - 1:i - 1:-1]
                    # else:
                    #     print("i = ", i, "j = ", j)
                    #     print("nodes:", self.nodes)
                    #     new_nodes = self.nodes[:]
                    #     print("to swap:", self.nodes[i - 1: j - 1:-1])
                    #     new_nodes[j:i] = self.nodes[i - 1: j - 1: -1]
                    #     print("New nodes else", new_nodes)
                    if self.path_distance(self.build_path(new_nodes)) < self.path_distance(self.path):
                        self.path = self.build_path(new_nodes)
                        self.nodes = new_nodes
                        improved = True

        self.path = self.build_path(self.nodes)
        self.dist = self.path_distance(self.path)
        print("End distance:", self.path_distance(self.path))
