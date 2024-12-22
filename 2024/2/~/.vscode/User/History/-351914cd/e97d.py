from typing import List


def evaluate_report(r: List[int])->bool:
    report = r.copy()
    last_direction = 0

    for i in range(len(report)-1):
        diff = report[i] - report[i+1]
        if abs(diff) not in (1,2,3):
            return False
        direction = 1 if diff>0 else -1 if diff<0 else 0
        if direction == 0:
            return False
        if last_direction == 0:
            last_direction = direction
        else:
            if last_direction != direction:
                return False

if __name__ == '__main__':
    with open('input.txt','r', encoding='utf8') as raw:
        data = [[int(s) for s in report.split(" ") if s !=''] 
                for report in raw.read().split("\n") if report != '']
        safe=len(data)
        print(f"there are {safe} reports")
        for idx,report in enumerate(data):
            print(f"{idx} Report has {len(report)} levels: ", end="")
            last_direction=0
            rejected=0

        print(f"\nnumber of safe reports: {safe}")
               


