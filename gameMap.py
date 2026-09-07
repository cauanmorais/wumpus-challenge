import random
from collections import deque
class GameMap: 
    def __init__(self):
        self.size = 4
        self.stench = False
        self.breeze = False
        
        # Entity trackers
        self.gold_location = None
        self.wumpus_location = None
        self.pit_locations = []
        
        self.grid = []
        self.available_positions = []

    def set_value(self, position: tuple, value: str):
        x, y = position
        if 1 <= x <= self.size and 1 <= y <= self.size:
            self.grid[y][x] = value
        else:
            raise IndexError("Coordinates out of bounds")

    def get_value(self, position: tuple) -> str:
        x, y = position
        if 0 <= x <= self.size + 1 and 0 <= y <= self.size + 1:
            return self.grid[y][x]
        else:
            raise IndexError("Coordinates out of bounds")

    def create_solvable_grid(self):
        """Generates random grids until a solvable one is found."""
        attempts = 0
        while True:
            attempts += 1
            self._generate_random_grid()
            
            if self.is_map_solvable():
                break

    def _generate_random_grid(self):
        """Builds the 2D array and places entities randomly."""
        # 1. Reset available positions for this attempt
        self.available_positions = [ 
            (x, y) for x in range(1, self.size + 1) for y in range(1, self.size + 1)
        ]
        self.available_positions.remove((1, 1))  # Reserve spawn point
        self.pit_locations.clear()

        # 2. Build empty grid with 'X' borders
        self.grid = []
        for y in range(self.size + 2):
            row = []
            for x in range(self.size + 2):
                if y == 0 or y == self.size + 1 or x == 0 or x == self.size + 1:
                    row.append('X')
                else:
                    row.append('.')
            self.grid.append(row)

        # 3. Spawn Robot
        self.set_value((1, 1), 'R')
        
        # 4. Spawn Hazards and Gold, saving their locations
        for _ in range(2):
            pit_pos = self._pop_random_position()
            self.set_value(pit_pos, 'P')
            self.pit_locations.append(pit_pos)

        self.gold_location = self._pop_random_position()
        self.set_value(self.gold_location, 'G')

        self.wumpus_location = self._pop_random_position()
        self.set_value(self.wumpus_location, 'W')

    def is_map_solvable(self) -> bool:
        """Uses Breadth-First Search (BFS) to guarantee a path to Gold exists."""
        start_x, start_y = 1, 1
        visited = set()
        visited.add((start_x, start_y))
        
        # Queue stores coordinates we need to check
        queue = deque([(start_x, start_y)])
        
        # Movement modifiers (Up, Right, Down, Left)
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        
        while queue:
            current_x, current_y = queue.popleft()
            
            # Did we find the gold?
            if self.get_value((current_x, current_y)) == 'G':
                return True
                
            # Check all 4 adjacent directions
            for dx, dy in directions:
                new_x, new_y = current_x + dx, current_y + dy
                
                if (new_x, new_y) not in visited:
                    target_cell = self.get_value((new_x, new_y))
                    
                    # Only add safe cells to our walk path
                    if target_cell in ('.', 'G'):
                        visited.add((new_x, new_y))
                        queue.append((new_x, new_y))
                        
        # If queue empties and we never found 'G', it's impossible
        return False

    def get_status_based_in_adjacent_cell(self, position: tuple):
        """Checks the 4 adjacent cells and updates stench and breeze."""
        x, y = position
        is_stench = False
        is_breeze = False
        
        # Look Up, Right, Down, Left
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            
            # Ensure we don't look outside the physical array
            if 0 <= new_x <= self.size + 1 and 0 <= new_y <= self.size + 1:
                target_cell = self.get_value((new_x, new_y))
                if target_cell == 'W':
                    is_stench = True
                elif target_cell == 'P':
                    is_breeze = True
                    
        self.stench = is_stench
        self.breeze = is_breeze

    def _pop_random_position(self) -> tuple:
        """Helper to fetch and remove a random coordinate."""
        if not self.available_positions:
            raise ValueError("No available positions left to generate.")
        
        position = random.choice(self.available_positions)
        self.available_positions.remove(position)
        return position

    def display(self):
        self.create_solvable_grid()
        for row in self.grid:
            print(' '.join(str(cell) for cell in row))