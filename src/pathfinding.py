from .Maze import Maze
from .Cell import Cell

Location = tuple[int, int]
Route = list[Location]


def build_route_bt(maze: Maze, location: Location) -> Route:
    """Builds a route of the maze from the given location to the start."""

    route: Route = [location]
    cell: Cell = maze[location[0]][location[1]]
    while cell.previous is not None:
        cell = cell.previous
        if cell.location is not None:
            route.append(cell.location)
    return route

def unmark_route_bt(maze: Maze, start: Location, end: Location) -> None:
    """Marks all cells as not visited from given start to given end."""

    cell: Cell = maze[end[0]][end[1]]
    while cell.location != start:
        cell.visited = False
        if cell.previous is not None:
            cell = cell.previous

def get_routes_bt(maze: Maze, start: Location, end: Location) -> list[Route]:
    """Returns all posible routes from start to end."""

    routes: list[Route] = []
    stack: list[Cell] = [maze[start[0]][start[1]]]
    previous: Cell | None = None

    while stack != []:
        cell: Cell = stack.pop()
        if cell.visited:
            continue
        cell.visited = True
        cell.previous = previous
        if cell.location == end:
            routes.append(build_route_bt(maze, end))
            branching_location: Location | None = stack[-1].location
            if branching_location is not None:
                unmark_route_bt(maze, branching_location, end)
            continue

        if cell.up is not None:
            stack.append(cell.up)
        if cell.down is not None:
            stack.append(cell.down)
        if cell.left is not None:
            stack.append(cell.left)
        if cell.right is not None:
            stack.append(cell.right)
        previous = cell

    return routes

