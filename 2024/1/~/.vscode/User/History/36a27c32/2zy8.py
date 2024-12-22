# Databricks notebook source

def main():
    with open('input.txt','r',encoding='utf8') as fh:
        data=fh.read().split("\n")
        data = [[int(f) for f in r.split(" ") if f!=''] for r in data if r!='']

        left = [i[0] for i in data]
        right = [i[1]for i in data]
        diff=[0 for i in data]
        left.sort()
        right.sort()
        similarity=0
    for i,v in enumerate(left):
          diff[i]=abs(v-right[i])
          sims=len([0 for r in right if r==v])
          similarity += sims
    r = sum(diff)
    print(f"the sum is {r}")



if __name__ == "__main__":
    main()
