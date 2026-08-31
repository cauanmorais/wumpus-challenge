class Robot:
    x = 0
    y = 0
    positions = []
    has_shot = False

    def __init__(self, x = 0, y = 0, name = "Robot"):
        self.name = name
        self.x = x
        self.y = y

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


    def shoot(self, item, direction):
        self.has_shot = True

        if direction == "up":
            item.y -= 1
            print(f"Item moved up to position: {item.position()}")
        elif direction == "down":
            item.y += 1
            print(f"Item moved down to position: {item.position()}")
        elif direction == "left":
            item.x -= 1    
            print(f"Item moved left to position: {item.position()}")   
        elif direction == "right":
            item.x += 1
            print(f"Item moved right to position: {item.position()}")


    def get_the_gold(self):
        return "You got the gold! You win!"