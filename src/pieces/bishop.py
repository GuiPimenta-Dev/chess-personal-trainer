from const import COLS, ROWS
from move import Move
from pieces import Piece


class Bishop(Piece):
    def __init__(self, id, direction, color, asset, fen_symbol):
        super().__init__(
            id=id, name="Bishop", fen_symbol=fen_symbol, direction=direction, color=color, asset=asset, value=3
        )

    def _get_possible_moves_in_each_direction(self, square, _):
        possible_moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            direction_moves = []
            for i in range(1, 8):
                new_row = square.row + i * dr
                new_col = square.col + i * dc
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    direction_moves.append(
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

            possible_moves.append(direction_moves)

        return possible_moves


class BlackBishop(Bishop):
    def __init__(self, id, direction):
        super().__init__(id, direction, "black", "black_bishop.png", fen_symbol="b")


class WhiteBishop(Bishop):
    def __init__(self, id, direction):
        super().__init__(id, direction, "white", "white_bishop.png", fen_symbol="B")
