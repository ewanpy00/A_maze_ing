from Cell import Cell
import random

class Maze:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.maze = [[Cell(x, y) for x in range(width)] for y in range(height)]
        # Creating a double array of Cells


    # basic Maze generation function
    def generate_maze(self, start_x, start_y):
        stack = []
        current = self.maze[start_x][start_y]
        current.visited = True
        while True:
            neighbors = self.get_unvisited_neighbors(current)
            if neighbors:
                next_cell = random.choice(neighbors)
                self.remove_walls(current, next_cell)
                stack.append(current)
                current = next_cell
                current.visited = True
            elif stack:
                current = stack.pop()
            else:
                break

    # check for unvisited nieghbours based on the Height and Width and .visited field
    def get_unvisited_neighbors(self, cell):
        neighbors = []
        x, y = cell.x, cell.y

        if y > 0 and not self.maze[y - 1][x].visited:
            neighbors.append(self.maze[y - 1][x])
        if y < self.height - 1 and not self.maze[y + 1][x].visited:
            neighbors.append(self.maze[y + 1][x])
        if x > 0 and not self.maze[y][x - 1].visited:
            neighbors.append(self.maze[y][x - 1])
        if x < self.width - 1 and not self.maze[y][x + 1].visited: 
            neighbors.append(self.maze[y][x + 1])

        return neighbors

    def remove_walls(self, current, next_cell):
        dx = next_cell.x - current.x
        dy = next_cell.y - current.y
        # dy and dx to understand which wall we should remove
        if dx == 1:
            current.east = False
            next_cell.west = False
        elif dx == -1:
            current.west = False
            next_cell.east = False
        elif dy == 1:
            current.south = False
            next_cell.north = False
        elif dy == -1:
            current.north = False
            next_cell.south = False

    # displaying the maze
    # display only based on the east and south wall.
    def print_maze(self):
        print("█" * (self.width * 2 + 1))
        for y in range(self.height):
            print("█", end='')
            for x in range(self.width):
                cell = self.maze[y][x]
                print(" ", end='')
                if cell.east:
                    print("█", end='')
                else:
                    print(" ", end='')
            print()
            print("█", end='')
            for x in range(self.width):
                cell = self.maze[y][x]
                if cell.south:
                    print("██", end='')
                else:
                    print(" █", end='')
            print()


# just for testing
maze = Maze(20, 20)
maze.generate_maze(3, 2)
maze.print_maze()