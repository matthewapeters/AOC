package main

import (
	"fmt"
	"os"
	"strings"
)

type Coord struct {
	X int
	Y int
}

type Box struct {
	GPS Coord
}

type Robot struct {
	GPS Coord
	Moves string
}


func (r *Robot)Move(direction rune){
	oldLocation := r.GPS
	newLocation := r.GPS.Move(direction)
	// Do nothing if we would be moving into a wall
	if Walls[newLocation] != nil{
		return
	}
	if Boxes[newLocation] != nil {
		if ! Boxes[newLocation].Move(direction) {
			return
		}
	}
	r.GPS = newLocation
	FloorMap[oldLocation] = '.'
	FloorMap[newLocation] = '@'
}

type Wall struct {
	GPS Coord
}

func (c Coord)Move(direction rune)(nc Coord){
	nc = Coord{c.X + Moves[direction].X,
			   c.Y + Moves[direction].Y}
	return
}


var FloorMap = map[Coord]rune {}
var Walls = map[Coord]*Wall{}
var Boxes  = map[Coord]*Box{}

// Translates runes to movement vectors
var Moves = map[rune]Coord{
	'^': {0,-1},
	'v': {0,1},
	'>': {1,0},
	'<': {-1,0},
}

func CoordToGPS(c Coord)int{
	// The GPS coordinate system is 0-indexed,
	// so the upper-left wall corner (X=0, Y=0)
	// is at y*100 + x = 0*100 + 0 == 0
	return c.Y*100 + c.X
}

func GetInventoryGPS()( c int){
	for _, b := range Boxes {
		c += CoordToGPS(b.GPS)
	}
	return
}


func (box *Box) Move(direction rune)bool{
	newLocation := box.GPS.Move(direction)
	oldLocation := box.GPS
	if FloorMap[newLocation] == '#'{
		return false
	}
	if FloorMap[newLocation]=='O' && ! Boxes[newLocation].Move(direction){
		return false
	}
	box.GPS = newLocation
	FloorMap[newLocation]='O'
	FloorMap[oldLocation]='.'
	delete(Boxes, oldLocation)
	Boxes[newLocation] = box
	return true
}

func ShowState(maxX, maxY int){
	for y := range maxY+1{
		for x := range maxX+1{
			fmt.Print(string(FloorMap[Coord{x,y}]))
		}
		fmt.Println()
	}
	fmt.Println()
}


func main() {
	fileNameRaw := os.Args[1]

	robot := &Robot{}

	rawInput,err := os.ReadFile((fileNameRaw))
	if err != nil {
		fmt.Printf("ERROR: COULD NOT OPEN FILE %s: %s\n", fileNameRaw, err)
		return
	}
	input := strings.Split(string(rawInput),"\n")
	maxX := 0
	maxY := 0
	for y, data := range input {
		// FloorMap data indicated by "#" in first character of string
		if len(data) == 0 {
			continue
		}

		if data[0] == '#' {
			for x,r := range data{

				location := Coord{x,y}
				// Add symbol to floor map - this is our state record
				FloorMap[location] = r
				if r == 'O'{
					// Add a Box
					Boxes[location] =  &Box{location}
				}
				if r == '#'{
					if x>maxX{
						maxX=x
					}					// Add a Wall
					if y>maxY{
						maxY = y
					}
					Walls[location] =  &Wall{location}
				}
				if r == '@' {
					// we found our robot
					robot.GPS = location
				}
			}

		}else {
			// This is move data
			robot.Moves += data
		}
	}
	fmt.Println("INITIAL STATE")
	//ShowState(maxX, maxY)
	for _,d := range robot.Moves {
		//fmt.Printf("Move %s\n",string(d))
		robot.Move(d)
		//ShowState(maxX, maxY)
		//fmt.Println()
	}
	fmt.Printf("Inventory GPS: %d\n", GetInventoryGPS())
}