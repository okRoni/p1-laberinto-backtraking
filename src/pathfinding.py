from .Maze import Maze
from .Cell import Cell

Location = tuple[int, int]
Route = list[Location]


def build_route(maze: Maze, location: Location) -> Route:
    """Builds a route of the maze from the given location to the start."""

    route: Route = [location]
    cell: Cell = maze[location[0]][location[1]]
    while cell.previous is not None:
        cell = cell.previous
        route.append((cell.row, cell.column))
    return route[::-1]

def unmark_route(maze: Maze, start: Location, end: Location) -> None:
    """Marks all cells as not visited from given start to given end."""

    cell: Cell = maze[end[0]][end[1]]
    while (cell.row, cell.column) != start:
        cell.visited = False
        if cell.previous is not None:
            cell = cell.previous

def get_routes_bt(maze: Maze, start: Location, end: Location) -> list[Route]:
    """Returns all posible routes from start to end."""

    routes: list[Route] = []
    # This algorithm needs to know from which cell every cell is visited.
    # The root cell is defined just to be the cell from which the start
    # cell is visited.
    root_cell: Cell = Cell(-1, -1)
    # The stack consists of a list of tuples (A, B), where A is a cell to
    # be visited and B is the cell from which A needs to be visited. The
    # 'previous' attribute of the cell A can't be used for this purpose
    # because cell A can be visited from multiple cells, for that reason
    # the cell B is used.
    stack: list[tuple[Cell, Cell]] = [(maze[start[0]][start[1]], root_cell)]
    previous: Cell | None = None

    while stack != []:
        cell_pair: tuple[Cell, Cell] = stack.pop()
        cell: Cell = cell_pair[0]
        cell.visited = True
        cell_location: Location = (cell.row, cell.column)

        if cell_location == end:
            routes.append(build_route(maze, end))
            if stack == []:
                break
            # The cell in which a branch occurs.
            branch_cell: Cell = stack[-1][1]
            branch_location: Location = (branch_cell.row, branch_cell.column)
            unmark_route(maze, branch_location, end)
            previous = branch_cell
            continue

        has_move: bool = False
        count = 0  # For debugging purposes
        up: Cell | None = cell.up
        if up is not None and not up.visited:
            stack.append((up, cell))
            up.previous = cell
            has_move = True
            count += 1
        down: Cell | None = cell.down
        if down is not None and not down.visited:
            stack.append((down, cell))
            down.previous = cell
            has_move = True
            count += 1
        left: Cell | None = cell.left
        if left is not None and not left.visited:
            stack.append((left, cell))
            left.previous = cell
            has_move = True
            count += 1
        right: Cell | None = cell.right
        if right is not None and not right.visited:
            stack.append((right, cell))
            right.previous = cell
            has_move = True
            count += 1

        if not has_move:
            if stack == []:
                break
            # The cell in which a branch occurs.
            branch_cell: Cell = stack[-1][1]
            branch_location: Location = (branch_cell.row, branch_cell.column)
            unmark_route(maze, branch_location, cell_location)
            previous = branch_cell
            continue

        cell.previous = previous
        previous = cell

    maze.unmark_all_cells()
    return routes


m = Maze(3)
m[0][0].connect_right(m[0][1])
m[0][1].connect_right(m[0][2])
m[0][2].connect_down(m[1][2])
m[1][2].connect_down(m[2][2])

m[0][0].connect_down(m[1][0])
m[1][0].connect_down(m[2][0])
m[2][0].connect_right(m[2][1])
m[2][1].connect_right(m[2][2])

m[0][1].connect_down(m[1][1])
m[1][1].connect_down(m[2][1])

print(m)
print(get_routes_bt(m, (0,0), (2,2)))
