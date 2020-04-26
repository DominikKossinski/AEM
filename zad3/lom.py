from init import *

from solution import Solution
from edges import Edges


class Move():
    def __init__(self, first, second, delta, action):
        self.first = first
        self.second = second
        self.delta = delta
        self.action = action

class Lom(Edges):

    def __init__(self, problem):
        super(Lom, self).__init__(problem, 'steep')
        
        self.good_moves = []
        self.new_moves = self.get_all_moves()

        
    def optimize(self):
        while True:
            if len(self.new_moves) > 0:
                for move in self.new_moves:
                    if move.delta < 0: self.good_moves.append(move)

            good_moves2 =[]
            for move in self.good_moves:
                if (self.check_move(move)): good_moves2.append(move)
            if len(good_moves2) == 0: break
            self.good_moves = sorted(good_moves2, key=lambda x: x.delta)
            best_move = self.good_moves[0]
            self.apply_move(best_move)
            self.good_moves.pop(0)
            
            self.new_moves = self.get_new_moves(best_move)

    def apply_move(self, move):
        if move.action == 'swap': self.do_swap_move()
        if move.action == 'outer': self.do_outer_move()
            
    def check_move(self, move):
        if move.action == 'swap':
            return (move.first in self.nodes and move.second in self.nodes)

        elif move.action == 'outer':
            return (move.first  in self.nodes and move.second in self.unused) or (move.second in self.nodes and move.first  in self.unused)

    def get_all_moves(self):
        moves = []
        for i in self.v_indexes:
            for j in self.v_indexes:
                if i == j: continue
                if (i in self.nodes and j in self.unused) or (j in self.nodes and i in self.unused):
                    delta = self.calc_outer_move(i, j)
                    moves.append(Move(i,j,delta, 'outer'))

                if i in self.nodes and j in self.nodes:
                    delta = self.calc_swap_move(i, j)
                    moves.append(Move(i,j,delta, 'swap'))

        return moves

    def get_new_moves(self, best_move):
        moves = []
        for i in self.v_indexes[best_move.first:best_move.second]:
            for j in (self.v_indexes[:best_move.first] + self.v_indexes[best_move.second:]):
                if i == j: continue
                if (i in self.nodes and j in self.unused) or (j in self.nodes and i in self.unused):
                    delta = self.calc_outer_move(i, j)
                    moves.append(Move(i,j,delta, 'outer'))

                if i in self.nodes and j in self.nodes:
                    delta = self.calc_swap_move(i, j)
                    moves.append(Move(i,j,delta, 'swap'))

        return moves