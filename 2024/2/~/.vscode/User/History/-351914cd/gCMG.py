from typing import List


def evaluate_report(r: List[int])->bool:
    pass

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
            for i in range(len(report)-1):
                print(f"{report[i]}:{report[i+1]} ", end="")
                diff = report[i] - report[i+1]
                if abs(diff) not in (1,2,3):
                    if rejected==0:
                        rejected+=1
                        print(f"XR{diff} ", end="")
                        continue
                    else:
                        print(f"XR{diff} ", end="")
                        rejected+=1
                        break
                direction = 1 if diff>0 else -1 if diff<0 else 0
                if direction == 0:
                    if rejected==0:
                        rejected+=1
                        print(f"X0{diff}{report[i]}-{report[i+1]} ", end="")
                        continue
                    else:
                        rejected+=1
                        safe-=1
                        print(f"X0{diff}{report[i]}-{report[i+1]} ", end="")
                        break
                if last_direction == 0:
                    last_direction = direction
                else:
                    if last_direction != direction:
                        if rejected==0:
                            rejected+=1
                            print("X! ", end="")
                            continue
                        else:
                            rejected+=1
                            print("X! ", end="")
                            break
            if rejected==2:
                print(f"BAD")
                safe-=1
            else:
                print(f"GOOD")
        print(f"\nnumber of safe reports: {safe}")
               


