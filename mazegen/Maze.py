from mazegen.Cell import Cell
import random

class Maze:
    def __init__(self, height, width, ENTRY, EXIT, seed=None):
        self.height = height
        self.width = width
        self.entry_y, self.entry_x = ENTRY
        self.exit_y, self.exit_x = EXIT
        self.seed = seed
        self.maze = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self.solution_path = []


    def apply_42_pattern(self):
        pattern_4 = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (0, 2), (1, 2), (3, 2), (4, 2)]
        pattern_2 = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2)]
        
        offset_y = self.height // 2 - 2
        offset_x_4 = self.width // 2 - 4
        offset_x_2 = self.width // 2 + 1

        if self.width < 10 or self.height < 7:
            print("Error: Maze size too small to draw '42' pattern.")
            return

        for dy, dx in pattern_4:
            self._lock_cell(offset_y + dy, offset_x_4 + dx)
        for dy, dx in pattern_2:
            self._lock_cell(offset_y + dy, offset_x_2 + dx)

    def _lock_cell(self, y, x):
        if 0 <= y < self.height and 0 <= x < self.width:
            cell = self.maze[y][x]
            cell.visited = True
            

    def generate_maze(self, output_file, perfect):
        for row in self.maze:
            for cell in row:
                cell.visited = False
                cell.north = cell.east = cell.south = cell.west = True
        self.solution_path = []
        if self.seed is not None:
            random.seed(self.seed)    # reed about Mersenne Twister(algorithms used to generate a random number) - interesting topic
        self.apply_42_pattern()ы
        stack = []
        current = self.maze[self.entry_y][self.entry_x]
        current.visited = True
        while True:
            if (current.x, current.y) == (self.exit_x, self.exit_y) and not self.solution_path:        
                self.solution_path = [(c.x, c.y) for c in stack] + [(current.x, current.y)]
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
        

    def get_unvisited_neighbors(self, cell):
        neighbors = []
        x, y = cell.x, cell.y

        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.maze[ny][nx].visited:
                    neighbors.append(self.maze[ny][nx])
        return neighbors

    def remove_walls(self, current, next_cell):
        dx = next_cell.x - current.x
        dy = next_cell.y - current.y
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

    def print_maze(self):
        print("█" * (self.width * 3 + 1))
        for y in range(self.height):
            line1 = "█"
            line2 = "█"
            for x in range(self.width):
                cell = self.maze[y][x]
                if (x, y) == (self.entry_x, self.entry_y):
                    symbol = "🟢"
                elif (x, y) == (self.exit_x, self.exit_y):
                    symbol = "🔴"
                elif cell.north and cell.east and cell.south and cell.west:
                    symbol = "██" 
                else:
                    symbol = "  "
                
                line1 += symbol + ("█" if cell.east else " ")
                line2 += ("███" if cell.south else "  █")
            
            print(line1)
            print(line2)