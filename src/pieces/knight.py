from const import COLS, ROWS
from move import Move
from pieces import Piece


class Knight(Piece):
    def __init__(self, id, direction, color, asset, fen_symbol):
        super().__init__(
            id=id, name="Knight", direction=direction,fen_symbol=fen_symbol, color=color, asset=asset, value=3
        )

    def _get_possible_moves_in_each_direction(self, square, _):
        possible_moves = []
        moves = [
            (-2, -1),
            (-2, 1),
            (2, -1),
            (2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
        ]

        for dr, dc in moves:
            new_row = square.row + dr
            new_col = square.col + dc
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                possible_moves.append(
                    [
                        Move(
                            initial_row=square.row,
                            initial_col=square.col,
                            target_row=new_row,
                            target_col=new_col,
                            piece=self,
                        )
                    ]
                )

        return possible_moves


class BlackKnight(Knight):
    def __init__(self, id, direction):
        super().__init__(id, direction, "black", "black_knight.png", fen_symbol="n")


class WhiteKnight(Knight):
    def __init__(self, id, direction):
        super().__init__(id, direction, "white", "white_knight.png", fen_symbol="N")
