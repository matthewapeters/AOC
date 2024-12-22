
from typing import Any

digits = [str(i) for i in range(10)] 
start_paren="("
end_paren=")"
comma = ","
valid=[*digits,start_paren, end_paren, comma]
operators = {'mul': lambda x,y: x*y, 'sum': lambda x,y: x+y}


class Node():
    def __init__(self, value: Any):
        self.value=value
        self.next: Node = None
    def __str__(self):
        if self.next is not None:
            return f"[{self.value}]-->"
        return f"[{self.value}]--X"

class Stack():
    head: Node = None
    count:int = 0

    def push(self, value:Any):
        n = Node(value)
        n.next = self.head
        self.head = n
        self.count += 1

    def pop(self)->Any:
        if self.head is None:
            return None
        h = self.head
        value = h
        self.head = h.next
        del(h)
        self.count -= 1
        return value

    def push_three(self, l,x,y):
        self.push(l)
        self.push(x)
        self.push(y)

    def compute(self)->Any:
        y = self.pop()
        x = self.pop()
        l = self.pop()
        if l is None or x is None or y is None:
            return None
        return operators[l](x,y)

    def __str__(self):
        s=""
        h = self.head
        while h:
            s+=str(h)
            h=h.next
        if s == "":
            s=="EMPTY"
        return s
        

totals = Stack()
work = Stack()

def scan_line(line:str, op:str ):
    eol=len(line)
    opl = len(op)+1
    # don't scan past where operator will not fit
    last_idx = eol-opl
    i = 0
    while i < last_idx:
        print(f"i: {i}\t", end="")
        end_of_op = i+opl
        if line[i:end_of_op] == f"{op}{start_paren}":
            print(f"\noperator {op} found")
            scan=""
            # we include the open paren with the operation
            paren_count = 1
            # we expect to find a series of digits
            print(f"range({end_of_op},{eol})")
            for s in range(end_of_op, eol):
                print(f"{s}:{line[s]} ",end="")
                # if we find a nested paren
                if line[s] == start_paren:
                    paren_count += 1
                if line[s] == end_paren:
                    paren_count -= 1
                if paren_count == 0:
                    # we have reached argument closure
                    if s>end_of_op+3:
                        scan=line[end_of_op:s]
                    break
                # we have found an invalid character and no closer
                # corrupt operator
                if line[s] not in valid:
                    print(f"invalid symbol found: {line[s]}")
                    break
            if scan != "":
                print(f"\nscan found {scan}")
                if scan[0]==start_paren and scan[-1]==end_paren:
                    parts=scan[1:-1].split(",")
                    if len(parts) != 2:
                        print("invalid args")
                    else:
                        if parts[0]==str(int(parts[0])) and parts[1]==str(int(parts[1])):
                            work.push_three(op, int(parts[0]), int(parts[1]))
                else:
                    print("cannot process scan ", scan)
                # advance iterator past scan
                i += end_of_op + len(scan)
                print(f"advance i to {i}")
                continue
        else:
            i += 1
                
    print()
            

if __name__ == '__main__':
    print(valid)
    with open('input.txt','r',encoding='utf8') as raw:
        data=raw.read().split("\n")
    #data = ["mul(1,2)mul(33,444)"]
    for op,l in operators.items():
        o_len = len(op)
        for d in data[0:1]:
            print(f"scan line '{d}' for operator: {op}")
            scan_line(d, op)
    print(work)

