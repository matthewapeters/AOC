package main

import (
	"aoc_16/pkg/edge"
	"aoc_16/pkg/min_priority_queue"
	"aoc_16/pkg/utils"

	"container/heap"
	"fmt"
	"os"
	"strings"
)



const MaxCoords = 'M'
const Wall = '#'
const Space = '.'
const Start = 'S'
const End = 'E'
const OneTurn = 1000
const OneMove = 1

// set of visited cells
var Visited = map[string]edge.Edge{}
func DrawTheMap(){
	//   Draw the map
	fmt.Print(" ")
	for x := range SPECIAL['M'].X+1 {
		fmt.Printf("%d", x%10)
	}
	fmt.Println()
	for y := range SPECIAL['M'].Y+1 {
		fmt.Printf("%d", y%10)
		for x := range SPECIAL['M'].X+1 {
			fmt.Printf("%s", string(MAP[utils.Coord{X:x,Y:y}.String()]))
		}
		fmt.Println()
	}
}



func LookAround(current edge.Edge, pq *min_priority_queue.PriorityQueue)(moves []edge.Edge){
	var edj *edge.Edge
	backwards  := (current.OutGoingDirection+ 2) % 4
	//fmt.Printf("Location: %s  Going %d (%s)  backwards is %d (%s) \n", current.Location, current.OutGoingDirection, string(utils.Symbols[current.OutGoingDirection]), backwards,string(utils.Symbols[backwards]) )

	// examine cells in cardinal directions from current.Location
	for direction := range 4 {
		newLocation := current.Location.To(direction)
		symbol := MAP[newLocation.String()]

		// ignore the "backwards" move and ignore walls
		if direction == backwards || symbol == Wall {
			continue
		}

		cost := current.CuumulativeCost + OneMove
		if direction != current.OutGoingDirection{
			cost += OneTurn
		}

		e := edge.Edge{
			Location: newLocation,
			IncomingDirection: current.OutGoingDirection,
			CuumulativeCost: cost,
			OutGoingDirection: direction,
			Symbol: symbol,
			Index: -1,
			Path: current.Path,
		}

		// used to check if any moves were found
		edj = &e

		if e2, ok := Visited[edj.OutVector().String()]; ok && cost < e2.CuumulativeCost {
				fmt.Printf("re-costing %s from %d to %d\n", e2, e2.CuumulativeCost, cost)
				delete(Visited, e2.OutVector().String())
				heap.Push(pq, e)
				continue
		}
		if e2, ok := Visited[edj.OutVector().String()]; ok {
				fmt.Printf("DON'T LOOP AT %s \n", e2)
				MAP[current.Location.String()]='@'
				continue
		}
		if _, ok := Visited[edj.OutVector().String()]; !ok &&( e.Symbol == Space || e.Symbol == End) {
			heap.Push(pq, e)
		}
	}
	if edj == nil {
		fmt.Printf("LOCATION %s IS DEAD END\n", current)
		MAP[current.Location.String()]='X'
	}
	return
}

func Dijkstra(pq *min_priority_queue.PriorityQueue)(winners []edge.Edge){
	// repeatedly process the lowest-cost edge until the end is found
	winners = []edge.Edge{}
	var bestScore = -1
	fmt.Printf("best score must be better than %d\n", bestScore)
	for (*pq).Len()>0 {
		var edj *edge.Edge = heap.Pop(pq).(*edge.Edge)
		// record that we have visited this location going this direction
		Visited[edj.OutVector().String()] = *edj
		edj.Path = append([]*(edge.Edge){}, append(edj.Path, edj)...)
		if edj.Location == SPECIAL[End]{
			if edj.CuumulativeCost <= bestScore || bestScore < 0 {
				bestScore = edj.CuumulativeCost
				winners = append(winners, *edj)
			}
			continue
		}
		// where can we go from here?
		LookAround(*edj, pq)
	}
	return
}


var MAP = map[string]rune{}

// Track start and end coordinates
var SPECIAL = map[rune]utils.Coord{}

func main() {
	fileName := os.Args[1]
	raw, err := os.ReadFile(fileName)
	if err != nil {
		fmt.Printf("ERROR: %s\n",err)
		return
	}

	rawInput := strings.Split(string(raw),"\n")
	for y,row := range rawInput{
		for x,r := range row{
			location := utils.Coord{X:x,Y:y}
			MAP[location.String()] = r
			if r == Start || r == End {
				//fmt.Printf("SPECIAL %s at %d,%d\n",string(r), location.X,location.Y)
				SPECIAL[r]=location
			}
			// track the last location as M for max
			SPECIAL[MaxCoords]=location
		}
	}

	DrawTheMap()

	pq := &min_priority_queue.PriorityQueue{}
	heap.Init(pq)
	e := edge.Edge{Location:SPECIAL['S'],IncomingDirection: utils.East,CuumulativeCost: 0,OutGoingDirection: utils.East, Symbol: Start,Index: 0, Path:[]*edge.Edge{}}
	e.Path = append(e.Path, &e)
	LookAround(e, pq)
	winners := Dijkstra(pq)


	bestSeats := map[string]bool{}
	for _, winner := range winners{
		// Render the map and the path taken
		//   First, copy the path taken into the map
		for _,e := range winner.Path {
			MAP[e.Location.String()] = 'O'
			bestSeats[e.Location.String()] = true
			fmt.Printf("%s  ", e)
		}
	}
	fmt.Printf("\n\n")
	DrawTheMap()
	fmt.Printf("There are %d winning tiles on the map\n", len(bestSeats))
}