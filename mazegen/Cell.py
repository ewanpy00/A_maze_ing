class Cell():
    def __init__(self, x, y):
        self.north = True
        self.south = True
        self.east = True
        self.west = True
        self.visited = False
        self.x = x
        self.y = y