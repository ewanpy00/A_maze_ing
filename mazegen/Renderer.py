import os
import sys
from typing import Dict, List, Tuple, Set, Optional

from utils.parse_arges import _die

from .Constants import Direction
from .Generator import MazeGenerator
from .Maze import Maze

_RESET = "\033[0m"
_BOLD = "\033[1m"

# Colour palettes: (wall_colour, reset)
_PALETTES: List[Tuple[str, str]] = [
    ("\033[97m", _RESET),  # bright white
    ("\033[33m", _RESET),  # yellow / gold
    ("\033[36m", _RESET),  # cyan
    ("\033[32m", _RESET),  # green
    ("\033[35m", _RESET),  # magenta
    ("\033[34m", _RESET),  # blue
]
_PATH_CLR = "\033[96m"  # bright cyan – solution path
_ENTRY_CLR = "\033[95m"  # bright magenta – entry cell
_EXIT_CLR = "\033[91m"  # bright red – exit cell
_PAT_CLR = "\033[90m"  # dark grey – "42" pattern cells
_DFS_CLR = "\033[92m"  # green – DFS current cell


def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def render_maze(
    gen: Maze,
    show_path: bool = False,
    palette: int = 0,
    current_cell: Optional[Tuple[int, int]] = None,
) -> None:
    wc, rs = _PALETTES[palette % len(_PALETTES)]
    w, h = gen.width, gen.height
    path_cells = _build_path_cells(gen) if show_path else set()

    lines: List[str] = []

    for y in range(h):
        # Top border
        top = ""
        for x in range(w):
            top += wc + "+" + rs
            top += (
                (
                    wc + "---" + rs
                    ) if (gen.grid[y][x].walls & Direction.NORTH) else "   "
            )
        top += wc + "+" + rs
        lines.append(top)

        # Row
        row = ""
        for x in range(w):
            row += (
                wc + "|" + rs
                ) if (gen.grid[y][x].walls & Direction.WEST) else " "

            # Decide cell symbol
            symbol = "   "
            if (x, y) == gen.entry:
                symbol = " " + _ENTRY_CLR + _BOLD + "E" + rs + " "
            elif (x, y) == gen.exit:
                symbol = " " + _EXIT_CLR + _BOLD + "X" + rs + " "
            elif current_cell and (x, y) == current_cell:
                symbol = " " + _DFS_CLR + _BOLD + "*" + rs + " "
            elif (x, y) in gen.pattern_cells:
                symbol = _PAT_CLR + "▓▓▓" + rs
            elif show_path and (x, y) in path_cells:
                symbol = _PATH_CLR + " · " + rs

            row += symbol

        row += (
            wc + "|" + rs
            ) if (gen.grid[y][w - 1].walls & Direction.EAST) else " "
        lines.append(row)

    # Bottom border
    bot = ""
    for x in range(w):
        bot += wc + "+" + rs
        bot += (
            (
                wc + "---" + rs
                ) if (gen.grid[h - 1][x].walls & Direction.SOUTH) else "   "
        )
    bot += wc + "+" + rs
    lines.append(bot)

    _clear()
    for line in lines:
        print(line)


def make_generator(params: Dict) -> MazeGenerator:
    gen = MazeGenerator(
        width=params["width"],
        height=params["height"],
        entry=params["entry"],
        exit_=params["exit_"],
        output_file=params["output_file"],
        perfect=params["perfect"],
        seed=params["seed"],
        animation=params["animation"],
    )
    gen.generate()
    return gen


def write_output(gen: MazeGenerator, path: str) -> None:

    try:
        with open(path, "w") as fh:
            for y in range(gen.height):
                fh.write(gen.get_hex_row(y) + "\n")
            fh.write("\n")
            ex, ey = gen.entry
            xx, xy = gen.exit
            fh.write(f"{ex},{ey}\n")
            fh.write(f"{xx},{xy}\n")
            fh.write("".join(gen.solution) + "\n")
    except OSError as exc:
        _die(f"Cannot write output file {path!r}: {exc}")


def _build_path_cells(gen: Maze) -> Set[Tuple[int, int]]:
    cells: Set[Tuple[int, int]] = set()
    if not gen.solution:
        return cells
    dx_map = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
    x, y = gen.entry
    cells.add((x, y))
    for letter in gen.solution:
        dx, dy = dx_map[letter]
        x, y = x + dx, y + dy
        cells.add((x, y))
    return cells


# -------------------------
# Interactive loop
# -------------------------
def interactive_loop(params: Dict, gen: MazeGenerator) -> None:
    show_path = False
    palette = 0

    if not params.get("animation", False):
        render_maze(gen, show_path, palette)

    while True:
        print()
        print(_BOLD + "=== A-Maze-ing ===" + _RESET)
        print("  1. Re-generate a new maze")
        print("  2. Show/Hide path from entry to exit")
        print("  3. Rotate maze wall colours")
        print("  4. Quit")
        print()

        try:
            choice = input("Choice (1 - 4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice == "1":
            params = {**params}
            gen = make_generator(params)

            if not gen.pattern_placed:
                print(
                    "Warning: maze is too small to embed the '42' pattern.",
                    file=sys.stderr,
                )
            show_path = False
            write_output(gen, params["output_file"])
            render_maze(gen, show_path, palette)
        elif choice == "2":
            show_path = not show_path
            render_maze(gen, show_path, palette)
        elif choice == "3":
            palette = (palette + 1) % len(_PALETTES)
            render_maze(gen, show_path, palette)
        elif choice == "4":
            break
        else:
            print("Please enter a number between 1 and 4.")
