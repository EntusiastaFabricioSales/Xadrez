import pygame
import os

from code.Const import LIGHT, DARK, TILE_SIZE, WIN_WIDTH, WIN_HEIGHT
 
class UI:

    def __init__(self, board):
        self.board = board
        self.piece_images = self.load_images()

    def load_images(self):
        names = [
                    "bb", "bk", "bn", "bp", "bq", "br",
                    "wb", "wk", "wn", "wp", "wq", "wr"
                ]
        images = {}

        for n in names:
            icon = pygame.image.load(os.path.join("assets", f"{n}.png"))
            images[n] = pygame.transform.scale(icon, (TILE_SIZE, TILE_SIZE))
        
        return images

    def draw(self, screen, selected_piece, controller):

         # 🟫 Fundo da área das peças capturadas
        pygame.draw.rect(screen, (220, 220, 220), (640, 0, 260, 640))  # fundo lateral

        pygame.draw.rect(screen, (180, 180, 180), (660, 30, 220, 270), border_radius=10)  # peças capturadas pretas
        pygame.draw.rect(screen, (180, 180, 180), (660, 340, 220, 270), border_radius=10)  # peças capturadas brancas

        self.draw_endgame(screen, controller)

        if controller.winner or controller.draw or controller.game_paused:
            return

        #Tabuleiro
        for row in range(8):
            for col in range(8):
                color = LIGHT if (row + col) % 2 == 0 else DARK
                pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

                piece = self.board.get_piece(row, col)
                if piece:
                    if not (controller.animation and (row, col) == controller.animation[2]):
                        screen.blit(self.piece_images[self.get_name_image(piece)], (col * TILE_SIZE, row * TILE_SIZE))

        if controller.selected_piece:
            self.highlight_moves(screen, controller.valid_moves)
        
        if hasattr(controller, 'invalid_move_pos'):
            elapsed = pygame.time.get_ticks() - controller.invalid_timer
            if elapsed < 800:  # mostra por 800ms
                r, c = controller.invalid_move_pos
                pygame.draw.rect(screen, (255, 0, 0), (c*80, r*80, 80, 80), 4)
            else:
                del controller.invalid_move_pos
                del controller.invalid_timer

        #Seleção
        if selected_piece:
            pygame.draw.rect(
                screen, 
                (0, 255, 0),
                (selected_piece.col * TILE_SIZE, selected_piece.row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                3
            )

        #cronometro
        font = pygame.font.SysFont("Arial", 24)

        def format_time(ms):
            total_seconds = max(ms // 1000, 0)
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes:02}:{seconds:02}"

        white_color = None
        black_color = None
        if controller.current_turn == 'white':
            white_color = (0, 128, 0)
            black_color = (0, 0, 0)
        else:
            black_color = (0, 128, 0)
            white_color = (0, 0, 0)

        black_time = format_time(controller.time_black)
        black_timer_text = font.render(f"{black_time}", True, black_color)
        screen.blit(black_timer_text, (665, 0))

        # Tempo do jogador branco (parte inferior do painel)
        white_time = format_time(controller.time_white)
        white_timer_text = font.render(f"{white_time}", True, white_color)
        screen.blit(white_timer_text, (665, 620 - 280))  # refletido verticalmente

        #Promoção
        if controller.promotion_pending:
            options = ['queen', 'rook', 'bishop', 'night']
            for i, name in enumerate(options):
                rect = pygame.Rect(160 + i * 80, 280, 64, 64)
                img = self.piece_images[f"{controller.current_turn[0]}{name[0]}"]
                screen.blit(img, rect)

        #Animação
        if controller.animation:
            piece, start, end, progress = controller.animation
            img = self.piece_images[self.get_name_image(piece)]

            sx, sy = start[1] * TILE_SIZE, start[0] * TILE_SIZE
            ex, ey = end[1] * TILE_SIZE, end[0] * TILE_SIZE

            x = sx + (ex - sx) * progress
            y = sy + (ey - sy) * progress

            screen.blit(img, (x, y))

    def draw_captured_pieces(self, screen, captured, x, y_start):
        for i, piece in enumerate(captured):
            img = self.piece_images[self.get_name_image(piece)]

            col = i % 4
            row = i // 4
            screen.blit(img, (x + col * 50, y_start + row * 40))

    def draw_pausedgame(self, screen, controller):
        if controller.game_paused:
            font = pygame.font.SysFont("Arial", 60, bold=True)
            text = font.render("⏸️ PAUSADO", True, (200, 0, 0))
            screen.blit(text, text.get_rect(center=(400, 320)))

            overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

    def draw_endgame(self, screen, controller):
        render = True

        if render and controller.winner or render and controller.draw:
            pygame.draw.rect(screen, (240, 240, 240), (120, 200, 560, 240), border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), (120, 200, 560, 240), 3, border_radius=10)

            font = pygame.font.SysFont("Arial", 36, bold=True)
            msg = f"{controller.draw_reason}" if controller.draw else f"{controller.winner.capitalize()} venceu!"
            text = font.render(msg, True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=(400, 240)))

            # Botões
            button_font = pygame.font.SysFont("Arial", 28)

            self.retry_button = pygame.Rect(200, 300, 190, 50)
            self.menu_button = pygame.Rect(440, 300, 160, 50)

            pygame.draw.rect(screen, (150, 200, 100), self.retry_button, border_radius=8)
            pygame.draw.rect(screen, (100, 150, 250), self.menu_button, border_radius=8)

            retry_text = button_font.render("Jogar Novamente", True, (255, 255, 255))
            menu_text = button_font.render("Menu Inicial", True, (255, 255, 255))

            screen.blit(retry_text, retry_text.get_rect(center=self.retry_button.center))
            screen.blit(menu_text, menu_text.get_rect(center=self.menu_button.center))

            for evento in pygame.event.get():
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.menu_button.collidepoint(x, y):
                        pygame.quit()
                        render = False
                        break

    def highlight_moves(self, screen, valid_moves):
        for row, col in valid_moves:
            pygame.draw.rect(screen, (255, 255, 0), (col * 80, row * 80, 80, 80), 4)  # amarelo vibrante

    def get_square_under_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        row = mouse_y // TILE_SIZE
        col = mouse_x // TILE_SIZE
        return row, col

    def get_name_image(self, piece):
        char_class = piece.__class__.__name__[0].lower()

        if piece.__class__.__name__ == 'Knight':
            char_class = 'n'
        
        name = f"{piece.color[0].lower()}{char_class}"
        
        return name
        