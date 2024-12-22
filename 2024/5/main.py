"""
AOC 2024 day 5

input is in two sections: rules and updates.
Rules contain "|"
Updates contain list of integers separated by ","
Ignore empty lines (separators)

* Rules look like X|Y, which means if an update contains X and Y, X must come before Y
* Multiple rules for each page can exist.
    * A|B
      A|X
      X|B

      means A comes before B and X, and X comes before B
* Dict of pages, with all pages they must be before?
    * A:[B,X]
      X:[B]

* feels like a classic B-tree pattern. each page is a node
  given a rule 97|13, we would make page 97 be LEFT of 13

             +--------+
             |   13   |
             +--------+
               /
              /
              |
        +----------+
        |    97    |
        +----------+
* what if this is just a custom __gt__ problem?
  Each page has a value (page number), but its sequence is defined by its
  position in the updates list.

    75,47,61,53,29

    page(0,75) < page(1,47) because 0<1
    page(1,47) < page(2,61) because 1<2
    however, if there was a rule 61|47, we would over-ride the sequence in the __gt__ evaluation

    so each page would have a list of pages that it comes before by rule, otherwise
    it is compared by sequence

    for each valid sequence, return the middle page number, then sum these for the proof

  """

from typing import List, Tuple

SAMPLE = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

VALIDATE=False


class Page():
    """Page"""
    def __init__(self, seq:int, page:int):
        self.sequence = seq
        self.page = page
        self.before:List[int] = []

    def __repr__(self)->str:
        return f"Page[{self.sequence}]:{self.page} "

    def add_rules(self, rules:List[Tuple[int,int]]):
        """add_rules"""
        for rule in rules:
            self.add_rule(rule)
        return self

    def add_rule(self, rule:Tuple[int,int]):
        """add_rule"""
        if rule[0] == self.page:
            self.before.append(rule[1])
            self.before.sort()

    def __lt__(self, o:'Page') -> bool:
        if o.page in self.before:
            return True
        return self.sequence<o.sequence

def main():
    """main"""
    raw: List[str] = None

    if not VALIDATE:
        with open("input.txt", 'r', encoding="utf") as fh:
            raw = fh.read().split("\n")
    else:
        raw = SAMPLE.split("\n")

    rules=[tuple(int(up) for up in a.split("|"))
           for a in raw if "|" in a ]
    updates = [ [Page(int(i),int(up)).add_rules(rules)
                 for i,up in enumerate(a.split(","))]
               for a in raw if "," in a]

    totals = 0
    for update in updates:
        c = update.copy()
        c.sort()
        print(update)
        print(c)
        print()
        if c != update:
            # get the middle page value
            middle = int(len(c)/2)
            totals += int(c[middle].page)
    print(f"totals: {totals}")


if __name__== "__main__":
    main()
