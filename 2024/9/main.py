"""
AOC 2024 day 9


"""

from typing import List, OrderedDict, Tuple


SAMPLE = "2333133121414131402"
TEST = False


class Disk:
    """Disk"""

    def __init__(self, size: int, fat: OrderedDict[int, Tuple[int, int]]):
        self.media: OrderedDict[int, int] = {i: -1 for i in range(size)}
        self.size = size
        self.file_allocation_table = fat
        self._read_head: int = 0
        self._write_head: int = 0

    def ls(self) -> List[int]:
        """
        ls
        Lists the file names
        """
        return list(self.file_allocation_table.keys())

    @property
    def write_head(self):
        """write_head"""
        return self._write_head

    @write_head.setter
    def write_head(self, i: int):
        self._write_head = i

    @property
    def read_head(self):
        """read_head"""
        return self._read_head

    @read_head.setter
    def read_head(self, i: int):
        self._read_head = i

    def swap(self):
        """
        swap
        swap the blocks at the read and write heads
        """
        t: int = self.media[self.write_head]
        self.media[self.write_head] = self.media[self.read_head]
        self.media[self.read_head] = t

    def format(self):
        """
        format
        writes file blocks to disk
        """
        self.read_head = 0
        self.write_head = 0
        for idx, v in self.file_allocation_table.items():
            len_blocks = v[0]
            len_free = v[1]
            for _ in range(len_blocks):
                self.media[self.write_head] = idx
                self.write_head += 1
            self.write_head += len_free

    def __str__(self) -> str:
        return "".join([f"{v}" if v >= 0 else "." for v in self.media.values()])

    def wh_seek_empty(self):
        """
        wh_seek_empty
        write head seek next empty space
        """
        while self.media[self.write_head] != -1 and self.write_head < self.size:
            self.write_head += 1
            if TEST:
                print(f"write_head: {self.write_head}")

    def rh_seek_ne(self):
        """
        rh_seek_ne
        read head seen next not-empty space
        """
        while self.media[self.read_head] == -1:
            self.read_head -= 1

    def checksum(self) -> int:
        blks = [i * v for i, v in self.media.items() if v != -1]
        return sum(blks)


if __name__ == "__main__":
    if not TEST:
        with open("input.txt", "r", encoding="utf8") as fh:
            raw = fh.read().strip()
    else:
        raw = SAMPLE

    data: OrderedDict[int, Tuple[int, int]] = {
        k: v
        for k, v in enumerate(
            [
                (int(raw[i]), 0 if i + 1 > len(raw) - 1 else int(raw[i + 1]))
                for i in range(0, len(raw), 2)
            ]
        )
    }

    blocks = [int(c) for c in raw]

    if TEST:
        print(SAMPLE)
        print(data)
    disk = Disk(size=sum(blocks), fat=data)
    disk.format()
    # if TEST:
    print(data)
    print(disk)
    print(disk.ls())

    disk.read_head = disk.size - 1
    disk.rh_seek_ne()
    disk.write_head = 0
    disk.wh_seek_empty()
    while disk.read_head > disk.write_head:
        if TEST:
            print(disk.read_head, disk.write_head)
        disk.swap()
        if TEST:
            print(disk)
        disk.rh_seek_ne()
        disk.wh_seek_empty()

    print(disk)
    print(f"disck checksum is: {disk.checksum()}")
