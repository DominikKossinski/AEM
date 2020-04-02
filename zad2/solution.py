from init import *
from problem import Problem

class Solution():
    def __init__(self, problem):
        self.p = problem
        self.nodes = []
        self.path = []

    def set_random(self, p):
        v = random.sample(p.vertices, int(np.ceil(p.n / 2)))
        self.nodes = v
        # print(v)

    def path_distance(self):
        dist = 0
        for edge in self.path:
            dist += self.p.distances[edge[0], edge[1]]
        return dist

    def visualise(filename, save):
        G = nx.Graph()
        plt.figure(figsize=(16, 16))
        for i in range(len(self.p.vertices)):
            G.add_node(i, pos=(self.p.vertices[i][1], self.p.vertices[i][2]))

        for edge in self.path:
            G.add_edge(edge[0], edge[1], weight=self.p.distances[edge[0], edge[1]])

        pos = nx.get_node_attributes(G, 'pos')
        labels = nx.get_edge_attributes(G, 'weight')

        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        nx.draw_networkx(G, pos, node_size=30, edge_labels=nx.get_node_attributes(G, "weight"))
        if save:
            plt.savefig(filename + "_" + self.distance + ".png")
        else:
            plt.show()


