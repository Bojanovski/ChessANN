import numpy as np
import FeatureExtractor as fe
import Evaluator as ev
import ChessANNBoardInterface as cabi
import Network as n
import GameLoader as gl
import pdb

net = n.NNetwork([[15,144,128],[10,110,100]], [100,1])
loader = gl.GameLoader('../Dataset/Games.txt')
interface = cabi.ChessANNBoardInterface(analyzer = cabi.BoardAnalyzer(network = net))


for i in range(loader.get_game_num()):
    X = [];
    Y = [];
    
    board = cabi.ChessANNBoardInterface()
    game = loader.get_game(0)
    game.format_data()
    for move in game.buffer:
        print(move)
        board.push_piece(move)
        X += fe.extract_features(board)
        stockfish = ev.evaluate_position(board.get_board(), depth=10)/float(100)
        Y += [stockfish]
        print(stockfish)
    X = np.array(X)
    Y = np.array(Y)
    
    net.train(X,Y,1,0.1)

while(not interface.get_board().is_game_over()):
    print(interface.get_board())
    
    mv = input("Please enter your move in algebraic notation: ")
    interface.push_piece(mv)
    interface.make_move()
