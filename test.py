from gameMap import GameMap
from gameLoop import GameLoop

game = GameLoop()

game.start()
print(" = " * 50)
game.update_ui((1,1), ".", (1,2), "R")
