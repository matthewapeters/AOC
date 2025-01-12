package main

import (
	"container/heap"
	"fmt"
	"os"
	"strings"
)

type Coord struct {
	X int
	Y int
}

func (c Coord)To(direction int) (Coord) {
	return Coord{c.X + Moves[direction].X, c.Y+Moves[direction].Y}
}

func (c Coord)String()string{
	return fmt.Sprintf("{%d,%d}", c.X, c.Y)
}

type Edge struct {
	Location Coord
	IncomingDirection int
	CuumulativeCost int
	OutGoingDirection int
	Symbol rune
	Index int
	Path []*Edge
}

func (e Edge)String()string{
	return fmt.Sprintf("%s%s%s%s[%d]%s", string(Symbols[e.IncomingDirection]),e.Location,string(Symbols[e.OutGoingDirection]), e.Location.To(e.OutGoingDirection), e.CuumulativeCost, string(e.Symbol))
}

type PriorityQueue []*Edge

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
	edge := x.(Edge)
	edge.Index = n
	fmt.Printf("push %s\n", edge)
	*pq = append(*pq, &edge)
}

func (pq *PriorityQueue) Pop() any {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // don't stop the GC from reclaiming the item eventually
	item.Index = -1 // for safety
	*pq = old[0 : n-1]
	return item
}

const MaxCoords = 'M'
const Wall = '#'
const Space = '.'
const Start = 'S'
const End = 'E'
const OneTurn = 1000
const OneMove = 1

// set of visited cells
var Visited = map[string]Edge{}

/*
To find the opposite of a direction, add 2 and % 4
To find the turns, add +1 or -1 and % 4
*/
const (	Right = iota
		Up
	  	Left
	   	Down
		)


var Symbols =[]rune {
	Right: '>',
	Up: '^',
	Left:'<',
	Down: 'V',
}

// Moves maps movement vectors to runes
var Moves = map[int]Coord{
	Up:{0,-1},
	Down:{0,1},
	Left: {-1,0},
	Right: {1,0},
}

func (current Edge)LookAround()(moves []Edge){
	// examine cells in cardinal directions from c
	// return unvisisted spaces (or the End) as a list of Edges
	// Edges are not costed
	moves = []Edge{}

	var partialPath = []*Edge{}
	if len(current.Path) >= 2 {
		partialPath = current.Path[:len(current.Path)-1]
	}
	for direction := range 4 {
		// ignore the "backwards" move
		if (direction + 2) % 4 == current.IncomingDirection ||
			MAP[current.Location.To(direction)] == Wall {
			continue
		}

		newLocation := current.Location.To(direction)
		cost := current.CuumulativeCost + OneMove
		// Symbol is what we found on the MAP ...
		if direction != current.IncomingDirection {
			cost += OneTurn
			// or what our old direction was if the direction changes
		}
		// clone the current Edge, but change its direction to the direction of the move
		// its path is no longer necessary
		clonedCurrent := Edge{current.Location, current.IncomingDirection, current.CuumulativeCost, direction, current.Symbol, current.Index, []*Edge{}}
		// create the edge for the new move
		edge := Edge{newLocation, direction, cost, direction, MAP[newLocation],-1,[]*Edge{}}
		edge.Path = append(partialPath, []*Edge{&clonedCurrent, &edge}...)

		if _, ok := Visited[edge.String()]; !ok &&( edge.Symbol == Space || edge.Symbol == End) {
			moves = append(moves, edge)
		} else {
			if e, ok := Visited[edge.String()]; ok && cost < e.CuumulativeCost {
				fmt.Printf("re-costing %s from %d to %d\n", e, e.CuumulativeCost, cost)
				e.CuumulativeCost = cost
				moves = append(moves, e)
			}
		}
	}
	return
}

func Dijkstra(pq *PriorityQueue)(winner *Edge){
	for (*pq).Len()>0 {
		var edge *Edge = heap.Pop(pq).(*Edge)
		if edge.Location == SPECIAL[End]{
			fmt.Printf("Found End at %s\n", edge)
			return edge
		}
		// repeatedly process the lowest-cost edge until the end is found
		for _, move := range  edge.LookAround() {
			heap.Push(pq, move)
			Visited[edge.String()] = move
		}
	}
	return
}


var MAP = map[Coord]rune{}

// Track start and end coordinates
var SPECIAL = map[rune]Coord{}

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
			location := Coord{x,y}
			MAP[location] = r
			if r == Start || r == End {
				//fmt.Printf("SPECIAL %s at %d,%d\n",string(r), location.X,location.Y)
				SPECIAL[r]=location
			}
			// track the last location as M for max
			SPECIAL[MaxCoords]=location
		}
	}

	pq := &PriorityQueue{}
	heap.Init(pq)
	e := Edge{SPECIAL['S'],Right,0,Right, Start,0, []*Edge{}}
	e.Path = []*Edge{&e}
	heap.Push(pq, e)

	winner := Dijkstra(pq)

	// Render the map and the path taken
	//   First, copy the path taken into the map
	for _,e := range winner.Path {
		MAP[e.Location] = Symbols[e.OutGoingDirection]
		fmt.Printf("%s  ", e)
	}
	fmt.Printf("\n\n")
	//   Draw the map
	fmt.Print(" ")
	for x := range SPECIAL['M'].X+1 {
		fmt.Printf("%d", x%10)
	}
	fmt.Println()
	for y := range SPECIAL['M'].Y+1 {
		fmt.Printf("%d", y%10)
		for x := range SPECIAL['M'].X+1 {
			fmt.Printf("%s", string(MAP[Coord{x,y}]))
		}
		fmt.Println()
	}
	fmt.Printf("\nThe winning score is %d\n", winner.CuumulativeCost)
}