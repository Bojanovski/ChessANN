import NetworkTrainer as nt
import numpy as np
from FeatureExtractor import extract_features
from ChessANNBoardInterface import ChessANNBoardInterface, BoardAnalyzer
from Network import NNetwork
import Evaluator as e
import random
import pdb

STOHASTIC_PROB=0.1

def train(game_num):
    net = NNetwork([[15,144,128],[10,110,100]],[100,1])
    cache = {}
    
    for i in range(game_num):
        board = ChessANNBoardInterface()
        print('Game {}/{}'.format(i+1, game_num))
        print(board.get_board())
        
        while(not board.get_board().is_game_over()):
            bestmove = ''
            if board.get_board().fen() in cache.keys():
                bestmove = cache[board.get_board().fen()]
            else:
                bestmove = e.get_best_move(board.get_board())
                cache[board.get_board().fen()] = bestmove
            moves = list(board.get_board().legal_moves)
            ratings = [1 if str(x) == bestmove else -1 for x in moves]
            copies = [board.copy() for x in moves]
            copies = [copies[x].push_piece_alt(moves[x]) for x in range(len(moves))]
            features = [extract_features(x) for x in copies]
            
            X = np.array(features)
            Y = np.array([ratings]).T
            
            print(net.train(X, Y, 100, 0.2)[-1])
            print(net.predict(X))
            
            if random.random() < STOHASTIC_PROB:
                board.push_piece(moves[random.randint(0, len(moves))])
            else:
                board.push_piece(moves[np.array(ratings).argmax()])
            
            print()
            print(board.get_board())
        
    return net


if __name__=="__main__":
    net = train(1)
    nt.play(net)
