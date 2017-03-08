#!/usr/bin/env python
# -*- coding: utf-8 -*-
from chessboard import chessboard
import re

class evaluation (object):

	def __init__(self):

		self.blackFive = re.compile('11111')
		self.whiteFive = re.compile('22222')
		self.fiveList = [self.blackFive, self.whiteFive]

		self.blackLivingFour = re.compile('011110')
		self.whiteLivingFour = re.compile('022220')
		self.livingFourList = [self.blackLivingFour, self.whiteLivingFour]

		self.blackGoFour1 = re.compile('011112')
		self.blackGoFour2 = re.compile('0101110')
		self.blackGoFour3 = re.compile('0110110')

		self.whiteGoFour1 = re.compile('022221')
		self.whiteGoFour2 = re.compile('0202220')
		self.whiteGoFour3 = re.compile('0220220')
		self.goFourList = [self.blackGoFour1, self.blackGoFour2, self.blackGoFour3, self.whiteGoFour1, self.whiteGoFour2, self.whiteGoFour3]


		self.blackLivingThree1 = re.compile('01110')
		self.blackLivingThree2 = re.compile('010110')

		self.whiteLivingThree1 = re.compile('02220')
		self.whiteLivingThree2 = re.compile('020220')
		self.livingThreeList = [self.blackLivingThree1, self.blackLivingThree2, self.whiteLivingThree2, self.whiteLivingThree1]

		self.blackLivingTwo1 = re.compile('00110')
		self.blackLivingTwo2 = re.compile('01010')
		self.blackLivingTwo3 = re.compile('010010')

		self.whiteLivingTwo1 = re.compile('00220')
		self.whiteLivingTwo2 = re.compile('02020')
		self.whiteLivingTwo3 = re.compile('020020')
		self.livingTwoList = [self.blackLivingTwo1, self.blackLivingTwo2,self.blackLivingTwo3,self.whiteLivingTwo1, self.whiteLivingTwo2, self.whiteLivingTwo3]

		self.patternList = [self.blackFive, self.whiteFive, self.blackLivingFour, self.whiteLivingFour, self.blackGoFour1, self.blackGoFour2, self.blackGoFour3, self.whiteGoFour1, self.whiteGoFour2, self.whiteGoFour3, self.blackLivingThree2, self.blackLivingThree1, self.whiteLivingThree1, self.whiteLivingThree2,self.blackLivingTwo1, self.blackLivingTwo2 ,self.blackLivingTwo3 ,self.whiteLivingTwo1,self.whiteLivingTwo2,self.whiteLivingTwo3]
		self.posValue = []

		# Index for every chess mode:
		self.LivingFive = 1		# Living Five	
		self.LivingFour = 2		# Living LivingFour
		self.GoFour = 3		# Go LivingFour
		self.LivingThree = 4		# Living LivingThree
		self.GoThree = 5		# Go LivingThree
		self.LivingTwo = 6		# Living LivingTwo
		self.GoTwo = 7	# Go LivingTwo
		
		self.BLACK = 1
		self.WHITE = 2
		
		self.count = []				# counts for every chess mode 
		
		for i in xrange(15):
			# center position has a higher value
			row = [ (7 - max(abs(i - 7), abs(j - 7))) for j in xrange(15) ]
			self.posValue.append(tuple(row))
		self.posValue = tuple(self.posValue)

		self.count = [[0 for i in xrange(8)] for j in xrange(3)]
	
	def evaluate (self, board, turn):
		self.count = [[0 for i in xrange(8)] for j in xrange(3)]
		score = self.evaluation(board, turn)
		return score

	def evaluation(self, board, turn):
		count = self.count

		self.horizontalCheck(board, count)
		self.verticalCheck(board, count)
		self.leftDiagonalCheck(board, count)
		self.rightDiagonalCheck(board, count)

		BLACK = self.BLACK
		WHITE = self.WHITE
		LivingFive = self.LivingFive


		if turn == self.WHITE:
			if count[BLACK][LivingFive] > 0:
				return -100000
			if count[WHITE][LivingFive] > 0:
				return 100000
		else:
			if count[WHITE][LivingFive] > 0:
				return -100000
			if count[BLACK][LivingFive] > 0:
				return 100000

		whiteValue, blackValue, win = 0, 0, 0
		if turn == WHITE:
			# these modes are unable to be defended by opponents
			if self.EnsuredWin(count, WHITE): 
				return 10000
			if self.EnsuredLose(count, WHITE):
				return -10000
			self.valueEvalution(turn, whiteValue, blackValue, count)
		else:
		# for black chess:
			if self.EnsuredWin(count, BLACK):
				return 10000
			if self.EnsuredLose(count, BLACK):
				return -10000
			self.valueEvalution(turn, blackValue, whiteValue, count)
		

		
		wc, bc = 0, 0
		for i in xrange(15):
			for j in xrange(15):
				stone = board[i][j]
				if stone != 0:
					if stone == WHITE:
						wc += self.posValue[i][j]
					else:
						bc += self.posValue[i][j]
		whiteValue += wc
		blackValue += bc
		
		if turn == WHITE:
			return whiteValue - blackValue
		return blackValue - whiteValue

	def EnsuredWin(self, count, turn):
		if turn == 1:
			opponent = 2
		else:
			opponent = 1

		if count[turn][self.LivingFour] > 0 or \
			count[turn][self.GoFour] > 1 or \
			(count[turn][self.GoFour] and count[turn][self.LivingThree]):
		 	return True
		else:
			return False

	def EnsuredLose(self, count, turn):
		if turn == 1:
			opponent = 2
		else:
			opponent = 1

		if count[opponent][self.LivingFour] > 0 or\
			count[opponent][self.GoFour] > 1 or \
			(count[opponent][self.GoFour] and count[opponent][self.LivingThree]):
			return True
		else:
			return False

	def valueEvalution(self, turn, selfValue, oppoValue, count):
		BLACK, WHITE = 1, 2
		if turn == BLACK:
			opponent = WHITE
		else:
			opponent = BLACK

		if count[turn][self.LivingThree] > 1:
			selfValue += 5000
		elif count[turn][self.LivingThree]:
			selfValue += 200
		if count[opponent][self.LivingThree] > 1:
			oppoValue += 5000
		elif count[opponent][self.LivingThree]:
			oppoValue += 200
		if count[turn][self.LivingTwo]:
			selfValue += count[turn][self.LivingTwo] * 5
		if count[opponent][self.LivingTwo]:
			oppoValue += count[opponent][self.LivingTwo] * 5


	def horizontalCheck (self, board, count):
		for i in xrange(15):
			line = ''
			for j in xrange(15):
				line+= str(board[i][j])
			self.lineEvaluation(line, count)
			

	def verticalCheck (self, board, count):
		for i in xrange(15):
			line = ''
			for j in xrange(15):
				line += str(board[j][i])
			self.lineEvaluation(line, count)

	def leftDiagonalCheck(self, board, count):

		for i in xrange(4, 25):
			line = ''
			if i <= 14:
				for j in xrange(i + 1):
					line += str(board[j][i - j])
				self.lineEvaluation(line, count)
			else:
				for j in xrange(i - 14, 15):
					line += str(board[j][i - j])
				self.lineEvaluation(line, count)



	def rightDiagonalCheck(self, board, count):
		for x in xrange(15):
			line = ''
			for y in xrange(15 - x):
				line += str(board[x + y][y])
			self.lineEvaluation(line, count)
		for y in xrange(15):
			line = ''
			for x in xrange(15 - y):
				line += str(board[x][y + x])
			self.lineEvaluation(line, count)



	def lineEvaluation(self, line, count):

		for pattern in self.patternList:
			if re.search(pattern, line) is not None:
				return self.searchPattern(pattern, count)


	def searchPattern(self, pattern, count):
		WHITE, BLACK = self.WHITE, self.BLACK
		for index, p in enumerate(self.patternList):
			if p == pattern:
				if index == 0:
					count[BLACK][self.LivingFive] += 1
				if index == 1:
					count[WHITE][self.LivingFive] += 1
				if index == 2:
					count[BLACK][self.LivingFour] += 1
				if index == 3:
					count[WHITE][self.LivingFour] += 1
				if 3 < index < 7:
					count[BLACK][self.GoFour] += 1
				if 6 < index < 10:
					count[WHITE][self.GoFour] += 1
				if 9 < index < 12:
					count[BLACK][self.LivingThree] += 1
				if 11< index < 14:
					count[WHITE][self.LivingThree] += 1
				if 13 < index < 17:
					count[BLACK][self.LivingTwo] += 1
				if 16 < index < 20:
					count[WHITE][self.LivingTwo] += 1
		return 0
		


				


