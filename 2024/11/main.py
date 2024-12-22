"""
AOC 2024 day 11
"""

from typing import List

TEST = False
SAMPLE = "125 17"


def blink(n: int) -> List[int]:
    # If the stone is engraved with the number 0, it is replaced by a
    #   stone engraved with the number 1.
    if n == 0:
        return [1]

    # If the stone is engraved with a number that has an even number of
    #   digits, it is replaced by two stones. The left half of the digits
    #   are engraved on the new left stone, and the right half of the digits
    #   are engraved on the new right stone. (The new numbers don't keep
    #   extra leading zeroes: 1000 would become stones 10 and 0.)
    if len(f"{n}") % 2 == 0:
        split = int(len(f"{n}") / 2)
        return [int(f"{n}"[:split]), int(f"{n}"[split:])]

    # If none of the other rules apply, the stone is replaced by a new stone;
    #   the old stone's number multiplied by 2024 is engraved on the new stone.
    return [n * 2024]


if __name__ == "__main__":
    if not TEST:
        with open("input.txt", "r", encoding="utf8") as fh:
            raw = fh.read().split(" ")
    else:
        raw = SAMPLE.split(" ")

    rocks = [int(n) for n in raw if n != ""]
    if TEST:
        print(rocks)

    for i in range(25):
        if TEST:
            print(i)
            print(rocks)
        rocks = [new_rock for r in rocks for new_rock in blink(r)]

    print(len(rocks))
