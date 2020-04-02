from init import *
from problem import Problem
from solution import Solution

class Nodes(Solution):
    '''Solution on the vertices'''
    def __init__(self, problem, style):
        super(Nodes, self).__init__(problem)
    

    def outside_move(self, v, u, v_indx, u_indx):
        
        random.shuffle(v_indx)
        random.shuffle(u_indx)
        q = False

        for i in v_indx:
            for j in u_indx:
                # print(i, j)
                v[i], u[j] = u[j], v[i] # swap to get neihbour solution

                path = self.build_path(v)
                dist = self.path_distance(path)

                if dist < self.dist:
                    self.dist = dist
                    self.path = path
                    print(dist)
                    q = True
                    break
                else:
                    v[i], u[j] = u[j], v[i] # swap back
            if q: break

    def inside_move(self, v, u, v_indx):

        random.shuffle(v_indx)
        v_indx2 = v_indx[:] #copy
        random.shuffle(v_indx)
        q = False

        for i in v_indx:
            for j in v_indx2:
                if i == j: continue
                # print(i, j)
                v[i], u[j] = u[j], v[i] # swap to get neihbour solution

                path = self.build_path(v)
                dist = self.path_distance(path)

                if dist < self.dist:
                    self.dist = dist
                    self.path = path
                    print(dist)
                    q = True
                    break
                else:
                    v[i], u[j] = u[j], v[i] # swap back
            if q: break

    def optimize_neighbours(self):
        #greedy
        v_indx = list(range(len(self.nodes)))
        u_indx = list(range(len(self.unused)))

        delta = 0.0
        prev_dist = 10**10

        while self.dist/prev_dist < 1.0 + delta:
            prev_dist = self.dist
            self.outside_move(self.nodes, self.unused, v_indx, u_indx)
            self.inside_move(self.nodes, self.unused, v_indx)
        print (self.dist)
