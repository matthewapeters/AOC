package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

var Mtx = &sync.Mutex{}
var MemoMtx = &sync.Mutex{}
var Changes *map[int64][2]int64 = &map[int64][2]int64{}
var Memo *map[[2]int64]int64  = &map[[2]int64]int64{}


func get_rocks()(rocks []int64){
	/*
	get_rocks()(rocks []int64)
	reads intput.txt, and parses into and returns a slice of int64
	*/
	var raw_data string
	input, err := os.ReadFile("input.txt")
	if err != nil {
		fmt.Printf("Error: %s", err)
		return
	}
	raw_data = string(input)
	for _, i := range strings.Split(strings.Trim(raw_data, "\n"), " "){
		num, err := strconv.ParseInt(i, 10, 64)
		if err != nil {
			fmt.Printf("Error: %s", err)
			return
		}
		rocks = append(rocks, num)
	}
	return
}

func Blink(rock int64)(int64, int64){
	Mtx.Lock()
	output, ok := (*Changes)[rock]
	Mtx.Unlock()

	if ok {
		return output[0],output[1]
	}
	if rock == 0 {
		(*Changes)[rock] = [2]int64{int64(1),-1}
		return int64(1), -1
	}
	if len(fmt.Sprintf("%d",rock)) % 2 == 0 {
		split_at := len(fmt.Sprintf("%d",rock)) / 2
		e1,_ := strconv.ParseInt(fmt.Sprintf("%d", rock)[:split_at],10,64)
		e2,_ := strconv.ParseInt(fmt.Sprintf("%d", rock)[split_at:],10,64)
		(*Changes)[rock] = [2]int64{e1, e2}
		return e1,e2
	}
	(*Changes)[rock] = [2]int64{rock*2024,-1}
	return rock*2024, -1
}

func BlinkALot(rock int64, blinks int64)(int64){
	MemoMtx.Lock()
	cached, ok := (*Memo)[[2]int64{rock, blinks}]
	MemoMtx.Unlock()
	if ok {
		return cached
	}
	leftRock, rightRock := Blink(rock)
	if blinks == 1 {
		if rightRock >= 0 {
			MemoMtx.Lock()
			(*Memo)[[2]int64{rock, blinks}] = 2
			MemoMtx.Unlock()
			return 2
		}else{
			MemoMtx.Lock()
			(*Memo)[[2]int64{rock, blinks}] = 1
			MemoMtx.Unlock()
			return 1
		}
	}
	count := BlinkALot(leftRock, blinks-1)
	if rightRock >= 0 {
		count += BlinkALot(rightRock, blinks-1)
	}
	MemoMtx.Lock()
	(*Memo)[[2]int64{rock, blinks}] = count
	MemoMtx.Unlock()
	return count
}


func main(){
	rocks := get_rocks()
	//rocks = []int64{125,17}
	fmt.Println(rocks)
	var wg sync.WaitGroup = sync.WaitGroup{}
	count := int64(0)
	oldCount := count
	blinks := int64(75)
	for _, rock := range rocks {
		fmt.Println(time.Now())
		fmt.Printf("blink %d times for %d", blinks, rock)
		count += BlinkALot(rock, blinks)
		fmt.Printf(" produces %d rocks\n", count-oldCount)
		oldCount = count
	}
	fmt.Println("Waiting for rocks to finish 75 transformations")
        fmt.Println(time.Now())
	fmt.Printf("final count: %d\n", count)
	wg.Wait()
}
