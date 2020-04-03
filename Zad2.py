import numpy as np

from DistanceCalculator import parse_file, calculate_distance


def create_random_solution():
    l = range(0, 100)
    return np.random.choice(l, 50, False)


if __name__ == '__main__':
    begin_solution = create_random_solution()
    print(begin_solution.shape)
    a = np.unique(begin_solution)
    print(a.shape)
    vertices = parse_file("kroA100" + ".tsp")
    distances = calculate_distance(vertices)

