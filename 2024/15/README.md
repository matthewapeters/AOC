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
its nearest wall (left or right).  EDIT: THIS APPEARS TO BE A MISSDIRECTION!  The `Boxes` index
will have two references to the same box - we need to reduce it to a set before computing the GPS!

My thinking is that Boxes will contain two entries for each box, and each Box will hold two GPS
Coordinates.  Walls will also contain two entries for each wall block.  I think Walls can retain
single GPS coordinates.

### Issues with recursion

I think I have to differentiate between the ability to move the left side of the box and the right
side of the box.  Trying to move the box based on two coordinates resulted in a stack overflow,
probably because I was recursing indefinitely.

_box.CanMove == box.CanMoveLeft && box.CanMoveRight_

Looking at some scenarios:

```sh
Direction ^:
############
##..........
##...#......
##..[]......
##..@.......
```

box.CanMoveLeft -> true BUT box.CanMoveRight -> false

```sh
Direction ^:
############
##..[]...... <- box C
##...[]..... <- box B
##..[]...... <- box A
##...@......
```

boxA.CanMove == boxB.CanMove == boxC.CanMove == false

```sh
Direction ^:
############
##.[]....... <- box C
##...[]..... <- box B
##..[]...... <- box A
##...@......
```

boxA.CanMove == boxB.CanMove == true

```sh
Direction >:
############
##.[]....... <- box C
##...[]..... <- box B
##..@[]..... <- box A
##..........
```

boxA.Left requires boxA.Right to move first - left side
cannot move because it is blocked by its right side - recursion
could address this, but we have to know what side to move first:

```sh
Direction <:
############
##.[]....... <- box C
##...[]..... <- box B
##...[]@.... <- box A
##..........
```

in this scenario, right requires left to move first.

Since recursion is necessary, at some point we may fan out and one
move will succeed and another will fail - moving the first back is
problematic.  

My solution is to include a CanMove function to validate the movement
train, and then move the boxes.  Also, (found through debugging), we
have to ensure that adjacent boxes are not the same box!

### GPS Coordinates

```sh
0123456789
########## 0
##.[]...## 100
##......## 200
##......##
```

100 + 3

```sh
0123456789
########## 0
##...[].## 100
##......## 200
##......##
```

100 + min(5, 9-6)
103?

Probably not -- the wording "Edge of the map to the closest edge of the box in question"
may only refer to the left edge of the map and the left edge of the box.

Which is a poorly worded statement because there are four edges of the map!  Excluding the
Y coordinates, there are still two edges relevent to the box's X coordinates
