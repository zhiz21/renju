#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, time
from eva import evaluation
from chessboard import chessboard


# DFS search:
class search (object):

	# initialize the state
	def __init__ (self):
		self.evaluation = evaluation()
		self.board = [ [ 0 for n in xrange(15) ] for i in xrange(15) ]
		self.maxdepth = 3

	# get the current chess status 
	def generateSuccessors (self, turn):
		moves = []
		mostLeft = 15
		mostRight = 0
		mostTop = 15
		mostBottom = 0
		# get the range of positions with chess on
		for i in xrange(15):
			for j in xrange(15):
				if self.board[i][j] != 0:
					mostLeft = min(mostLeft, i)
					mostRight = max(mostRight, i)
					mostTop = min(mostTop, j)
					mostBottom = max(mostBottom, j)

		# search for positions have a less than three distance to node with chess on
		for i in range(max(mostLeft-3, 0), min(mostRight+3, 15)):
			for j in range(max(mostTop-3, 0), min(mostBottom+3, 15)):
				if self.board[i][j] == 0:
					score = self.evaluation.posValue[i][j]
					
					moves.append((score, i, j))

		moves.sort()
		moves.reverse()
		return moves
	
	# search for optimal evaluation
	def alphaBetaSearch (self, turn, depth, alpha = float('-Inf'), beta = float('Inf')):

		# evaluate and return if depth = 0 
		if depth <= 0: 
			return self.evaluation.evaluate(self.board, turn)

		# return if game ends
		score = self.evaluation.evaluate(self.board, turn)
		if abs(score) >= 99999 and depth < self.maxdepth: 
			return score

		# generate next movement
		moves = self.generateSuccessors(turn)
		optimalMove = None

		# for all next movements:
		for score, row, col in moves:

			# set the given position with correct chess
			self.board[row][col] = turn
			
			# get the next turn
			if turn == 1:
				nextTurn = 2
			else:
				nextTurn = 1

			# use DFS search to return the evaluation and position
			score = - self.alphaBetaSearch(nextTurn, depth - 1, -beta, -alpha)

			# delete the chess we set during the search
			self.board[row][col] = 0

			# alpha/beta pruning 
			# use alpha/beta to speed the search
			if score > alpha:
				alpha = score
				optimalMove = (row, col)
				if alpha >= beta:
					break
		
		# record the best movement at first depth 
		if depth == self.maxdepth and optimalMove:
			self.optimalMove = optimalMove

		# return the optimal score and movement
		return alpha

	

	# main search function, given current chessboard state, turn and depth
	def search (self, turn, depth = 3):
		self.maxdepth = depth
		self.optimalMove = None
		score = self.alphaBetaSearch(turn, depth)
		if abs(score) > 90000:
			self.maxdepth = depth
			score = self.alphaBetaSearch(turn, 1)
		row, col = self.optimalMove
		return score, row, col



	def minimaxSearch (self, turn, depth):

		# evaluate and return if depth = 0 
		if depth <= 0:
			score = self.evaluation.evaluate(self.board, turn)
			return score

		# generate next movement
		moves = self.generateSuccessors(turn)
		optimalMove = None
		optimalScore = float('-Inf')
		# for all next movements:
		for score, row, col in moves:

			# set the given position with correct chess
			self.board[row][col] = turn
			
			# get the next turn
			if turn == 1:
				nextTurn = 2
			else:
				nextTurn = 1

			# use DFS search to return the evaluation and position
			score = - self.minimaxSearch(nextTurn, depth - 1, -beta, -alpha)

			# delete the chess we set during the search
			self.board[row][col] = 0
			
			if score > optimalScore:
				optimalScore = score
				optimalMove = (row, col)
		
		# record the best movement at first depth 
		if depth == self.maxdepth and optimalMove:
			self.optimalMove = optimalMove

		# return the optimal score and movement
		return optimalScore