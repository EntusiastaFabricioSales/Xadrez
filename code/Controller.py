import pygame
import sys
from code.Board import Board
from code.Pawn import Pawn
from code.UI import UI
from code.Piece import Piece
from code.Queen import Queen
from code.Rook import Rook
from code.Bishop import Bishop
from code.Knight import Knight

class Controller:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.ui = UI(self.board)
        self.selected_piece = None
        self.current_turn = 'white'
        self.last_time = pygame.time.get_ticks()
        self.pause_start = pygame.time.get_ticks
        self.time_white = 10 * 60 * 1000
        self.time_black = 10 * 60 * 1000
        self.promotion_pending = None
        self.animation = None
        self.winner = None
        self.draw = False
        self.draw_reason = "Empate"
        self.game_paused = False
        self.halfmove_clock = 0  # zera no início da partida

        self.captured_white = []
        self.captured_black = []

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.game_paused:
                pause_duration = pygame.time.get_ticks() - self.pause_start
                self.last_time += pause_duration

                self.game_paused = False
            else:
                self.pause_start = pygame.time.get_ticks()
                self.game_paused = True

        if self.winner or self.draw or self.game_paused:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if self.ui.retry_button.collidepoint(x, y):
                    self.__init__(self.screen)  # reinicia o jogo
                elif self.ui.menu_button.collidepoint(x, y):
                    return "menu"
            return

        if self.promotion_pending and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            options = ['queen', 'rook', 'bishop', 'knight']

            for i, name in enumerate(options):
                rect = pygame.Rect(160 + i * 80, 280, 64, 64)
                if rect.collidepoint(x, y):
                    pawn, pos = self.promotion_pending
                    new_piece = {
                        'queen': Queen,
                        'rook': Rook,
                        'bishop': Bishop,
                        'knight': Knight
                    }[name](pawn.color, *pos)
                    self.board.grid[pos[0]][pos[1]] = new_piece
                    self.current_turn = 'black' if self.current_turn == 'white' else 'white'
                    self.start_time = pygame.time.get_ticks()
                    self.promotion_pending = None

            return
        
        if self.animation or self.promotion_pending:
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            row, col = self.ui.get_square_under_mouse()
            piece = self.board.get_piece(row, col)

            if self.selected_piece:
                if (row, col) in self.board.get_legal_moves(self.selected_piece):
                    start_pos = (self.selected_piece.row, self.selected_piece.col)
                    result = self.board.move_piece(self.selected_piece, row, col)

                    if result == 'promote':
                        self.promotion_pending = (self.selected_piece, (row, col))
                    else:
                        if isinstance(result, Piece) and result.color != self.selected_piece.color:
                            if result.color == 'white':
                                self.captured_white.append(result)
                            else:
                                self.captured_black.append(result)

                            if result.__class__.__name__ == "Pawn":
                                self.halfmove_clock = 0
                            else:
                                self.halfmove_clock += 1
                        else:
                            self.halfmove_clock += 1

                        self.animation = (self.selected_piece, start_pos, (row, col), 0)
                    
                    self.selected_piece = None
                else:
                    if 0 <= row < 8 and 0 <= col < 8:
                        self.invalid_move_pos = (row, col)  # armazena onde o jogador tentou clicar
                        self.invalid_timer = pygame.time.get_ticks()

                    self.selected_piece = None
            elif piece and piece.color == self.current_turn:
                if self.board.is_in_check(piece.color) and not self.board.get_legal_moves(piece):
                        self.invalid_move_pos = (piece.row, piece.col)  # armazena onde o jogador tentou clicar
                        self.invalid_timer = pygame.time.get_ticks()
                        self.selected_piece = None
                else:
                    self.selected_piece = piece
                    self.valid_moves = self.board.get_legal_moves(piece)

            if self.halfmove_clock >= 100:  # 100 halfmoves = 50 lances (1 por jogador)
                self.draw = True
                self.draw_reason = "Regra dos 50 lances"

    def update(self):
        if self.winner or self.draw or self.game_paused:
            return
        
        if self.promotion_pending:
            return
        
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_time
        self.last_time = current_time

        if self.current_turn == 'white':
            self.time_white -= elapsed
            if self.time_white <= 0:
                if self.has_mating_material('black'):
                    self.winner = 'black'
                else:
                    self.draw_reason = "Empate por peças insuficientes para cheque mate"
                    self.draw = True
                return
        elif self.current_turn == 'black':
            self.time_black -= elapsed
            if self.time_black <= 0:
                if self.has_mating_material('white'):
                    self.winner = 'white'
                else:
                    self.draw_reason = "Empate por peças insuficientes para cheque mate"
                    self.draw = True
                return

        if self.animation:
            piece, start, end, progress = self.animation
            progress += 0.05
            if progress >= 1:
                opponent = 'black' if self.current_turn == 'white' else 'white'

                if self.is_checkmate(opponent):
                    self.winner = self.current_turn
                elif self.is_stalemate(opponent):
                    self.draw_reason = "Empate por afogamento"
                    self.draw = True
                else:
                    self.current_turn = opponent
                
                self.start_time = pygame.time.get_ticks()
                self.animation = None
            else:
                self.animation = (piece, start, end, progress)

    def is_checkmate(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    if self.board.get_legal_moves(piece):
                        return False
                    
        return self.board.is_in_check(color)

    def is_stalemate(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    if self.board.get_legal_moves(piece):
                        return False
                    
        return not self.board.is_in_check(color)

    def has_mating_material(self, color):
        pieces = []
        for row in self.board.grid:
            for piece in row:
                if piece and piece.color == color:
                    pieces.append(piece.__class__.__name__)

        # Ignorar o rei
        pieces = [p for p in pieces if p != 'King']

        # Casos em que é impossível dar mate
        if not pieces:
            return False
        
        #Peças suficientes para ganhar um jogo
        if 'Queen' in pieces or 'Rook' in pieces:
            return True

        # Dois bispos ou bispo + cavalo também conseguem dar mate
        if pieces.count('Bishop') >= 2:
            return True
        if 'Bishop' in pieces and 'Knight' in pieces:
            return True
        
        # Apenas um bispo ou um cavalo: insuficiente
        if pieces in ([], ['Bishop'], ['Knight']):
            return False
        
        return True

    def f_draw(self):
        self.ui.draw(self.screen, self.selected_piece, self)
        self.ui.draw_captured_pieces(self.screen, self.captured_black, 660, 380)
        self.ui.draw_captured_pieces(self.screen, self.captured_white, 660, 40)
