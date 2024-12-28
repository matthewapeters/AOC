package main

/**

Add 10000000000000 to both prize coordinates
*/

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Button struct {
	DeltaX int
	DeltaY int
	Name rune
	Cost int
}

func (b *Button)String()(str string) {
	str = fmt.Sprintf("%s (%d coins): dX:%d, dy:%d ",string(b.Name),b.Cost, b.DeltaX, b.DeltaY)
	return
}


type ClawMachine struct {
	PrizeX int
	PrizeY int
	A *Button
	B *Button
	Determinate float64
	ACount int
	BCount int
	Cost int
}

func NewClawMachine(inputs []string)(cm *ClawMachine, err error) {
	/**
	Sample inputs:
    [
	"Button A: X+23, Y+97",
	"Button B: X+93, Y+12",
	"Prize: X=6993, Y=2877",
	"\n",
	]

	PART 2 - add 10000000000000 to each Prize Coordinate

	*/
	// remove the label, split on comma

	prizeOffset := 10000000000000

	if len(inputs) != 4 {
		fmt.Println("ERROR: expected 4 lines for input")
		return nil, err
	}
	bAstr := strings.Split(strings.Split(inputs[0],":")[1],",")
	bBstr := strings.Split(strings.Split(inputs[1],":")[1],",")
	pStr := strings.Split(strings.Split(inputs[2],":")[1],",")

	// configure button A
	A := &Button{Name:'A', Cost:3}
	aX,err := strconv.Atoi(strings.Split((bAstr[0]),"+")[1])
	if err != nil {
		fmt.Printf("ERROR: %s\n",err)
		fmt.Print(inputs)
		return nil, err
	}
	A.DeltaX = aX
	aY,err := strconv.Atoi(strings.Split((bAstr[1]),"+")[1])
	if err != nil {
		fmt.Printf("ERROR: %s\n",err)
		fmt.Print(inputs)
		return nil, err
	}
	A.DeltaY = aY

	// configure button B
	B := &Button{Name:'B', Cost:1}
	bX,err := strconv.Atoi(strings.Split((bBstr[0]),"+")[1])
	if err != nil {
		fmt.Printf("ERROR: %s\n",err)
		fmt.Print(inputs)
		return
	}
	B.DeltaX = bX
	bY,err := strconv.Atoi(strings.Split((bBstr[1]),"+")[1])
	if err != nil {
		fmt.Printf("ERROR: %s\n",err)
		fmt.Print(inputs)
		return
	}
	B.DeltaY = bY
	// configure Prize

	pX,err := strconv.Atoi(strings.Split((pStr[0]),"=")[1])
	if err != nil {
		fmt.Printf("ERROR: %s\n",err)
		fmt.Print(inputs)
		return
	}
	pX += prizeOffset
	pY,err := strconv.Atoi(strings.Split((pStr[1]),"=")[1])
	if err != nil {
		fmt.Printf("ERROR: %s\n",err)
		fmt.Print(inputs)
		return
	}
	pY += prizeOffset
	determinate :=(float64(A.DeltaX)* float64(B.DeltaY)) - (float64(A.DeltaY)*float64(B.DeltaX))
	if determinate == 0 {
		err = fmt.Errorf(("determinate is 0"))
		return
	}
	ac :=(float64(pX*B.DeltaY) - float64(pY*B.DeltaX))/determinate
	bc :=(float64(pY*A.DeltaX) - float64(pX*A.DeltaY))/determinate
	if float64(int(ac)) != ac {
		ac=0
	}
	if float64(int(bc)) != bc {
		bc = 0
	}
	cost := 0.0
	if ac>0 && bc>0 {
		cost =ac*float64(A.Cost) + bc*float64(B.Cost)
		if float64(int(cost)) !=  cost {
			cost = 0.0
		}
	}
	cm = &ClawMachine{
		A:A,
		B:B,
		PrizeX: pX,
		PrizeY: pY,
		Determinate: determinate,
		ACount: int(ac),
		BCount: int(bc),
		Cost: int(cost),
	}
	return
}

func (cm *ClawMachine)String()(string) {
	return fmt.Sprintf("Buttons: {%s, %s} Pize: (%d,%d) Presses: A: %d  B: %d  Cost: %d",cm.A, cm.B, cm.PrizeX, cm.PrizeY, cm.ACount, cm.BCount, cm.Cost)
}


func main() {
	fileName := os.Args[1]

	raw, err := os.ReadFile(fileName)
	if err != nil {
		fmt.Printf("ERROR: %s",err)
		return
	}
	data := strings.Split(string(raw),"\n")
	if len(data) % 4 != 0 {
		fmt.Printf("data length not multiple of 4 (%d)\n", len(data))
	}
	var clawMachines = []*ClawMachine{}
	for i:=0; i<len(data); i+=4 {
		cm, err := NewClawMachine(data[i:i+4])
		if err != nil {
			fmt.Printf("ERROR: %s\n", err)
			return
		}else{
			clawMachines = append(clawMachines, cm)
		}

	}
	totalCost := 0
	for _, cm := range clawMachines {
		fmt.Println(cm)
		totalCost += cm.Cost
	}
	fmt.Printf("the final cost is %d",totalCost)

}