package utils

import "fmt"



type Coord struct {
	X int
	Y int
}

/*
To find the opposite of a direction, add 2 and % 4
To find the turns, add +1 or -1 and % 4
*/
const (	East = iota
		North
	  	West
	   	South
		)


var Symbols =[]rune {
	East: '>',
	North: '^',
	West:'<',
	South: 'V',
}


func (c Coord)To(direction int) (Coord) {
	return Coord{c.X + Moves[direction].X, c.Y+Moves[direction].Y}
}

func (c Coord)String()string{
	return fmt.Sprintf("{%d,%d}", c.X, c.Y)
}

type Vector struct {
	Point Coord
	Direction rune
}

func (v Vector) String() string {
	return fmt.Sprintf("%s,%s",v.Point, string(v.Direction))
}

// Moves maps movement vectors to runes
var Moves = map[int]Coord{
	North:{0,-1},
	South:{0,1},
	West: {-1,0},
	East: {1,0},
}