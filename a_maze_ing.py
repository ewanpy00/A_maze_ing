import random
import utils
import mazegen


def save_to_file(maze, filename):
    try:
        with open(filename, 'w') as f:
            for y in range(maze.height):
                row_hex = ""
                for x in range(maze.width):
                    cell = maze.maze[y][x]
                    val = 0
                    if cell.north:
                        val += 1
                    if cell.east:
                        val += 2
                    if cell.south:
                        val += 4
                    if cell.west:
                        val += 8
                    
                    row_hex += format(val, 'x')
                f.write(row_hex + '\n')
            f.write(f"\n{maze.entry_x},{maze.entry_y}\n")
            f.write(f"{maze.exit_x},{maze.exit_y}\n")
            f.write(mazegen.get_solution_path(maze))
        print(f"Maze successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")


def a_maze_ing():
    config = utils.parse_args("config.txt")
    maze = mazegen.Maze(config["width"], 
                        config["height"], 
                        config["entry"], 
                        config["exit"],
                        1)   # pass the seed value here
    show_path = False
    while True:
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/hide the path from entry to exit")
        print("3. Quit")
        number = int(input("CHoice (1-4): "))
        match number:
            case 1:
                maze.seed = random.randint(0, 2**32 - 1)
                print(f"Generating maze with seed: {maze.seed}")
                maze.generate_maze(config["output_file"], config["perfect"],)
                maze.print_maze()
                continue
            case 2:
                if show_path == False:
                    mazegen.solve_maze(maze)
                    show_path = True
                    continue
                else:
                    maze.print_maze()
                    show_path = False
                    continue
            case 3:
                break

    save_to_file(maze, config["output_file"])


if __name__ == "__main__":
    a_maze_ing()
