
from typing import Any
VERBOSE=False
VERBOSE2=True

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
        return f"[{self.value}]--|"

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
        value = h.value
        self.head = h.next
        del(h)
        self.count -= 1
        return value

    def push_three(self, l,x,y):
        if VERBOSE2:
            print(f"push_three('{l}', {x}, {y})")
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
do_op = True

def scan_line(line:str, op:str ):
    global do_op
    eol=len(line)
    opl = len(op)+1
    # don't scan past where operator will not fit
    last_idx = eol-opl
    i = 0
    while i < last_idx:
        if VERBOSE:
            print(f"\ni: {i}:{line[i]}\t", end="")
        end_of_op = i+opl
        if do_op and line[i:end_of_op] == f"{op}{start_paren}":
            if VERBOSE:
                print(f"\noperator {op} found")
            scan=""
            # we include the open paren with the operation
            paren_count = 1
            # we expect to find a series of digits
            if VERBOSE:
                print(f"range({end_of_op},{eol})")
            for s in range(end_of_op, eol):
                if VERBOSE:
                    print(f"{s}:{line[s]} ",end="")
                # if we find a nested paren
                if line[s] == start_paren:
                    paren_count += 1
                if line[s] == end_paren:
                    paren_count -= 1
                if paren_count == 0:
                    # we have reached argument closure
                    if s>=end_of_op+3:
                        scan=line[end_of_op:s]
                    break
                # we have found an invalid character and no closer
                # corrupt operator
                if line[s] not in valid:
                    if VERBOSE:
                        print(f"invalid symbol found: {line[s]}")
                    i = s
                    if VERBOSE:
                        print(f"advance i to {i}")
                    break
            if scan != "":
                if VERBOSE:
                    print(f"\nscan found {scan}")
                parts=scan.split(",")
                if len(parts) != 2:
                    if VERBOSE:
                        print("invalid args")
                    pass
                else:
                    if VERBOSE:
                        print(f"parts[0]:{parts[0]}\t parts[1]:{parts[1]}")
                    if parts[0]==str(int(parts[0])) and parts[1]==str(int(parts[1])):
                        work.push_three(op, int(parts[0]), int(parts[1]))
                # advance iterator past scan
                i = s
                if VERBOSE:
                    print(f"advance i to {i}")
                continue
        elif line[i:i+4] == "do()":
            if VERBOSE2:
                print(f"found {line[i:i+4]} (do_op was {do_op})")
            do_op = True
            i += 4 
        elif line[i:i+7] == "don't()":
            if VERBOSE2:
                print(f"found {line[i:i+7]} (do_op was {do_op})")
            do_op = False
            i += 7
        else:
            i += 1
                
if __name__ == '__main__':
    print(valid)
    with open('input.txt','r',encoding='utf8') as raw:
        data=raw.read().split("\n")
    #data = ["mul(1,2)mul(33,444)"]
    #data = ['xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))',]
    #data = [r"xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))",]
    for op,l in operators.items():
        if op == "mul":
            o_len = len(op)
            for d in data:
                if d=='':
                    continue
                if VERBOSE2:
                    print(f"scan line '{d}' for operator: {op}")
                scan_line(d, op)
    if VERBOSE:
        print(work)
    while work.head:
        totals.push(work.compute())
    if VERBOSE:
        print(totals)
    sum_total = 0
    while totals.head:
        sum_total += totals.pop()
    print(f"sum totals = {sum_total}")


