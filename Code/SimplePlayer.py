from dependencies import chess
import random
import numpy as np

class BoardAnalyzer:
  def rate(self, board):
    return random.random();
    
  def train(self, inputs, outputs):
    return;

class Decider:
  def __init__(self, analyzer = BoardAnalyzer()):
    self.analyzer = analyzer
  
  def make_move(self, board):
    legal_moves = list(board.legal_moves)
    values = np.array([self.evaluate(board, x) for x in legal_moves])
    board.push(legal_moves[np.argmax(values)])
    
  def evaluate(self, board, move):
    board.push(move)
    rating = self.analyzer.rate(board)
    board.pop()
    return rating

	
b = BoardAnalyzer()