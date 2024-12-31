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
	GPS [2]Coord
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

func CoordToGPS(c [2]Coord, maxX int)int{
	// The GPS coordinate system is 0-indexed,
	// so the upper-left wall corner (X=0, Y=0)
	// is at y*100 + x = 0*100 + 0 == 0
	vertical := c[0].Y*100
	horizontal := c[0].X
	return vertical + horizontal
}

func GetInventoryGPS(maxX int)( c int){
	// create a set of boxes
	boxList := map[*Box]bool {}
	for _, b := range Boxes {
		boxList[b]=true
	}
	for b := range boxList {
		c += CoordToGPS(b.GPS, maxX)
	}


	return
}

func (box *Box) CanMove(direction rune)(moveable bool) {
	// A box can move if any adjacent boxes can move (and so on)
	newLocation := [2]Coord{box.GPS[0].Move(direction), box.GPS[1].Move(direction)}
	// if either side of the box is blocked by a wall,
	// the box cannot move
	if Walls[newLocation[0]] != nil || Walls[newLocation[1]] != nil {
		return false
	}
	// create a set of adjacent boxes
	// aligned boxes will create only one entry
	// offset boxes can create fan-outs
	boxList := map[*Box]bool{}
	for _, l := range newLocation {
		if Boxes[l] != nil && Boxes[l] != box{
			boxList[Boxes[l]]=true
		}
	}
	moveable = true
	for bx := range boxList{
		if bx != box{
			moveable = moveable && bx.CanMove(direction)
		}
	}
	return
}


func (box *Box) Move(direction rune)bool{
	if ! box.CanMove(direction){
		return false
	}
	oldLocation := box.GPS
	newLocation := [2]Coord{box.GPS[0].Move(direction), box.GPS[1].Move(direction)}
	// create a set of adjacent boxes
	// aligned boxes will create only one entry
	// offset boxes can create fan-outs
	boxList := map[*Box]bool{}
	for _, l := range newLocation {
		if Boxes[l] != nil && Boxes[l] != box{
			boxList[Boxes[l]]=true
		}
	}
	for bx := range boxList{
		if bx != box {
			bx.Move(direction)
		}
	}
	box.GPS = newLocation
	r1 := FloorMap[oldLocation[0]]
	r2 := FloorMap[oldLocation[1]]
	FloorMap[oldLocation[0]]='.'
	FloorMap[oldLocation[1]]='.'
	FloorMap[newLocation[0]]= r1
	FloorMap[newLocation[1]]= r2
	delete(Boxes, oldLocation[0])
	delete(Boxes, oldLocation[1])
	Boxes[newLocation[0]] = box
	Boxes[newLocation[1]] = box
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
			for x_pre,r := range data{
				x := x_pre * 2
				location1 := Coord{x,y}
				location2 := Coord{x+1,y}

				// Add symbol to floor map - this is our state record
				if r == 'O'{
					// Add a Box
					box :=&Box{[2]Coord{location1,location2}}
					Boxes[location1] = box
					Boxes[location2] = box
					FloorMap[location1] = '['
					FloorMap[location2] = ']'
				}
				if r == '#'{
					// Add a Wall
					if x+1>maxX{
						maxX=x+1
					}
					if y>maxY{
						maxY = y
					}
					Walls[location1] =  &Wall{location1}
					Walls[location2] =  &Wall{location2}
					FloorMap[location1] = '#'
					FloorMap[location2] = '#'
				}
				if r == '@' {
					// we found our robot
					robot.GPS = location1
					FloorMap[location1]='@'
					FloorMap[location2]='.'
				}
				if r == '.' {
					FloorMap[location1]='.'
					FloorMap[location2]='.'
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
	fmt.Printf("Inventory GPS: %d\n", GetInventoryGPS(maxX))
}