from const import COLS, ROWS


class Move:
    def __init__(
        self,
        initial_row,
        initial_col,
        target_row,
        target_col,
        piece,
        captured_piece=None,
        promotion=None,
        castling_square=None,
        en_passant=False,
    ):
        self.initial_row = initial_row
        self.initial_col = initial_col
        self.target_row = target_row
        self.target_col = target_col
        self.piece = piece
        self.captured_piece = captured_piece
        self.promotion = promotion
        self.castling_square = castling_square
        self.en_passant = en_passant

    @property
    def is_castling(self):
        return self.castling_square is not None

    def is_inside_grid(self):
        return 0 <= self.target_row < ROWS and 0 <= self.target_col < COLS

    def __repr__(self):
        return f"({self.row}, {self.col})"

    def __eq__(self, other):
        return (
            self.initial_row == other.initial_row
            and self.initial_col == other.initial_col
            and self.target_row == other.target_row
            and self.target_col == other.target_col
            and self.piece.id == other.piece.id
        )
