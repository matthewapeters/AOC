"""
AOC 2024 Day 6 part 2

* gurad is represented by characters:
    * '^' for moving up (0,-1)
    * '>' for moving right (1,0)
    * 'v' for moving down (0,1)
    * (Assumed) '<' for moving left (-1,0)

* obstacles as '#'
* places visisted are 'X'
* when next move is blocked by '#', guard rotates clockwise 90
  degrees.
* A move that would take the guard off the map is considered the end
  of analysis

# Count how many places we can put one obstacle to cause gaurd to go
  go into a loop.

  * any turning could put the guard into a loop.
  * pass a number to the move() that indicates after how many moves
    to place an obstacle directly in the path of the guard.  Then,
    detect if the gaurd goes into a loop.
  * we only have to try as many times as there are moves in the map
    before the guard leaves (as we can only place one obstacle)
  * We need a count of moves before exit (separate from distinct
    cells visisited)
  * Replace 'X' with vector.  If the next move puts the guard on a
    cell where the vector is 90-degrees to the right, and the cell
    just beyond the next cell is free, it is a candidate for looping.
  * keep a new set of positions for where to place obstacles.
  * Since guard can visist the same cell going different directions,
    replace visisted with a Dict[Tuple[int,int],set[Vector]]  - do
    not rely on cell decoration - look at set of vectors to determine
    right-turns into a loop.
  * Draw placed obstacles as 'O' - do not actually place obstacles!

"""

# pylint: disable=too-few-public-methods

from typing import Dict, List, Set, Tuple
from time import sleep


def clear_screen():
    # Move cursor to top-left and clear screen
    print("\033[H\033[2J", end="")


class Vector:
    """Vector"""

    def __init__(self, name: str, direction: Tuple[int, int]):
        self.name = name
        self.d_x = direction[0]
        self.d_y = direction[1]
        self._turn: "Vector" = None

    def __add__(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        add

        param: pos:Tuple[int, int]  Current x,y position of gaurd

        returns Tuple[int,int] new x,y position of gaurd

        """

        return (pos[0] + self.d_x, pos[1] + self.d_y)

    @property
    def turn(self) -> "Vector":
        """
        turn
        gets the new vector when guard turns
        """
        return self._turn

    @turn.setter
    def turn(self, v: "Vector"):
        self._turn = v


vectors: Dict[str, Vector] = {
    "^": Vector("^", (0, -1)),
    ">": Vector(">", (1, 0)),
    "v": Vector("V", (0, 1)),
    "<": Vector("<", (-1, 0)),
}

vectors["^"].turn = vectors[">"]
vectors[">"].turn = vectors["v"]
vectors["v"].turn = vectors["<"]
vectors["<"].turn = vectors["^"]


class Guard:
    """Guard"""

    def __init__(
        self,
        position: Tuple[int, int],
        start_vector: Vector,
        floor_map: List[List[str]],
    ):
        self.x: int = position[0]
        self.y: int = position[1]
        # set of positions (x,y)
        self.visited: Dict[str, Set[Tuple[int, int]]] = {}

        self.map: List[List[str]] = [list(row) for row in floor_map]
        self.direction = start_vector
        self.obstacles = set()

    @property
    def floor_map(self) -> List[List[str]]:
        """floor_map"""
        return self.map

    @floor_map.setter
    def floor_map(self, floor_map: List[List["str"]]):
        self.map = [list(row) for row in floor_map]

    @property
    def position(self):
        """position"""
        return (self.x, self.y)

    @position.setter
    def position(self, p: Tuple[int, int]):
        if self.position in self.visited:
            self.visited[self.position].add(self.direction)
        else:
            self.visited[self.position] = set([self.direction])

        self.map[self.position[1]][self.position[0]] = (
            self.direction.name if self.position not in self.obstacles else "O"
        )
        self.x = p[0]
        self.y = p[1]

    def show(self):
        """show"""
        for row in self.map:
            print("".join(row))

    def put_obstacle(self, pos):
        """put_obstacle"""
        self.map[pos[1]][pos[0]] = "O"

    def set_obstacle(self) -> Tuple[int, int]:
        """
        set_obstacle
        for testing if the placing an obstacle at the next move
        would cause the guard to go into a loop.
        """
        set_location = self.direction + self.position
        if (
            set_location[0] >= 0
            and set_location[0] <= len(self.floor_map[0]) - 1
            and set_location[1] >= 0
            and set_location[1] <= len(self.floor_map) - 1
        ):
            self.put_obstacle(set_location)
            return set_location
        return None

    def clear_obstacle(self, location: Tuple[int, int]):
        """
        clear_obstacle
        for clearing a tested obstacle
        """
        self.map[location[1]][location[0]] = "."

    def move(self):
        """
        move
        moves the guard around the floor/map.
        When the guard moves off the map, returns 'Gone'
        If next move would be into an obstacle, turns direction 90 degrees and returns ""
        If the next move has been visisted going the same direction, the guard has
        entered a loop and returns "loop"
        """
        next_move = self.direction + self.position
        if (
            next_move[0] < 0
            or next_move[1] < 0
            or next_move[1] > len(self.map) - 1
            or next_move[0] > len(self.map[0]) - 1
        ):
            if self.position in self.visited:
                self.visited[self.position].add(self.direction)
            else:
                self.visited[self.position] = set([self.direction])
            self.map[self.position[1]][self.position[0]] = self.direction.name
            return (
                f"Gone (exit at {next_move}) -- {len(self.visited)} distinct locations ",
                None,
            )
        try:
            if self.map[next_move[1]][next_move[0]] in ("#", "O"):
                if self.position in self.visited:
                    if self.direction.turn in self.visited[self.position]:
                        return "loop", None
                    self.visited[self.position].add(self.direction)
                else:
                    self.visited[self.position] = set([self.direction])

                self.direction = self.direction.turn
                self.visited[self.position].add(self.direction)
                return f"Turned at {self.position} to {self.direction.name}", None
        except Exception as ex:
            return "", f"ERR: invalid location {next_move}: {ex}"

        if next_move in self.visited and self.direction in self.visited[next_move]:
            return "loop", None

        self.position = next_move
        return "", None


SAMPLE = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

TEST = False
USE_TEST = False


def main():
    """main"""
    if not USE_TEST:
        with open("input.txt", "r", encoding="utf8") as fh:
            raw = fh.read()
    else:
        raw = SAMPLE
    data = [list(row) for row in raw.split("\n") if row != ""]
    # bounds = [[0, 0], [len(data), len(data[0])]]

    # find the starting position
    start = (-1, -1)
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if col == "^":
                start = (j, i)
                break
    if start == (-1, -1):
        print("start position not found")
        return
    # print(f"guard starts at {start}")
    guard = Guard(start, vectors["^"], data)
    o = ""
    i = 0
    moves = ""
    while o[:4] not in ("loop", "Gone"):
        i += 1
        o, err = guard.move()
        if err is None:
            if TEST:
                moves += f"\n{o}" if o != "" else ""
                guard.show()
                print(moves)
                sleep(0.05)
                clear_screen()
    if TEST:
        sleep(5)
    summary = f"{i} moves before exit"
    distinct_moves = guard.visited
    print(summary)
    print(o)
    if TEST:
        for row in data:
            print("".join(row))
    print()
    clear_screen()
    del guard
    loopers: List[Tuple[int, int]] = []
    # run as many tests as there are cells in the floor plan
    # may not be enough!
    last_test = 0
    for test, test_location in enumerate(distinct_moves.keys()):
        # if test in [4251]:
        #    TEST = True
        # else:
        #    TEST = False
        guard = Guard(start, vectors["^"], data)
        moves = ""
        o = ""
        last_test = test
        clear_screen()
        print(summary)
        print(f"test {test}")
        print(f"obstacle at {test_location}")
        if guard.floor_map[test_location[1]][test_location[0]] == ".":
            guard.put_obstacle(test_location)
            while o[:4] not in ("loop", "Gone"):
                o, err = guard.move()
                if err is None:
                    if TEST:
                        moves += f"\n{o}" if o != "" else ""
                        guard.show()
                        print(moves)
                    if o == "loop":
                        loopers.append(test_location)
                        print("loop detected")
                else:
                    print(err)
                    return
        else:
            print(
                test_location,
                "is not .",
                guard.floor_map[test_location[1]][test_location[0]],
            )
            if TEST:
                guard.show()
                sleep(0.5)

    print(summary)
    print(list(distinct_moves.keys()))
    print(f"Number of tests: {last_test}")
    guard = Guard(start, vectors["^"], data)
    for ob in loopers:
        guard.put_obstacle(ob)
    print(f"{len(loopers)} locations where obstacles cause loops\n{loopers}")
    guard.show()


if __name__ == "__main__":
    main()
