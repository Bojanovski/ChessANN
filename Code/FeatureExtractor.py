from dependencies import chess
import random
import numpy as np
import SimplePlayer as sp

def is_empty(board, square):
	return board.piece_type_at(square) == None
	
def get_material_configuration(board):
	wq = len(board.pieces(chess.QUEEN, chess.WHITE))
	wr = len(board.pieces(chess.ROOK, chess.WHITE))
	wb = len(board.pieces(chess.BISHOP, chess.WHITE))
	wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
	wp = len(board.pieces(chess.PAWN, chess.WHITE))
	
	bq = len(board.pieces(chess.QUEEN, chess.BLACK))
	br = len(board.pieces(chess.ROOK, chess.BLACK))
	bb = len(board.pieces(chess.BISHOP, chess.BLACK))
	bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
	bp = len(board.pieces(chess.PAWN, chess.BLACK))
	return [wq, wr, wb, wn, wp, bq, br, bb, bn, bp] 
	
def get_castling_rights(board):
	k_white = board.has_kingside_castling_rights(chess.WHITE) \
					and is_empty(board, chess.F1) \
					and is_empty(board, chess.G1)
	
	q_white = board.has_queenside_castling_rights(chess.WHITE) \
					and is_empty(board, chess.B1) \
					and is_empty(board, chess.C1) \
					and is_empty(board, chess.D1)
					
	k_black = board.has_kingside_castling_rights(chess.BLACK) \
					and is_empty(board, chess.F8) \
					and is_empty(board, chess.G8)
					
	q_black = board.has_queenside_castling_rights(chess.BLACK) \
					and is_empty(board, chess.B8) \
					and is_empty(board, chess.C8) \
					and is_empty(board, chess.D8)
					
	return [k_white, q_white, k_black, q_black]
					
def extract_global_features(board):
	assert(board.is_valid())
	vec = []
	
	# White's turn
	vec.append(board.turn)
	
	# Material configuration
	vec.extend(get_material_configuration(board))
	
	# Castling rights
	vec.extend(get_castling_rights(board))
	
	return

def extract_piece_centric_features(board):
	assert(board.is_valid())
	vec = []
	
	wqp 
	
	print(vec)
	return

def extract_attack_def_maps(board):
  assert(board.is_valid())
  
  value_dict = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK:5, chess.QUEEN:9}
  
  
  print(board.attackers(chess.WHITE, chess.F3))
	
board = chess.Board()
dec = sp.Decider()

while (True):
	print(board)
	#extract_global_features(board)
	#extract_piece_centric_features(board)
	extract_attack_def_maps(board)
  
	dec.make_move(board)
	input()


