import chess
import sys






def main():


	fenovi = []
	f = open(sys.argv[2],"w")
	i=0
	with open(sys.argv[1]) as infile:
		for line in infile:
			moves = get_moves(line)
			
			
			if not len(moves):	
				continue
			
			if moves[0] == '1.': 	#Nova igra
				board = chess.Board()
			(fenovi,illegal) = get_fens(moves,board)
			

			for fen in fenovi:
				
				f.write(fen)
				f.write("\n") 
				


	

	return

def get_fens(moves, board):

	
	illegal = []
	fenovi = []
	for move in moves:
			
		try:
			board.parse_san(move)
			board.push_san(move)
			fen = board.fen()
			if fen not in fenovi:
				fenovi.append(board.fen())
		except ValueError:
			illegal.append(move)
				

	return (fenovi,illegal)




def get_moves(line):
	
	
	moves = []
	
	
	if line[0]!= '' and line[0]!="[":
		moves = line.split()
	


	return moves




if __name__ == '__main__': main()