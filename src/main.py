import copy
import time
import pygame
import sys

from chatgpt import ChatGPT
from const import COLS, PANEL_WIDTH, ROWS, WIDTH, HEIGHT, SQUARE_SIZE
from game import Game
from minimax import Minimax
from stockfish import Stockfish
import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "..","assets")

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH + PANEL_WIDTH, HEIGHT + 50))  # Extra space for the reload button
        pygame.display.set_caption("Chess")
        self.play_as_white = None  # Set to None initially until user chooses
        self.game = None
        self.board = None
        self.grid = None
        self.dragger = None
        self.minimax = None
        self.stockfish = Stockfish()  # Initialize Stockfish
        self.chatgpt = ChatGPT()
        self.round = 1
        self.best_move = None
        self.modal_visible = True
        self.ai_helps_after_round = 3
        self.ally_depth = 18
        self.enemy_depth = 5
        self.last_analysis = ""
        

    def initialize_game(self):
        self.game = Game(play_as_white=self.play_as_white)
        self.board = self.game.board
        self.grid = self.board.grid
        self.dragger = self.game.dragger
        self.minimax = Minimax(self.board, max_depth=2)
        self.best_move = None
        self.round = 1

    def draw_modal(self):
        modal_width, modal_height = 400, 200
        modal_x = (WIDTH - modal_width + PANEL_WIDTH) // 2
        modal_y = (HEIGHT - modal_height) // 2

        pygame.draw.rect(self.screen, (200, 200, 200), (modal_x, modal_y, modal_width, modal_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (modal_x, modal_y, modal_width, modal_height), 2)

        font = pygame.font.SysFont("Arial", 24)
        text = font.render("Choose your color", True, (0, 0, 0))
        self.screen.blit(text, (modal_x + 100, modal_y + 20))

        crown_size = 80

        white_crown = pygame.image.load(f"{ASSETS_DIR}/images/80px/white_queen.png")
        white_crown = pygame.transform.scale(white_crown, (crown_size, crown_size))
        self.screen.blit(white_crown, (modal_x + 70, modal_y + 80))

        black_crown = pygame.image.load(f"{ASSETS_DIR}/images/80px/black_queen.png")
        black_crown = pygame.transform.scale(black_crown, (crown_size, crown_size))
        self.screen.blit(black_crown, (modal_x + 250, modal_y + 80))


    def draw_reload_button(self):
        button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT + 10, 100, 30)
        pygame.draw.rect(self.screen, (100, 100, 100), button_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)

        font = pygame.font.SysFont("Arial", 20)
        text = font.render("Reload", True, (255, 255, 255))
        self.screen.blit(text, (WIDTH // 2 - 30, HEIGHT + 15))

        return button_rect

    def draw_panel(self):
        panel_x = WIDTH
        pygame.draw.rect(self.screen, (230, 230, 230), (panel_x, 0, PANEL_WIDTH, HEIGHT))
        
       
    def draw_analysis_text(self, panel_x, start_y):
        font = pygame.font.SysFont("Arial", 14)
        margin = 20
        max_width = PANEL_WIDTH - margin * 2
        
        wrapped_lines = []
        for line in self.last_analysis.split('\n'):
            words = line.split()
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                width, _ = font.size(test_line)
                if width < max_width:
                    current_line.append(word)
                else:
                    wrapped_lines.append(' '.join(current_line))
                    current_line = [word]
            wrapped_lines.append(' '.join(current_line))
        
        y_pos = start_y
        for line in wrapped_lines:  # Limit to 8 lines
            text_surface = font.render(line, True, (30, 30, 30))
            self.screen.blit(text_surface, (panel_x + margin, y_pos))
            y_pos += 18

    def my_ai_move(self):
        fen = self.grid.fen
        self.best_move = self.stockfish.get_best_move(fen, self.ally_depth)
        if self.best_move:
            color = "white" if self.play_as_white else "black"
            self.last_analysis = self.chatgpt.analyze_move(str(self.grid.board), color, self.best_move)
            self.game.show_ai_best_move(self.screen, self.best_move)

    def enemy_ai_move(self):
        fen = self.grid.fen
        best_move = self.stockfish.get_best_move(fen, self.enemy_depth)
        if best_move:
            from_square = self.grid.get_square_by_uci(best_move[:2])
            to_square = self.grid.get_square_by_uci(best_move[2:])
            self.board.move(to_square.row, to_square.col, from_square.piece)

    def run(self):
        while True:
            if self.modal_visible:
                self.screen.fill((0, 0, 0))
                self.draw_modal()
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        modal_x = (WIDTH + PANEL_WIDTH - 400) // 2
                        modal_y = (HEIGHT - 200) // 2

                        # Check if white crown is clicked
                        if modal_x + 70 <= mouse_x <= modal_x + 150 and modal_y + 80 <= mouse_y <= modal_y + 160:
                            self.play_as_white = True
                            self.modal_visible = False
                            self.initialize_game()

                        # Check if black crown is clicked
                        elif modal_x + 250 <= mouse_x <= modal_x + 330 and modal_y + 80 <= mouse_y <= modal_y + 160:
                            self.play_as_white = False
                            self.modal_visible = False
                            self.initialize_game()

            else:
                my_color = "white" if self.play_as_white else "black"
                self.draw_panel()
                self.draw_analysis_text(WIDTH, 10)
                self.game.show_bg(self.screen)
                self.game.show_hover(self.screen)
                self.game.show_last_move(self.screen)
                self.game.show_check(self.screen)
                self.game.show_ai_best_move(self.screen, self.best_move)
                self.game.show_pieces(self.screen)
                self.game.show_possible_moves(self.screen)
                self.game.show_uci(self.screen)

                if self.best_move is None and self.board.turn == my_color:
                    if (len(self.board.moves) // 2 ) >= self.ai_helps_after_round -1:
                        self.my_ai_move()
                if self.board.turn != my_color:
                    self.enemy_ai_move()
                    self.best_move = None

                if self.dragger.dragging:
                    self.dragger.update_blit(self.screen)

                reload_button_rect = self.draw_reload_button()

                for event in pygame.event.get():

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos

                        # Check if reload button is clicked
                        if reload_button_rect.collidepoint(mouse_x, mouse_y):
                            self.modal_visible = True

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        clicked_row = mouse_y // SQUARE_SIZE
                        clicked_col = mouse_x // SQUARE_SIZE
                        square = self.grid.get_square_by_row_and_col(
                            clicked_row, clicked_col
                        )
                        if not square.has_piece() or square.piece.color != self.board.turn:
                            continue

                        self.dragger.update_mouse(event.pos)
                        self.dragger.save_initial(event.pos)
                        self.dragger.drag_piece(square.piece)

                    elif event.type == pygame.MOUSEMOTION:
                        mouse_x, mouse_y = event.pos
                        clicked_row = mouse_y // SQUARE_SIZE
                        clicked_col = mouse_x // SQUARE_SIZE

                        if (
                            clicked_col < 0
                            or clicked_col >= COLS
                            or clicked_row < 0
                            or clicked_row >= ROWS
                        ):
                            continue

                        self.game.set_hover(clicked_row, clicked_col)

                        if self.dragger.dragging:
                            self.dragger.update_mouse(event.pos)
                            self.game.show_bg(self.screen)
                            self.game.show_hover(self.screen)
                            self.game.show_last_move(self.screen)
                            self.game.show_check(self.screen)
                            self.game.show_ai_best_move(self.screen, self.best_move)
                            self.game.show_pieces(self.screen)
                            self.game.show_possible_moves(self.screen)
                            self.game.show_uci(self.screen)
                            self.dragger.update_blit(self.screen)
                            
                            

                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.dragger.update_mouse(event.pos)
                        clicked_row = self.dragger.mouse_y // SQUARE_SIZE
                        clicked_col = self.dragger.mouse_x // SQUARE_SIZE
                        self.board.move(clicked_row, clicked_col, self.dragger.piece)
                        self.dragger.undrag_piece()
                        
                            
                        

                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.update()
                if self.board.is_game_over:
                    time.sleep(2)
                    self.modal_visible = True
                    

            
if __name__ == "__main__":
    Main().run()
