package main

import (
	"fmt"
	"math"
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

func (r *Robot)Move(n int, floorSize Coord){
	extendendVector := Coord{r.Vector.X*n%floorSize.X, r.Vector.Y*n%floorSize.Y}
	newPos := Coord{X:(r.Position.X + extendendVector.X+floorSize.X)%floorSize.X, Y:(r.Position.Y + extendendVector.Y+floorSize.Y)%floorSize.Y}
	r.Position = newPos

	midX := int(math.Ceil(float64(floorSize.X)/2.0)) -1
	midY := int(math.Ceil(float64(floorSize.Y)/2.0)) -1
	quadX := -1
	quadY := -1
	var quadrant *Coord
	if r.Position.X<midX{
		quadX = 0
	}
	if r.Position.X > midX {
		quadX = 1
	}
	if r.Position.Y <midY{
		quadY = 0
	}
	if r.Position.Y>midY {
		quadY = 1
	}
	if quadX>=0 && quadY >=0 {
		quadrant = &Coord{quadX, quadY}
	}
	r.Quadrant = quadrant
}


func main() {
	fileName := os.Args[1]
	moves, err := strconv.Atoi(os.Args[2])
	if err != nil {
		fmt.Printf("ERROR: %s",err)
		return
	}
	raw, err := os.ReadFile(fileName+".txt")
	if err != nil {
		fmt.Printf("ERROR: %s\n",err)
		return
	}
	dataRows := strings.Split(strings.Trim(string(raw),"\n"), "\n")

	raw, err = os.ReadFile(fileName + "_floor.txt")
	if err != nil {
		fmt.Printf("ERROR: %s\n",err)
		return
	}
	floorDimsRaw := strings.Split(strings.Trim(string(raw),"\n")," ")
	x,err := strconv.Atoi(floorDimsRaw[0])
	if err != nil {
		fmt.Printf("ERROR CONVERTING FLOR DIMS: %s", err)
		return
	}
	y,err := strconv.Atoi(floorDimsRaw[1])
	if err != nil {
		fmt.Printf("ERROR CONVERTING FLOR DIMS: %s", err)
		return
	}
	Robots := []*Robot{}
	floorLayout := map[Coord]int{}
	for _,i := range dataRows {
		r := NewRobot(i)
		Robots = append(Robots, r)
	}

	floorDims := Coord{x,y}
	// divide the floor into quadrants:
	// {0,0}, {0,1}, {1,0}, {1,1}
	// by dividing the floor in 2 in each dimension
	floorQuadrants := map[Coord]int{{0,0}:0, {0,1}:0, {1,0}:0, {1,1}:0}
	midX := int(math.Ceil(float64(floorDims.X)/2.0)) -1
	midY := int(math.Ceil(float64(floorDims.Y)/2.0)) -1

	for _,r := range Robots{
		r.Move(moves, floorDims)
		floorLayout[r.Position] += 1
		if r.Quadrant != nil {
			floorQuadrants[*r.Quadrant] += 1
		}
	}
	safetyFactor := 1
	for _,c := range floorQuadrants {
		safetyFactor = safetyFactor * c
	}

	fmt.Printf("floor dims are: %s\n", floorDims)
	fmt.Printf("quad dividers are X: %d and Y: %d\n", midX, midY)
	fmt.Printf("there are %d robots\n", len(Robots))
	fmt.Printf("results after %d moves\n",moves)
	fmt.Printf("Robots: %s\n",Robots)
	fmt.Printf("floorLayout:\n%s\n",floorLayout)
	fmt.Printf("Quadrant Distribution: %s\n", floorQuadrants)
	fmt.Printf("THE SAFETY FACTOR IS %d\n", safetyFactor)

	for y := range floorDims.Y {
		for x := range floorDims.X {
			if floorLayout[Coord{x,y}] == 0 {
				fmt.Print(".")
			}else{
				fmt.Print(floorLayout[Coord{x,y}])
			}
		}
		fmt.Println()
	}
}