from constants import DIRECTIONS

class Robot:
    def __init__(self, x = 1, y = 4):
        self.initial_position = (x, y)
        self.x = x
        self.y = y
        self.record = list()
        
        # State tracking
        self.alive = True
        self.has_shot = False
        self.found_gold = False  # Fixed: This should start False!
        self.bumped = False
        

    def position(self) -> tuple:
        return (self.x, self.y)

    def set_position(self, x: int, y: int):
        """Allows you to easily teleport or force-update the robot."""
        self.x = x
        self.y = y

    def move(self, direction: int):
        # 1. Look up the math in our master dictionary
        dx, dy = DIRECTIONS[direction]
        
        # 3. Apply the movement
        self.x += dx
        self.y += dy

    def shoot_arrow(self, direction: int) -> tuple:
        self.has_shot = True
        
        # Look up the trajectory from our master dictionary
        dx, dy = DIRECTIONS[direction]
        
        # The arrow starts exactly where the robot is
        tx = self.x
        ty = self.y
        
        # We can calculate the cell the arrow hits right here
        target_x = tx + dx
        target_y = ty + dy
        
        return (target_x, target_y)

    def _append_old_position(self, action: int):
        """Saves the current position to the history list."""
        self.record.append([self.x,self.y,action])

    def get_the_gold(self):
        self.found_gold = True
        
    def bumped_in_wall(self):
        self.bumped = True
        
    def reset(self):
        """Fully resets the robot to a brand new state."""
        self.x, self.y = self.initial_position
        self.record.clear() # Empty the history
        
        self.alive = True
        self.bumped = False
        self.has_shot = False 
        self.found_gold = False 
    