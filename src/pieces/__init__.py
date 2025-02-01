import copy
import os
from abc import ABC, abstractmethod
from typing import List, NamedTuple

from move import Move
from square import Square

current_dir = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(current_dir, "..", "..", "assets", "images")


class Direction(NamedTuple):
    UP = -1
    DOWN = 1


class Piece(ABC):
    def __init__(
        self,
        id,
        name,
        color,
        asset,
        fen_symbol,
        direction: Direction,
        value=None,
        texture_rect=None,
    ):
        self.id = id
        self.name = name
        self.color = color
        self.value = value
        self.fen_symbol = fen_symbol
        self.texture_size = 80
        self.direction = direction
        self.asset = os.path.join(ASSETS_DIR, "80px", asset)
        self.texture_rect = texture_rect
        self.moving = False
        self.moves = []
        self.possible_moves = []

    @property
    def has_moved(self):
        return len(self.moves) > 0

    def __str__(self):
        return f"{self.color.capitalize()} {self.name} ({self.id})"

    def update_asset_size(self, size):
        asset = self.asset.split(os.sep)[-1]
        self.asset = os.path.join(ASSETS_DIR, f"{size}px", asset)

    def get_possible_moves(self, row, col, grid):
        initial_square = grid.get_square_by_row_and_col(row, col)

        possible_moves = []
        moves = []

        possible_moves = self._get_possible_moves_in_each_direction(
            initial_square, grid
        )
        for possible_direction in possible_moves:
            for possible_square in possible_direction:
                target_square = grid.get_square_by_row_and_col(
                    possible_square.target_row, possible_square.target_col
                )
                if possible_square.promotion:
                    moves.append(possible_square)
                elif not target_square.has_piece():
                    if possible_square.is_inside_grid():
                        moves.append(possible_square)
                elif target_square.has_enemy(self.color):
                    possible_square.captured_piece = target_square.piece
                    if possible_square.is_inside_grid():
                        moves.append(possible_square)
                    break
                else:
                    break

        return moves

    def add_move(self, move: Move):
        self.moves.append(move)

    def set_moving(self, moving):
        self.moving = moving

    @abstractmethod
    def _get_possible_moves_in_each_direction(self, square: Square, grid):
        pass