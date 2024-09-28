from __future__ import annotations


class Cell:
    """Class that represents a cell of a maze."""

    def __init__(self) -> None:
        self.up: Cell | None = None
        self.down: Cell | None = None
        self.left: Cell | None = None
        self.right: Cell | None = None
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
