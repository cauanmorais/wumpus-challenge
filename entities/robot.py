class Robot:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.old_x = 0
        self.old_y = 0
        self.positions = []
        self.has_shot = False
        self.bump = False
        self.alive = True

    def position(self):
        return (self.x, self.y)

    def move(self, direction):
        if direction == "up":
            self.append_old_position()
            self.y -= 1
        elif direction == "down":
            self.append_old_position()
            self.y += 1
        elif direction == "left":
            self.append_old_position()
            self.x -= 1
        elif direction == "right":
            self.append_old_position()
            self.x += 1
        else:
            raise ValueError("Invalid direction. Use 'up', 'down', 'left', or 'right'.")

    def append_old_position(self):
        self.old_x = self.x
        self.old_y = self.y
        old_position = (self.old_x, self.old_y)
        self.positions.append(old_position)


    def shoot(self, direction) -> tuple:
        self.has_shot = True

        if direction == "up":
            arrow_position = (self.x, self.y - 1)
        elif direction == "down":
            arrow_position = (self.x, self.y + 1)
        elif direction == "left":
            arrow_position = (self.x - 1, self.y)
        elif direction == "right":
            arrow_position = (self.x + 1, self.y)
        else:
            raise ValueError("Invalid direction. Use 'up', 'down', 'left', or 'right'.")
        return arrow_position                           

    def get_the_gold(self):
        return "You got the gold! You win!"