PathFinding.js
==============

Initiatives
------------

* We have created a new heuristics which we have provided in the project by the name of Optimized Manhatten. Having tested the heuristic on benchmark, we have managed time reduction by approx 50% in case of Astar algorithm and approx 15% reduction in time in Best First Search. The length of path and number of operations remain unaltered, hence we have not applied greedy algorithm to reduce time and compromise on the optimal path. *

![](images/Astar_manhatten.PNG)
![](images/Astar_optimised_manhatten.PNG)

The first picture shows the results for bench in case of standard manhatten for A star algorithm, when diagonal traversal is set to 'false'. The second shows the execution of new heuristic.

![](images/BFS_manhatten.PNG)
![](images/BFS_optimised_manhatten.PNG)

The first picture shows the results for bench in case of standard manhatten for Best First Search, when diagonal traversal is set to 'false'. The second shows the execution of new heuristic.

* Adding an option of speed in the naivigation bar, the speed with which the rover reaches the space station can be managed. *

Gateway Heuristic
------------

The maze and patterns present in the repository were added to test a new heuristic called the Gateway heuristic. The gateway heuristic pre-calculates the distances between entrances/exits of the areas. It also proceeds in two phases.
Preprocessing Phase:
The map is decomposed into areas in an identical way as for the dead-end heuristic. We define the boundaries between areas as gateways (or gates). A gateway can be of an arbitrary size, but an artifact of our decomposition algorithm is that its orientation is always either horizontal or vertical. Next we use multiple A* searches to pre-calculate the (static) distance between gates. For each gateway we calculate the path distance to all the other gateways (cost of infinity if no path exists). Alternatively, one could calculate only the distances between gateways within each room and then use a small search to accumulate the total cost during run-time. However, our approach results in more accurate heuristic estimates and faster run-time access
