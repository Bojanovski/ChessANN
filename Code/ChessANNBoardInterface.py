from dependencies import chess
import random
import numpy as np
import pdb
import FeatureExtractor as fe
import copy

random.seed(2)

def get_xy_from_index(i):
    x = i % 8
    y = i // 8
    return x, y

def get_xy_from_char_and_number(cn):
    x = ord(cn[0]) - ord('a')
    y = ord(cn[1]) - ord('1')
    return x, y
    
class BoardAnalyzer:
    def __init__(self, network=None):
        self.net = network
    
    def rate(self, board):
        #   neural network will go here
        if self.net == None:
            return random.random();
        else:
            return self.net.predict([np.array(fe.extract_features(board))])[0,0]

class Piece:
    def __init__(self, piece, color, index, pos):
        self.piece = piece
        self.color = color
        self.index = index
        self.pos = pos
        return
        
class ChessANNBoardInterface:
        
    def __init__(self, analyzer = BoardAnalyzer()):
        self.moveCounter = 0
        self.analyzer = analyzer
        self.board = chess.Board()
        self.movesList = []
		
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

    def copy(self):
        interface = ChessANNBoardInterface()
        for move in self.movesList:
            interface.push_piece(move)
        return interface
	
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
        # copy board to cpy
        cpy = self.copy()
        cpy.push_piece(move)
        rating = self.analyzer.rate(cpy)
        # board.pop()
        return rating
    
    # returns the rook move if there is castling
    def is_castling(self, move):
        posXY = get_xy_from_char_and_number(move.uci()[0:2])
        moveToXY = get_xy_from_char_and_number(move.uci()[2:4])
        pieceType = self.boardArray[posXY].piece
        pieceColor = self.boardArray[posXY].color
        if (pieceType == chess.KING):
            if (pieceColor == chess.WHITE):
                if (moveToXY[0] + 1 < posXY[0]): # left castling
                    return ((0, 0), (moveToXY[0]+1, 0))
                elif (moveToXY[0] - 1 > posXY[0]): # right castling
                    return ((7, 0), (moveToXY[0]-1, 0))
            else: # black
                if (moveToXY[0] + 1 < posXY[0]): # left castling
                    return ((0, 7), (moveToXY[0]+1, 7))
                elif (moveToXY[0] - 1 > posXY[0]): # right castling
                    return ((7, 7), (moveToXY[0]-1, 7))
        return None
        
    def push_piece(self, move):
        if isinstance(move, str):
            self.board.push_san(move)
            move = self.board.pop()
        
        self.moveCounter += 1
        
        posXY = get_xy_from_char_and_number(move.uci()[0:2])
        moveToXY = get_xy_from_char_and_number(move.uci()[2:4])
        
        self.board.push(move)
        self.movesList.append(move)
		
        c_ret = self.is_castling(move)
        if (c_ret):
            c_posXY, c_moveToXY = c_ret
            self.boardArray[c_moveToXY] = self.boardArray[c_posXY]
            self.boardArray[c_moveToXY].pos = c_moveToXY
            self.boardArray[c_posXY] = None
        
        self.boardArray[moveToXY] = self.boardArray[posXY]
        self.boardArray[moveToXY].pos = moveToXY
        self.boardArray[posXY] = None
    
    def make_move(self):
        #self.moveCounter += 1
        legal_moves = list(self.board.legal_moves)
        values = np.array([self.evaluate(self, x) for x in legal_moves])
        if (len(values) == 0):
            print("Check mate, br0!")
        i = np.argmax(values)
        move = legal_moves[i]
        #posXY = get_xy_from_char_and_number(move.uci()[0:2])
        #moveToXY = get_xy_from_char_and_number(move.uci()[2:4])
        #self.board.push(move)
        
        # update interface's position data
        #c_ret = self.is_castling(move)
        #if (c_ret):
        #    c_posXY, c_moveToXY = c_ret
        #    self.boardArray[c_moveToXY] = self.boardArray[c_posXY]
        #    self.boardArray[c_moveToXY].pos = c_moveToXY
        #    self.boardArray[c_posXY] = None
        #
        #self.boardArray[moveToXY] = self.boardArray[posXY]
        #self.boardArray[moveToXY].pos = moveToXY
        #self.boardArray[posXY] = None
        
        self.push_piece(move)
        
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
        
    def space_to_move_left_down(self, posXY, color):
        x = posXY[0]
        y = posXY[1]
        count = 0
        steps = min(x, y)
        for i in range(1, steps+1):
            if self.boardArray[x-i,y-i] != None:
                if self.boardArray[x-i,y-i].color != color:
                    count += 1  # eating the enemy means one additional
                                # step in that direction
                break
            else:
                count += 1
        return count
        
    def space_to_move_left_up(self, posXY, color):
        x = posXY[0]
        y = posXY[1]
        count = 0
        steps = min(x, 7-y)
        for i in range(1, steps+1):
            if self.boardArray[x-i,y+i] != None:
                if self.boardArray[x-i,y+i].color != color:
                    count += 1  # eating the enemy means one additional
                                # step in that direction
                break
            else:
                count += 1
        return count

    def space_to_move_right_down(self, posXY, color):
        x = posXY[0]
        y = posXY[1]
        count = 0
        steps = min(7-x, y)
        for i in range(1, steps+1):
            if self.boardArray[x+i,y-i] != None:
                if self.boardArray[x+i,y-i].color != color:
                    count += 1  # eating the enemy means one additional
                                # step in that direction
                break
            else:
                count += 1
        return count
        
    def space_to_move_right_up(self, posXY, color):
        x = posXY[0]
        y = posXY[1]
        count = 0
        steps = min(7-x, 7-y)
        for i in range(1, steps+1):
            if self.boardArray[x+i,y+i] != None:
                if self.boardArray[x+i,y+i].color != color:
                    count += 1  # eating the enemy means one additional
                                # step in that direction
                break
            else:
                count += 1
        return count
