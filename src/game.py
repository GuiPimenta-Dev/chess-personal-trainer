import pygame
from board import Board
from const import ROWS, COLS, SQUARE_SIZE
from dragger import Dragger
from move import Move
from pieces import Piece
from pieces.pawn import Pawn
from square import Square
import copy


class Game:
    def __init__(self, play_as_white=True):
        self.play_as_white = play_as_white
        self.hovered_square = None
        self.board = Board(play_as_white)
        self.dragger = Dragger()
        self.check = {
            "white": {"checks": [], "protective_moves": []},
            "black": {"checks": [], "protective_moves": []},
        }

    def show_bg(self, screen):

        for row in range(ROWS):
            for col in range(COLS):
                display_row = row if self.play_as_white else ROWS - 1 - row
                display_col = col if self.play_as_white else COLS - 1 - col

                if (display_row + display_col) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)

                pygame.draw.rect(
                    screen,
                    color,
                    (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                )

    def show_pieces(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                square = self.board.grid.get_square_by_row_and_col(row, col)
                if square.has_piece() and square.piece != self.dragger.piece:
                    img = pygame.image.load(square.piece.asset)
                    img_center = (
                        col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2,
                    )
                    square.piece.texture_rect = img.get_rect(center=img_center)
                    screen.blit(img, square.piece.texture_rect)

    def show_last_move(self, screen):
        if len(self.board.moves) > 0:
            last_move = self.board.moves[-1]
            initial_row = last_move.initial_row
            initial_col = last_move.initial_col
            target_row = last_move.target_row
            target_col = last_move.target_col

            initial_rect = (
                initial_col * SQUARE_SIZE,
                initial_row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE,
            )
            target_rect = (
                target_col * SQUARE_SIZE,
                target_row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE,
            )

            color = (172, 195, 51)
            pygame.draw.rect(screen, color, initial_rect)
            pygame.draw.rect(screen, color, target_rect)

    def show_hover(self, screen):
        if self.hovered_square:
            color = (180, 180, 180)
            rect = (
                self.hovered_square.col * SQUARE_SIZE,
                self.hovered_square.row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE,
            )
            pygame.draw.rect(screen, color, rect, width=3)

    def show_check(self, screen):
        check_color = (255, 180, 180)
        for color in ["white", "black"]:
            if self.board.is_king_in_check(color):
                squares = []
                for move in self.board.get_checks(color):
                    squares += self.board.grid.get_squares_between(move)

                for square in squares:
                    rect = (
                        square.col * SQUARE_SIZE,
                        square.row * SQUARE_SIZE,
                        SQUARE_SIZE,
                        SQUARE_SIZE,
                    )
                    pygame.draw.rect(screen, check_color, rect)

    def set_hover(self, row, col):
        self.hovered_square = self.board.grid.get_square_by_row_and_col(row, col)

    # def _verify_if_king_is_checked(self, color):
    #     checks = self._get_checks(color)
    #     protective_moves = self._get_protective_moves(color) if checks else []
    #     self.check[color] = {
    #         "checks": checks,
    #         "protective_moves": protective_moves
    #     }

    # def _get_checks(self, color):
    #     self._reset_possible_moves()
    #     checks = []
    #     for row in range(ROWS):
    #         for col in range(COLS):
    #             square: Square = self.board.squares[row][col]
    #             if square.has_piece() and square.has_enemy(color):
    #                 self.set_possible_moves(row, col)
    #                 for move in self.possible_moves:
    #                     if move.captured_piece and move.captured_piece.name == "King":
    #                         checks.append(move)
    #     return checks

    # def _get_protective_moves(self, color):
    #     """
    #     Returns a list of all moves that can protect the king of the specified color from being in check.
    #     """
    #     protective_moves = []

    #     for row in range(ROWS):
    #         for col in range(COLS):
    #             square = self.board.squares[row][col]

    #             # Ensure the square has a piece of the specified color
    #             if square.has_piece() and square.piece.color == color:
    #                 piece = square.piece

    #                 # Generate possible moves for this piece
    #                 self.set_possible_moves(row, col)
    #                 for move in self.possible_moves:
    #                     # Save the state before making the move
    #                     captured_piece = self.board.squares[move.target_row][move.target_col].piece
    #                     initial_square = self.board.squares[move.initial_row][move.initial_col]
    #                     target_square = self.board.squares[move.target_row][move.target_col]

    #                     # Apply the move
    #                     target_square.piece = piece
    #                     initial_square.piece = None

    #                     # Check if the king is in check
    #                     if not self._get_checks(color):
    #                         protective_moves.append(move)

    #                     # Undo the move
    #                     initial_square.piece = piece
    #                     target_square.piece = captured_piece

    #     return protective_moves

    # def _find_move(self, row, col):
    #     for move in self.possible_moves:
    #         if move.target_row == row and move.target_col == col:
    #             return move
    #     return None

    def show_ai_best_move(self, screen, best_move):
        if best_move:
            first_uci = best_move[:2]
            second_uci = best_move[2:]
            first_square = self.board.grid.get_square_by_uci(first_uci)
            second_square = self.board.grid.get_square_by_uci(second_uci)
            initial_row = first_square.row
            initial_col = first_square.col
            target_row = second_square.row
            target_col = second_square.col

            initial_rect = (
                initial_col * SQUARE_SIZE,
                initial_row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE,
            )
            target_rect = (
                target_col * SQUARE_SIZE,
                target_row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE,
            )

            color = (128, 0, 128)

            pygame.draw.rect(screen, color, initial_rect, width=10)
            pygame.draw.rect(screen, color, target_rect)

    def show_possible_moves(self, screen):
        for move in self.board.possible_moves:
            if move.piece == self.dragger.piece:
                center_x = move.target_col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = move.target_row * SQUARE_SIZE + SQUARE_SIZE // 2
                radius = SQUARE_SIZE // 4
                color = (
                    (100, 100, 100, 60) if not move.captured_piece else (200, 100, 100)
                )
                pygame.draw.circle(screen, color, (center_x, center_y), radius)
