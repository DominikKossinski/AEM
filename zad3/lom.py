from init import *

from solution import Solution
from edges import Edges


class Move():
    def __init__(self, first, second, delta, action):
        self.first = first
        self.second = second
        self.delta = delta
        self.action = action
    def show(self):
        return [self.first, self.second, self.delta]

class Lom(Edges):

    def __init__(self, problem):
        super(Lom, self).__init__(problem, 'steep')
        
        self.good_moves = []
        self.new_moves = []
        
    def optimize(self):
        print("Start distance", self.path_distance(self.path))
        self.new_moves = self.get_all_moves()
        # print(len(self.new_moves))
        # k = 0
        while True:
            # print (self.new_moves)
            if len(self.new_moves) > 0:
                # self.good_moves = []
                for move in self.new_moves:
                    if move.delta < 0: self.good_moves.append(move)

            # print(self.good_moves[0].delta, self.good_moves[0].first, self.good_moves[0].second)
            good_moves2 =[]
            for move in self.good_moves:
                if self.check_move(move):
                    if move.action == 'outer': move.delta = self.calc_outer_move(move.first, move.second)
                    if move.action == 'swap': move.delta = self.calc_swap_move(move.first, move.second)
                    if move.delta < 0: good_moves2.append(move)
            # print(len(self.good_moves) - len(good_moves2))
            if len(good_moves2) == 0: break
            self.good_moves = sorted(good_moves2, key=lambda x: x.delta)
            best_move = self.good_moves[0]
            # print(best_move.delta, best_move.first, best_move.second)
            self.apply_move(best_move)
            self.good_moves.pop(0)
            # print("s", self.good_moves[0].delta)
            # print([x.show() for x in self.good_moves])
            
            self.new_moves = self.get_new_moves(best_move)
            # self.new_moves = []
            # self.new_moves = self.get_all_moves()
            # k+=1
            # if k > 0: break
        print("End distance:", self.dist)

    def apply_move(self, move):
        # print(self.nodes)
        if move.action == 'swap': self.do_swap_move(move.first, move.second)
        if move.action == 'outer': self.do_outer_move(move.first, move.second)
        # print(self.nodes)
        # print(self.dist + move.delta)
        self.path = self.build_path(self.nodes)
        self.dist = self.path_distance(self.path)
        # print(move.delta, self.nodes,self.path)
        # print(self.dist)
            
    def check_move(self, move):
        i_in = move.first in self.nodes
        j_in = move.second in self.nodes
        if move.action == 'swap':
            return (i_in and j_in)

        elif move.action == 'outer':
            return (i_in and not j_in)# or (j_in and not i_in)

    def get_all_moves(self):
        moves = []
        for i in self.v_indexes:
                i_in = i in self.nodes
                for j in self.v_indexes:
                    if i == j: continue
                    j_in = j in self.nodes
                    if (i_in and not j_in):# or (j_in and not i_in):
                        delta = self.calc_outer_move(i, j)# * (1 if i_in else -1)
                        moves.append(Move(i,j,delta, 'outer'))

                    if i_in and j_in:
                        delta = self.calc_swap_move(i, j)
                        moves.append(Move(i,j,delta, 'swap'))

        return moves

    def get_new_moves(self, best_move):
        moves = []
        if best_move.action == 'swap':
            v_i = self.v_indexes[best_move.first:best_move.second]
            for i in v_i:
                i_in = i in self.nodes
                v_j = self.v_indexes[:best_move.first] + self.v_indexes[best_move.second:]
                for j in v_j:
                    if i == j: continue
                    j_in = j in self.nodes
                    if i_in and j_in:
                        delta = self.calc_swap_move(i, j)
                        moves.append(Move(i,j,delta, 'swap'))

            v_i = [best_move.first, best_move.second, best_move.second -1]
            if best_move.first + 1 <= len(self.nodes): v_i.append(best_move.first + 1)
            else: v_i.append(self.nodes[1]) 
            for i in v_i:
                i_in = i in self.nodes
                v_j = self.unused
                for j in v_j:
                    if i == j: continue
                    j_in = j in self.nodes
                    if (i_in and not j_in):# or (j_in and not i_in):
                        delta = self.calc_outer_move(i, j)# * (1 if i_in else -1)
                        moves.append(Move(i,j,delta, 'outer'))
        # if False: pass
        else:
            v_i = [best_move.second, best_move.second -1]
            if best_move.second + 1 <= len(self.nodes): v_i.append(best_move.second + 1)
            else: v_i.append(self.nodes[1]) 
            for i in v_i:
                i_in = i in self.nodes
                v_j = self.unused
                for j in v_j:
                    if i == j: continue
                    j_in = j in self.nodes
                    if (i_in and not j_in):# or (j_in and not i_in):
                        delta = self.calc_outer_move(i, j)# * (1 if i_in else -1)
                        moves.append(Move(i,j,delta, 'outer'))

            v_i = [best_move.first, best_move.second]
            for i in v_i:
                i_in = i in self.nodes
                v_j = self.nodes
                for j in v_j:
                    if i == j: continue
                    j_in = j in self.nodes
                    if i_in and j_in:
                        delta = self.calc_swap_move(i, j)
                        moves.append(Move(i,j,delta, 'swap'))
        return moves