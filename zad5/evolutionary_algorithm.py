import random
import time

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from zad5.solution import Solution


class Action:

    def __init__(self, v1, v2, action):
        self.v1 = v1
        self.v2 = v2
        self.action = action


class EvolutionaryAlgorithm(Solution):

    def __init__(self, problem, time, debug=False):
        super(EvolutionaryAlgorithm, self).__init__(problem)
        self.population_size = 3
        self.time = time
        self.iterations = 0
        self.population = []
        self.v_indexes = list(map(lambda x: x[0], self.p.vertices))
        self.nodes = list(map(lambda x: x[0], self.nodes))
        self.unused = list(map(lambda x: x[0], self.unused))
        self.debug = debug

    def create_population(self):
        while len(self.population) != self.population_size:
            random.shuffle(self.v_indexes)
            nodes = self.v_indexes[:int(np.ceil(self.p.n / 2))]
            if nodes not in self.population:
                dist, nodes = self.run_algorithm(nodes)
                # path = self.build_path(nodes)
                # dist = self.path_distance(path)
                self.population.append((dist, nodes))
        for i in self.population:
            print(i[0])

    def run(self):
        start_time = time.time() * 1000
        self.create_population()
        while True:
            self.iterations += 1
            self.generate_child()
            current_time = time.time() * 1000
            if current_time - start_time > self.time > 10_000:
                break

        print("TotalTime:", current_time - start_time)
        best_nodes = min(self.population, key=lambda x: x[0])[1]
        self.path = self.build_path(best_nodes)
        self.dist = self.path_distance(self.path)
        print("Best Dist:", self.dist)

    def generate_child(self):
        parents = np.random.randint(0, self.population_size, (2))
        child = self.find_common(parents)
        dist, nodes = self.run_algorithm(child)
        max_dist = max(self.population, key=lambda x: x[0])
        index = self.population.index(max_dist)
        print("Dist:", dist)
        print("Max dist:", max_dist[0], "Index:", index)
        if dist < max_dist[0] and (dist, nodes) not in self.population:
            self.population[index] = (dist, nodes)
            path = self.build_path(nodes)
            self.visualise(False, "", path=path)
            print("Change")
        # exit(0)

    def find_common(self, parents):
        # TODO remove
        parents = [0, 1]
        p0 = self.population[parents[0]]
        path0 = self.build_path(p0[1])
        p1 = self.population[parents[1]]
        path1 = self.build_path(p1[1])

        i = 0
        common_parts = []
        common_v = []
        while i < len(p0[1]):
            j = 0
            found = False
            while j < len(p1[1]):
                part1 = []
                temp_i = i
                temp_j = j
                if i >= len(p0[1]):
                    break

                while p0[1][i] \
                        == p1[1][j]:
                    part1.append(p0[1][i])
                    found = True
                    i += 1
                    j += 1
                    if i >= len(p0[1]) or j >= len(p1[1]):
                        break
                if len(part1) > 1:  # jeśli znalazłem wspólną ścieżkę
                    common_parts.append(part1)
                    common_v += part1
                    continue
                j = temp_j
                i = temp_i
                part2 = []
                while p0[1][i] == p1[1][j]:
                    found = True
                    part2.append(p0[1][i])
                    i += 1
                    j -= 1
                    if i >= len(p0[1]) or j < 0:
                        break
                if part2:
                    common_parts.append(part2)
                    common_v += part2
                j += 1
            if not found:
                i += 1
        if self.debug:
            print("P0:", p0)
            print("P1:", p1)
            print("Common parts:", common_parts)
            print("Common v:", len(common_v), common_v)
        self.visualise_common(path0, path1, common_parts, common_v)

        unused = np.setdiff1d(np.arange(1, self.p.n + 1), np.array(common_v))
        random.shuffle(unused)
        to_add = (self.p.n // 2) - len(common_v)
        for i in range(to_add):
            common_parts.append([unused[i]])
        nodes = []
        for part in common_parts:
            nodes += part
        if self.debug:
            print("Unused:", len(unused))
            print("To add:", to_add)
            print("New Nodes:", len(nodes), nodes)
            print("Unique len:", len(np.unique(np.array(nodes))))
        return nodes

    def run_algorithm(self, nodes):
        unused = np.setdiff1d(np.arange(1, self.p.n + 1), nodes)
        while True:
            best_action = None
            best_delta = 0
            for e, i in enumerate(nodes):
                for j in nodes[e + 1:]:
                    if i == j: continue
                    delta = self.calc_swap_move(i, j, nodes)
                    if delta < best_delta:
                        best_action = Action(i, j, "swap")
                        best_delta = delta
                for j in unused:
                    if i == j: continue
                    delta = self.calc_outer_move(i, j, nodes)
                    if delta < best_delta:
                        best_action = Action(i, j, "outer")
                        best_delta = delta
            if best_delta < 0:
                if best_action.action == "swap":
                    nodes = self.do_swap_move(best_action.v1, best_action.v2, nodes)
                else:
                    nodes = self.do_outer_move(best_action.v1, best_action.v2, nodes)
                    unused = np.setdiff1d(np.arange(1, self.p.n + 1), nodes)
            else:
                break
        path = self.build_path(nodes)
        dist = self.path_distance(path)
        return dist, nodes

    def calc_outer_move(self, v1, v2, nodes):
        delta = 0
        if v1 not in nodes:
            temp = v1
            v1 = v2
            v2 = temp
        v1_ind = nodes.index(v1)
        pre = nodes[v1_ind - 1]
        aft = nodes[(v1_ind + 1) % (self.p.n // 2)]
        delta -= self.p.distances[pre - 1, v1 - 1]
        delta -= self.p.distances[v1 - 1, aft - 1]
        delta += self.p.distances[pre - 1, v2 - 1]
        delta += self.p.distances[v2 - 1, aft - 1]
        return delta

    def calc_swap_move(self, v1, v2, nodes):
        delta = 0
        v1_ind = nodes.index(v1)
        v2_ind = nodes.index(v2)
        if abs(v2_ind - v1_ind) == 0 or abs(v1_ind - v2_ind) == (self.p.n // 2) - 1:
            return 0

        if v2_ind < v1_ind == v2_ind + 1:
            return 0

        delta -= self.p.distances[v1 - 1, nodes[v1_ind - 1] - 1]
        delta -= self.p.distances[nodes[(v2_ind + 1) % (self.p.n // 2)] - 1, v2 - 1]

        delta += self.p.distances[v1 - 1, nodes[(v2_ind + 1) % (self.p.n // 2)] - 1]
        delta += self.p.distances[nodes[v1_ind - 1] - 1, v2 - 1]
        return delta

    def do_swap_move(self, v1, v2, nodes):
        v1_ind = nodes.index(v1)
        v2_ind = nodes.index(v2)
        return self.swap_nodes(v1_ind, v2_ind, nodes)

    def swap_nodes(self, start, end, nodes):
        if start == end: return nodes
        new_nodes = nodes.copy()
        if start < end:
            new_nodes = nodes.copy()
            new_nodes[0:start] = nodes[0:start]
            new_nodes[start:end + 1] = nodes[start:end + 1][::-1]
            new_nodes[end + 1:] = nodes[end + 1:]
        else:
            exit(-2)
            new_nodes[:self.p.n // 2 - start] = nodes[start:][::-1]
            new_nodes[self.p.n // 2 - start + 1: self.p.n // 2 - end] = nodes[end + 1: start]
            new_nodes[self.p.n // 2 - end:] = nodes[:end + 1][::-1]

        return new_nodes

    def do_outer_move(self, v1, v2, nodes):
        if v1 in nodes:
            v1_ind = nodes.index(v1)
            nodes[v1_ind] = v2
        else:
            v2_ind = nodes.index(v2)
            nodes[v2_ind] = v1
        return nodes

    def visualise_common(self, p0, p1, common_parts, common_v):
        G = nx.Graph()
        plt.figure(figsize=(16, 16))
        for i in range(len(self.p.vertices)):
            G.add_node(i, pos=(self.p.vertices[i][1], self.p.vertices[i][2]))

        parent_0 = []
        for edge in p0:
            parent_0.append((edge[0] - 1, edge[1] - 1))
        parent_1 = []
        for edge in p1:
            parent_1.append((edge[0] - 1, edge[1] - 1))

        common_list = []
        common_v = [v - 1 for v in common_v]
        for part in common_parts:
            new_part = []
            for i, v in enumerate(part[:-1]):
                new_part.append((v - 1, part[i + 1] - 1))
            if new_part:
                common_list.append(new_part)

        pos = nx.get_node_attributes(G, 'pos')
        nx.draw_networkx(G, pos, node_size=30)
        nx.draw_networkx_edges(G, pos, edgelist=parent_0, edge_color='b')
        nx.draw_networkx_edges(G, pos, edgelist=parent_1, edge_color='y')
        for part in common_list:
            nx.draw_networkx_edges(G, pos, edgelist=part, edge_color='r')
        nx.draw_networkx_nodes(G, pos, nodelist=common_v, node_color='r', node_size=60)
        plt.axis("off")
        plt.show()
