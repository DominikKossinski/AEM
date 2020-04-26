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

    def __init__(self, problem, style):
        super(Lom, self).__init__(problem)
        
        self.good_moves = []
        self.new_moves = self.get_all_moves()

        
    def optimize(self):
        while True:
            for move in self.new_moves:
                if move.delta < 0: self.good_moves.append(move)

            good_moves2 =[]
            for move in self.good_moves:
                if (self.check_move(move)): good_moves2.append(move)
            if len(self.good_moves) == 0: break
            self.good_moves = sorted(good_moves2, key=lambda x: x.delta)
            self.apply_move(self.good_moves[0])
            self.good_moves.pop(0)
            
            new_moves = []

            #TODO 

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

                if i in self.nodes and j in self.nodes:
                    delta = self.calc_swap_move(i, j)
                    moves.append(Move(i,j,delta, 'swap'))