"""
AOC 2024 Day 4
"""

# pylint: disable=redefined-outer-name

from typing import List, Tuple

VALIDATE = True

#
#
#
#
#                  [-1][0]
#    [0][-1]       [y][x]      [0][1]
#                  [1][0]
#
# ---------------------
#
# When checking extents, we check length -1,
# because of 0 indexing
#
#  5
#  6S     S
#  7 A   A
#  8  M M
#  9   X
#   0123456789

TARGET = list("XMAS")
SEARCH_DIRECTIONS = [
    (1, 1),
    (-1, -1),
    (1, -1),
    (-1, 1),
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]


def in_bounds(
    proposed: Tuple[int, int], limits: List[Tuple[int]], *args, **kwargs
) -> bool:
    """
    in_bounds
    confirms the proposed position is in-bounds given the limits
    """
    return (
        proposed[0] >= limits["min"][0]
        and proposed[0] <= limits["max"][0]
        and proposed[1] <= limits["max"][1]
        and proposed[1] >= limits["min"][1]
    )


def search_directions(
    x: int, y: int, length: int, limits: List[Tuple[int]]
) -> List[int]:
    """search_directions
    returns a list of search directions allows given the current starting position
    """
    return [
        direction
        for direction, extent in {
            d: (x + (d[0] * (length - 1)), y + (d[1] * (length - 1)))
            for d in SEARCH_DIRECTIONS
        }.items()
        if in_bounds(extent, limits, direction=direction, x=x, y=y)
    ]


def search(
    target: List[str],
    data: List[List[str]],
    x: int,
    y: int,
    length: int,
    limits: List[Tuple[int]],
    proof: List[List[str]] = None,
) -> int:
    """
    search
    given x and y, return the number of target instances found in any direction
    """
    if x == 3 and y == 9:
        pass
    # only consider x,y if it is the first letter of the target
    if data[y][x] != target[0]:
        return 0
    if VALIDATE:
        directions = search_directions(x, y, length, limits)
        found = {
            d: all(
                (
                    data[y + (d[1] * i)][x + (d[0] * i)] == target[i]
                    for i in range(length)
                )
            )
            for d in directions
        }
        for d in [d for d, f in found.items() if f]:
            for i in range(length):
                proof[y + (d[1] * i)][x + (d[0] * i)] = target[i]

    return sum(
        all(
            (
                data[y + (d[1] * i)][x + (d[0] * i)] == target[i]
                for i in range(1, length)
            )
        )
        for d in search_directions(x, y, length, limits)
    )


def main():
    """main"""
    with open("input.txt", "r", encoding="utf8") as fh:
        raw = fh.read()
        raw = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
        data = [list(row) for row in raw.split("\n") if row != ""]
    len_y = len(data)
    len_x = len(data[0])

    proof: List[List[str]] = None
    if VALIDATE:
        proof = [["." for i in range(len_x)] for j in range(len_y)]
    limits = {"min": (0, 0), "max": (len_x, len_y)}
    found = 0
    length = len(TARGET)
    for y in range(len_y):
        for x in range(len_x):
            # we do not need to consider X, so extent length is one less
            found += search(TARGET, data, x, y, length, limits, proof)
    print(f"found {found} instances of {TARGET}")

    if VALIDATE:
        for r in proof:
            for l in r:
                print(l, end="")
            print()


if __name__ == "__main__":
    main()
