class Item:
    def __init__(self, name: str, x: int = 0, y: int = 0):
        self.name = name
        self.x = x
        self.y = y

    def position(self):
        return (self.x, self.y)
