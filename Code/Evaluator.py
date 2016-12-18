import subprocess
import re

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
    matcher = re.match(".*score cp ([0-9]+).*", line)
    score = int(matcher.group(1))
    return score
