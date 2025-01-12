# Day 16 - Reindeer Races

My initial approach, which is to create a "forking" solution to traverse the map,
worked well for small maps.  The input.txt map is too large, with too many branches
for this solution: the solution just consumed all of the RAM.  Each simulated deer
kept is own score and path, and copied these with each fork.  Each deer ended if it
could not move in its current direction, and each fork (new direction) incurred a turn
fee of 1000 points. The number of duplicated data points for common path history is just
too wasteful.

Looking at Reddit for discussion, I came accross [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm),
which I did not know by name.  I also came across the term "Prioritized Queue" which is implemented in Go with the [`heap`](https://pkg.go.dev/container/heap) package from the common library.

 These pieces point to a change in solution direction:

## Prioritized Queue

A Prioritized Queue uses a heap for sorting items.  The sorting is performed using a cost and priority.  The interface implements Push, Pop, and Swap methods.  The heap is essentially a slice of items, which
are re-ordered using the elements' `Priority` property (think cost or score).  The heap is either a Minimized or Maximized flavor, indicating the direction of the sort.

There are no simulated deer in this approach.  We use a minimum priority queue instead to hold those nodes we wish to visit.  

The queue starts empty, and we start the search by pushing the starting position to it with a cuumulative cost of 0 and direction, representing our current-facing direction.

```txt
while the queue is not empty, we pop the minimum element from it
    add the cell to the map of visisted cells
    if the cell is the end cell, return the cost
    look around the cell - get the neighbor cells
      ignore walls and visited cells
      if the cell is in the same direction, push the cell, its direction, and the current current cell's cost + 1 to the queue
      else push the cell, its direction and the current cells cost + 1001 to the queue

the queue is empty, return nothing
```

This solution does not fork.  
Using the cuumulative cost prioritizes exploring the cheapest move first.
