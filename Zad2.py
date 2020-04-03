import numpy as np

from DistanceCalculator import parse_file, calculate_distance, build_path, path_distance, visualise


def create_random_solution(n):
    l = range(0, 100)
    return np.random.choice(l, n, False)


def calculate_delta(to_remove, pre, aft, new, distances):
    delta = 0
    delta -= distances[pre, to_remove]
    delta -= distances[to_remove, aft]
    delta += distances[pre, new]
    delta += distances[new, aft]
    return delta


def one_from_one_no(distances, vertices, n=50):
    begin_solution = create_random_solution(n)
    whole = np.arange(100)
    print(begin_solution.shape)
    begin_path = build_path(begin_solution)
    begin_distance = path_distance(begin_path, distances)
    visualise(vertices, distances, begin_path, "", distances, False)
    print(begin_path)
    print("Begin distance: ", begin_distance)
    for a in range(100):
        # sub = np.setdiff1d(whole, begin_solution)
        # np.random.shuffle(sub)
        for i in range(len(begin_solution)):
            sub = np.setdiff1d(whole, begin_solution)
            np.random.shuffle(sub)
            aft_ind = i + 1 if i + 1 < len(begin_solution) else 0
            pre_ind = i - 1
            found = False
            for j in sub:
                delta = calculate_delta(begin_solution[i], begin_solution[pre_ind], begin_solution[aft_ind], j,
                                        distances)
                if delta < 0:
                    # print("Delta", delta)
                    # print("I = ", i)
                    # print("Change toRemove: ", begin_solution[i], " new: ", j)
                    np.put(begin_solution, i, j)
                    # print("Act solution shape", begin_solution.shape, " ", begin_solution)

                    # path = build_path(begin_solution)
                    # visualise(vertices, distances, path, "", distances, False)
                    found = True
                    break
            # if found:
            # break
        if a % 20 == 0:
            print("A = ", a)
            path = build_path(begin_solution)
            visualise(vertices, distances, path, "", distances, False)

    path = build_path(begin_solution)
    visualise(vertices, distances, path, "", distances, False)
    dist = path_distance(path, distances)
    print("End dist:", dist)


#not working
def delt(i, j, old_sol, new_sol, n, distances):
    delta = 0
    delta -= distances[old_sol[i - 1], old_sol[i]]
    delta -= distances[old_sol[(i + 1) % n], old_sol[(i + 2) % n]]
    delta -= distances[old_sol[j - 1], old_sol[j]]
    delta -= distances[old_sol[(j + 1) % n], old_sol[(j + 2) % n]]
    delta += distances[new_sol[i - 1], new_sol[j]]
    delta += distances[new_sol[(j + 1) % n], new_sol[(i + 2) % n]]
    delta += distances[new_sol[j - 1], new_sol[i]]
    delta += distances[new_sol[(i + 1) % n], new_sol[(j + 2) % n]]
    return delta

#Not working
def swap_edges(distances, vertices, n=50):
    begin_solution = create_random_solution(n)
    path = build_path(begin_solution)
    begin_distance = path_distance(path, distances)
    visualise(vertices, distances, path, "", distances, False)
    print(path)
    print("Begin distance: ", begin_distance)
    for a in range(1):
        for i in range(n):
            for j in range(n):
                if i - 1 != j and i != j and i + 1 != j:
                    print("I = ", i, " J = ", j)
                    cp = begin_solution.copy()
                    j_next = (j + 1) % n
                    i_next = (i + 1) % n
                    tmp_j = begin_solution[j]
                    tmp_j_next = begin_solution[j_next]
                    np.put(cp, j, cp[i])
                    np.put(cp, j_next, cp[i_next])
                    np.put(cp, i, tmp_j)
                    np.put(cp, i_next, tmp_j_next)
                    delta = delt(i, j, begin_solution, cp, n, distances)
                    if delta < 0:
                        print(begin_solution)
                        print(cp)
                        begin_solution = cp
                        path = build_path(begin_solution)
                        visualise(vertices, distances, path, "", "", False)
                        exit(0)


if __name__ == '__main__':
    vertices = parse_file("kroA100" + ".tsp")
    distances = calculate_distance(vertices)
    one_from_one_no(distances, vertices)
    #swap_edges(distances, vertices)
