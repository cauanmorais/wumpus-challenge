import numpy
from entities.robot import Robot
from gameMap import GameMap
class GameLoop:
    def __init__(self):
        self.robot = Robot()
        self.game_map = GameMap()
        self.score = 0.0
        #Locations to save game state in case of death
        self.state = {
            'robot_position': (1,1),
            'gold_position': (),
            'wumpus_position': (),
            'pit_positions': [(),()],
            'wumpus_alive': True,
            'maze_exists': False,
            'score': 0.0   
        }
        self.mazeExists = False
        self.goldLocY = 0
        self.goldLocX = 0
        # self.resetAgent()

    def start(self):
        # Create a random maze and ensure it is solvable
        while True:
            self.makeRandomMaze()
            if self.mazeExists:
                break
        self.game_map.display()

    def update(self):
        self.game_map.display()
    
    def is_map_solvable(self):
        #RandomWalk to check is maze is solvable
        xm=[0,1,0,-1]
        ym=[-1,0,1,0]
        maxSteps = 10000
        temp_x=1
        temp_y=1
        for i in range(maxSteps):
                #Random action of up,down,left or right
                action = numpy.random.choice([0,1,2,3])
                #Is this new position within the bounds of the maze (index of list)?
                if not (0 <= temp_x + xm[action] < self.game_map.size and 0 <= temp_y + ym[action] < self.game_map.size):
                    continue

                if self.game_map.get_value((temp_x+xm[action], temp_y+ym[action]))=='X':
                    continue

                #Is this new position a PIT or WUMPUS?
                if self.game_map.get_value((temp_x+xm[action], temp_y+ym[action]))=='P':
                    continue

                if self.game_map.get_value((temp_x+xm[action], temp_y+ym[action]))=='W':
                    continue
                else:
                    #new position is '.' or 'G'
                    temp_x=temp_x+xm[action]
                    temp_y=temp_y+ym[action]
                    #If we found 'G' by only walking on '.', the maze is solvable
                    if self.game_map.get_value((temp_x, temp_y))=='G':
                        print(f"Maze solvable was found in {i + 1 } steps")
                        return True
        #Couldnt reach 'G' by following only '.'
        return False

    def makeRandomMaze(self):
        while not self.mazeExists:
            self.game_map.create_grid()
            self.mazeExists = self.is_map_solvable()

    def resetAgent(self):
       pass
        
    def moveAgent(self, action):
        #Action = move up,down,left or right
        robotPos = [(self.robot.x, self.robot.y)]
        self.score = self.score-1
        xm = [0,1,0,-1]
        ym = [-1,0,1,0]
        tx = self.robot.x+xm[action]
        ty = self.robot.y+ym[action]
        
        #If current position is Gold
        if self.game_map.get_value((tx, ty)) == 'G':
            self.glitter=True
            self.score=self.score+1000
            self.goldLocY=ty
            self.goldLocX=tx
            print("Agent found the gold!")
        
        if self.game_map.get_value((tx, ty)) != 'G':
            self.glitter=False
        #If current position is a wall, returns bump
        if self.game_map.get_value((tx, ty)) == 'X':
            self.bump=True
            print(self.game_map.get_value((tx, ty)))
            return "Alive: ",self.alive,"Bump: ",self.bump,"Stench: ",self.stench,"Glitter: ", self.glitter,"Breeze: ",self.breeze,"Score: ",self.score
        else:
            self.bump=False
        #If new position is not a wall, current position becomes '.'
        if self.game_map.get_value((tx, ty)) != 'X':
            self.game_map.set_value((self.xPos, self.yPos), '.')
            self.xPos=tx
            self.yPos=ty
        #If we walk on Pit or Wumpus, we die, lose points and reset the agent/game state    
        if self.game_map.get_value((self.xPos, self.yPos)) == 'P' or self.game_map.get_value((self.xPos, self.yPos)) == 'W':
            self.alive=False
            self.score=self.score-1000
            return self.resetAgent()  
        else:
            #New position becomes 'A'(Agent)
            self.game_map.set_value((self.xPos, self.yPos), 'A')
        #If adjacent nodes to new position is a Pit    
        if self.game_map.get_status == "B":
            self.breeze=True
        else:
            self.breeze=False
        #If adjacent nodes to new position is a Wumpus
        if self.game_map.get_status == "W":
            self.stench=True
        else:
            self.stench=False
        #Returns maze and sensors
        print(self.game_map)
        print("Current Position of A: ",self.robot.position())
        return "Alive: ",self.alive,"Bump: ",self.bump,"Stench: ",self.stench,"Glitter: ", self.glitter,"Breeze: ",self.breeze,"Score: ",self.score

