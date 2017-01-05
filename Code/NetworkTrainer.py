import numpy as np
from FeatureExtractor import extract_features
from ChessANNBoardInterface import ChessANNBoardInterface, BoardAnalyzer
from Network import NNetwork
from GameLoader import GameLoader

def load_data():
    loader = GameLoader('../Dataset/Games.txt')

    with open('../Dataset/ratings') as f:
        lines = f.read().splitlines()
        ratings = [[int(x) for x in line.split()] for line in lines]
    count = 0

    X = []
    Y = []
    for i in range(loader.get_game_num()):
        board = ChessANNBoardInterface()
        game = loader.get_game(0)
        game.format_data()
        moves = game.buffer
        if count < len(ratings) and len(moves) == len(ratings[count]):
            for i in range(len(moves)):
                try:
                    board.push_piece(moves[i])
                    X += [extract_features(board)]
                    Y += [[ratings[count][i]]]
                except Exception:
                    continue
            count += 1
            print(count/float(len(ratings)))

    X = np.array(X)
    Y = np.array(Y)
    Y = (Y-Y.min())/(Y.max()-Y.min()) * 2 - 1

    return X, Y


####### ZANIMLJIVI DIO KODA #######

def train(X, Y):
    net = NNetwork([[15,144,128],[10,110,100]], [100,Y.shape[1]])

    batch_size = 200
    batch_num = int(X.shape[0]/batch_size)
    epochs = 1000

    niter = 1
    lr = 1e-5

    print("Training NN for {} epochs; batch_size is {}, eta is {}"\
            .format(epochs, batch_size, lr))

    for i in range(epochs):
        perm = np.random.permutation(X.shape[0])
        Xperm = X[perm]
        Yperm = Y[perm]

        X_batches = np.array_split(Xperm, batch_num, axis=0)
        Y_batches = np.array_split(Yperm, batch_num, axis=0)
        print('Epoch: {}/{}'.format(i, epochs))

        err_sum = 0
        for it, (batX, batY) in enumerate(zip(X_batches, Y_batches)):
            err = net.train(batX, batY, niter, lr)
            err_sum += err[-1]
            # print('\tBatch ({}/{}) error: {}'.format(it, batch_num, err[-1]))
        print('Epoch average error: {}'.format(err_sum/float(batch_num)))

    return net


def play(net):
    interface = ChessANNBoardInterface(analyzer = BoardAnalyzer(network = net))
    while (not interface.get_board().is_game_over()):
        print(interface.get_board())
        try:
            mv = input("Please enter your move in algebraic notation: ")
        except ValueError:
            continue
        interface.push_piece(mv)
        interface.make_move()

if __name__=="__main__":
    X, Y = load_data()
    net = train(X, Y)
    play(net)
