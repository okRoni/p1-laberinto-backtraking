from __future__ import annotations
import random

class Cell:
    """Class that represents a cell of a maze."""

    def __init__(self, row, column) -> None:
        # avaiable paths
        self.up: Cell | None = None
        self.down: Cell | None = None
        self.left: Cell | None = None
        self.right: Cell | None = None
        # position in the matrix
        self.row: int = row
        self.column: int = column
        self.visited: bool = False

    def connect_up(self, cell: Cell) -> None:
        self.up = cell
        cell.down = self

    def connect_down(self, cell: Cell) -> None:
        self.down = cell
        cell.up = self

    def connect_left(self, cell: Cell) -> None:
        self.left = cell
        cell.right = self

    def connect_right(self, cell: Cell) -> None:
        self.right = cell
        cell.left = self

    def connect(self, cell: Cell) -> None:
        """Checks what direction the cell is in and connects it to the cell."""
        if cell.row == self.row:
            if cell.column == self.column - 1:
                self.connect_left(cell)
            elif cell.column == self.column + 1:
                self.connect_right(cell)
        elif cell.column == self.column:
            if cell.row == self.row - 1:
                self.connect_up(cell)
            elif cell.row == self.row + 1:
                self.connect_down(cell)

    def __str__(self) -> str:
        """
        Represents the cell in the format 'abcd', where a, b, c and d are 0
        or 1 if the attributes up, right, down and left are or aren't None,
        respectively.
        """

        char_up = '0' if self.up is None else '1'
        char_right = '0' if self.right is None else '1'
        char_down = '0' if self.down is None else '1'
        char_left = '0' if self.left is None else '1'
        return char_up + char_right + char_down + char_left
