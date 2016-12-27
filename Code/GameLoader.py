
import re 

def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line

class Game:
    def __init__(self):
        self.buffer = ''
        return
        
    def append(self, string):
        self.buffer = self.buffer + string
        
    def format_data(self):
        # discard the comments
        self.buffer = re.sub(r'{[^}]*}', '', self.buffer)
        
        # discard the numbers
        self.buffer = re.sub(r'[0123456789]*\.', '', self.buffer)
        
        self.buffer = str.split(self.buffer)
        
        self.buffer = self.buffer[:-1]

class GameLoader:
    def __init__(self, gamesFile):
        self.f = open(gamesFile)
        return
        
    def get_game(self, skip):
        
        done = False
        games_loaded = -1
        game = Game()
        while(not done):
            
            if (len(peek_line(self.f)) > 5 and \
                peek_line(self.f)[0:6] == '[Event'):
                games_loaded = games_loaded + 1
        
            if (games_loaded > skip):
                done = True
        
            line = self.f.readline()
            if (line[0] != '['):
                game.append(line)
        
        return game
        
        
# main
gameLoader = GameLoader('..\Dataset\Games.txt')
game = gameLoader.get_game(0)
game.format_data()
print(game.buffer)