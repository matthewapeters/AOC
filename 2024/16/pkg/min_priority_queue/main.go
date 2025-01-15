package min_priority_queue

import (
	"aoc_16/pkg/edge"
	"fmt"
)

type PriorityQueue []*edge.Edge

func (pq PriorityQueue)Len()int {
	return len(pq)
}

func (pq PriorityQueue) Swap(i,j int) {
	pq[i],pq[j] = pq[j],pq[i]
	pq[i].Index = i
	pq[j].Index = j
}

func (pq PriorityQueue)Less(i,j int) bool {
	return pq[i].CuumulativeCost < pq[j].CuumulativeCost
}

func (pq *PriorityQueue)Push(x any){
	n := len(*pq)
	edge := x.(edge.Edge)
	edge.Index = n
	//fmt.Printf("push %s\n", edge)
	*pq = append(*pq, &edge)
}

func (pq *PriorityQueue) Pop() any {
	old := *pq
	n := len(old)
	//fmt.Println(old)
	item := old[n-1]
	old[n-1] = nil  // don't stop the GC from reclaiming the item eventually
	item.Index = -1 // for safety
	*pq = old[0 : n-1]
	fmt.Printf("pop %s\n", item)
	return item
}