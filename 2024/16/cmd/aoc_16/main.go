package main

import (
	"fmt"
	"os"
	"strings"
	"sync"
	"time"
)

type Coord struct {
	X int
	Y int
}

func (c Coord)To(direction rune) (Coord) {
	return Coord{c.X + Moves[direction].X, c.Y+Moves[direction].Y}
}

const Up = 'U'
const Down = 'D'
const Left = 'L'
const Right = 'R'
const MaxCoords = 'M'
const Wall = '#'
const Space = '.'
const Start = 'S'
const End = 'E'
const OneTurn = 1000


// Moves maps movement vectors to runes
var Moves = map[rune]Coord{
	Up:{0,-1},
	Down:{0,1},
	Left: {-1,0},
	Right: {1,0},
}
func (c Coord)LookAround()(seenObjects map[rune][]rune){
	// returns the mapping of runes in the cardinal
	// directions to the current coordinant
	// Because the map has walls, we will not look beyond the map
		seenObjects = map[rune][]rune{Space:{}}
		view := map[rune]rune{
			Up: MAP[c.To(Up)],
			Down: MAP[c.To(Down)],
			Left: MAP[c.To(Left)],
			Right: MAP[c.To(Right)],
		}
		for k,v := range view {
			if v == Space || v == End {
				seenObjects[Space]=append(seenObjects[Space],k)
			}
		}
	return
}

type Turning struct {
	Location Coord
	InitialDirection rune
	TriedDirection rune
}

// Mutex to allow multiple Deer access the BadTurns
var BadTurnMtx = &sync.Mutex{}
// BadTurns are turnings that lead to dead-ends
// the rune refers to the Move vector
var BadTurns = map[Coord][]rune{}

type Deer struct {
	Name string
	Location Coord
	PreviousLocation Coord
	Direction rune
	Path map[Coord] int
	Turns []Turning // a stack
	Score int
}

func NewDeer(name string, startPosition Coord)*Deer{
	return &Deer{Name:name, Location:startPosition, Direction: Right ,
		Turns:[]Turning{{startPosition, Right, Right}},
		Path:map[Coord]int{startPosition:0}}
}

func (d *Deer)Clone(newDirection rune)(nd *Deer){
	t := []Turning{}
	t = append(t,d.Turns...)
	p := map[Coord]int{}
	for k,v := range d.Path{
		p[k] = v
	}
	s := d.Score + OneTurn
	t = append([]Turning{{d.Location, d.Direction, newDirection}}, t...)
	nd = &Deer{Name:d.Name+string(newDirection), Location:d.Location, PreviousLocation: d.PreviousLocation, Direction:newDirection, Path:p, Turns: t, Score: s}
	//fmt.Printf("%s cloned to %s at %d, %d\n",d.Name, nd.Name, d.Location.X, d.Location.Y)
	return
}

func (d *Deer)Move(){
	d.PreviousLocation = d.Location
	d.Location = d.Location.To(d.Direction)
	//fmt.Printf("%s moves to %d,%d\n", d.Name, d.Location.X, d.Location.Y)
	d.Path[d.Location] = len(d.Path)
	d.Score += 1
}

func (d *Deer)Race(finishedRacers chan *Deer, joinTheRace chan *Deer, wg *sync.WaitGroup){
	/*
	*/
	defer wg.Done()
	time.Sleep(600 * time.Millisecond)
	for {
		/*
		The race starts on a Turning location, but we don't know that
		yet.
			* If we are on the End, send the deer's pointer on the finishedRacers Channel and return from race
			* Look around.  Exclude '#' and BadTurns and the last location in our path
			   * exclude our PriorLocation and any known bad locations, and any locations in our Path (to prevent looping)
			   * if there are no '.' in our view, we are on a dead-end, so resign
			   * if there are '.' in our view but in a new direction, clone a new deer to explore that path and move there
			   * if there is a '.' in our view in our direction, move there
			* if there are no valid moves or turns, resign
		*/
		if MAP[d.Location] == End || (d.Location.X == SPECIAL[End].X && d.Location.Y == SPECIAL[End].Y ){
			finishedRacers <- d
			fmt.Printf("%s reached the end with score %d!!!\n",d.Name, d.Score)
			return
		}
		view := d.Location.LookAround()
		// if the current location has bad turns, build a set (map[direction rune]bool true)
		BadTurnMtx.Lock()
		badTurnsHere := map[rune]bool{}
		for _, dir := range BadTurns[d.Location]{
			badTurnsHere[dir]=true
		}
		BadTurnMtx.Unlock()

		openings := []rune{}
		for _, direction := range view[Space] {
			// ignore our last position and bad turns
			newPos := d.Location.To(direction)
 			_, beenThere := d.Path[newPos]
			if newPos == d.PreviousLocation || badTurnsHere[direction] || beenThere {
				continue
			}else{
				openings = append(openings,direction)
			}
		}
		// Dead-end
		if len(openings) == 0 {
			// mark the last turning in this direction as bad
			// end this racer
			lastTurn := d.Turns[0]
			BadTurnMtx.Lock()
			if BadTurns[lastTurn.Location] != nil {
				BadTurns[d.Location] = append(BadTurns[d.Location], lastTurn.TriedDirection)
			}else{
				BadTurns[d.Location] = []rune{d.Turns[0].TriedDirection}
			}
			BadTurnMtx.Unlock()
			fmt.Printf("%s found dead-end at %d,%d and resigns\n",d.Name, d.Location.X, d.Location.Y)
			d.Path = nil
			d.Turns = nil
			d.Name=""
			return
		}
		doMove := false
		for _, direction := range openings{
			// for any forks or changes in directions, we spawn a new deer by
			// cloning this one.  The change in direction incurs a turn cost.
			// if we are capable of continuing in our original direction, we
			// do that after spawning clones.
			if direction != d.Direction {
				nd := d.Clone(direction)
				nd.Move()
				wg.Add(1)
				joinTheRace <- nd
			}else {
				doMove = true
			}
		}
		if doMove {
			// if the direciton is the current direction, there is no score change
			d.Name = d.Name + "M"
			//time.Sleep(100 * time.Microsecond)
			d.Move()
		} else {
			// cannot move in the same direction, and have cloned new deer for changes
			// in direction.  We have not made it to the finish, so there is nothing left
			// to do but resign the race
			fmt.Printf("%s has no good turns and cannot move forawards at %d,%d and resigns\n",d.Name, d.Location.X, d.Location.Y)
			d.Path = nil
			d.Turns = nil
			d.Name=""
			return
		}
	}
}

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
			location := Coord{x,y}
			MAP[location] = r
			if r == Start || r == End {
				//fmt.Printf("SPECIAL %s at %d,%d\n",string(r), location.X,location.Y)
				SPECIAL[r]=location
			}
			// track the last location as M for max
			SPECIAL[MaxCoords]=location
		}
	}

	finishedRacers := make(chan *Deer, 100)
	joinTheRace := make(chan *Deer, 1000)
	nextStep := make(chan bool)
	waitGroup := &sync.WaitGroup{}


	go func(wg *sync.WaitGroup, raceQueue chan *Deer, next chan bool){
		fmt.Println("waiting for deer to join the race")
		close(next)
		for deer := range raceQueue{
			go deer.Race(finishedRacers, raceQueue, wg)
			fmt.Printf("%s joined the race\n",deer.Name)
		}
		fmt.Println("joinTheRace is closed")
	}(waitGroup, joinTheRace, nextStep)

	waitGroup.Add(1)
	joinTheRace <- NewDeer(string(Start), SPECIAL[Start])
	<- nextStep
	nextStep = make(chan bool)

	go func(wg *sync.WaitGroup, join, finished chan *Deer, next chan bool){
		wg.Wait()
		close(next)
		close(finished)
		close(join)
	}(waitGroup, joinTheRace, finishedRacers, nextStep)

	var winner *Deer
	go func(){
		processing:
		for {
			select {
			case racer := <- finishedRacers:
				fmt.Printf("racer %s got score %d\n", racer.Name, racer.Score)
				if winner == nil {
					winner = racer
				}else{
					if racer.Score < winner.Score {
						fmt.Printf("so far, racer %s score %d is the best\n", racer.Name, racer.Score)
						winner = racer
					}
				}
			case <- nextStep:
				break processing
			}
		}

	}()
	<- nextStep
	if winner != nil {
		fmt.Printf("racer %s is the Winner with score of %d\n", winner.Name, winner.Score)
		for location := range winner.Path {
			MAP[location] = '*'
		}
		for y := range SPECIAL[MaxCoords].Y+1{
			for x := range SPECIAL[MaxCoords].X+1{
				fmt.Print(string(MAP[Coord{x,y}]))
			}
			fmt.Println()
		}
		for loc := range winner.Path{
			fmt.Printf("%d, %d  ", loc.X, loc.Y)
		}
		fmt.Println(len(winner.Path))
	}else {
		fmt.Println("No Winner Found")
	}
	fmt.Println(BadTurns)
}