from copy import deepcopy
from typing import Optional
from tqdm import tqdm
from board import Board
from const import COLS, ROWS
from move import Move
from functools import lru_cache  # Memoization decorator for caching

class Minimax:
    def __init__(self, board: Board, max_depth: int = 3):
        self.board = board
        self.max_depth = max_depth
        self.transposition_table = {}  # Memoization table

    @lru_cache(maxsize=None)  # Caching evaluations
    def evaluate_board(self, board: Board) -> int:
        """
        Evaluate the current board state.
        Positive scores favor white, negative scores favor black.
        """
        score = 0
        for row in range(ROWS):
            for col in range(COLS):
                square = board.grid.get_square_by_row_and_col(row, col)
                if square.has_piece():
                    piece = square.piece
                    score += piece.value if piece.color == "white" else -piece.value
        return score

    def minimax(self, depth: int, maximizing: bool, alpha: int, beta: int) -> int:
        """
        Recursive minimax algorithm with alpha-beta pruning.
        """
        if depth == 0 or self.is_game_over():
            return self.evaluate_board(self.board)

        color = "white" if maximizing else "black"
        moves = self.board.get_possible_moves_by_color(color)

        if maximizing:
            max_eval = float('-inf')
            # Prioritize most promising moves first (e.g., heuristic-based move ordering)
            moves = self.order_moves(moves, maximizing)
            for move in tqdm(moves, desc="Maximizing", leave=False):
                temp_board = deepcopy(self.board)  # Avoid deepcopy
                self.simulate_move(temp_board, move)
                eval = self.minimax_with_board(temp_board, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break  # Beta pruning
            return max_eval
        else:
            min_eval = float('inf')
            # Prioritize most promising moves first (e.g., heuristic-based move ordering)
            moves = self.order_moves(moves, maximizing)
            for move in tqdm(moves, desc="Minimizing", leave=False):
                temp_board = deepcopy(self.board)  # Avoid deepcopy
                self.simulate_move(temp_board, move)
                eval = self.minimax_with_board(temp_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break  # Alpha pruning
            return min_eval

    def find_best_move(self, color: str):
        """
        Find the best move for the given color using the minimax algorithm with alpha-beta pruning.
        """
        best_move = None
        best_value = float('-inf') if color == "white" else float('inf')

        moves = self.board.get_possible_moves_by_color(color)
        for move in tqdm(moves, desc="Evaluating moves", leave=False):
            temp_board = deepcopy(self.board)  # Avoid deepcopy
            self.simulate_move(temp_board, move)
            eval = self.minimax_with_board(temp_board, self.max_depth - 1, color == "black", float('-inf'), float('inf'))

            if (color == "white" and eval > best_value) or (color == "black" and eval < best_value):
                best_value = eval
                best_move = move

        return best_move

    def minimax_with_board(self, board: Board, depth: int, maximizing: bool, alpha: int, beta: int) -> int:
        """
        A helper function to use a given board state for minimax evaluation with alpha-beta pruning.
        """
        # Check the transposition table first
        board_state = board.get_state()  # Assume get_state() returns a hashable state
        if board_state in self.transposition_table:
            return self.transposition_table[board_state]

        if depth == 0 or self.is_game_over():
            eval = self.evaluate_board(board)
            self.transposition_table[board_state] = eval
            return eval

        color = "white" if maximizing else "black"
        moves = board.get_possible_moves_by_color(color)

        if maximizing:
            max_eval = float('-inf')
            for move in tqdm(moves, desc="Maximizing", leave=False):
                temp_board = deepcopy(board)  # Avoid deepcopy
                self.simulate_move(temp_board, move)
                eval = self.minimax_with_board(temp_board, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break  # Beta pruning
            self.transposition_table[board_state] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for move in tqdm(moves, desc="Minimizing", leave=False):
                temp_board = deepcopy(board)  # Avoid deepcopy
                self.simulate_move(temp_board, move)
                eval = self.minimax_with_board(temp_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break  # Alpha pruning
            self.transposition_table[board_state] = min_eval
            return min_eval

    def simulate_move(self, board: Board, move: Move):
        """
        Simulate a move on a given board.
        """
        board.grid.move_piece(move)
        board.moves.append(move)
        move.piece.add_move(move)

    def is_game_over(self) -> bool:
        """
        Check if the game is over (e.g., one of the kings is in checkmate).
        """
        white_moves = self.board.get_possible_moves_by_color("white")
        black_moves = self.board.get_possible_moves_by_color("black")
        return not white_moves or not black_moves

    def order_moves(self, moves, maximizing):
        """
        Order moves based on some heuristic (e.g., capturing pieces first).
        This could be improved further by adding your own move-ordering logic.
        """
        # For example, prioritize moves that capture pieces or other criteria
        return sorted(moves, key=lambda move: self.evaluate_move(move), reverse=maximizing)

    def evaluate_move(self, move: Move):
        """
        A simple heuristic to evaluate a move.
        You can enhance this with more sophisticated criteria.
        """
        return move.piece.value if move.piece.color == "white" else -move.piece.value