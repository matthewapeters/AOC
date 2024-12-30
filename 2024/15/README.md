# Day 15 Notes

## Part 1

This is a fairly simple OO problem.  I did not optomize in any way: information is duplicated in the
FloorMap (overall state record) and indexes for Walls and Boxes.  The problem of moving adjacent
boxes is handled through recursion.

## Part 2 (before solving)

This looks like part 1 but everything except the robot is twice as wide: 

- If the tile is `#`, the new map contains `##` instead.
- If the tile is `O`, the new map contains `[]` instead.
- If the tile is `.`, the new map contains `..` instead.
- If the tile is `@`, the new map contains `@.` instead.

This makes the mapping of physical space to objects 1/2:1
or, conversely, the mapping of objects to space 2:1 (except the robot).

In the first part, I could index each object by its location.  But in part 2,
objects, other than the robot, occupy 2 locations.

This might not be too difficult, it means that walls and boxes need TWO GPS coordinates
to track and move.  If the robot wants to move one part of a box, both parts need to 
move. The recursive movement logic requires that both parts of the box be capable of moving
to return true.

there is also a change to the Coordinate logic.  We will need to track the horizontal middle of 
the floor to determine what side of the room the box is on for determining how close it is to 
its nearest wall (left or right).  

My thinking is that Boxes will contain two entries for each box, and each Box will hold two GPS
Coordinates.  Walls will also contain two entries for each wall block.  I think Walls can retain
single GPS coordinates.

