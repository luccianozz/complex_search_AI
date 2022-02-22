"""
Name: Luciano Zavala
Date: 02/07/22
Assignment: Module 4: Project- Complex Search
Due Date: 01/26/22
About this project: Implement applications that utilize classical Artificial Intelligence techniques, such as
  search algorithms. In this specific code i'm implementing hill climbing search and hill climbing with random
  restarts.
Assumptions:NA
All work below was performed by LZZ
"""
from __future__ import absolute_import
from maze import Maze
from maze_viz import Visualizer
from dataStructures import *
import copy
from astar import *


def RandomSearch(maze):
    row_curr, col_curr = maze.entry_coor  # Where to start searching

    maze.grid[row_curr][col_curr].visited = True
    # Set initial cell to visited

    path = list()
    # To track path of solution and backtracking cells

    exploredNodesPath = list()
    # To track path of solution and backtracking cells

    path.append(((row_curr, col_curr), False))
    exploredNodesPath.append(((row_curr, col_curr), False))

    # Add coordinates to part of search path
    # false indicates not a back tracker visit

    fringe = Queue()  # queue
    fringe.push(path)
    explored = set()

    NumNodesExpanded = 0

    while not (fringe.isEmpty()):
        NumNodesExpanded += 1
        currentPath = fringe.randomPop()
        currentNode = currentPath[len(currentPath) - 1]
        row_curr, col_curr = currentNode[0][0], currentNode[0][1]

        exploredNodesPath.append(((row_curr, col_curr), False))

        maze.grid[row_curr][col_curr].visited = True
        # Move to that neighbour

        if (row_curr, col_curr) == maze.prize_coor_list[0]:
            # print("Expanded ",NumNodesExpanded," nodes.")
            return exploredNodesPath, currentPath

        explored.add((row_curr, col_curr))

        neighbour_indices = maze.find_neighbours(row_curr, col_curr)
        # Find neighbour indices
        neighbour_indices = maze.validate_neighbours_solve(neighbour_indices, row_curr, col_curr)
        if neighbour_indices is not None:
            for NI in neighbour_indices:
                if NI not in explored:
                    Path = currentPath.copy()
                    Path.append((NI, False))
                    if not (fringe.contains(Path)):
                        fringe.push(Path)
    return None, None


# #############################################################################
# Generate a neighbor function:                                               #
# This function is designed to take a maze object and swap two of the prize   #
#   locations.                                                                #
# #############################################################################
def GenerateANeighbor(maze):

    # generate two random numbers based on the number of prize points
    int1 = random.randint(0, maze.numPrizeLocations - 1)
    int2 = random.randint(0, maze.numPrizeLocations - 1)

    # assign the values to variables
    rand_coors = maze.prize_coor_list[int1]
    rand_coors2 = maze.prize_coor_list[int2]

    # swap the values
    maze.prize_coor_list[int1] = rand_coors
    maze.prize_coor_list[int2] = rand_coors2

    return maze


# #############################################################################
# Hill climbing function:                                                     #
# ------------------------                                                    #
# Its is designed to implement a function that will generate a path between   #
#   a copy of the maze and the maze.                                          #
# #############################################################################
def hill_climbing(maze):
    # Path for the maze
    path = list()

    # Path for the neighbor maze
    path_neighbor = list()

    # generates a path for the maze
    maze.solution_path = GenerateAPath(maze)

    # appends it to the list
    for i in maze.solution_path:
        path.append(i)

    # Copy the maze into a new one
    neighbor_maze = copyMaze(maze)

    # Swap to prize points
    neighbor_maze = GenerateANeighbor(neighbor_maze)

    # generate a path for the neighbor
    neighbor_maze.solution_path = GenerateAPath(neighbor_maze)

    # appends the path to the list
    for i in neighbor_maze.solution_path:
        path_neighbor.append(i)

    # Evaluates which path is closer and returns it
    if len(path) < len(path_neighbor):
        return path
    else:
        return path_neighbor


# #############################################################################
# Hill climbing with random restarts function:                                #
# ---------------------------------------------                               #
# Its is designed to implement a function that will generate a path between   #
#   a copy of the maze and the maze. Moreover, it will randomly restart the   #
#   function based on the parameter passed.                                   #
# #############################################################################
def hill_climbing_with_RandomRestarts(maze, num):
    # Path to be returned
    path = list()

    # Iterate the number of times the parameter num is passed
    for i in range(num - 1):
        # restart the hill climbing function everytime
        path = hill_climbing(maze)
    return path


def PathTwoPoints(pointA_indices, pointB_indices, grid):
    num_rows = 10
    num_cols = 10
    the_maze = Maze(num_rows, num_cols, numPzLocs=1, id=0, entryPt=pointA_indices, exitPt=pointB_indices)
    the_maze.grid = grid
    the_maze.solution_path = AStarSearch(the_maze)

    # vis = Visualizer(theMaze, cell_size=1, media_filename="")
    # vis.show_maze_solution()

    SolPathTemp = the_maze.solution_path
    SolPath = []
    # print("Sol path with back trackers=",SolPathTemp)

    # remove back trackers
    list_of_backtrackers = []
    for path_element in SolPathTemp:
        if path_element[1]:
            list_of_backtrackers.append(path_element[0])
    # print("back trackers=",list_of_back trackers)

    SolPath.append(((SolPathTemp[0][0][0], SolPathTemp[0][0][1]), SolPathTemp[0][1]))

    # print("len=", SolPathTemp.__len__())
    for i in range(1, SolPathTemp.__len__()):
        ## print(i)
        ## print(SolPathTemp[i][0])
        point1 = SolPathTemp[i][0]
        point2 = SolPathTemp[i - 1][0]
        if not (point1 in list_of_backtrackers) and \
                not (point2 in list_of_backtrackers):
            SolPath.append(((SolPathTemp[i][0][0], SolPathTemp[i][0][1]), SolPathTemp[i][1]))
    return SolPath


def GenerateAPath(maze):
    path = list()
    listPrizePoints = maze.prize_coor_list.copy()
    pointA_indices = maze.entry_coor
    maze.ClearSolution()
    bFirst = True
    while len(listPrizePoints) > 0:
        pointB_indices = listPrizePoints.pop()
        pathToAdd = PathTwoPoints(pointA_indices, pointB_indices, maze.grid)
        # if not first path remove duplicate point
        if not bFirst:
            pathToAdd.remove((pointA_indices, False))

        path.extend(pathToAdd)

        bFirst = False
        maze.ClearSolution()
        pointA_indices = pointB_indices
    return path


def copyMaze(maze):
    the_maze = copy.deepcopy(maze)
    the_maze.ClearSolution()
    return the_maze


# Generate Maze
numRows = 10
numCols = 10
numPrizePoints = 10
theMaze = Maze(numRows, numCols, numPrizePoints, 0, None, None)

# Show Maze Start
vis = Visualizer(theMaze, cell_size=1, media_filename="")
vis.show_maze()

print("**********************")
print("Random Solution")

## solPath = PathTwoPoints(theMaze.entry_coor,theMaze.prize_coor_list[0],theMaze.grid)
## print(solPath)

theMaze.ClearSolution()

theMaze.solution_path = GenerateAPath(theMaze)
### print(theMaze.solution_path)

# Show what points were explored to find the solution
vis = Visualizer(theMaze, cell_size=1, media_filename="")
vis.animate_maze_solution()

# Show Solution Path
vis = Visualizer(theMaze, cell_size=1, media_filename="")
vis.show_maze_solution()

print("Distance Solution = ", len(theMaze.solution_path))

# Hill Climbing

print("**********************")
print("Hill Climbing")

theMaze.solution_path = hill_climbing(theMaze)

# Show what points were explored to find the solution
vis = Visualizer(theMaze, cell_size=1, media_filename="")
vis.animate_maze_solution()

# Show Solution Path
vis = Visualizer(theMaze, cell_size=1, media_filename="")
vis.show_maze_solution()

print("Distance Solution = ", len(theMaze.solution_path))

# Hill Climbing with Random Restarts

## ****************************************
k = 5
print("**********************")
print("Hill Climbing with Random Restarts  k= ", k)
theMaze.ClearSolution()
theMaze.solution_path = hill_climbing_with_RandomRestarts(theMaze, k)

# Show what points were explored to find the solution
vis = Visualizer(theMaze, cell_size=1, media_filename="")
vis.animate_maze_solution()

# Show Solution Path
vis = Visualizer(theMaze, cell_size=1, media_filename="")
vis.show_maze_solution()
print("Distance Solution = ", len(theMaze.solution_path))
prevBestDist = len(theMaze.solution_path)
