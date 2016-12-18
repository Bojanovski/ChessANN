import subprocess

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

    last_line = ""
    while True:
        line = engine.stdout.readline().strip()
        if "bestmove" in line:
            break
        else:
            last_line = line

    engine.stdin.write("quit\n")

    # score in centipawns
    score = last_line.split()[9]

    return score
