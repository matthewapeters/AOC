package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)


type Coord struct {
	X int
	Y int
}

func (c Coord)String()string {
	return fmt.Sprintf("[%d,%d]",c.X, c.Y)
}

type Robot struct {
	Position Coord
	Vector Coord
	Quadrant *Coord
}

func NewRobot(input string)(r *Robot){
	/**
	Sample Input
		"p=3,0 v=-2,-2"
	*/
	r = &Robot{}
	p0 := strings.Split(input," ")[0]
	v0 :=strings.Split(input," ")[1]
	p0 = strings.Split(p0,"=")[1]
	v0 = strings.Split(v0,"=")[1]
	px, _ := strconv.Atoi(strings.Split(p0,",")[0])
	py, _ := strconv.Atoi(strings.Split(p0,",")[1])
	vx, _ := strconv.Atoi(strings.Split(v0,",")[0])
	vy, _ := strconv.Atoi(strings.Split(v0,",")[1])
	r.Position= Coord{px, py}
	r.Vector = Coord{vx,vy}
	return
}

func (r *Robot)String()string {
	qx := ""
	qy := ""
	if r.Quadrant == nil {
		qx = "-"
		qy = "|"
	}else{
		qx = fmt.Sprintf("%d",r.Quadrant.X)
		qy = fmt.Sprintf("%d",r.Quadrant.Y)
	}
	return fmt.Sprintf("Robot{p=%d,%d v=%d,%d Q=%s,%s}\n", r.Position.X, r.Position.Y, r.Vector.X, r.Vector.Y, qx, qy)
}

func (r *Robot)Move(moves int, floorSize Coord){
	extendendVector := Coord{
		(r.Vector.X*moves)%floorSize.X,
		(r.Vector.Y*moves)%floorSize.Y}
	r.Position = Coord{
		X:(r.Position.X + extendendVector.X+floorSize.X)%floorSize.X,
		Y:(r.Position.Y + extendendVector.Y+floorSize.Y)%floorSize.Y}
}


func GetRobots() (*[]*Robot, *Coord) {
	fileName := os.Args[1]
	raw, err := os.ReadFile(fileName+".txt")
	if err != nil {
		fmt.Printf("ERROR: %s\n",err)
		return nil, nil
	}
	dataRows := strings.Split(strings.Trim(string(raw),"\n"), "\n")

	raw, err = os.ReadFile(fileName + "_floor.txt")
	if err != nil {
		fmt.Printf("ERROR: %s\n",err)
		return nil, nil
	}
	floorDimsRaw := strings.Split(strings.Trim(string(raw),"\n")," ")
	x,err := strconv.Atoi(floorDimsRaw[0])
	if err != nil {
		fmt.Printf("ERROR CONVERTING FLOOR DIMS: %s", err)
		return nil, nil
	}
	y,err := strconv.Atoi(floorDimsRaw[1])
	if err != nil {
		fmt.Printf("ERROR CONVERTING FLOOR DIMS: %s", err)
		return nil, nil
	}
	Robots := []*Robot{}
	for _,i := range dataRows {
		r := NewRobot(i)
		Robots = append(Robots, r)
	}
	floorDims := Coord{x,y}

	return &Robots, &floorDims
}


func MoveN(Robots *[]*Robot, floorLayout *map[Coord]int ,floorDims *Coord, moves int){
	for _,r := range (*Robots){
		r.Move(moves, *floorDims)
		(*floorLayout)[r.Position] += 1
	}
}

func PrintFloor(moves int, floorLayout *map[Coord]int, floorDims *Coord){
	fmt.Println("MOVES: ", moves)
	for y := range floorDims.Y {
		for x := range floorDims.X {
			if (*floorLayout)[Coord{x,y}] == 0 {
				fmt.Print(" ")
			}else{
				fmt.Print("@")
			}
		}
		fmt.Println()
	}
	fmt.Println()
}

func main(){
	startMovesRaw := os.Args[2]
	startMoves, _ := strconv.Atoi(startMovesRaw)
	Robots, floorDims := GetRobots()

	if Robots == nil {
		fmt.Println("ERROR")
		return
	}

	moves := startMoves
	floorLayout := &map[Coord]int{}
	MoveN(Robots, floorLayout, floorDims,moves)
	PrintFloor(moves, floorLayout, floorDims)

	keys := make(chan *string,3)
	go HandleKeystrokes(keys)

	for {
		select {
		case key, open := <- keys:
			if !open {
				return
			}
			if *key == "^" {
				moves += floorDims.X
				floorLayout := &map[Coord]int{}
				MoveN(Robots, floorLayout, floorDims,floorDims.X)
				PrintFloor(moves, floorLayout, floorDims)
				continue
			}
			if *key == ">" {
				moves ++
				floorLayout := &map[Coord]int{}
				MoveN(Robots, floorLayout, floorDims,1)
				PrintFloor(moves, floorLayout, floorDims)
				continue
			}
			if *key == "<" {
				moves --
				floorLayout := &map[Coord]int{}
				MoveN(Robots, floorLayout, floorDims, -1)
				PrintFloor(moves, floorLayout, floorDims)
				continue
			}
		}
	}
}