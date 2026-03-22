from typing import Tuple, Optional
from .Maze import Maze


class MazeGenerator(Maze):
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
        perfect: bool = True,
        seed: Optional[int] = None,
        animation: Optional[bool] = False,
    ) -> None:
        super().__init__(
            width=width,
            height=height,
            entry=entry,
            exit_=exit_,
            perfect=perfect,
            seed=seed,
            animation=animation)
        self.perfect = perfect
        self.pattern_placed = True

    def get_hex_row(self, y: int) -> str:
        return "".join(
            format(self.grid[y][x].walls, "X") for x in range(self.width))
