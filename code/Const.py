import pygame
import os

C_ORANGE = (255, 128, 0)
C_YELLOW = (255, 255, 128)
C_WHITE = (255, 255, 255)
C_GREEN = (0, 128, 0)
C_CYAN = (0, 128, 128)
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)

# M
MENU_OPTION = ('NEW GAME 1P(Unavailable)',
                'NEW GAME 2P',
               'EXIT')

# S
SPAWN_TIME = 4000

# T
TIMEOUT_STEP = 100  # 100ms
TIMEOUT_LEVEL = 20000  # 20s
TILE_SIZE = 80  

# W
WIN_WIDTH = 900
WIN_HEIGHT = 640

# S
SCORE_POS = {'Title': (WIN_WIDTH / 2, 50),
             'EnterName': (WIN_WIDTH / 2, 80),
             'Label': (WIN_WIDTH / 2, 90),
             'Name': (WIN_WIDTH / 2, 110),
             0: (WIN_WIDTH / 2, 110),
             1: (WIN_WIDTH / 2, 130),
             2: (WIN_WIDTH / 2, 150),
             3: (WIN_WIDTH / 2, 170),
             4: (WIN_WIDTH / 2, 190),
             5: (WIN_WIDTH / 2, 210),
             6: (WIN_WIDTH / 2, 230),
             7: (WIN_WIDTH / 2, 250),
             8: (WIN_WIDTH / 2, 270),
             9: (WIN_WIDTH / 2, 290),
             }