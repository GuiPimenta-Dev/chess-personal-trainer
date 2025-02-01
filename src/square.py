from const import COLS, ROWS


class Square:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.uci = None

    def is_empty(self):
        return self.piece is None

    def has_piece(self):
        return self.piece is not None

    def has_ally(self, color):
        return self.piece and self.piece.color == color

    def has_enemy(self, color):
        return self.piece and self.piece.color != color

    def is_inside_grid(self):
        return 0 <= self.row < ROWS and 0 <= self.col < COLS
