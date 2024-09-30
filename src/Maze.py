from __future__ import annotations
from os import path, mkdir
from .Cell import Cell


class Maze:
    """Class that represents a maze."""

    def __init__(self, size: int | None = None, name: str = '') -> None:
        self.__build_cell_matrix(size)
        self.start: Cell | None = None
        self.end: Cell | None = None
        self.name: str = name

    def __build_cell_matrix(self, size: int) -> None:
        if size is None or not isinstance(size, int) or size < 1:
            return
        self.cell_matrix: list[list[Cell]] = \
            [[Cell() for _ in range(size)] for _ in range(size)]

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


# Tests
# m = Maze(size=3, name='maze1')
# m2 = Maze()
#
# m[0][0].connect_right(m[0][1])
# m[1][1].connect_up(m[0][1])
# m.store()
# m2.load(path.join('mazes', 'maze1.txt'))
# print(m, '\n\n', m2, sep='')
