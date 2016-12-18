from dependencies import chess
import random
import numpy as np

def get_xy_from_index(i):
    x = i % 8
    y = i // 8
    return x, y

def get_xy_from_char_and_number(cn):
    x = ord(cn[0]) - ord('a')
    y = ord(cn[1]) - ord('1')
    return x, y
    
class BoardAnalyzer:
    def rate(self, board):
        #   neural network will go here
        return random.random();

    def train(self, inputs, outputs):
        return;

class Piece:
    def __init__(self, piece, color, index, pos):
        self.piece = piece
        self.color = color
        self.index = index
        self.pos = pos
        return
        
class ChessANNBoardInterface:
        
    def __init__(self):
        self.analyzer = BoardAnalyzer()
        self.board = chess.Board()
        
        self.boardArray = {}
        for i in range(8):
            for j in range(8):
                self.boardArray[i,j] = None
        
        self.get_exists_and_position(chess.KING, chess.WHITE)
        self.get_exists_and_position(chess.QUEEN, chess.WHITE)
        self.get_exists_and_position(chess.ROOK, chess.WHITE)
        self.get_exists_and_position(chess.BISHOP, chess.WHITE)
        self.get_exists_and_position(chess.KNIGHT, chess.WHITE)
        self.get_exists_and_position(chess.PAWN, chess.WHITE)

        self.get_exists_and_position(chess.KING, chess.BLACK)
        self.get_exists_and_position(chess.QUEEN, chess.BLACK)
        self.get_exists_and_position(chess.ROOK, chess.BLACK)
        self.get_exists_and_position(chess.BISHOP, chess.BLACK)
        self.get_exists_and_position(chess.KNIGHT, chess.BLACK)
        self.get_exists_and_position(chess.PAWN, chess.BLACK)
        
        #print(self.boardArray)
        
        return
        
    def get_board(self):
        return self.board
    
    def get_piece(self, piece, color):
        pList = []
        for key in self.boardArray:
            if self.boardArray[key] != None and \
                self.boardArray[key].piece == piece and \
                self.boardArray[key].color == color:
                pList.append(self.boardArray[key])
        return pList
    
    def get_exists_and_position(self, piece, color):
        p = self.board.pieces(piece, color)
        n = len(p)
        elements = []
        i = 0
        for sq in p:
            x, y = get_xy_from_index(sq)
            newEle = Piece(piece, color, i, (x, y))
            i += 1
            elements.append(newEle)
            self.boardArray[x, y] = newEle
        return elements
    
    def evaluate(self, board, move):
        board.push(move)
        rating = self.analyzer.rate(board)
        board.pop()
        return rating
        
    def make_move(self):
        legal_moves = list(self.board.legal_moves)
        values = np.array([self.evaluate(self.board, x) for x in legal_moves])
        i = np.argmax(values)
        move = legal_moves[i]
        posXY = get_xy_from_char_and_number(move.uci()[0:2])
        moveToXY = get_xy_from_char_and_number(move.uci()[2:4])
        self.board.push(move)
        
        # update interface's position data      
        self.boardArray[moveToXY] = self.boardArray[posXY]
        self.boardArray[moveToXY].pos = moveToXY
        self.boardArray[posXY] = None
        
    def space_to_move_left(self, posXY, color):
        x = posXY[0]
        y = posXY[1]
        count = 0
        for i in reversed(range(x)):
            if self.boardArray[i,y] != None:
                if self.boardArray[i,y].color != color:
                    count += 1  # eating the enemy means one additional
                                # step in that direction
                break
            else:
                count += 1
        return count
        
    def space_to_move_right(self, posXY, color):
        x = posXY[0]
        y = posXY[1]
        count = 0
        for i in range(x+1, 8):
            if self.boardArray[i,y] != None:
                if self.boardArray[i,y].color != color:
                    count += 1  # eating the enemy means one additional
                                # step in that direction
                break
            else:
                count += 1
        return count
        
    def space_to_move_up(self, posXY, color):
        x = posXY[0]
        y = posXY[1]
        count = 0
        for i in range(y+1, 8):
            if self.boardArray[x,i] != None:
                if self.boardArray[x,i].color != color:
                    count += 1  # eating the enemy means one additional
                                # step in that direction
                break
            else:
                count += 1
        return count
        
    def space_to_move_down(self, posXY, color):
        x = posXY[0]
        y = posXY[1]
        count = 0
        for i in reversed(range(y)):
            if self.boardArray[x,i] != None:
                if self.boardArray[x,i].color != color:
                    count += 1  # eating the enemy means one additional
                                # step in that direction
                break
            else:
                count += 1
        return count
        
    def space_to_move_left(self, posXY, color):
        x = posXY[0]
        y = posXY[1]
        count = 0
        for i in reversed(range(x)):
            if self.boardArray[i,y] != None:
                if self.boardArray[i,y].color != color:
                    count += 1  # eating the enemy means one additional
                                # step in that direction
                break
            else:
                count += 1
        return count
