import random

class GameMap: 
    def __init__(self):
        self.size = 4
        self.stench = False
        self.glitter = False
        self.breeze = False
        
        self.available_positions = [ 
            (x, y) for x in range(1, self.size + 1) for y in range(1, self.size + 1)
        ]

        # Remove the starting position (1, 1) from available positions to prevent placing hazards or gold there
        self.available_positions.remove((1, 1))  

    def set_value(self, position, value):
        x, y = position
        # Restrict writing strictly to the playable area (1 to self.size)
        if 1 <= x <= self.size and 1 <= y <= self.size:
            self.grid[y][x] = value
        else:
            raise IndexError("Coordinates out of bounds")

    def get_value(self, position):
        x, y = position
        # Allow reading from the entire grid (0 to self.size + 1) 
        if 0 <= x <= self.size + 1 and 0 <= y <= self.size + 1:
            return self.grid[y][x]
        else:
            raise IndexError("Coordinates out of bounds")

    def create_grid(self):
        self.grid = []
        # We need a grid size of (size + 2) to accommodate the walls on both sides.
        # For size 4, this creates a 6x6 list (indices 0 through 5).
        for y in range(self.size + 2):
            row = []
            for x in range(self.size + 2):
                # If we are on the first/last row or first/last column, place a wall
                if y == 0 or y == self.size + 1 or x == 0 or x == self.size + 1:
                    row.append('X')
                else:
                    row.append('.')
            self.grid.append(row)

        # Spawn robot at the new 1-indexed starting position
        self.set_value((1, 1), 'R')
        
        # Spawn hazards and gold at random positions
        self.set_value(self.generate_random_position(), 'P')
        self.set_value(self.generate_random_position(), 'P')
        self.set_value(self.generate_random_position(), 'G')
        self.set_value(self.generate_random_position(), 'W')

    def display(self):
        for row in self.grid:
            print(' '.join(str(cell) for cell in row))

    def update_robot_position(self, old_position, new_position):
        self.set_value(old_position, '.')
        self.set_value(new_position, 'R')

    def generate_random_position(self):
        if not self.available_positions:
            raise ValueError("No available positions left to generate.")
        position = random.choice(self.available_positions)
        self.available_positions.remove(position)
        return position

    # Return the status of the robot based on its current position and the adjacent cells
    def get_status(self, position):
        adjacent_cells = self.get_adjacent_cells(position)
        self.stench = any(self.get_value(cell) == 'W' for cell in adjacent_cells)
        self.breeze = any(self.get_value(cell) == 'P' for cell in adjacent_cells)

    def get_adjacent_cells(self, position):
        x, y = position
        adjacent_cells = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if 1 <= new_x <= self.size and 1 <= new_y <= self.size:
                adjacent_cells.append((new_x, new_y))
        return adjacent_cells