from dependencies import chess
from dependencies.chess import \
        WHITE, BLACK, KING, QUEEN, ROOK, BISHOP, KNIGHT, PAWN, \
        A1, A2, A3, A4, A5, A6, A7, A8, B1, B2, B3, B4, B5, B6, B7, B8, \
        C1, C2, C3, C4, C5, C6, C7, C8, D1, D2, D3, D4, D5, D6, D7, D8, \
        E1, E2, E3, E4, E5, E6, E7, E8, F1, F2, F3, F4, F5, F6, F7, F8, \
        G1, G2, G3, G4, G5, G6, G7, G8, H1, H2, H3, H4, H5, H6, H7, H8
import ChessANNBoardInterface as cabi


def is_empty(board, square):
    return board.piece_type_at(square) is None


def get_material_configuration(board):
    wq = len(board.pieces(QUEEN,  WHITE)) / 1.0
    wr = len(board.pieces(ROOK,   WHITE)) / 2.0
    wb = len(board.pieces(BISHOP, WHITE)) / 2.0
    wn = len(board.pieces(KNIGHT, WHITE)) / 2.0
    wp = len(board.pieces(PAWN,   WHITE)) / 8.0

    bq = len(board.pieces(QUEEN,  BLACK)) / 1.0
    br = len(board.pieces(ROOK,   BLACK)) / 2.0
    bb = len(board.pieces(BISHOP, BLACK)) / 2.0
    bn = len(board.pieces(KNIGHT, BLACK)) / 2.0
    bp = len(board.pieces(PAWN,   BLACK)) / 8.0
    return [wq, wr, wb, wn, wp, bq, br, bb, bn, bp]


def get_castling_rights(board):
    k_white = float(board.has_kingside_castling_rights(WHITE) \
                    and is_empty(board, F1) \
                    and is_empty(board, G1))

    q_white = float(board.has_queenside_castling_rights(WHITE) \
                    and is_empty(board, B1) \
                    and is_empty(board, C1) \
                    and is_empty(board, D1))

    k_black = float(board.has_kingside_castling_rights(BLACK) \
                    and is_empty(board, F8) \
                    and is_empty(board, G8))

    q_black = float(board.has_queenside_castling_rights(BLACK) \
                    and is_empty(board, B8) \
                    and is_empty(board, C8) \
                    and is_empty(board, D8))

    return [k_white, q_white, k_black, q_black]


def extract_global_features(board):
    assert(board.is_valid())
    vec = []

    # White's turn
    vec.append(float(board.turn))

    # Material configuration
    vec.extend(get_material_configuration(board))

    # Castling rights
    vec.extend(get_castling_rights(board))

    return vec


def create_feature_vector_piece_slot(listOfPieces, slotSize, slotsNum):
    vec = [0.0]*slotsNum*slotSize
    for ele in listOfPieces:
        vec[ele.index*slotSize + 0] = 1.0
        vec[ele.index*slotSize + 1] = ele.pos[0] / 7.0
        vec[ele.index*slotSize + 2] = ele.pos[1] / 7.0

    return vec

# sliding in this directions:
#       0
#     0 0 0
#       0
def create_feature_vector_sliding_plus_slot(interface, listOfPieces, slotsNum):
    slotSize = 4
    vec = [0]*slotsNum*slotSize
    for ele in listOfPieces:
        posXY = (ele.pos[0], ele.pos[1])
        c = ele.color
        # how much can I go left
        vec[ele.index*slotSize + 0] = interface.space_to_move_left(posXY, c) / 7.0
        # how much can I go right
        vec[ele.index*slotSize + 1] = interface.space_to_move_right(posXY, c) / 7.0
        # how much can I go up
        vec[ele.index*slotSize + 2] = interface.space_to_move_up(posXY, c) / 7.0
        # how much can I go down
        vec[ele.index*slotSize + 3] = interface.space_to_move_down(posXY, c) / 7.0

    return vec

# sliding in this directions:
#     0   0
#       0
#     0   0
def create_feature_vector_sliding_cross_slot(interface, listOfPieces, slotsNum):
    slotSize = 4
    vec = [0]*slotsNum*slotSize
    for ele in listOfPieces:
        posXY = (ele.pos[0], ele.pos[1])
        c = ele.color
        # how much can I go left down
        vec[ele.index*slotSize + 0] = interface.space_to_move_left_down(posXY, c) / 7.0
        # how much can I go right
        vec[ele.index*slotSize + 1] = interface.space_to_move_left_up(posXY, c) / 7.0
        # how much can I go up
        vec[ele.index*slotSize + 2] = interface.space_to_move_right_down(posXY, c) / 7.0
        # how much can I go down
        vec[ele.index*slotSize + 3] = interface.space_to_move_right_up(posXY, c) / 7.0

    return vec    

def extract_piece_centric_features(interface):
    assert(interface.get_board().is_valid())
    slotSize = 3
    vec = []

    # whites
    list = interface.get_piece(KING, WHITE)
    v = create_feature_vector_piece_slot(list, slotSize, 1)
    vec.extend(v)
    
    list = interface.get_piece(QUEEN, WHITE)
    v = create_feature_vector_piece_slot(list, slotSize, 1)
    vec.extend(v)

    list = interface.get_piece(ROOK, WHITE)
    v = create_feature_vector_piece_slot(list, slotSize, 2)
    vec.extend(v)
    
    list = interface.get_piece(BISHOP, WHITE)
    v = create_feature_vector_piece_slot(list, slotSize, 2)
    vec.extend(v)
    
    list = interface.get_piece(KNIGHT, WHITE)
    v = create_feature_vector_piece_slot(list, slotSize, 2)
    vec.extend(v)
    
    list = interface.get_piece(PAWN, WHITE)
    v = create_feature_vector_piece_slot(list, slotSize, 8)
    vec.extend(v)
    
    # blacks
    list = interface.get_piece(KING, BLACK)
    v = create_feature_vector_piece_slot(list, slotSize, 1)
    vec.extend(v)
    
    list = interface.get_piece(QUEEN, BLACK)
    v = create_feature_vector_piece_slot(list, slotSize, 1)
    vec.extend(v)

    list = interface.get_piece(ROOK, BLACK)
    v = create_feature_vector_piece_slot(list, slotSize, 2)
    vec.extend(v)
    
    list = interface.get_piece(BISHOP, BLACK)
    v = create_feature_vector_piece_slot(list, slotSize, 2)
    vec.extend(v)
    
    list = interface.get_piece(KNIGHT, BLACK)
    v = create_feature_vector_piece_slot(list, slotSize, 2)
    vec.extend(v)
    
    list = interface.get_piece(PAWN, BLACK)
    v = create_feature_vector_piece_slot(list, slotSize, 8)
    vec.extend(v)
    
    # sliding pieces mobility
    # whites
    list = interface.get_piece(QUEEN, WHITE)
    v = create_feature_vector_sliding_cross_slot(interface, list, 1)
    vec.extend(v)
    v = create_feature_vector_sliding_plus_slot(interface, list, 1)
    vec.extend(v)
    
    list = interface.get_piece(ROOK, WHITE)
    v = create_feature_vector_sliding_plus_slot(interface, list, 2)
    vec.extend(v)
    
    list = interface.get_piece(BISHOP, WHITE)
    v = create_feature_vector_sliding_cross_slot(interface, list, 2)
    vec.extend(v)
    
    # blacks
    list = interface.get_piece(QUEEN, BLACK)
    v = create_feature_vector_sliding_cross_slot(interface, list, 1)
    vec.extend(v)
    v = create_feature_vector_sliding_plus_slot(interface, list, 1)
    vec.extend(v)
    
    list = interface.get_piece(ROOK, BLACK)
    v = create_feature_vector_sliding_plus_slot(interface, list, 2)
    vec.extend(v)
    
    list = interface.get_piece(BISHOP, BLACK)
    v = create_feature_vector_sliding_cross_slot(interface, list, 2)
    vec.extend(v)
    
    #print(vec)
    return vec


def extract_attack_def_maps(board):
    assert board.is_valid(), "Invalid board!"

    value_dict = {'P': 1, 'p': 1,  # pawn
                  'N': 3, 'n': 3,  # knight
                  'B': 3, 'b': 3,  # bishop
                  'R': 5, 'r': 5,  # rook
                  'Q': 9, 'q': 9,  # queen
                  'K':15, 'k':15}  # king

    white_attackers_list = []
    black_attackers_list = []
    maxVal = max((value_dict[key] for key in value_dict), default=0)

    for sq in chess.SQUARES:
        # get attacker positions for each square
        w_attacker_pos = board.attackers(WHITE, sq)
        b_attacker_pos = board.attackers(BLACK, sq)

        # find out which pieces they are
        w_attackers = [board.piece_at(pos).symbol() for pos in w_attacker_pos]
        b_attackers = [board.piece_at(pos).symbol() for pos in b_attacker_pos]

        # find the lowest-valued attacking piece, if any
        w_val = min((value_dict[piece] for piece in w_attackers), default=0)
        b_val = min((value_dict[piece] for piece in b_attackers), default=0)

        white_attackers_list += [ w_val / maxVal ]
        black_attackers_list += [ b_val / maxVal ]

    # determine who is doing the attacking
    attack_list = white_attackers_list if board.turn else black_attackers_list
    defense_list = black_attackers_list if board.turn else white_attackers_list

    #print(attack_list+defense_list)
    vec = []
    vec.extend(attack_list)
    vec.extend(defense_list)
    #print(vec)
    return vec
    
def extract_features(board_interface):
    vec = []
    v = extract_global_features(board_interface.get_board())
    vec.extend(v)
    v = extract_piece_centric_features(board_interface)
    vec.extend(v)
    v = extract_attack_def_maps(board_interface.get_board())
    vec.extend(v)
    
    return vec;


if __name__=="__main__":

    interface = cabi.ChessANNBoardInterface()
    i = 0
    while (True):
        print(interface.get_board())
        
        vec = []
        v = extract_global_features(interface.get_board())
        vec.extend(v)
        v = extract_piece_centric_features(interface)
        vec.extend(v)
        v = extract_attack_def_maps(interface.get_board())
        vec.extend(v)
        
        if (i == 30):
            ijo = interface.copy()
            print('copy')
            print(ijo.get_board())
        
        #print(vec)
        
        interface.make_move()
        #input()
