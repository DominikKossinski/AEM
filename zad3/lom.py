from init import *

from solution import Solution
from random import randint


class Move():
	def __init__(self, first, second):
		self.first = first
		self.second = second
		self.delta = 0

class Lom(Solution):

    def __init__(self, problem, style):
        super(Lom, self).__init__(problem)
        
        self.good_moves = []
		self.new_moves = self.get_all_moves()

		
	def optimize(self):
		while True:
			for move in self.new_moves:
				if move.delta < 0: good_moves.append(move)

			good_moves2 =[]
			for move in good_moves:
				if (self.check_move(move)): good_moves2.append(move)
			if len(good_moves) == 0: break
			good_moves = sorted(good_moves2, key=lambda x: x.delta)
			self.apply_move(good_moves[0])
			
			new_moves = []

	def apply_move(self, move):
        self.nodes[move.first:move.second] = self.nodes[move.second - 1:move.first - 1:-1]
        self.path = self.build_path(self.nodes)
			
    def check_move(self, move):
    	if move.first not in self.nodes: return False
    	if move.second not in self.nodes: return False
    	return True

    def get_all_moves(self):
    	pass
    	#TODO