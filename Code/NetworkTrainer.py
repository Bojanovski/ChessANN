import numpy as np
import FeatureExtractor as fe
import Evaluator as ev
import ChessANNBoardInterface as cabi
import Network as n
import GameLoader as gl

net = n.NNetwork([[15,144,128],[10,110,100]], [100,1])
loader = gl.GameLoader('Games.txt')

for i in range(loader.get_game_num()):
    X = [];
    Y = [];
    
    board = cabi.ChessANNBoardInterface()
    for move in loader.get_game(0).get_moves():
        board.push_piece(move)
        X += fe.extract_features(board)
        Y += [ev.evaluate_position(board.get_board(), DEPTH=5)/float(250)]
    X = np.array(X)
    Y = np.array(Y)
    
    net.train(X,Y,100,0.1)

interface = cabi.ChessANNBoardInterface(analyzer = cabi.BoardAnalyzer(network = net))
while(not interface.get_board().is_game_over()):
    print(interface.get_board())
    
    mv = input("Please enter your move in algebraic notation: ")
    interface.push_piece(mv)
    interface.make_move()
