from move import Move
from pieces import Piece


class Rook(Piece):
    def __init__(self, id, direction, color, asset, fen_symbol="r"):
        super().__init__(
            id=id, name="Rook", fen_symbol=fen_symbol, direction=direction, color=color, asset=asset, value=5
        )

    def _get_possible_moves_in_each_direction(self, square, _):
        possible_moves = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for dr, dc in directions:
            directional_moves = []
            for i in range(1, 8):
                new_row = square.row + i * dr
                new_col = square.col + i * dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
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


class BlackRook(Rook):
    def __init__(self, id, direction):
        super().__init__(id, direction, "black", "black_rook.png", fen_symbol="r")


class WhiteRook(Rook):
    def __init__(self, id, direction):
        super().__init__(id, direction, "white", "white_rook.png", fen_symbol="R")
