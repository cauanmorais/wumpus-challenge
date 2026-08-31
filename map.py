class Map: 
    def __init__(self, size, entities, robot):
        self.entities = entities
        self.robot = robot
        self.size = size

    def set_value(self, x, y, value):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[y][x] = value
        else:
            raise IndexError("Coordinates out of bounds")

    def get_value(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[y][x]
        else:
            raise IndexError("Coordinates out of bounds")

    def create_grid(self):
        self.grid = [['.' for _ in range(self.size + 1)] for _ in range(self.size + 1)]
        self.set_value(self.robot.x, self.robot.y, 'R')


    def display(self):
        for row in self.grid:
            print(' '.join(str(cell) for cell in row))


    def update_grid(self):
        self.set_value(self.robot.old_x, self.robot.old_y, '.')
        self.set_value(self.robot.x, self.robot.y, 'R')   
