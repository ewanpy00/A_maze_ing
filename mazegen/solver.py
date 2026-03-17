def get_solution_path(maze) -> str:
    path = ""
    for i in range(len(maze.solution_path) - 1):
        curr = maze.solution_path[i]
        next_node = maze.solution_path[i+1]
        
        dx = next_node[0] - curr[0]
        dy = next_node[1] - curr[1]
        
        if dy == -1:
            path += "N"
        elif dx == 1:
            path += "E"
        elif dy == 1:
            path += "S"
        elif dx == -1:
            path += "W"
    return path
    

def solve_maze(maze):
    print("█" * (maze.width * 3 + 1))

    for y in range(maze.height):
        line1 = "█"
        line2 = "█"

        for x in range(maze.width):
            cell = maze.maze[y][x]
            
            if (x, y) == (maze.entry_x, maze.entry_y):
                symbol = "🟢"
            elif (x, y) == (maze.exit_x, maze.exit_y):
                symbol = "🔴"
            elif (x, y) in maze.solution_path:
                symbol = "··" 
            elif cell.north and cell.east and cell.south and cell.west:
                symbol = "██" 
            else:
                symbol = "  "
            line1 += symbol + ("█" if cell.east else " ")
            line2 += ("███" if cell.south else "  █")
        
        print(line1)
        print(line2)

# modify the logic of solve maze. No it skips the cells on the Y axis