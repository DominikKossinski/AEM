from init import *

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

    def save_results(self, results):
        min_dist = min(results)
        max_dist = max(results)
        mean_dist = np.mean(results)
        file_path = os.path.join(self.name, "results.csv")
        file = open(file_path, "w+")
        file.write(self.name + ";\n")
        file.write("min;" + str(min_dist) + "\n")
        file.write("max;" + str(max_dist) + "\n")
        file.write("mean;" + str(mean_dist) + "\n")
        print(results)
        file.close()