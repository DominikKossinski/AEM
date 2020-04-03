from init import *
from problem import Problem
from solution import Solution

class Nodes(Solution):
    '''Solution on the vertices'''
    def __init__(self, problem, style):
        super(Nodes, self).__init__(problem)
        self.style = style

    def outside_move_greedy(self, v, u, v_indx, u_indx):
        
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


    def inside_move_greedy(self, v, v_indx):

        random.shuffle(v_indx)
        v_indx2 = v_indx[:] #copy
        random.shuffle(v_indx)
        q = False

        for i in v_indx:
            for j in v_indx2:
                if i == j: continue
                # print(i,j,v[i][0], v[j][0])
                v[i], v[j] = v[j], v[i] # swap to get neihbour solution
                
                # print(i,j,v[i][0], v[j][0])
                # path_o = deepcopy(self.path)
                path = self.build_path(v)
                # path2 = self.rebuild_path(v, self.path, i, j, True)
                dist = self.path_distance(path)
               
                # print(path[i-1], path2[i-1], path_o[i-1])
                # print(path[i], path2[i], path_o[i])
                # print(path[i+1], path2[i+1], path_o[i+1])
                # print("")
                # print(path[j-1], path2[j-1], path_o[j-1])
                # print(path[j], path2[j], path_o[j])
                # print(path[j+1], path2[j+1], path_o[j+1])
                # print("")
                # print("")
                # print(dist, self.path_distance(path2))

                if dist < self.dist:
                    self.dist = dist
                    self.path = path
                    print(dist)
                    q = True
                    break
                else:
                    v[i], v[j] = v[j], v[i] # swap back
            if q: break




    def outside_move_steep(self, v, u, v_indx, u_indx):
          
        for i in v_indx:
            for j in u_indx:
                v[i], u[j] = u[j], v[i] # swap to get neihbour solution

                path = self.build_path(v)
                dist = self.path_distance(path)

                if dist < self.dist:
                    self.dist = dist
                    self.path = path
                    print(dist)
                else:
                    v[i], u[j] = u[j], v[i] # swap back

    def inside_move_steep(self, v, v_indx):
          
        for i in v_indx:
            for j in v_indx:
                v[i], v[j] = v[j], v[i] # swap to get neihbour solution

                path = self.build_path(v)
                dist = self.path_distance(path)

                if dist < self.dist:
                    self.dist = dist
                    self.path = path
                    print(dist)
                else:
                    v[i], v[j] = v[j], v[i] # swap back


    def optimize_neighbours(self):
        v_indx = list(range(len(self.nodes)))
        u_indx = list(range(len(self.unused)))

        delta = 0.0
        prev_dist = 10**10

        while self.dist/prev_dist < 1.0 + delta:
            prev_dist = self.dist
            if self.style == 'greedy':
                self.outside_move_greedy(self.nodes, self.unused, v_indx, u_indx)
                self.inside_move_greedy(self.nodes, v_indx)
            elif self.style == 'steep':
                self.outside_move_steep(self.nodes, self.unused, v_indx, u_indx)
                self.inside_move_steep(self.nodes, v_indx)
        print (self.dist)