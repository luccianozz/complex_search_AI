import math


def AStarSearch(maze):
    row_curr, col_curr = maze.entry_coor  # Where to start searching

    maze.grid[row_curr][col_curr].visited = True
    # Set initial cell to visited
    visited_cells = list()

    # Stack of visited cells for backtracking

    path = list()
    # To track path of solution and backtracking cells

    while len(maze.prize_coor_list) >0:
        # While the exit cell has not been encountered

        neighbour_indices = maze.find_neighbours(row_curr, col_curr)
        # Find neighbour indices

        neighbour_indices = maze.validate_neighbours_solve(neighbour_indices, row_curr,col_curr)
        if neighbour_indices is not None:
            # If there are unvisited neighbour cells

            visited_cells.append((row_curr, col_curr))
            # Add current cell to stack

            path.append(((row_curr, col_curr), False))
            # Add coordinates to part of search path
            # false indicates not a back tracker visit

            row_next, col_next = towardsPrize(neighbour_indices,maze.prize_coor_list)
            # Choose random neighbour

            maze.grid[row_next][col_next].visited = True
            # Move to that neighbour

            row_curr = row_next
            col_curr = col_next

        elif len(visited_cells) > 0:
            # If there are no unvisited neighbour cells

            path.append(((row_curr, col_curr), True))
            # Add coordinates to part of search path
            # true indicates it is a back tracker visit

            row_curr, col_curr = visited_cells.pop()
            # Pop previous visited cell (backtracking)

        if (row_curr, col_curr) in maze.prize_coor_list:
           maze.prize_coor_list.remove((row_curr, col_curr))
    path.append(((row_curr, col_curr), False))  # Append final location to path

    return path


def towardsPrize(neighbour_indices,prize_coor_list):
    MinDistNeighbor = None
    MinDist = 100000

    for NI in neighbour_indices:
        for PZ in prize_coor_list:
            dist = math.sqrt((NI[0]-PZ[0])**2 + (NI[1]-PZ[1])**2)
            if dist < MinDist:
                MinDist = dist
                MinDistNeighbor = NI
    return MinDistNeighbor