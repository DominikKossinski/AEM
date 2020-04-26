import random

import networkx as nx
import numpy as np
from solution import Solution
import matplotlib.pyplot as plt


class Action():

    def __init__(self, v1, v2, action):
        self.v1 = v1
        self.v2 = v2
        self.action = action


class Edges(Solution):

    def __init__(self, problem, style):
        super(Edges, self).__init__(problem)
        print(self.p.vertices)
        self.style = style
        self.v_indexes = list(map(lambda x: x[0], self.p.vertices))

    def set_random(self, problem):
        v = problem.vertices.copy()
        random.shuffle(v)
        self.nodes = v[:int(np.ceil(problem.n / 2))]
        self.unused = v[int(np.ceil(problem.n / 2)):]

        self.v_indexes = list(map(lambda x: x[0], self.p.vertices))
        self.nodes = list(map(lambda x: x[0], self.nodes))
        self.unused = list(map(lambda x: x[0], self.unused))

        self.path = self.build_path(self.nodes)
        self.dist = self.path_distance(self.path)

    def path_distance(self, path):
        dist = 0
        #print("Path", path)
        for edge in path:
            dist += self.p.distances[edge[0] - 1, edge[1] - 1]
        return dist

    def visualise(self, save, alg, style):
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

    def optimize(self):
        if self.style == 'greedy':
            print("Greedy")
            self.optimize_greedy()
        elif self.style == 'steep':
            self.new_steepest()

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
        return new_nodes


    def calc_outer_move(self, v1, v2):
        delta = 0
        if v1 not in self.nodes:
            temp = v1
            v1 = v2
            v2 = temp
        if v1 not in self.nodes:
            exit(-5)
        v1_ind = self.nodes.index(v1)
        pre = self.nodes[v1_ind - 1]
        aft = self.nodes[(v1_ind + 1) % 50]
        delta -= self.p.distances[pre - 1, v1 - 1]
        delta -= self.p.distances[v1 - 1, aft - 1]
        delta += self.p.distances[pre - 1, v2 - 1]
        delta += self.p.distances[v2 - 1, aft - 1]
        return delta

    def calc_swap_move(self, v1, v2):
        delta = 0
        v1_ind = self.nodes.index(v1)
        v2_ind = self.nodes.index(v2)
        if abs(v2_ind - v1_ind) == 0 or abs(v1_ind - v2_ind) == 49:
            return 0
        if v2_ind < v1_ind:
            return 0
        else:
            delta -= self.p.distances[v1 - 1, self.nodes[v1_ind - 1] - 1]
            delta -= self.p.distances[self.nodes[(v2_ind + 1) % 50] - 1, v2 - 1]

            delta += self.p.distances[v1 - 1, self.nodes[(v2_ind + 1)  % 50] - 1]
            delta += self.p.distances[self.nodes[v1_ind - 1] - 1, v2 - 1]
        if delta < 0:
             print("Nodes:", self.nodes)
             print("V1", v1)
             print("V2", v2)
             print("V1_ind", v1_ind)
             print("V2_ind", v2_ind)

             print("Delta =", delta)
        return delta

    def do_swap_move(self, v1, v2):
        v1_ind = self.nodes.index(v1)
        v2_ind = self.nodes.index(v2)
        self.nodes = self.swap_nodes(v1_ind, v2_ind, self.nodes)

    def do_outer_move(self, v1, v2):
        if v1 in self.nodes:
            v1_ind = self.nodes.index(v1)
            self.nodes[v1_ind] = v2
            self.unused.remove(v2)
            self.unused.append(v1)
        else:
            v2_ind = self.nodes.index(v2)
            self.nodes[v2_ind] = v1
            self.unused.remove(v1)
            self.unused.append(v2)

    def optimize_greedy(self):
        self.path = self.build_path(self.nodes)
        print("Start distance", self.path_distance(self.path))
        improved = True
        a = 0
        while improved:
            improved = False
            best_action = None
            for i in self.v_indexes:
                for j in self.v_indexes:
                    if i == j: continue
                    if (i in self.nodes and j in self.unused) or (j in self.nodes and i in self.unused):
                        delta = self.calc_outer_move(i, j)
                        if self.calc_outer_move(i, j) < 0:
                            print("i = ", i, "j = ", j)
                            best_action = Action(i, j, "outer")
                            improved = True
                            break
                    if i in self.nodes and j in self.nodes:
                        # print("Swap delta", self.calc_swap_move(i, j))
                        if self.calc_swap_move(i, j) < 0:
                            best_action = Action(i, j, "swap")
                            improved = True
                            break
                if improved:
                    break
            if improved:
                if best_action.action == "swap":
                    self.do_swap_move(best_action.v1, best_action.v2)
                else:
                    self.do_outer_move(best_action.v1, best_action.v2)
                self.path = self.build_path(self.nodes)

        self.path = self.build_path(self.nodes)
        self.dist = self.path_distance(self.path)
        print("End distance:", self.dist)


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
