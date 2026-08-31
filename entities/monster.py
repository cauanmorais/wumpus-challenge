class Monster:
    x = 0
    y = 0

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def position(self):
        return (self.x, self.y)

    def shout(self):
        return "ROAR!"