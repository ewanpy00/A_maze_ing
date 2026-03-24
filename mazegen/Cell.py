from .Constants import Direction, OPPOSITE


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        west = Direction.WEST
        self.walls = Direction.NORTH | Direction.EAST | Direction.SOUTH | west
        self.visited = False
        self.locked = False

    def remove_wall(self, other: "Cell", direction: Direction) -> None:
        self.walls &= ~direction
        other.walls &= ~OPPOSITE[direction]
