from init import *
from problem import Problem

class Solution():
    def __init__(self, problem):
        self.p = problem
        self.nodes = [] #vertices in the path
        self.path = []
        self.unused = [] # vertices outside the path
        self.dist = 0

    def set_random(self, p):
        # v = random.sample(p.vertices, int(np.ceil(p.n / 2)))
        v = p.vertices.copy()
        random.shuffle(v)
        self.nodes = v[:int(np.ceil(p.n / 2))]
        self.unused = v[int(np.ceil(p.n / 2)):]
        self.path = self.build_path(self.nodes)
        self.dist = self.path_distance(self.path)

        # print(self.nodes, self.unused)

    def path_distance(self, path):
        dist = 0
        for edge in path:
            dist += self.p.distances[edge[0][0]-1, edge[1][0]-1]
        return dist

    def build_path(self, nodes):
        path = []
        for i in range(len(nodes)):
            if i + 1 < len(nodes):
                path.append((nodes[i], nodes[i + 1]))
            else:
                path.append((nodes[i], nodes[0]))
        return path

    def visualise(self, save, filename = ""):
        G = nx.Graph()
        plt.figure(figsize=(16, 16))
        for i in range(len(self.p.vertices)):
            G.add_node(i, pos=(self.p.vertices[i][1], self.p.vertices[i][2]))

        for edge in self.path:
            G.add_edge(edge[0][0]-1, edge[1][0]-1, weight=self.p.distances[edge[0][0]-1, edge[1][0]-1])

        pos = nx.get_node_attributes(G, 'pos')
        labels = nx.get_edge_attributes(G, 'weight')

        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        nx.draw_networkx(G, pos, node_size=30, edge_labels=nx.get_node_attributes(G, "weight"))
        if save:
            plt.savefig(filename + "_" + self.distance + ".png")
        else:
            plt.show()


