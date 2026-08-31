from map import Map
from entities.robot import Robot
from entities.item import Item

robo = Robot()

itens = [
    Item("arrow", 1, 1),
    Item("pit", 0, 0),
    Item("pit", 0, 1),
    Item("treasure", 2,2)
]


class Game: 
    points = 0
    steps = 0

    def __init__(self):
        self.map = Map(4,itens, robo)
        self.map.create_grid()
        self.map.display()

    def update(self):
        self.map.update_grid()
        self.map.display()
