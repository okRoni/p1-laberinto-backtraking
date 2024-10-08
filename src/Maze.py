from __future__ import annotations
from os import path, mkdir
from .Cell import Cell
import random
import sys

sys.setrecursionlimit(10**6)

class Maze:
    """Class that represents a maze."""

    def __init__(self, size: int | None = None, name: str = '') -> None:
        """Initializes the object."""

        self.__build_cell_matrix(size)
        self.start: Cell | None = None
        self.end: Cell | None = None
        self.name: str = name

    def __build_cell_matrix(self, size: int | None) -> None:
        """Initializes the matrix of cells."""
        if size is None or not isinstance(size, int) or size < 1:
            return
        self.cell_matrix: list[list[Cell]] = \
            [[Cell(row, column) for column in range(size)] for row in range(size)]

    def __getitem__(self, key: int) -> list[Cell]:
        return self.cell_matrix[key]

    def __str__(self) -> str:
        """
        Represents the maze as a matrix of cells using the __str__ method to
        represent each cell.
        """
        rows: list[str] = []
        for row in self.cell_matrix:
            cells: list[str] = [str(cell) for cell in row]
            rows.append(' '.join(cells))
        return '\n'.join(rows)

    def store(self) -> None:
        """Stores the maze in a .txt file with the name of the maze."""

        if self.name == '':  # Can't store an unnamed maze.
            return
        maze_string = self.__str__()
        folder: str = 'src/mazes' # accesed from app.py
        filename: str = self.name + '.txt'
        try:
            with open(path.join(folder, filename), 'w') as file:
                file.write(maze_string)
        except FileNotFoundError:
            mkdir(folder)
            with open(path.join(folder, filename), 'w') as file:
                file.write(maze_string)

    def load(self, filepath: str) -> None:
        """Loads a maze from a .txt file."""

        if not isinstance(filepath, str) or filepath == '':
            return
        raw_content: str = ''
        with open(filepath, 'r') as file:
            raw_content = file.read()
        raw_rows: list[str] = raw_content.split('\n')
        # In this project we asume a square maze (# rows == # columns).
        maze_size: int = len(raw_rows)
        raw_cell_matrix: list[list[str]] = [row.split(' ') for row in raw_rows]
        self.__build_cell_matrix(maze_size)

        for i in range(maze_size):
            for j in range(maze_size):
                cell: Cell = self.cell_matrix[i][j]
                raw_cell: str = raw_cell_matrix[i][j]
                if raw_cell[0] == '1':
                    cell.connect_up(self.cell_matrix[i - 1][j])
                if raw_cell[1] == '1':
                    cell.connect_right(self.cell_matrix[i][j + 1])
                if raw_cell[2] == '1':
                    cell.connect_down(self.cell_matrix[i + 1][j])
                if raw_cell[3] == '1':
                    cell.connect_left(self.cell_matrix[i][j - 1])

    def generate_maze(self) -> None:
        """Generates random paths in the blank maze."""
        self.generate_with_dfs(self.cell_matrix[0][0])
        self.unvisit_all()
        self.add_extra_paths()

    def generate_with_dfs(self, cell: Cell) -> None:
        """Generates the maze base using DFS."""
        cell.visited = True
        next_cell : Cell = self.get_unvisited_neighbour(cell)

        while next_cell is not None:
            cell.connect(next_cell)
            self.generate_with_dfs(next_cell)
            next_cell = self.get_unvisited_neighbour(cell)
    
    def get_unvisited_neighbour(self, cell : Cell) -> Cell | None:
        """Returns a random unvisited neighbour of the cell."""
        if cell is None:
            return None
        neighbours: list[Cell] = []
        cell_row: int = cell.row
        cell_column: int = cell.column
        
        # Check neighbours in all directions (very ugly right now)
        if cell_row > 0 and not self.cell_matrix[cell_row - 1][cell_column].visited:
            neighbours.append(self.cell_matrix[cell_row - 1][cell_column])
        if cell_column < len(self.cell_matrix) - 1 and not self.cell_matrix[cell_row][cell_column + 1].visited:
            neighbours.append(self.cell_matrix[cell_row][cell_column + 1])
        if cell_row < len(self.cell_matrix) - 1 and not self.cell_matrix[cell_row + 1][cell_column].visited:
            neighbours.append(self.cell_matrix[cell_row + 1][cell_column])
        if cell_column > 0 and not self.cell_matrix[cell_row][cell_column - 1].visited:
            neighbours.append(self.cell_matrix[cell_row][cell_column - 1])
        
        #return the random neighbour
        if len(neighbours) == 0:
            return None
        return random.choice(neighbours)
    
    def unvisit_all(self) -> None:
        """Unvisits all cells in the maze."""
        for row in self.cell_matrix:
            for cell in row:
                cell.visited = False

    def add_extra_paths(self):
        """Adds extra paths to the maze."""
        quantity : int = len(self.cell_matrix)
        for _ in range(quantity):
            row : int = random.randint(1, len(self.cell_matrix) - 2)
            column : int = random.randint(1, len(self.cell_matrix) - 2)
            random_cell : Cell = self.cell_matrix[row][column]
            random_neighbour : Cell = self.get_unvisited_neighbour(random_cell)
            if random_neighbour:
                random_cell.connect(random_neighbour)

    def visitSolutionPath(self, solution: list[tuple[int, int]]):
        """Change to True the 'visited' attribute of all the cells in the solution."""

        for location in solution:
            self.cell_matrix[location[0]][location[1]].visited = True

    def get_state(self) -> list[list[bool]]:
        """Returns a matrix of booleans representing the 'visited' atribute every cell."""

        return [[cell.visited for cell in row] for row in self]


# Tests
# m = Maze(size=3, name='maze1')
# m2 = Maze()
#
# m[0][0].connect_right(m[0][1])
# m[1][1].connect_up(m[0][1])
# m.store()
# m2.load(path.join('mazes', 'maze1.txt'))
# print(m, '\n\n', m2, sep='')
