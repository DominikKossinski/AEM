import random

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


class Solution():
    def __init__(self, problem):
        self.p = problem
        self.nodes = []  # vertices in the path
        self.path = []
        self.unused = []  # vertices outside the path
        self.dist = 0

    def set_random(self):
        # v = random.sample(p.vertices, int(np.ceil(p.n / 2)))
        v = self.p.vertices.copy()
        random.shuffle(v)
        self.nodes = v[:int(np.ceil(self.p.n / 2))]
        self.unused = v[int(np.ceil(self.p.n / 2)):]
        self.path = self.build_path(self.nodes)
        self.dist = self.path_distance(self.path)

        # print(self.nodes)
        # print(self.path)

    def path_distance(self, path):
        dist = 0
        for edge in path:
            dist += self.p.distances[edge[0] - 1, edge[1] - 1]
        return dist

    # def rebuild_path(self, nodes, path, x, y, inside, unused = None):
    #     # Faster version of build_path (when only one swap)
    #     if inside:
    #         # print(path[x])
    #         path[x - 1] = (path[x - 1][0], nodes[x])
    #         path[x] = (nodes[x], path[x][1])
    #         # a,b = path[x]
    #         # path[x] = (a, nodes[x])
    #         # a,b = path[x - 1]
    #         # path[x-1] = (nodes[x], b)
    #          # (path[x][0] + 1 ,0)
    #         # print(path[x])
    #         path[y - 1] = (path[y - 1][0], nodes[y])
    #         path[y] = (nodes[y], path[y][1])
    #     else:
    #         path[x - 1] = (path[x - 1][0], unused[y])
    #         path[x] = (unused[y], path[x][1])
    #     return path

    def build_path(self, nodes):
        path = []
        for i in range(len(nodes)):
            if i + 1 < len(nodes):
                path.append((nodes[i][0], nodes[i + 1][0]))
            else:
                path.append((nodes[i][0], nodes[0][0]))
        return path

    def visualise(self, save, alg, style=""):
        G = nx.Graph()
        plt.figure(figsize=(16, 16))
        for i in range(len(self.p.vertices)):
            G.add_node(i, pos=(self.p.vertices[i][1], self.p.vertices[i][2]))

        for edge in self.path:
            G.add_edge(edge[0] - 1, edge[1] - 1, weight=self.p.distances[edge[0] - 1, edge[1] - 1])

        pos = nx.get_node_attributes(G, 'pos')
        labels = nx.get_edge_attributes(G, 'weight')

        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        nx.draw_networkx(G, pos, node_size=30, edge_labels=nx.get_node_attributes(G, "weight"))
        if save:
            plt.savefig(alg + "_" + style + ".png")
            plt.show()
        else:
            plt.show()
