if __name__ == '__main__':
    with open('input.txt','r', encoding='utf8') as raw:
        data = [[int(s) for s in report.split(" ") if s !=''] 
                for report in raw.read().split("\n") if report != '']
        safe=len(data)
        for report in data:
            print(f"\nreport has {len(report)} levels")
            last_direction=0
            rejected=0
            for i in range(len(report)-1):
                print(f"{i} ", end="")
                diff = report[i] - report[i+1]
                if abs(diff) not in (1,2,3):
                    if rejected==0:
                        rejected+=1
                        print("XD ", end="")
                        continue
                    else:
                        safe-=1
                        break
                direction = 1 if diff>0 else -1 if diff<0 else 0
                if direction == 0:
                    if rejected==0:
                        rejected+=1
                        print("X0 ", end="")
                        continue
                    else:
                        safe-=1
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
                            safe-=1
                            break
        
        print(f"\nnumber of safe reports: {safe}")
               


