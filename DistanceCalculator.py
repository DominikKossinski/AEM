import os

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from ast import literal_eval as make_tuple


def parse_file(path):
    file = open(path, "r")
    lines = file.readlines()[6:-1]
    vertices = []
    for line in lines:
        tab = [int(x) for x in line.replace("\n", "").split(" ")]
        vertices.append(tab)
    file.close()
    return vertices


def calculate_distance(vertices):
    n = len(vertices)
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            a = vertices[i]
            b = vertices[j]
            distance = np.round(np.sqrt(np.power(a[1] - b[1], 2) + np.power(a[2] - b[2], 2)))
            distances[i][j] = distance
            distances[j][i] = distance
    # print(distances)
    return distances


def visualise(vertices, distances, path):
    G = nx.Graph()
    plt.figure(figsize=(16, 16))
    for i in range(len(vertices)):
        G.add_node(i, pos=(vertices[i][1], vertices[i][2]))

    for edge in path:
        G.add_edge(edge[0], edge[1], weight=distances[edge[0], edge[1]])

    pos = nx.get_node_attributes(G, 'pos')
    labels = nx.get_edge_attributes(G, 'weight')

    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    nx.draw_networkx(G, pos, node_size=30, edge_labels=nx.get_node_attributes(G, "weight"))
    plt.show()
    # plt.savefig("nodes.png")


def find_nearest(distances, begin_vertex, instance):
    begin = begin_vertex
    min_distance = None
    min_index = None
    for i in range(len(distances)):
        if i != begin:
            if min_distance is None:
                min_distance = distances[begin, i]
                min_index = i
            elif min_distance > distances[begin, i]:
                min_distance = distances[begin, i]
                min_index = i
    path = [(begin, min_index)]
    tab = [begin, min_index]
    print(path)
    n = int(np.ceil(len(distances) / 2) - 2)
    for i in range(n):
        min_distance = None
        min_index = None
        min_act = None
        for act in path:
            for j in range(len(distances)):
                if j not in tab:
                    distance = min(distances[act[0], j], distances[j, act[1]])
                    if min_distance is None:
                        min_distance = distance
                        min_index = j
                        min_act = act
                    elif min_distance > distance:
                        min_distance = distance
                        min_index = j
                        min_act = act
        path = add_between(path, min_act, min_index)
        tab.append(min_index)
        print("Tab:", tab)
        print("Path: ", path)
        print("Min dist: ", min_distance, " Min ind: ", min_index, " Min act: ", min_act)
    print("PathLen:", len(path), "\nPath: ", path)
    save_hamilton_path(os.path.join(instance, "path" + str(begin_vertex)), path)
    return path


def path_distance(path, distances):
    dist = 0
    for edge in path:
        dist += distances[edge[0], edge[1]]
    return dist


def add_between(path, act, j):
    new_path = []
    for edge in path:
        if edge != act:
            new_path.append(edge)
        else:
            new_path.append((edge[0], j))
            new_path.append((j, edge[1]))
    if new_path[-1][1] != new_path[0][0]:
        new_path.append((new_path[-1][1], new_path[0][0]))
    return new_path


def save_hamilton_path(file_path, hamilton_path):
    file = open(file_path, "w+")
    for edge in hamilton_path:
        file.write(str(edge) + "\n")
    file.close()


def load_hamilton_path(file_path):
    file = open(file_path, "r")
    lines = file.readlines()
    path = [make_tuple(line) for line in lines]
    file.close()
    return path


def save_results(instance, results):
    min_dist = min(results)
    max_dist = max(results)
    mean_dist = np.mean(results)
    file_path = os.path.join(instance, "results.csv")
    file = open(file_path, "w+")
    file.write(instance + ";\n")
    file.write("min;" + str(min_dist) + "\n")
    file.write("max;" + str(max_dist) + "\n")
    file.write("mean;" + str(mean_dist) + "\n")
    print(results)
    file.close()


if __name__ == '__main__':
    vertices = parse_file("kroA100.tsp")
    print(vertices)
    distances = calculate_distance(vertices)
    instances = ["kroA100", "kroB100"]
    # Second algorithm 'Zal'
    for instance in instances:
        vertices = parse_file(instance + ".tsp")
        distances = calculate_distance(vertices)
        n = len(distances)
        results = []
        if not os.path.exists(instance + "Greedy"):
            os.mkdir(instance + "Greedy")
        for i in range(n):
            path = find_nearest(distances, i, instance + "Greedy")
            path_len = path_distance(path, distances)
            results.append(path_len)
        save_results(instance + "Greedy", results)

    vertices = parse_file("kroA100.tsp")
    distances = calculate_distance(vertices)
    path = load_hamilton_path(os.path.join("kroA100Greedy", "path0"))
    print(path)
    visualise(vertices, distances, path)
