import os
class GameStatus:
    def __init__(self):
        self.health = 100
    def reduce_health(self):
        self.health -= 10
        if self.health <= 0:
            game_over()

def main_game():
    game_status = GameStatus()
    #...
    # when player gets hurt
    game_status.reduce_health()
    # ...

def game_over():
    print ('"game over, sorry"')
    os._exit(1)