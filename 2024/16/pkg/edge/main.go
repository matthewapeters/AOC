package edge

import (
	"aoc_16/pkg/utils"
	"fmt"
)


type Edge struct {
	Location utils.Coord
	IncomingDirection int
	CuumulativeCost int
	OutGoingDirection int
	Symbol rune
	Index int
	Path []*Edge
}

func (e Edge)String()string{
	return fmt.Sprintf("%s%s%s%s[%d]",
		e.Location,
		string(utils.Symbols[e.IncomingDirection]),
		string(e.Symbol),
		string(utils.Symbols[e.OutGoingDirection]),
		e.CuumulativeCost,
		)
}

func (e Edge)OutVector()utils.Vector{
	return utils.Vector{Point: e.Location, Direction: rune(e.OutGoingDirection)}
}

