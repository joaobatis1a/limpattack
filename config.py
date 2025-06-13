import os
import sys

BASE_WIN_WIDTH = 1280/2 #640
BASE_WIN_HEIGHT = 960/2#480
MENU_OVERLAY_COLOR = (0, 0, 0, 170)

TILESIZE = 32
FPS = 30

UP_LAYER = 5
PLAYER_LAYER = 4
MID_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1
DOWN_LAYER = 0

PLAYER_SPEED = 8

RED = (255,0,0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
LIGHT_ORANGE = (255, 204, 102)
CHARACTER_BG = (184, 200, 168)
ENEYMY_BG = (0, 0, 0)          
TERRAIN_BG = (0, 0, 0)         

fases = [True, True, True, True, True, True]

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)