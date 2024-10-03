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

def printv(maze: Maze):
    # Prints visited cells as a matrix. For testing purposes only.
    for row in maze:
        for cell in row:
            if cell.visited:
                print("* ", end='')
            else:
                print("- ", end='')
        print()
    print()

def get_routes(maze: Maze, start: Location, end: Location,
               enable_optimization: bool) -> list[Route]:
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
    # Used as heuristic to implement A*.
    def get_manhattan_distance(cell: Cell | None) -> int:
        if cell is None:
            return 0
        return abs(cell.row - end[0]) + abs(cell.column - end[1])
    previous: Cell | None = None
    printv(maze)
    # TODO: This sometimes returns duplicate routes. Check why.
    while stack != []:
        cell_pair: tuple[Cell, Cell] = stack.pop()
        cell: Cell = cell_pair[0]
        cell.visited = True
        cell_location: Location = (cell.row, cell.column)
        printv(maze)


        if cell_location == end:
            routes.append(build_route(maze, end))
            if enable_optimization:
                maze.unvisit_all()
                return routes  # In this case just one route is returned.
            if stack == []:
                break
            # The cell in which a branch occurs.
            branch_cell: Cell = stack[-1][1]
            branch_location: Location = (branch_cell.row, branch_cell.column)
            unmark_route(maze, branch_location, end)
            previous = branch_cell
            continue

        has_move: bool = False
        neighbors: list[Cell | None] = [cell.up, cell.right, cell.down, cell.left]
        if enable_optimization:
            neighbors.sort(key=get_manhattan_distance)
        # Given that in a stack the first item pushed is popped last and viceversa,
        # and bacause we need to preserve the neighbors insertion order when
        # optimization is enabled, then the items are pushed in reverse order
        # to counteract the stack's last-in-first-out behavior.
        for neighbor in reversed(neighbors):
            if neighbor is not None and not neighbor.visited:
                stack.append((neighbor, cell))
                neighbor.previous = cell
                has_move = True

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

    maze.unvisit_all()
    routes.sort(key=len)  # Sort found routes by ascending length.
    unique_routes: list[Route] = []
    for route in routes:  # Temporary (i hope) solution to duplicate routes.
        if route not in unique_routes:
            unique_routes.append(route)
    return unique_routes