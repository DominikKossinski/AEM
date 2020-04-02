from init import *
from problem import Problem
from solution import Solution

class Nodes(Solution):
    '''Solution on the vertices'''
    def __init__(self, problem, style):
        super(Nodes, self).__init__(problem)
    
    def outside_move(self):
        #greedy
        v = self.nodes[:]
        random.shuffle(v)
        u = self.unused[:]
        random.shuffle(u)

        best_dist = [self.dist, -1, -1]

        for i in range(len(v)):
            for j in range(len(u)):
                v[i], u[j] = u[j], v[i] # swap to get neihbour solution

                path = self.build_path(v)
                dist = self.path_distance(path)

                if dist < best_dist[0]:
                    best_dist = [dist, i, j]
                    # print(dist)
                else:
                    v[i], u[j] = u[j], v[i] # swap back

        print (self.dist, best_dist )

        if best_dist[1] > -1:
            self.nodes = v[:]
            self.unused = u[:]
            self.dist = best_dist[0]