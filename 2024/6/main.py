"""
AOC 2024 Day 6

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

# Count distinct places visisted
"""

# pylint: disable=too-few-public-methods

from typing import Dict, List, Tuple


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
        self.visisted = set()
        self.map = floor_map
        self.direction = start_vector

    @property
    def position(self):
        """position"""
        return (self.x, self.y)

    @position.setter
    def position(self, p: Tuple[int, int]):
        self.visisted.add(self.position)
        self.map[self.position[1]][self.position[0]] = "X"
        self.x = p[0]
        self.y = p[1]

    def move(self):
        """
        move
        moves the guard around the floor/map.
        When the guard moves off the map, returns 'Gone'
        If next move would be into an obstacle, turns, and resumes moving
        """
        next_move = self.direction + self.position
        if (
            next_move[0] < 0
            or next_move[1] < 0
            or next_move[1] > len(self.map) - 1
            or next_move[0] > len(self.map[0]) - 1
        ):
            self.visisted.add(self.position)
            self.map[self.position[1]][self.position[0]] = "X"
            return (
                f"Gone (exit at {next_move}) -- {len(self.visisted)} distinct locations"
            )
        try:
            if self.map[next_move[1]][next_move[0]] == "#":
                self.direction = self.direction.turn
                if TEST:
                    print(f"Turned at {self.position} to {self.direction.name}")
                return self.move()
        except Exception as ex:
            print(f"invalid location {next_move}")
            return f"ERR: {ex}"

        self.position = next_move
        return ""


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


def main():
    """main"""
    if not TEST:
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
    print(f"guard starts at {start}")
    guard = Guard(start, vectors["^"], data)
    o = ""
    while o == "":
        o = guard.move()

    print(o)

    if TEST:
        for row in data:
            print("".join(row))


if __name__ == "__main__":
    main()
