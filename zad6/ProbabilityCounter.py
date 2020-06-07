import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr


class ProbabilityCounter:

    def __init__(self, problem, nodes_list, results, debug=False):
        self.p = problem
        self.debug = debug
        self.nodes_list = nodes_list
        self.results = results
        self.best_result = min(self.results)
        self.best_solution = self.nodes_list[self.results.index(self.best_result)]
        self.best_solution_path = self.build_path(self.best_solution)
        self.common_edges_p = dict()  # [result] =  list(p_vertices)
        self.common_vertices_p = dict()  # [result] = list(p_edges)
        self.i = 0
        for nodes, result in zip(nodes_list, results):
            self.debug = self.i % 100 == 0
            self.find_common(nodes, result)
            self.i += 1
        self.visualise_probabilities()

    def find_common(self, nodes, result):
        i = 0
        common_parts = []
        common_v = []
        while i < len(self.best_solution):
            j = 0
            found = False
            while j < len(nodes):
                part1 = []
                temp_i = i
                temp_j = j
                if i >= len(self.best_solution):
                    break

                while self.best_solution[i] \
                        == nodes[j]:
                    part1.append(self.best_solution[i])
                    found = True
                    i += 1
                    j += 1
                    if i >= len(self.best_solution) or j >= len(nodes):
                        break
                if len(part1) > 1:  # jeśli znalazłem wspólną ścieżkę
                    common_parts.append(part1)
                    common_v += part1
                    continue
                j = temp_j
                i = temp_i
                part2 = []
                while self.best_solution[i] == nodes[j]:
                    found = True
                    part2.append(self.best_solution[i])
                    i += 1
                    j -= 1
                    if i >= len(self.best_solution) or j < 0:
                        break
                if part2:
                    common_parts.append(part2)
                    common_v += part2
                j += 1
            if not found:
                i += 1
        if self.debug:
            path1 = self.build_path(nodes)
            print("P1:", nodes)
            print("Common parts:", common_parts)
            print("Common v:", len(common_v), common_v)
            self.visualise_common(path1, common_parts, common_v)
        all_parents = np.unique(self.best_solution + nodes)
        print("AllParents: ", len(all_parents))
        print("Common Vertices:", len(common_v))
        p_vertices = len(common_v) / len(nodes)
        if result in self.common_vertices_p.keys():
            self.common_vertices_p[result].append(p_vertices)
        else:
            self.common_vertices_p[result] = [p_vertices]
        edges_count = 0
        for part in common_parts:
            edges_count += len(part) - 1
        print("Common edges:", edges_count)
        p_edges = edges_count / len(nodes)
        if result in self.common_edges_p.keys():
            self.common_edges_p[result].append(p_edges)
        else:
            self.common_edges_p[result] = [p_edges]

    def build_path(self, nodes):
        path = []
        for i in range(len(nodes)):
            if i + 1 < len(nodes):
                path.append((nodes[i], nodes[i + 1]))
            else:
                path.append((nodes[i], nodes[0]))
        return path

    def visualise_common(self, p1, common_parts, common_v):
        G = nx.Graph()
        plt.figure(figsize=(16, 16))
        for i in range(len(self.p.vertices)):
            G.add_node(i, pos=(self.p.vertices[i][1], self.p.vertices[i][2]))

        parent_0 = []
        for edge in self.best_solution_path:
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
        plt.savefig(f"Common{self.i}.png")
        plt.show()

    def visualise_probabilities(self):

        mean_p_vertices = []
        mean_p_edges = []
        results_for_plot = []
        for result in self.common_edges_p.keys():
            results_for_plot.append(result)
            mean_p_edges.append(np.mean(self.common_edges_p[result]))
            mean_p_vertices.append(np.mean(self.common_vertices_p[result]))

        cor_edges = pearsonr(results_for_plot, mean_p_edges)
        print("Cor edges", cor_edges)

        cor_vertices = pearsonr(results_for_plot, mean_p_vertices)
        print("Cor vertices:", cor_vertices)

        with open("results.txt", "w+") as f:
            f.write(f"Cor edges;{cor_edges}\n")
            f.write(f"cor vercices;{cor_vertices}\n")
            f.write(f"best_result;{self.best_solution}")
            f.flush()
            f.close()

        plt.plot(results_for_plot, mean_p_vertices, 'o')
        plt.title("Prawdopodobieństwo wspólnego wierzchołka")
        plt.savefig("P_nodes.png")
        plt.show()

        plt.plot(results_for_plot, mean_p_edges, 'o')
        plt.title("Prawdopodobiaństwo wspólnej krawędzi")
        plt.savefig("P_edges.png")
        plt.show()
