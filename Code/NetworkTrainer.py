import numpy as np
import FeatureExtractor as fe
import ChessANNBoardInterface as cabi
import Network as n
import GameLoader as gl
import pdb

loader = gl.GameLoader('../Dataset/Games.txt')

with open('../Dataset/ratings') as f:
    lines = f.read().splitlines()
    ratings = [[int(x) for x in line.split()] for line in lines]
cnt = 0

X = [];
Y = [];
for i in range(loader.get_game_num()):
    board = cabi.ChessANNBoardInterface()
    game = loader.get_game(0)
    game.format_data()
    moves = game.buffer
    if cnt < len(ratings) and len(moves) == len(ratings[cnt]):
        for i in range(len(moves)):
            try:
                board.push_piece(moves[i])
            except Exception:
                continue
            X += [fe.extract_features(board)]
            Y += [[ratings[cnt][i]]]
        cnt += 1
        print(cnt/float(len(ratings)))
        
X = np.array(X)
Y = np.array(Y)
Y = (Y-Y.min())/(Y.max()-Y.min())

####### ZANIMLJIVI DIO KODA #######
net = n.NNetwork([[15,144,128],[10,110,100]], [100,1])

batch_size = 50
batch_num = X.shape[0]/batch_size
epochs = 100

niter = 1000
lr = 0.05
for i in range(epochs):
    perm = np.random.permutation(X.shape[0])
    Xperm = X[perm]
    Yperm = Y[perm]
    
    X_batches = np.array_split(Xperm, batch_num, axis=0)
    Y_batches = np.array_split(Yperm, batch_num, axis=0)
    print('Epoch: {}/{}'.format(i, epochs))
    
    for batX, batY in zip(X_batches, Y_batches):
        err = net.train(batX, batY, niter, lr)
        print('\tBatch error: {}'.format(err[-1]))

interface = cabi.ChessANNBoardInterface(analyzer = cabi.BoardAnalyzer(network = net))
while(not interface.get_board().is_game_over()):
    print(interface.get_board())
    
    mv = input("Please enter your move in algebraic notation: ")
    interface.push_piece(mv)
    interface.make_move()
