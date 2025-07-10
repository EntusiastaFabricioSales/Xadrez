import sys
import pygame
from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.Menu import Menu
from code.Controller import Controller

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while True:
            menu = Menu(self.window)  # retorna "play" ou "quit"
            menu_return = menu.run()

            if menu_return in [MENU_OPTION[0]]:
                pass
            elif menu_return in [MENU_OPTION[1]]:
                controller = Controller(self.window)
                running = True
                state = "game"
            elif  menu_return in [MENU_OPTION[2]]:
                running = False
                pygame.quit()
                quit()
            else:
                pygame.quit()
                sys.exit()

            while running:
                for event in pygame.event.get():
                    result = controller.handle_event(event)
                    if event.type == pygame.QUIT or result == "menu":
                        running = False
                    
                controller.update()
                controller.f_draw()
                pygame.display.flip()
                clock.tick(60)