import os
import sys
from mazegen.Renderer import interactive_loop
from mazegen.Generator import MazeGenerator
from utils.parse_arges import parse_args, validate_config

os.system("cls" if os.name == "nt" else "clear")


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <config_file>", file=sys.stderr)
        sys.exit(1)

    raw_config = parse_args(sys.argv[1])
    params = validate_config(raw_config)
    gen = MazeGenerator(**params)
    gen.generate()

    if not gen.pattern_placed:
        print(
            "Warning: maze is too small to embed the '42' pattern.",
            file=sys.stderr)

    if not gen.solution:
        print("Warning: no path found between entry and exit.",
              file=sys.stderr)

    interactive_loop(params, gen)


if __name__ == "__main__":
    main()
