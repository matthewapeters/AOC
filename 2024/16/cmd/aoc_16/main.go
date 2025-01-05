package main

import (
	"fmt"
	"os"
	"strings"
	"sync"
)

type Coord struct {
	X int
	Y int
}

const Up = 'U'
const Down = 'D'
const Left = 'L'
const Right = 'R'
const MaxCoords = 'M'
const OneTurn = 1000
var Moves = map[rune]Coord{
	Up:{0,-1},
	Down:{0,1},
	Left: {-1,0},
	Right: {1,0},
}
func (c Coord)LookAround()(view map[rune]rune){
	// returns the mapping of runes in the cardinal
	// directions to the current coordinant
	// Because the map has walls, we will not look beyond the map
		view = map[rune]rune{
			Up: MAP[Coord{c.X+Moves[Up].X, c.Y+Moves[Up].Y}],
			Down: MAP[Coord{c.X+Moves[Down].X, c.Y+Moves[Down].Y}],
			Left: MAP[Coord{c.X+Moves[Left].X, c.Y+Moves[Left].Y}],
			Right: MAP[Coord{c.X+Moves[Right].X, c.Y+Moves[Right].Y}],
		}
	return
}

type Turning struct {
	Location Coord
	InitialDirection rune
	TriedDirections []rune
}

// Mutex to allow multiple Deer access the BadTurns
var BadTurnMtx = &sync.Mutex{}
// BadTurns are turnings that lead to dead-ends
// the rune refers to the Move vector
var BadTurns = map[Coord][]rune{}

type Deer struct {
	Name string
	Location Coord
	Direction rune
	Path []Coord 	// a stack
	Turns []Turning // a stack
	Score int
}

func NewDeer(name string, startPosition Coord)*Deer{
	return &Deer{Name:name, Location:startPosition, Direction: Left, Turns:[]Turning{}, Path:[]Coord{startPosition}}
}

func (d *Deer)LastPosition() Coord {
	pathLength := len(d.Path)
	if pathLength <= 1 {
		return d.Location
	}
	return (d.Path[1])
}

func (d *Deer)Turn(turnDirection rune){
	// Turnings are treated as a stack
	if turnDirection == d.Direction{
		return
	}
	// changes the Deer's direction, and increase its score appropriately.
	lenTurns := len(d.Turns)
	if lenTurns == 0 {
		d.Turns = append( []Turning{{d.Location, d.Direction, []rune{turnDirection}}}, d.Turns... )
	} else {
		t := d.Turns[lenTurns-1]
		if t.Location == d.Location {
			t.TriedDirections = append(t.TriedDirections, turnDirection)
		} else {
			d.Turns = append([]Turning{{d.Location, d.Direction, []rune{turnDirection}}}, d.Turns... )
		}
	}
	d.Score += Turns[d.Direction][turnDirection]
	d.Direction = turnDirection
}

func (d *Deer)Move(){
	fmt.Printf("%s moves %s ", d.Name, string(d.Direction))
	d.Location = d.NextMove()
	fmt.Printf("to %d,%d\n", d.Location.X, d.Location.Y)
	d.Path = append([]Coord{d.Location}, d.Path...)
	d.Score += 1
}

func (d *Deer)NextMove()Coord{
	// give the Coord of the next move, used for evaluating
	// collisions or bad turnings
	return Coord{
		d.Location.X + Moves[d.Direction].X,
		d.Location.Y + Moves[d.Direction].Y}
}

func (d *Deer)BackToLastTurn(){
	fmt.Printf("racer %s hit dead end and going back to last turn\n", d.Name)
	// retreat to last turning location, reducing score, re-setting direction
	// and marking the bad turning
	qtyTurns := len(d.Turns)
	lastTurning := d.Turns[qtyTurns-1]
	if d.Location == lastTurning.Location{
		// this occurs if we have returned to our last turning,
		// but there are no new directions to try
		// remove this from the Turns, and retreat to the prior Turning
		d.Turns = d.Turns[:qtyTurns-1]
		qtyTurns --
		lastTurning = d.Turns[qtyTurns-1]
	}
	// retrace our path until we are on lastTurning.Location
	for i:= len(d.Path)-1; i>=0; i--{
		// if we are back to the last turning, break out of this loop
		if (d.Path[i]) == lastTurning.Location{
			d.Location = (d.Path[i])
			break
		}
		// back out the score for the move
		d.Score --
	}
	d.Direction = lastTurning.InitialDirection
	// back out the score for the last tried turn
	tries := len(lastTurning.TriedDirections)
	d.Score -= Turns[lastTurning.InitialDirection][lastTurning.TriedDirections[tries-1]]
	BadTurnMtx.Lock()
	BadTurns[d.Location] = append(BadTurns[d.Location], lastTurning.TriedDirections[tries-1])
	BadTurnMtx.Unlock()
}

func (d *Deer)Race(wg *sync.WaitGroup){
	defer wg.Done()
	/*
	*/
	for {
		/*
		The race starts on a Turning location, but we don't know that
		yet.
			First, Look around.  Exclude '#' and BadTurns and the last location in our path
			* if 'E' is in our view
			  * turn towards it (no cost if turn is our current direction)
			  * Move()
			  * return (HURRAY!)
			* if there are no '.' in our view, we are on a dead-end.
			  * Move back to last turning - our score will be corrected, and
			    the bad turning decision recorded
			  * continue
			* If there are at least one '.' in our view, it is an opening to move to
			    * we assume that we are at a turning point, and move in the direction
				  of the '.'. If the direction of the '.' is our current direction,
				  the turn is not recorded (d.Turn() is no-op)
				* Move(), continue
		*/
		view := d.Location.LookAround()
		openings := []rune{}
		lookDirection:
		for direction, mapSymbol := range view {
			// ignore our last position
			pos := Coord{(d.Location.X + Moves[direction].X), (d.Location.Y + Moves[direction].Y)}
			if pos == d.LastPosition(){
				continue
			}
			// if we see the End, move to it and return
			if mapSymbol == 'E' {
				d.Turn(direction)
				d.Move()
				return
			}
			// if the current location has bad turns, ignore those directions
			BadTurnMtx.Lock()
			badTurnsHere := BadTurns[d.Location]
			BadTurnMtx.Unlock()
			for _, badDirection := range badTurnsHere {
				if direction == badDirection{
					continue lookDirection
				}
			}
			// what remains are possible moves
			if mapSymbol == '.' || mapSymbol == 'S' {
				if direction == d.Direction {
					// if the direction is our current direction, make it
					// the first in the list (preferenced move)
					openings = append([]rune{direction}, openings...)
				}else{
					openings = append(openings,direction)
				}
			}
		}
		// Dead-end
		if len(openings) == 0 {
			d.BackToLastTurn()
			continue
		}
		// if the direciton is the current direction, there is no score change
		d.Turn(openings[0])
		d.Move()
	}
}




// Turns defines available turns and costs
// available to any currently-facing direction
// Directions are cardinal (map) directions, not
// reltaive to the direction the Deer if facing
var Turns = map[rune]map[rune]int{
	Up:{Left:OneTurn,Right:OneTurn, Down:2*OneTurn},
	Left:{Up:OneTurn,Down:OneTurn, Right:2*OneTurn},
	Down:{Left:OneTurn,Right:OneTurn, Up:2*OneTurn},
	Right:{Up:OneTurn,Down:OneTurn, Left:2*OneTurn},
}


//
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
			location :=Coord{x,y}
			MAP[location] = r
			if r == 'E' || r=='S' {
				SPECIAL[r]=location
			}
			// track the last location as M for max
			SPECIAL[MaxCoords]=location
		}
	}

	wg := &sync.WaitGroup{}
	wg.Add(2)
	racers := []*Deer{}
	for direction, view := range SPECIAL['S'].LookAround(){
		if view == '.' {
			newRacer := NewDeer(string(direction), SPECIAL['S'])
			newRacer.Location = SPECIAL['S']
			if direction != newRacer.Direction{
				newRacer.Turn(direction)
			}
			racers = append(racers, newRacer)
		}
	}
	for _, racer := range racers {
		go racer.Race(wg)
	}
	wg.Wait()
	var winner *Deer
	for _, racer := range racers {
		if winner == nil {
			winner = racer
		}
		if racer.Score < winner.Score {
			winner = racer
		}
		fmt.Printf("racer %s got score %d\n", racer.Name, racer.Score)
	}
	fmt.Printf("racer %s is the winner\n", winner.Name)

	for _,location := range winner.Path {
		MAP[location] = '*'
	}
	for y := range SPECIAL[MaxCoords].Y+1{
		for x := range SPECIAL[MaxCoords].X+1{
			fmt.Print(string(MAP[Coord{x,y}]))
		}
		fmt.Println()
	}
	for _, loc := range winner.Path{
		fmt.Printf("%d, %d  ", loc.X, loc.Y)
	}
	fmt.Println(len(winner.Path))

}