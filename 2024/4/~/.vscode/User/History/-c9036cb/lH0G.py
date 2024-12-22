"""
AOC 2024 Day 4
"""

# pylint: disable=redefined-outer-name

from typing import Dict, List, Tuple

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
    proposed: Tuple[int, int], limits: Dict[str, Tuple[int, int]], *args, **kwargs
) -> bool:
    """
    in_bounds
    confirms the proposed position is in-bounds given the limits
    param: proposed: Tuple(x:int, y:int)
    param: limits: List[(minx,miny), (maxx,maxy)]
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
    # When checking extents, we check length -1,
    # because of 0 indexing
    #
    #  5|
    #  6|S     S
    #  7| A   A
    #  8|  M M
    #  9|SAMXMAS
    #   +---------
    #   0123456789

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
    # only consider x,y if it is the first letter of the target
    if data[y][x] != target[0]:
        return 0
    directions = search_directions(x, y, length, limits)
    if VALIDATE:
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
                # we never have to check X (again), regardless of direction
                for i in range(1, length)
            )
        )
        for d in directions
    )


def main():
    """main"""
    with open("input.txt", "r", encoding="utf8") as fh:
        raw = fh.read()
        if VALIDATE:
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
    # limits are 0-indexed
    limits = {"min": (0, 0), "max": (len_x - 1, len_y - 1)}
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
