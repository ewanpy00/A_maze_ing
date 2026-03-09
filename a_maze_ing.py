import utils
import mazegen

def a_maze_ing():
    config = utils.parse_args("config.txt")
    maze = mazegen.Maze(config["width"], 
                        config["height"], 
                        config["entry"], 
                        config["exit"])
    maze.generate_maze(config["output_file"], config["perfect"],)
    maze.print_maze()

a_maze_ing()