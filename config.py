from enum import Enum


# ===================== #
# ### CONFIGURATION ### #
# ===================== #

# Game settings
WINDOW_WIDTH = 2670
WINDOW_HEIGHT = 1200
FPS = 60

# Scale factor (2670x1200 is 6.675x 400x800)
SCALE = 6.675

# Objects
PIPE_GAP = int(150 * SCALE)
PIPE_WIDTH = int(80 * SCALE)
PIPE_SPEED = int(-6 * SCALE)
PIPE_SPAWN_RATE = 90

# Player
KEY_POWER = -9
PLAYER_SIZE = int(20 * SCALE)
PLAYER_START_X = int(60 * SCALE)
PLAYER_START_Y = WINDOW_HEIGHT // 2 - PLAYER_SIZE // 2

# Contraints
GRAVITY = 0.5
GROUND_HEIGHT = int(50 * SCALE)
GROUND_Y = WINDOW_HEIGHT - GROUND_HEIGHT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
SKY_BLUE = (135, 206, 235)
GROUND_COLOR = (34, 139, 34)


# NOTE: Breakout into a types module if we generate more than one state/type
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
