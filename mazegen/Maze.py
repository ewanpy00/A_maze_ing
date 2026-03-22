import random
import time
from typing import List, Tuple, Optional, Set, Dict
from collections import deque

from .Constants import DELTA, P2, P4, MIN_H, MIN_W, OPPOSITE, Direction
from .Cell import Cell


class Maze:
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
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_
        self.rand = random.Random(seed)
        self.animation = animation
        self.perfect = perfect

        # Initialize all cells
        self.grid: List[List[Cell]] = [
            [Cell(x, y) for x in range(width)] for y in range(height)
        ]

        self.solution: List[str] = []
        self.pattern_cells: Set[Tuple[int, int]] = set()

    # -------------------------
    # Pattern embedding
    # -------------------------
    def apply_pattern(self) -> None:
        if self.width < MIN_W or self.height < MIN_H:
            return

        px = (self.width - 7) // 2
        py = (self.height - 5) // 2

        for row in range(5):
            for col in range(3):
                if P4[row][col]:
                    self._lock(px + col, py + row)
                if P2[row][col]:
                    self._lock(px + 4 + col, py + row)

    def _lock(self, x: int, y: int) -> None:
        self.grid[y][x].locked = True
        self.pattern_cells.add((x, y))

    # -------------------------
    # Maze generation (DFS)
    # -------------------------
    def generate(self) -> None:
        self.apply_pattern()

        start = self.grid[self.entry[1]][self.entry[0]]
        stack = [start]
        start.visited = True

        while stack:
            current = stack[-1]
            neighbors = self._neighbors(current)
            if neighbors:
                direction, nxt = self.rand.choice(neighbors)
                current.remove_wall(nxt, direction)
                nxt.visited = True
                stack.append(nxt)
                if self.animation:
                    from .Renderer import render_maze
                    render_maze(
                        self, show_path=False, current_cell=(nxt.x, nxt.y))
                    time.sleep(0.05)
            else:
                stack.pop()

        # If perfect=False, randomly remove walls to create loops
        if not self.perfect:
            self._create_loops()

        self._solve()

    def _neighbors(self, cell: Cell) -> List:
        result = []
        for d, (dx, dy) in DELTA.items():
            nx, ny = cell.x + dx, cell.y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                n = self.grid[ny][nx]
                if not n.visited and not n.locked:
                    result.append((d, n))
        return result

    # -------------------------
    # Create loops for imperfect mazes
    # -------------------------
    def _create_loops(self, fraction: float = 0.1) -> None:
        # Remove some walls randomly to introduce cycles, avoiding 3x3 open.
        num_walls = int(self.width * self.height * fraction)
        attempts = 0
        removed = 0
        while removed < num_walls and attempts < num_walls * 5:
            x = self.rand.randint(0, self.width - 1)
            y = self.rand.randint(0, self.height - 1)
            if self._remove_random_wall_safe(x, y):
                removed += 1
            attempts += 1

    def _remove_random_wall_safe(self, x: int, y: int) -> bool:
        """Try to remove a wall safely. Undo if 3x3 block forms."""
        cell = self.grid[y][x]
        dirs = list(DELTA.keys())
        self.rand.shuffle(dirs)

        for d in dirs:
            dx, dy = DELTA[d]
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = self.grid[ny][nx]
                if (cell.walls & d) and not neighbor.locked:
                    old_walls_cell = cell.walls
                    old_walls_neighbor = neighbor.walls
                    cell.walls &= ~d
                    neighbor.walls &= ~OPPOSITE[d]

                    if self._has_3x3_open_area():
                        # Undo removal
                        cell.walls = old_walls_cell
                        neighbor.walls = old_walls_neighbor
                    else:
                        return True
        return False

    def _has_3x3_open_area(self) -> bool:
        """Return True if any 3x3 block has all internal walls removed."""
        for by in range(self.height - 2):
            for bx in range(self.width - 2):
                if self._is_block_open(bx, by, 3, 3):
                    return True
        return False

    def _is_block_open(self, bx: int, by: int, bw: int, bh: int) -> bool:
        """Return True if all internal walls in a block are removed."""
        for cy in range(by, by + bh):
            for cx in range(bx, bx + bw):
                c = self.grid[cy][cx]
                if cx < bx + bw - 1 and (c.walls & Direction.EAST):
                    return False
                if cy < by + bh - 1 and (c.walls & Direction.SOUTH):
                    return False
        return True

    # -------------------------
    # Solve maze (for solution path)
    # -------------------------
    def _solve(self) -> None:
        queue = deque([self.entry])
        parent: Dict[Tuple[int, int], Optional[Tuple[int, int, Direction]]] = {
            self.entry: None
        }

        while queue:
            x, y = queue.popleft()
            if (x, y) == self.exit:
                break
            cell = self.grid[y][x]
            for d, (dx, dy) in DELTA.items():
                if not (cell.walls & d):
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in parent:
                        parent[(nx, ny)] = (x, y, d)
                        queue.append((nx, ny))

        path = []
        cur = self.exit
        while parent[cur] is not None:
            px, py, d = parent[cur]  # type: ignore[misc]
            path.append(d.name[0])
            cur = (px, py)
        path.reverse()
        self.solution = path
