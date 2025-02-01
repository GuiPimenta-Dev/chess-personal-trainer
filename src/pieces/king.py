from const import COLS, ROWS
from move import Move
from pieces import Piece


class King(Piece):
    def __init__(self, id, direction, color, asset, fen_symbol):
        super().__init__(
            id=id, name="King", fen_symbol=fen_symbol,direction=direction, color=color, asset=asset,value=1000
        )

    def _get_possible_moves_in_each_direction(self, square, grid):
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
                            piece=square.piece,
                        )
                    ]
                )

        # Castling
        if not self.has_moved:
            rook_squares = grid.get_squares_by_piece_name_and_color("Rook", self.color)
            for rook_square in rook_squares:
                if rook_square.piece.has_moved:
                    continue

                if self.can_castle(rook_square, square, grid):
                    # Add castling moves to the possible moves
                    new_king_row = square.row
                    if rook_square.col > square.col:  # Castling to the right
                        new_king_col = square.col + 2  # King moves to column 6
                    else:  # Castling to the left
                        new_king_col = square.col - 2  # King moves to column 2
                    possible_moves.append(
                        [
                            Move(
                                initial_row=square.row,
                                initial_col=square.col,
                                target_row=new_king_row,
                                target_col=new_king_col,
                                piece=square.piece,
                                castling_square=rook_square,
                            )
                        ]
                    )

        return possible_moves

    def can_castle(self, rook_square, king_square, grid):
        """
        Check if castling is possible:
        - No pieces between the King and Rook.
        - The King does not move through or end in check.
        """
        # Determine the direction of castling
        if rook_square.col > king_square.col:  # Castling to the right
            start_col = king_square.col + 1
            end_col = rook_square.col
            step = 1
        else:  # Castling to the left
            start_col = king_square.col - 1
            end_col = rook_square.col
            step = -1

        # Check if squares between King and Rook are empty
        for col in range(start_col, end_col, step):
            target_square = grid.get_square_by_row_and_col(king_square.row, col)
            if target_square.has_piece():
                return False  # Pieces between King and Rook

        # Here, you could add a check to make sure the King doesn't move through or end in check
        # For now, we assume it's safe to castle.
        return True


class BlackKing(King):
    def __init__(self, id, direction):
        super().__init__(id, direction, "black", "black_king.png", fen_symbol="k")


class WhiteKing(King):
    def __init__(self, id, direction):
        super().__init__(id, direction, "white", "white_king.png", fen_symbol="K")
