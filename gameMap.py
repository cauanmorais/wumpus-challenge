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
        self.robot_initial_position = (1,4)
        
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

    def create_random_solvable_grid(self):
        """Generates random grids until a solvable one is found."""
        while True:
            self._generate_random_grid()
            
            if self.is_map_solvable():
                break

    def create_solvable_grid(self):
        """Generates grids until a solvable one is found."""
        while True:
            self._generate_grid()
                
            if self.is_map_solvable():
                break
            else: 
                print("O mapa é impossível de resolver, tente novamente")

    def _generate_random_grid(self):
        """Builds the 2D array and places entities randomly."""
        # 1. Reset available positions for this attempt
        self.available_positions = [ 
            (x, y) for x in range(1, self.size + 1) for y in range(1, self.size + 1)
        ]
        self.available_positions.remove(self.robot_initial_position)  # Reserve spawn point
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
        self.set_value(self.robot_initial_position, 'R')
        
        # 4. Spawn Hazards and Gold, saving their locations
        for _ in range(2):
            pit_pos = self._pop_random_position()
            self.set_value(pit_pos, 'P')
            self.pit_locations.append(pit_pos)

        self.gold_location = self._pop_random_position()
        self.set_value(self.gold_location, 'G')

        self.wumpus_location = self._pop_random_position()
        self.set_value(self.wumpus_location, 'W')

    def _generate_grid(self):
            """Builds the 2D array and places entities."""
            # 1. Reset available positions for this attempt
            self.available_positions = [ 
                (x, y) for x in range(1, self.size + 1) for y in range(1, self.size + 1)
            ]
            self.available_positions.remove(self.robot_initial_position)  # Reserve spawn point
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
            self.set_value(self.robot_initial_position, 'R')
            
            # 4. Spawn Hazards and Gold, saving their locations
            for _ in range(2):
                pit_pos = self._get_tuple_data_from_user_input("Poço")
                self.set_value(pit_pos, 'P')
                self.pit_locations.append(pit_pos)
    
            self.wumpus_location = self._get_tuple_data_from_user_input("Monstro")
            self.set_value(self.wumpus_location, 'W')

            self.gold_location = self._get_tuple_data_from_user_input("Ouro")
            self.set_value(self.gold_location, 'G')

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

    def _get_tuple_data_from_user_input(self, elemento: str) -> tuple:
        while True:
            entrada = input(f"Digite as posições X,Y para o elemento {elemento} separados por vírgula: ")
            
            try:
                # 1. Divide a entrada e limpa os espaços
                partes = [parte.strip() for parte in entrada.split(',')]
                
                if len(partes) != 2:
                    print("Erro: Você deve digitar exatamente dois valores (X, Y). Tente novamente.")
                    continue
                
                x, y = int(partes[0]), int(partes[1])
                
                if not (1 <= x <= self.size and 1 <= y <= self.size):    
                    print(f"Erro: As coordenadas estão fora dos limites (deve ser entre 1 e {self.size}). Tente novamente.")
                    continue
                
                return (x, y)
                
            except ValueError:
                print("Erro: Formato inválido. Digite apenas números inteiros separados por vírgula.")

    def display(self):
        for row in self.grid:
            print(' '.join(str(cell) for cell in row))
        print()
