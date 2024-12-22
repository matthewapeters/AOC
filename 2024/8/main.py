"""
AOC 2024 Day 8

The dictionary "antinodes" is keyed by coordinates (x,y) on the layout map.
Values are the symbols for antennae having antinodes at said coordinates

Scan the layout for any symbol other than "."
When an antena if found, scan forward for all other instances of the same
symbol.  Call the function to compute the antinodes for the first and each
matching antena and track in the "antinodes" dictionary

How many unique locations within the bounds of the map contain an antinode?
To answer this, get the count of antinode keys.

we can do a single scan over the layout map to create a dict of symbols to a list of locations.
Iterating over the map will reduce repeated scans

"""

from typing import Dict, List, Tuple

TEST = False
SAMPLE = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

MAX_X = "MAXX"
MAX_Y = "MAXY"
MIN_X = "MINX"
MIN_Y = "MINY"


def find_antinodes(
    symbol: str, a, b: Tuple[int, int], lim: Dict[str, int]
) -> Dict[List[Tuple[int, int]], str]:
    """
    antinodes

    compute the positive and negative antinodes between antennae
    If the antinode is outside of the limits

    b.y >= a.y

    param: symbol: str
    param: a: Tuple[int,int] x,y of first antena
    param: b: Tuble[int,int] x,y of the second antena
    param: lim: Dict[str,int] limits/bounds of the map

    """
    dx = b[0] - a[0]
    dy = b[1] - a[1]  # always >= 0
    offset_x = dx
    offset_y = dy
    pre_a = ((a[0] - offset_x), (a[1] - offset_y))
    post_b = ((b[0] + offset_x), (b[1] + offset_y))
    if TEST:
        print(symbol, pre_a, a, b, post_b)
    return {
        p: [symbol]
        for p in [pre_a, post_b]
        if p[0] >= lim[MIN_X]
        and p[0] <= lim[MAX_X]
        and p[1] >= lim[MIN_Y]
        and p[1] <= lim[MAX_Y]
    }


if __name__ == "__main__":
    if not TEST:
        with open("input.txt", "r", encoding="utf8") as fh:
            raw = fh.read().split("\n")
    else:
        raw = SAMPLE.split("\n")

    layout = [list(row) for row in raw if row != ""]
    antennae = {
        (x, y): c for y, row in enumerate(layout) for x, c in enumerate(row) if c != "."
    }
    symbols_index = {
        s: [p for p in antennae if antennae[p] == s] for s in set(antennae.values())
    }

    antinodes: Dict[Tuple[int, int], str] = {}
    limits = {MIN_X: 0, MIN_Y: 0, MAX_Y: len(layout) - 1, MAX_X: len(layout[0]) - 1}

    if TEST:
        print(symbols_index)

    results = set(
        found_position
        for symbol, positions in symbols_index.items()
        for i, a in enumerate(positions[:-1])
        for b in positions[i + 1 :]
        for found_position in find_antinodes(symbol, a, b, limits).keys()
    )

    if TEST:
        print(results)
        for p in results:
            layout[p[1]][p[0]] = "#"
        for row in layout:
            print("".join(row))

    print(f"count of unique antinodes is {len(results)}")
