import numpy
from entities.robot import Robot
from gameMap import GameMap
from constants import DIRECTIONS

class GameLoop: 
    def __init__(self):
        self.robot = Robot()
        self.game_map = GameMap()
        self.score = 0.0  
        self.mazeExists = False
        
        grid_dimensions = self.game_map.size + 2
        self.Q = numpy.ones((grid_dimensions, grid_dimensions, 8))
        self.normalizeQ()
        
    def start(self):
        # Create a random maze and ensure it is solvable
        self.game_map.create_solvable_grid()
        self.game_map.display()
        

    def update_ui(self, oldPosition: tuple, oldValue: str, newPosition: tuple, newValue: str):
        self.game_map.set_value(oldPosition, oldValue)
        self.game_map.set_value(newPosition, newValue)
        

    def move_agent(self, action: int):
        self.score -= 1
        
        # 1. Look ahead using our global constants 
        dx, dy = DIRECTIONS[action]
        tx = self.robot.x + dx
        ty = self.robot.y + dy

        # 2. Fetch the target cell only ONCE
        target_cell = self.game_map.get_value((tx, ty))

        # 3. Handle Wall (Movement fails)
        if target_cell == 'X':
            self.robot.bumped_in_wall()
            self.score -= 10 
            print(f"Robot bumped into a wall, trying to move to {tx,ty}")

        # 4. Handle Death States (Pit or Wumpus)
        elif target_cell in ('P', 'W'):
            self.robot.alive = False
            self.score -= 1000
            print(f"Robot died, trying to move to {tx,ty}")
            
        # 5. Handle Safe Movement ('.' or 'G')
        else:
            print("Safe movement, the map should be updated")
            self.game_map.set_value(self.robot.position(), '.')
            
            self.robot.move(action)
            
            self.game_map.set_value(self.robot.position(), 'R')

            # Check for Gold
            if target_cell == 'G':
                self.robot.get_the_gold()
                self.score += 1000
                print("Agent found the gold!")

            # Ask the map to update the Stench and Breeze sensors based on the new location
            self.game_map.get_status_based_in_adjacent_cell(self.robot.position())

        # 6. Unified Return: Display everything once at the end instead of in every 'if' block
        self.game_map.display()
        return self.showCurrentState()
    
    def getAction(self, exploration=0.0):
        # Capture state BEFORE moving
        current_x = self.robot.x
        current_y = self.robot.y

        # Checks if random (0-1) is less than exploration
        if numpy.random.random() < exploration:
            action = numpy.random.choice([0,1,2,3,4,5,6,7])
        else:
            # Takes action based on our Q-tables probabilities
            action = numpy.random.choice([0,1,2,3,4,5,6,7], p=self.Q[current_x][current_y])        
            
        # FIX 5: Typo corrected from moveAgent to move_agent
        if action < 4:
            print("Robot will try to move")
            self.move_agent(action)
        elif action > 4 and not self.robot.has_shot:
            arrow_position = self.robot.shoot_arrow(action - 4)
            print(f"Robot shoot an arrow to {arrow_position}")

            if self.game_map.get_value(arrow_position) == "W":
                self.score += 1000
                print("The robot killed the monster, yeah!!")
        elif action > 4:
             print("Robot tried to shoot an arrow, but it had already shooted")
            
        # Safety fix for your record: Needs x, y, and action so updatePolicy doesn't crash!
        self.robot.record.append((current_x, current_y, action))
        return action
        
    def normalizeQ(self):
        # 1. Get the sum of actions for every cell at once
        sums = self.Q.sum(axis=-1, keepdims=True)
        
        # 2. Divide, safely handling the zeroes
        self.Q = numpy.divide(self.Q, sums, out=numpy.full_like(self.Q, 1.0 / self.Q.shape[-1]), where=(sums != 0))
                    
    def updatePolicy(self, learningRate=0.001):
        if self.robot.alive == True and self.score > 950:
            for x, y, a in self.robot.record:
                self.Q[x][y][a] += learningRate
        else:
            for x, y, a in self.robot.record:
                if self.Q[x][y][a] > 0.1:
                    self.Q[x][y][a] -= learningRate
                    
        self.normalizeQ()
        self.robot.record.clear()

    def showCurrentState(self):
        print(f"Current Position of R: {self.robot.position()}")
        
        print(f"Current Score: {self.score}")
        print(f"Robot Alive: {self.robot.alive}")
        print(f"Robot Bump: {self.robot.bumped}")
        
        print(f"Stench: {self.game_map.stench}")
        print(f"Breeze: {self.game_map.breeze}")

        print(" = " * 50)