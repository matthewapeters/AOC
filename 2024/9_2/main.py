"""
AOC 2024 day 9 part 2

Move while files in descending file number order to first
continguous block of free space that can hold the file.
If no contiguous space is available, the file does not move.

The FAT comes in handy now, because we can scan the sizes of
empty blocks after each file.

We do not have to update the FAT

"""

from typing import Dict, List, OrderedDict, Tuple


SAMPLE = "9953877292941"  # "1313165"  # "2333133121414131402"
TEST = False


class Disk:
    """Disk"""

    def __init__(self, size: int, fat: OrderedDict[int, List[Dict[int, List[int]]]]):
        self.media: List[int] = [-1 for i in range(size)]
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

    def compress(self, file: int, insert_after: int):
        """ "
        compress
        inserts file in the free spaces at end of insert_after
        updates the file_allocation_table and the media
        """
        file_to_move = self.file_allocation_table[file]
        file_size = list(file_to_move[0].keys())[0]
        file_block_range = file_to_move[0][file_size]

        target = self.file_allocation_table[insert_after]
        target_free_size = list(target[1].keys())[0]
        target_free = target[1][target_free_size]

        # if the file is currently further left than the free space, just return
        if file_block_range[0] < target_free[0]:
            return

        # write file to media
        # identify the new block range
        block_start = target_free[0]
        block_end = target_free[0] + file_size - 1
        # range second parameter is not inclussive, so add 1
        for b in range(block_start, block_end + 1):
            self.media[b] = file
        # wipe media where file had been
        for b in range(file_block_range[0], file_block_range[1] + 1):
            self.media[b] = -1

        # update the blocks of the file
        file_to_move[0][file_size] = [block_start, block_end]
        # update the free at the end of the file
        free_start = block_end + 1
        free_end = target_free[1]
        if free_end >= free_start:
            file_to_move[1] = {free_end - free_start + 1: [free_start, free_end]}
        else:
            file_to_move[1] = {0: []}

        # insert_after now has no free blocks
        target[1] = {0: []}

    def format(self):
        """
        format
        writes file blocks to disk
        """
        self.read_head = 0
        self.write_head = 0
        for idx, details in self.file_allocation_table.items():
            used_blocks: Dict[int, List[int]] = details[0]
            blocks_size = list(used_blocks.keys())[0]
            blocks_range = used_blocks[blocks_size]
            blocks_range.append(self.write_head)
            free: Dict[int, List[int]] = details[1]
            free_size = list(free.keys())[0]
            free_range = free[free_size]

            for _ in range(blocks_size):
                self.media[self.write_head] = idx
                self.write_head += 1
            # the end of the range is the prior write_head position
            blocks_range.append(self.write_head - 1)
            free_range.append(self.write_head)
            free_range.append(self.write_head + free_size - 1)
            self.write_head += free_size

    def __str__(self) -> str:
        return "".join([f"[{v}]" if v >= 0 else "." for v in self.media])

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
        """checksum"""
        blks = [i * v for i, v in enumerate(self.media) if v != -1]
        return sum(blks)

    def seek_contig_empty(self, size: int) -> List[int]:
        """
        seek_contig_empty
        scans the FAT for first available contiguous space large
        enough to hold size
        Returns the
        """
        fill_range = []
        for i, v in self.file_allocation_table.items():
            if v[1] >= size:
                break

        return fill_range


if __name__ == "__main__":
    if not TEST:
        with open("input.txt", "r", encoding="utf8") as fh:
            raw = fh.read().strip()
    else:
        raw = SAMPLE

    # k: file number
    # list of dict where [{size:range},{free:range}]
    # actual ranges are unknown until the disk is formatted
    data: OrderedDict[int, List[Dict[int, List[int]]]] = {
        k: [{s: []} for s in v]
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
    if TEST:
        print(data)
        # print(disk)
        # print(disk.ls())

    disk.read_head = disk.size - 1

    # work files by id in descending order
    files = disk.ls()
    files.sort(reverse=True)

    # before processing
    if TEST:
        print(disk)
    # the first file is "compressed" - there is no need to (re)processes it
    for file_id in files[:-1]:
        file = disk.file_allocation_table[file_id]
        space_needed = list(file[0].keys())[0]
        target_id: int = -1
        target_free_space: int = -1
        last_target_id: int = -1
        # we are scanning files in the order they appear on the media
        for target_id in disk.media:
            # ignore the same file, files already examined, and empty space
            if target_id in (file_id, last_target_id, -1):
                continue
            last_target_id = target_id
            target_free_space = list(disk.file_allocation_table[target_id][1].keys())[0]
            if target_free_space >= space_needed:
                # print(f"compress({file_id},{target_id})")
                disk.compress(file_id, target_id)
                if TEST:
                    print(disk)
                break

        # if we scanned the whole FAT and found no space,
        # move on to the next file to move

    print("---------------")
    print(disk)
    # print(disk.file_allocation_table)
    print(f"disk checksum is: {disk.checksum()}")
