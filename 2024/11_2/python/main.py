"""
AOC 2024 day 11 part 2

Brute force shows rediculous growth of stones; the dots
at the end of each blink report.

the solution shown tries to address broken pipe issues
by repeating calls to the process pool and limiting the
number of arguments to "chunk_size"
    chunk_size: int = 8000000

Even with functools.cache the system dies at blink 43.

Earlier testing shows that more looping smaller chunks performs
much worse.

0:00:00.016554 0 1            8 .
0:00:00.006077 1 1           11 .
0:00:00.005873 2 1           13 .
0:00:00.005441 3 1           21 .
0:00:00.005936 4 1           32 .
0:00:00.006288 5 1           48 .
0:00:00.009940 6 2           71 .
0:00:00.007332 7 2          112 .
0:00:00.005884 8 2          151 .
0:00:00.006909 9 2          226 .
0:00:00.006623 10 2          393 .
0:00:00.005978 11 2          572 .
0:00:00.010191 12 3          840 .
0:00:00.008991 13 3         1249 .
0:00:00.010218 14 3         1928 .
0:00:00.009493 15 3         3084 .
0:00:00.009003 16 3         4423 .
0:00:00.010659 17 3         6707 .
0:00:00.010598 18 4        10432 .
0:00:00.016640 19 4        15492 .
0:00:00.020410 20 4        24053 .
0:00:00.021066 21 4        36192 .
0:00:00.026295 22 4        54707 .
0:00:00.031597 23 4        83905 .
0:00:00.036053 24 5       125396 .
0:00:00.040058 25 5       193899 .
0:00:00.055377 26 5       293299 .
0:00:00.075857 27 5       440359 .
0:00:00.096023 28 5       678053 .
0:00:00.147671 29 5      1021284 .
0:00:00.192817 30 6      1557292 .
0:00:00.267820 31 6      2369051 .
0:00:00.389266 32 6      3573580 .
0:00:00.598912 33 6      5473980 .
0:00:00.923911 34 6      8266193 . .
0:00:01.319577 35 6     12563489 . .
0:00:01.937404 36 7     19171786 . . .
0:00:03.151302 37 7     28932596 . . . .
0:00:04.809951 38 7     44135507 . . . . . .
0:00:07.269576 39 7     66967145 . . . . . . . . .
0:00:11.415399 40 7    101567247 . . . . . . . . . . . . .
0:00:17.528290 41 7    154804410 . . . . . . . . . . . . . . . . . . . .
0:00:24.255526 42 8    234204983 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
KILLED


But there are a limited number of discrete imputs that are heavily repeated.
What if for each blink we send a SET of rocks, and then rebuild the list with the
results from the map
"""

from typing import List
from functools import cache

TEST = False
SAMPLE = "125 17"
# SAMPLE = "0 0 0 0 0 0 0 0 0 0"


@cache
def blink(n: int):
    """blink"""
    # print(f"blink {n}")
    # If the stone is engraved with the number 0, it is replaced by a
    #   stone engraved with the number 1.
    if n == 0:
        return (1, None)

    # If the stone is engraved with a number that has an even number of
    #   digits, it is replaced by two stones. The left half of the digits
    #   are engraved on the new left stone, and the right half of the digits
    #   are engraved on the new right stone. (The new numbers don't keep
    #   extra leading zeroes: 1000 would become stones 10 and 0.)
    if len(f"{n}") % 2 == 0:
        split = len(f"{n}") // 2
        return (int(f"{n}"[:split]), int(f"{n}"[split:]))

    # If none of the other rules apply, the stone is replaced by a new stone;
    #   the old stone's number multiplied by 2024 is engraved on the new stone.
    return (n * 2024, None)


# pylint: disable=redefined-outer-name
@cache
def blink_a_bunch(blinks: int, rock: int) -> int:
    """
    blink_a_bunch
    """
    left_rock, right_rock = blink(rock)
    if blinks == 1:
        if right_rock is not None:
            return 2
        else:
            return 1
    count = blink_a_bunch(blinks - 1, left_rock)
    if right_rock is not None:
        count += blink_a_bunch(blinks - 1, right_rock)
    return count


if __name__ == "__main__":
    if not TEST:
        with open("../input.txt", "r", encoding="utf8") as fh:
            raw = fh.read().split(" ")
    else:
        raw = SAMPLE.split(" ")

    rocks: List[int] = [int(n) for n in raw if n != ""]
    print(rocks)
    print()

    blink_times: int = 75

    print(f"compute changes over {blink_times} blinks")
    total: int = 0
    last_total: int = 0
    for r in rocks:
        total += blink_a_bunch(blink_times, r)
        print(f"{blink_times} blinks for {r} produces {total-last_total} rocks\n")
        last_total = total

    print(total)
