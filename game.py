from player import Player
class Game:
    def __init__(self, m: int):
        self.mem = set()
        self.player_list = []
        self.current_players = 0
        self.max_players = m
    
    def add_word(self, word: str):
        self.mem.add(word)

    def add_player(self, name: str):
        if self.current_players > self.max_players - 1:
            print('placeholder for error handling')
            return 
        self.current_players += 1
        self.player_list.append(Player(name, self.current_players))
