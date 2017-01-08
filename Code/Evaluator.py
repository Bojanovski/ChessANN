import subprocess
import re
import pdb
import chess
from GameLoader import GameLoader
import time

ENGINE_BIN = "stockfish"
DEPTH = 20

def evaluate_position(board, depth=DEPTH):
    """Evaluates the board's current position.

    Returns the Stockfish scalar score, at the given depth, in centipawns.
    """

    engine = subprocess.Popen(ENGINE_BIN, bufsize=0, universal_newlines=True,
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    # take care of initial (credits) line
    engine.stdout.readline()

    # search from current position to given depth
    engine.stdin.write("position fen "+board.fen()+"\n")
    engine.stdin.write("go depth "+str(DEPTH)+"\n")

    while True:
        line = engine.stdout.readline().strip()
        if line.startswith("info") and (" depth "+str(DEPTH)) in line \
                and "score cp" in line and "bound" not in line:
            break

    engine.stdin.write("quit\n")
    # score in centipawns
    matcher = re.match(".*score cp (-?[0-9]+).*", line)
    score = int(matcher.group(1))
    return score


def get_best_move(board, depth=DEPTH):
    engine = subprocess.Popen(ENGINE_BIN, bufsize=0, universal_newlines=True,
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    # take care of initial (credits) line
    engine.stdout.readline()

    # search from current position to given depth
    engine.stdin.write("position fen "+board.fen()+"\n")
    engine.stdin.write("go depth "+str(DEPTH)+"\n")

    while True:
        line = engine.stdout.readline().strip()
        if line.startswith("bestmove"):
            break

    engine.stdin.write("quit\n")
    # score in centipawns
    move = line.split()[1]
    return move


def evaluate_dataset(file_path):
    loader = GameLoader(file_path)
    cache = {}
    with open("../Dataset/60-x", "w") as result_file:
        gamenum = loader.get_game_num()
        loader.get_game(60)
        for i in range(60, gamenum):
            print('Game {}/{}'.format(i, gamenum), flush=True)
            try:
                game = loader.get_game(0)
                game.format_data()
                board = chess.Board()
                ratelist = []
                count = 1
                moves = game.buffer
                for move in moves:
                    print('\tMove {}/{}'.format(count, len(moves)), flush=True)
                    count += 1
                    board.push_san(move)
                    if board.fen() in cache.keys():
                        ratelist += [cache[board.fen()]]
                    else:
                        print('\t\tEvaluating...', flush=True)
                        ratelist += [evaluate_position(board, depth=10)]
                        cache[board.fen()] = ratelist[-1]
                print(" ".join([str(x) for x in ratelist]), file=result_file, flush=True)
            except:
                continue

if __name__ == '__main__':
    evaluate_dataset('../Dataset/Games.txt')
