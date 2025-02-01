from const import COLS, ROWS
from move import Move
from pieces import Piece


class Queen(Piece):
    def __init__(self, id, direction, color, asset, fen_symbol="q"):
        super().__init__(
            id=id, name="Queen", fen_symbol=fen_symbol, direction=direction, color=color, asset=asset, value=9
        )

    def _get_possible_moves_in_each_direction(self, square, _):
        possible_moves = []
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        for dr, dc in directions:
            directional_moves = []
            for i in range(1, COLS):
                new_row = square.row + i * dr
                new_col = square.col + i * dc
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    directional_moves.append(
                        Move(
                            initial_row=square.row,
                            initial_col=square.col,
                            target_row=new_row,
                            target_col=new_col,
                            piece=self,
                        )
                    )
                else:
                    break

            if directional_moves:
                possible_moves.append(directional_moves)

        return possible_moves


class BlackQueen(Queen):
    def __init__(self, id, direction):
        super().__init__(id, direction, "black", "black_queen.png", fen_symbol="q")


class WhiteQueen(Queen):
    def __init__(self, id, direction):
        super().__init__(id, direction, "white", "white_queen.png", fen_symbol="Q")
