"""
AOC 2024 Day 7

Two operators (+ and *) are expected to be used with test data to produce the expected test result.
If they can, then the expected test result is added to the final value

Evaluate possible combinations of operators with test data to determine if the test should
be included in the final value.

* the data is in the form <expected>:<arg>" "<arg>...
* evaluate the number of possible operators, and try various combinations to evaluate the
  various results.
* hint - if the data being processed creates an intermidiary value >= the test value before the last
  operator is appled (and the last operator > 0) then the permutation cannot work - exit early
* the number of possible operator combinations is a function of number of arguments: there are
  len(arguments) - 1 places to use operators.

  for example:
    83: 17 5
    has one possible place for an operator.
    There are 2 operators.  This means there are 2 evaluations that can be made.

    7290: 6 8 6 15
    has 3 possible places for an operator

    all of one kind:
    +++
    ***

    2 of +
    ++*
    +*+
    *++

    2 of *
    +**
    *+*
    **+

    There are 8 possible combinations (2^3)

    The itertools.product from the standard library is an effective
    means of producing each of the combinations of possible values
    given the length of the string to produce

"""

from itertools import product
from typing import Callable, List

TEST_DATA = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

TEST = False

OPERATORS = {"+": lambda x, y: x + y, "*": lambda a, b: a * b}


class Test:
    """Test"""

    def __init__(self, s: str):
        self.expected = int(s.split(":")[0])
        self.args = [int(a) for a in s.split(":")[1].split(" ") if a != ""]

    def evaluate(self) -> int:
        """evaluate"""
        operations: List[Callable[...]] = [
            [OPERATORS[ops] for ops in o]
            for o in product(OPERATORS.keys(), repeat=len(self.args) - 1)
        ]
        results = []
        for test in operations:
            solution = self.args[0]
            for i, b in enumerate(self.args[1:]):
                solution = test[i - 1](solution, b)
                if solution > self.expected:
                    break
            results.append(solution == self.expected)
        return self.expected if any(results) else 0


if __name__ == "__main__":
    if not TEST:
        with open("input.txt", "r", encoding="utf8") as fh:
            raw = fh.read()
    else:
        raw = TEST_DATA
    tests = [Test(r).evaluate() for r in raw.split("\n") if r != ""]
    print(sum(tests))
