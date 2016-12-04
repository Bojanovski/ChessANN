import chess;
import random;
import numpy as np;
class decider:
  
  def make_move(self, board):
    legal_moves = list(board.legal_moves)
    values = np.array([self.evaluate(board, x) for x in legal_moves])
    board.push(legal_moves[np.argmax(values)])
    
  def evaluate(self, board, move):
    board.push(move);
    rating = self.rate(board);
    board.pop()
    return rating;
    
  def rate(self, board):
    return random.random();
