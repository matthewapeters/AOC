# Databricks notebook source

def main():
    with open('input.txt','r',encoding='utf8') as fh:
        data=fh.read().split("\n")
        data = [[f for f in r.split(" ") if f!=''] for r in data]
    print(data[0])

    #left = [i[0] for i in data ]
    #right = [i[1]for i in data ]
    #left.sort()
    #right.sort()
    #diff=[i[2] for i in data]
    #for i,v in enumerate(left):
    #      diff[i]=abs(v-right[i])
    #sum=sum(diff)
    #print(f"the sum is {sum}")


if __name__ == "__main__":
    main()
