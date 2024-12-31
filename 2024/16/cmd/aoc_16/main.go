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

type Turning struct {
	Location Coord
	InitialDirection rune
	TurnDirection rune
}

type Deer struct {
	Location Coord
	Direction rune
	Path []*Coord
	Turns []Turning
	Score int
}

func (d *Deer)Turn(turnDirection rune){
	// changes the Deer's direction, and increase
	// its score appropriately.
	if d.Turns == nil {
		d.Turns = []Turning{}
	}
	d.Turns = append(d.Turns, Turning{d.Location, d.Direction, turnDirection})
	d.Direction = turnDirection
	d.Score += Turns[d.Direction][turnDirection]
}

func (d *Deer)Move(){
	d.Location = Coord{
		d.Location.X + Moves[d.Direction].X,
		d.Location.Y + Moves[d.Direction].Y}
	d.Score += 1
}

func (d *Deer)BackToLastTurn(){
	lastTurning := d.Turns[len(d.Turns)-1]
	reverseDirection := Coord{Moves[d.Direction].X * -1, Moves[d.Direction].Y * -1}
	for {
		// if we are back to the last turning, break out of this loop
		if d.Location == lastTurning.Location{
			break
		}
		d.Location = Coord{d.Location.X + reverseDirection.X, d.Location.Y+reverseDirection.Y}
		// back out the score for the move
		d.Score --
	}
	d.Direction = lastTurning.InitialDirection
	// back out the score for the turn
	d.Score -= Turns[lastTurning.InitialDirection][lastTurning.TurnDirection]
	BadTurnMtx.Lock()
	defer BadTurnMtx.Unlock()
	BadTurns[d.Location] = lastTurning.TurnDirection
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

// Turns defines available 90-degree turns
// available to any currently-facing
// direction
var Turns = map[rune]map[rune]int{
	Up:{Left:OneTurn,Right:OneTurn, Down:2*OneTurn},
	Left:{Up:OneTurn,Down:OneTurn, Right:2*OneTurn},
	Down:{Left:OneTurn,Right:OneTurn, Up:2*OneTurn},
	Right:{Up:OneTurn,Down:OneTurn, Left:2*OneTurn},
}
var BadTurnMtx = &sync.Mutex{}
// BadTurns are turnings that lead to dead-ends
// the rune refers to the Move vector
var BadTurns = map[Coord]rune{}

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

}