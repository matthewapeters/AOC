package main

import (
	"fmt"
	"os"
	"strings"
	"sync"
	"unicode"
)

type Coordinant struct {
	X int
	Y int
}
type Region struct {
	RegionType rune
	Coordinates []Coordinant
	FenceLength int
	Corners map[Coordinant]int
}

func (r *Region)String()(string){
	return fmt.Sprintf("%s: Area: %d, FenceLength: %d  Sides: %d Price: $%d  Coords: %s",
		string(r.RegionType), r.Area(), r.FenceLength, r.Perimeter(), r.Price(), r.Coordinates)
}

func (r *Region)Area()int {
	return len(r.Coordinates)
}

func (r *Region)Price()int {
	// price for part 1
	// return r.Area() * r.FenceLength
	// Price for part 2
	return r.Area() * r.Perimeter()
}

func (r *Region)Perimeter()(p int) {
	// the number of sides matches the number of corners
	for _,count := range r.Corners {
		p += count
	}
	return
}


var MrMtx = &sync.Mutex{}
var MappedRegions map[rune] []*Region =map[rune][]*Region {}

func FmtMappedRegion(mr *map[rune][]*Region) (output string) {
	for k,v := range (*mr) {
		for _, reg := range v{
			output += fmt.Sprintf("%s: %s\n", string(k), reg)
		}
	}
	return
}

func FmtGroundMap(gm *[][]rune)(output string) {
	for _,row := range (*gm){
		output += "["
		for _, r := range row {
			output += string(r)
		}
		output += "]\n"
	}
	return
}

var UP = Coordinant{0,-1}
var DOWN = Coordinant{0,1}
var RIGHT= Coordinant{1,0}
var LEFT = Coordinant{-1,0}

// Movements describes a clock-wise sequence of movements
var Movements []Coordinant = []Coordinant{ RIGHT, DOWN, LEFT, UP }

func (c Coordinant) String()(string) {
	return fmt.Sprintf("{X:%d, Y:%d}",c.X, c.Y)
}

func CountCorners(r rune, c Coordinant, groundMap *[][]rune) (corners int) {
	/*
	Check the number of corners this cell has:
		Convex:
			if the cell above and to the right do not match the rune, it has
			a convex corner to the upper-right
		Concave:
			if the cell above and to the right match, but the upper-right
			does not, we have a concave corner

	*/
	maxX := len((*groundMap)[0])
	maxY := len((*groundMap))

	// convex corner check
	matchUp := false
	matchRight := false
	matchDown := false
	matchLeft := false

	up := Coordinant{(c.X+UP.X), (c.Y + UP.Y)}
	if up.Y<0 {
		matchUp=false
	}else {
		matchUp = unicode.ToUpper((*groundMap)[up.Y][up.X]) == r
	}
	right := Coordinant{c.X+RIGHT.X, c.Y+RIGHT.Y}
	if right.X >=maxX {
		matchRight=false
	}else {
		matchRight = unicode.ToUpper((*groundMap)[right.Y][right.X]) == r
	}
	down := Coordinant{c.X+DOWN.X, c.Y+DOWN.Y}
	if down.Y >= maxY {
		matchDown = false
	} else {
		matchDown = unicode.ToUpper((*groundMap)[down.Y][down.X]) == r
	}
	left := Coordinant{c.X+LEFT.X, c.Y+LEFT.Y}
	if left.X < 0 {
		matchLeft = false
	} else {
		matchLeft = unicode.ToUpper((*groundMap)[left.Y][left.X]) == r
	}
	if ! matchUp && ! matchRight {
		corners ++
	}
	if ! matchUp && ! matchLeft {
		corners ++
	}
	if ! matchDown && ! matchRight {
		corners ++
	}
	if ! matchDown && ! matchLeft {
		corners ++
	}
	// concave corner check

	upperRight := Coordinant{c.X+UP.X+RIGHT.X, c.Y+UP.Y+RIGHT.Y}
	lowerRight := Coordinant{c.X+DOWN.X+RIGHT.X, c.Y+DOWN.Y+RIGHT.Y}
	upperLeft:= Coordinant{c.X+UP.X+LEFT.X, c.Y+UP.Y+LEFT.Y}
	lowerLeft:= Coordinant{c.X+DOWN.X+LEFT.X, c.Y+DOWN.Y+LEFT.Y}
	// upperRight must be on the groundMap if there might be a concave corner
	if upperRight.X<maxX && upperRight.Y>=0 {
		if unicode.ToUpper((*groundMap)[upperRight.Y][upperRight.X]) != r && matchUp && matchRight {
			corners ++
		}
	}
	if upperLeft.X>=0 && upperLeft.Y>=0 {
		if unicode.ToUpper((*groundMap)[upperLeft.Y][upperLeft.X]) != r && matchUp && matchLeft {
			corners ++
		}
	}

	if lowerRight.X<maxX && lowerRight.Y<maxY {
		if unicode.ToUpper((*groundMap)[lowerRight.Y][lowerRight.X]) != r && matchDown && matchRight {
			corners ++
		}
	}
	if lowerLeft.X>=0 && lowerLeft.Y<maxY {
		if unicode.ToUpper((*groundMap)[lowerLeft.Y][lowerLeft.X]) != r && matchDown && matchLeft {
			corners ++
		}
	}

	return
}


func MapRegions(x,y int, r rune, groundMap *[][]rune, region *Region) {
	var fenceLength int
	coord := Coordinant{x,y}

	MrMtx.Lock()
	if region == nil {
		region = &Region{}
		region.RegionType = r
		region.Corners = map[Coordinant]int{}
		region.Coordinates = []Coordinant{coord}
		MappedRegions[r] = append(MappedRegions[r], region)
	} else {
		region.Coordinates = append(region.Coordinates, coord)
	}
	(*groundMap)[y][x] = unicode.ToLower(r)
	corners := CountCorners(r, coord, groundMap)
	if corners>0 {
		region.Corners[coord]=corners
	}
	MrMtx.Unlock()

	for _, surround := range Movements {
		nextX := x + surround.X
		nextY := y + surround.Y
		//fmt.Printf("checking %d, %d for %s\n", nextX, nextY, string(r))
		MrMtx.Lock()
		checkNext := (nextX >= 0) && (nextX < len((*groundMap)[0])) && (nextY >= 0) && (nextY < len(*groundMap))
		isMatch := false
		isLowerMatch := false
		if checkNext {
			isMatch =(*groundMap)[nextY][nextX] == r
			isLowerMatch = unicode.ToLower(r) == (*groundMap)[nextY][nextX]
		}
		MrMtx.Unlock()
		if checkNext {
			if isMatch{
				// matching rune means it is part of the same region
				MapRegions(nextX, nextY, r, groundMap, region)
			} else {
				if ! isLowerMatch {
					fenceLength += 1
				}
		}
		} else {
			fenceLength += 1
		}
	}
	if fenceLength < 0 {
		fmt.Printf("how did we get a fenceLength of %d at %d,%d?\n", fenceLength, x, y)
	} else {
		MrMtx.Lock()
		region.FenceLength += fenceLength
		MrMtx.Unlock()
	}
}


func main(){
	source_file := os.Args[1]
	fmt.Printf("reading source file %s\n", source_file)
	raw, err := os.ReadFile(source_file)
	if err != nil{
		fmt.Print(err)
		return
	}
	d1 :=strings.Split(string(raw), "\n")
	var data [][]rune = [][]rune{}
	for i, row := range  d1 {
		if row == "" {
			continue
		}
		data = append(data, []rune{})
		for _, value := range row {
			data[i] = append(data[i], value)
		}
	}

	// identify regions of the map
	for y, row := range data {
		for x, r := range row {
			// only map regions where the rune is uppercase
			if unicode.IsUpper(r) {
				MapRegions(x,y,r, &data, nil)
			}
		}
	}

	fmt.Println(FmtGroundMap(&data))
	fmt.Print(FmtMappedRegion(&MappedRegions))
	totalPrice := 0
	for _,v := range MappedRegions{
		for _, reg := range v {
			totalPrice += reg.Price()
		}
	}
	fmt.Printf("The final Price of Fencing is $%d\n", totalPrice)
}