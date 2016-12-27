
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
        
    def clear(self): 
        self.buffer = ''
        
    def format_data(self):
        # discard the comments
        self.buffer = re.sub(r'{[^}]*}', '', self.buffer)
        
        # discard the numbers
        self.buffer = re.sub(r'[0123456789]*\.', '', self.buffer)
        
        # to list
        self.buffer = str.split(self.buffer)
        self.buffer = self.buffer[:-1]

class GameLoader:
    def __init__(self, gamesFile):
        self.f = open(gamesFile)
        return
        
    def get_game(self, skip):
    
        games_loaded = -1
        game = Game()
        while(True):
            
            if (len(peek_line(self.f)) > 5 and \
                peek_line(self.f)[0:6] == '[Event'):
                games_loaded = games_loaded + 1
                if (games_loaded > skip):
                    break
                else:
                    game.clear()
            
            if (peek_line(self.f) == ''):
                    break
            
            line = self.f.readline()
            if (line[0] != '['):
                game.append(line)
        
        return game
        
    def get_game_num(self):
        
        pos = self.f.tell()
        self.f.seek(0)
        games_loaded = 0
        for line in self.f:
            
            if (len(line) > 5 and line[0:6] == '[Event'):
                games_loaded = games_loaded + 1
        
        self.f.seek(pos)
        return games_loaded
        
# main
if __name__=="__main__":
    gameLoader = GameLoader('..\Dataset\Games.txt')
    gameLoader.get_game_num()
    
    game = gameLoader.get_game(0)
    game.format_data()
    print(game.buffer)
    
    game = gameLoader.get_game(0)
    game.format_data()
    print(game.buffer)
    
    #print(gameLoader.get_game_num())
