import os

import numpy as np


class Problem():
    def __init__(self, name):
        self.name = name
        self.vertices = self.parse_file(name + ".tsp")
        self.n = len(self.vertices)
        self.distances = self.calculate_distance()

    def parse_file(self,path):
        file = open(path, "r")
        lines = file.readlines()[6:-1]
        vertices = []
        for line in lines:
            tab = [int(x) for x in line.replace("\n", "").split(" ")]
            vertices.append(tab)
        file.close()
        return vertices

    def calculate_distance(self):
        distances = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(i + 1, self.n):
                a = self.vertices[i]
                b = self.vertices[j]
                distance = np.round(np.sqrt(np.power(a[1] - b[1], 2) + np.power(a[2] - b[2], 2)))
                distances[i][j] = distance
                distances[j][i] = distance
        return distances

    def save_results(self,alg, style, results, times=None, path = None):
        min_dist = min(results)
        max_dist = max(results)
        mean_dist = np.mean(results)
        if times is not None:
            min_time = min(times)
            max_time = max(times)
            mean_time = np.mean(times)
        else:
            min_time = None
            max_time = None
            mean_time = None
        file_path = os.path.join(self.name, style, alg + "_results.csv")
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        file = open(file_path, "w+")
        file.write(self.name + ";\n")
        file.write("min;" + str(min_dist) + "\n")
        file.write("mean;" + str(mean_dist) + "\n")
        file.write("max;" + str(max_dist) + "\n")
        if times is not None:
            file.write("min_t;" + str(min_time) + "\n")
            file.write("mean_t;" + str(mean_time) + "\n")
            file.write("max_t;" + str(max_time) + "\n")
        print(results)
        file.close()
        if path is not None:
            print(path)
            file_path = os.path.join(self.name, style, alg + "_min_cycle.pkl")
            import pickle
            with open(file_path, 'wb') as fp:
                pickle.dump(path, fp)