from typing import List


def evaluate_report(report: List[int])->bool:
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
    return True

def is_safe(report: List[int])->bool:
    if evaluate_report(report):
        return True
    return all( [ evaluate_report( [ x 
                                    for j,x in enumerate(report) 
                                    if j !=i ])
                for i in range(len(report))
                ])

if __name__ == '__main__':
    with open('input.txt','r', encoding='utf8') as raw:
        data = [[int(s) for s in report.split(" ") if s !=''] 
                for report in raw.read().split("\n") if report != '']
        safe=len(data)
        print(f"there are {safe} reports")
        for idx,report in enumerate(data):
            safe += 0 if is_safe(report) else -1

        print(f"\nnumber of safe reports: {safe}")
               


