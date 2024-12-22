"""
AOC 2024 Day 4 part 2

The issue is no longer a vector-based search.  Instead it is now radial:
  * we seek the center letter of the target word
  * we need two diagonal finds.
  * vectors can be used based on specific offsets from the center letter
     * assume the radius is int(wordLength/2)
     * there are 4 offsets to consider -- the corners
     * each offset is tied to one search vector (vectors are x,y tuples)
       * lower-left corner is only satisfied with vector (1,-1)
       * upper-right corner is only satisfied with vector (-1,1)
       * lower-right is only satisfied wtih (-1,-1)
       * upper-left is only satisifed with (1,1)
    * an X is solved if either of two possible diagonals are found given the first diagonal
      * if (1,1) is found, only (-1,1) or (1,-1)
      * conversly, the satisfying directions is the set of directions excluding
            * the first direction found
            * the opposite of the first direction found
      * This suggest that there are two classes of directions:
        * descending: shaped like "\" regardless of starting in upper or lower corner
        * ascending: shaped like "/" regardless of starting in upp or lower corner
      * an X can only be satisfied if it is capable of at least one ascending direction
        and one descending direction - if ascending or descending break limits, there is
        no point in scanning.

    * Name each of the corners:
      * UR: upper right -- (-1,1)  -- asc
      * LR: lower right -- (-1,-1) -- desc
      * LL: lower left -- (1,-1) -- asc
      * UL: upper left -- (1,1) -- desc
    * checking boundaries is easier because we can apply radius-offsets to our row
      and column ranges
        * if the word is "MAS" the radius is 1
        * only search range(1, len(data)-radius-1) for row
        * only search range(1, len(data[0]-radius-1)) for column
        * in this way, the corners will always be within the limits
        * only works if words have odd-number of letters
    * simply - given center, compute the corners for ascending and the corners for
      descending searches
    * satisfy at least one ascending and one descending search to count one X
    * The corner for each vector is found by applying its sibiling vector * radius to
      the center coordinates.

"""

# pylint: disable=redefined-outer-name

from typing import Dict, List, Tuple

VALIDATE = False
TARGET = list("MAS")


class Vector():
    """Vector"""
    x: int
    y: int
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, scalar)->'Vector':
        self.x = self.x * scalar
        self.y = self.y * scalar
        return self

    def __add__(self, coords: Tuple[int,int])->Tuple[int, int]:
        return (coords[0]+self.x, coords[1]+self.y)

    def invert(self)->'Vector':
        """invert
        provides a new vector in the same asc/desc class, but reading
        the opposite direction.  Retains scale.
        """
        return Vector(self.x*-1, self.y*-1)

    @staticmethod
    def asc():
        """asc"""
        return [Vector(-1,1), Vector(1,-1)]
    @staticmethod
    def desc():
        """desc"""
        return [Vector(-1,-1), Vector(1,1)]

    def is_asc(self):
        """is_asc"""
        return self.x != self.y



_diagonals = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
_verticals = [(0, 1), (1, 0)]
_horizontals = [(0, -1), (-1, 0)]
SEARCH_DIRECTIONS = [*_diagonals, *_verticals, *_horizontals]


def in_bounds(proposed: Tuple[int, int], limits: Dict[str, Tuple[int, int]]) -> bool:
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
        if in_bounds(extent, limits)
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

def x_search(
    target: List[str],
    data: List[List[str]],
    coords: Tuple[int,int],
    radius: int,
    proof: List[List[str]] = None,
) -> int:
    """
    search
    given x and y, return the number of target instances found in any direction
    """
    x=coords[0]
    y=coords[1]
    # only consider x,y if it is the first letter of the target
    if data[y][x] != target[radius]:
        return 0

    families:Dict[str,List[Vector]] = {"asc": Vector.asc(), "desc": Vector.desc()}

    found = [(name, vec)
             for name,vec in {
                 name:[ v
                       for v,inv in { v:(v.invert()*radius)
                                     for v in family
                                     }.items()
                       if all((
                           data[y+(v.y*i)+(inv.y)][x+(v.x*i)+(inv.x)] == target[i]
                           for i in range(len(target))))
                       ]
                 for name, family in families.items()
                 }.items()
        if len(vec)==1]

    if len(found) < 2:
        return 0

    if VALIDATE:
        for t in found:
            n=t[0]
            vectors=t[1]
            for v in vectors:
                inv = v.invert()*radius
                for i,_ in enumerate(target):
                    proof[y + (v.y * i)+(inv.y)][x + (v.x * i)+inv.x] = target[i]

    return 1

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
    radius = int(length/2)
    for y in range(radius, len_y-radius):
        for x in range(radius, len_x-radius):
            # we do not need to consider X, so extent length is one less
            # found += search(TARGET, data, x, y, radius, limits, proof)
            found += x_search(TARGET, data, (x,y), radius, proof)
    print(f"found {found} instances of {TARGET}")

    if VALIDATE:
        for r in proof:
            for l in r:
                print(l, end="")
            print()


if __name__ == "__main__":
    main()
