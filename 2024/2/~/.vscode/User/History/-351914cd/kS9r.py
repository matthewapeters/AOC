if __name__ == '__main__':
    with open('input.txt','r', encoding='utf8') as raw:
        data = [[int(s) for s in report.split(" ") if s !=''] 
                for report in raw.read().split("\n") if report != '']
        safe=len(data)
        for report in data:
            last_direction=0
            for i in range(len(data)-1):
                diff = data[i] - data[i+1]
                if abs(diff) not in (1,2,3):
                    safe-=1
                    break
                direction = 1 if diff>0 else -1 if diff<0 else 0
                if direction == 0:
                    safe-=1
                    break
                if last_direction == 0:
                    last_direction = direction
                else:
                    if last_direction != direction:
                        safe-=1
                        break
        
        print(f"number of safe reports: {safe}")
               


