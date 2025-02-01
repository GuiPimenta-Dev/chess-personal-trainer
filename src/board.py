import sys
from typing import List
from const import COLS, ROWS
from grid import Grid
from move import Move
from pieces import Piece
from pieces.queen import Queen
from square import Square


class Board:
    def __init__(self, play_as_white=True, grid=None):
        self.grid = grid or Grid(play_as_white)
        self.turn = "white"
        self.checks = {"white": [], "black": []}
        self.moves = []
        self.is_game_over = False
        self.possible_moves = self._get_all_possible_moves(self.turn)

    def move(self, row, col, piece):
        moves = []
        
        for possible_move in self.possible_moves:
            if (
                possible_move.target_row == row
                and possible_move.target_col == col
                and piece == possible_move.piece
            ):
                moves.append(possible_move)

        if not moves:
            return

        move = moves[0]
        self.grid.move_piece(move)
        self.moves.append(move)
        move.piece.add_move(move)
        self._verify_promotion()
        self._switch_turn()

    def _get_all_possible_moves(self, color):
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                piece: Piece = self.grid.get_square_by_row_and_col(row, col).piece
                if piece and piece.color == color:
                    moves.extend(piece.get_possible_moves(row, col, self.grid))
        
        return moves

    def _switch_turn(self):
        self.turn = "white" if self.turn == "black" else "black"
        is_white_mate = self.is_check_mate("white")
        is_black_mate = self.is_check_mate("black")
        if is_white_mate:
            print("White is in checkmate")
            self.is_game_over = True
            
        if is_black_mate:
            print("Black is in checkmate")
            self.is_game_over = True
            
        white_possible_moves = self.get_possible_moves_by_color("white")
        black_possible_moves = self.get_possible_moves_by_color("black")
        self.possible_moves = white_possible_moves + black_possible_moves

    def is_check_mate(self, color):
        return self.is_king_in_check(color) and not self.get_possible_moves_by_color(color)

    def get_possible_moves_by_color(self, color):
        is_king_in_check = self.is_king_in_check(color)

        if is_king_in_check:
            return self._get_protective_moves(color)

        safe_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                square = self.grid.get_square_by_row_and_col(row, col)
                if square.has_piece() and square.piece.color == color:
                    piece = square.piece
                    possible_moves = piece.get_possible_moves(row, col, self.grid)

                    for move in possible_moves:
                        # Simulate the move
                        captured_piece = self.grid.get_square_by_row_and_col(
                            move.target_row, move.target_col
                        ).piece
                        initial_square = self.grid.get_square_by_row_and_col(
                            move.initial_row, move.initial_col
                        )
                        target_square = self.grid.get_square_by_row_and_col(
                            move.target_row, move.target_col
                        )

                        target_square.piece = piece
                        initial_square.piece = None

                        if not self.is_king_in_check(color):
                            safe_moves.append(move)

                        # Undo the simulated move
                        initial_square.piece = piece
                        target_square.piece = captured_piece

        return safe_moves

    def _get_protective_moves(self, color):
        protective_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                square = self.grid.get_square_by_row_and_col(row, col)
                if square.has_piece() and square.piece.color == color:
                    piece = square.piece
                    possible_moves = piece.get_possible_moves(row, col, self.grid)
                    for move in possible_moves:
                        captured_piece = self.grid.get_square_by_row_and_col(
                            move.target_row, move.target_col
                        ).piece
                        initial_square = self.grid.get_square_by_row_and_col(
                            move.initial_row, move.initial_col
                        )
                        target_square = self.grid.get_square_by_row_and_col(
                            move.target_row, move.target_col
                        )
                        target_square.piece = piece
                        initial_square.piece = None
                        if not self.is_king_in_check(color):
                            protective_moves.append(move)
                        initial_square.piece = piece
                        target_square.piece = captured_piece
        return protective_moves

    def is_king_in_check(self, color: str) -> bool:
        enemy_color = "black" if color == "white" else "white"
        king_square = self.grid.get_square_by_piece_name_and_color("King", color)
        for move in self._get_all_possible_moves(enemy_color):
            if (
                king_square
                and move.target_row == king_square.row
                and move.target_col == king_square.col
            ):
                return True

        return False

    def _verify_promotion(self):
        white_pawns = self.grid.get_squares_by_piece_name_and_color("Pawn", "white")
        black_pawns = self.grid.get_squares_by_piece_name_and_color("Pawn", "black")
        all_pawns = white_pawns + black_pawns
        
        for pawn_square in all_pawns:
            if (
                pawn_square.row == 0
                or pawn_square.row == ROWS - 1
            ):
                existent_queens = self.grid.get_squares_by_piece_name_and_color("Queen", pawn_square.piece.color)
                asset = "black_queen.png" if pawn_square.piece.color == "black" else "white_queen.png"
                self.grid.squares[pawn_square.row][pawn_square.col].piece = Queen(id=len(existent_queens) + 1, color=pawn_square.piece.color, asset=asset, direction=pawn_square.piece.direction)

    def get_checks(self, color: str) -> List[Move]:
        checks = []
        enemy_color = "black" if color == "white" else "white"
        king_square = self.grid.get_square_by_piece_name_and_color("King", color)
        for move in self._get_all_possible_moves(enemy_color):
            if (
                move.target_row == king_square.row
                and move.target_col == king_square.col
            ):
                checks.append(move)

        return checks

    def get_state(self):
        """
        Retorna uma representação única do estado atual do tabuleiro.
        Aqui, estamos criando uma tupla contendo a posição e o tipo das peças.
        """
        state = []
        for row in range(ROWS):
            for col in range(COLS):
                square = self.grid.get_square_by_row_and_col(row, col)
                if square.has_piece():
                    piece = square.piece
                    # Representação simples da peça como uma tupla (cor, tipo)
                    state.append((row, col, piece.color, piece.__class__.__name__))
                else:
                    state.append((row, col, None))  # Nenhuma peça na posição
        return tuple(state)  # Retorna uma tupla para ser usada como hashable