"""
AOC 2024 day 10

Topographical map analysis

* trail heads start with 0
* trails only go up by 1 elevation step until level 9 is reached
* travel only in cardinal directions (no diagonal moves)
* trail heads are scored by the number of different peaks they can
  reach
"""

from typing import Dict, List, Set, Tuple

TEST = False

SAMPLE = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


def hike(start: Tuple[int, int], topo_map: List[List[int]]) -> List[Tuple[int, int]]:
    """hike"""
    max_y = len(topo_map) - 1
    max_x = len(topo_map[0]) - 1
    elevation = topo_map[start[1]][start[0]]
    if elevation == 9:
        return [start]
    # these are the possible directions to travel
    # they are within the bounds of the map,
    # and their elevation change is +1
    return [
        peek
        for t in [
            (start[0] + 1, start[1]),
            (start[0] - 1, start[1]),
            (start[0], start[1] + 1),
            (start[0], start[1] - 1),
        ]
        if t[0] >= 0
        and t[1] >= 0
        and t[0] <= max_x
        and t[1] <= max_y
        and topo_map[t[1]][t[0]] - elevation == 1
        for peek in hike(t, topo_map)
    ]


if __name__ == "__main__":
    if not TEST:
        with open("input.txt", "r", encoding="utf8") as fh:
            raw = fh.read().split("\n")
    else:
        raw = SAMPLE.split("\n")

    topo = [[int(c) for c in row] for row in raw if row != ""]

    # get each of the trail heads (locations where value is "0")
    # initialize their sets of reachable peaks
    trails: Dict[Tuple[int, int], int] = {
        (x, y): len(set([peek for peek in hike(start=(x, y), topo_map=topo)]))
        for y, row in enumerate(topo)
        for x, c in enumerate(row)
        if c == 0
    }

    if TEST:
        for row in topo:
            print("".join([f"{d}" for d in row]))
        print(trails)
    print(f"total map score is {sum(trails.values())}")
