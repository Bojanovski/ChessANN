from dependencies import chess
import random
import numpy as np

def get_xy_from_index(i):
	x = i % 8
	y = i // 8
	return x, y

class BoardAnalyzer:
	def rate(self, board):
		#	neural network will go here
		return random.random();

	def train(self, inputs, outputs):
		return;
	
class ChessANNBoardInterface:
		
	def __init__(self):
		self.analyzer = BoardAnalyzer()
		self.board = chess.Board()

		self.wq = self.get_exists_and_position(chess.QUEEN, chess.WHITE)
		self.wr = self.get_exists_and_position(chess.ROOK, chess.WHITE)
		self.wb = self.get_exists_and_position(chess.BISHOP, chess.WHITE)
		self.wn = self.get_exists_and_position(chess.KNIGHT, chess.WHITE)
		self.wp = self.get_exists_and_position(chess.PAWN, chess.WHITE)

		self.bq = self.get_exists_and_position(chess.QUEEN, chess.BLACK)
		self.br = self.get_exists_and_position(chess.ROOK, chess.BLACK)
		self.bb = self.get_exists_and_position(chess.BISHOP, chess.BLACK)
		self.bn = self.get_exists_and_position(chess.KNIGHT, chess.BLACK)
		self.bp = self.get_exists_and_position(chess.PAWN, chess.BLACK)

		return
		
	def get_board(self):
		return self.board
		
	def get_exists_and_position(self, piece, color):
		p = self.board.pieces(piece, color)
		n = len(p)
		elements = []
		for sq in p:
			elements.append(get_xy_from_index(sq))
		return elements
    
	def evaluate(self, board, move):
		board.push(move)
		rating = self.analyzer.rate(board)
		board.pop()
		return rating
		
	def make_move(self):
		legal_moves = list(self.board.legal_moves)
		values = np.array([self.evaluate(self.board, x) for x in legal_moves])
		i = np.argmax(values)
		move = legal_moves[i]
		print(move)
		self.board.push(move)
		
		
		
		
		
