from enum import Enum
# ===================== #
# ### CONFIGURATION ### #
# ===================== #


class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

# Game settings
WINDOW_WIDTH = 2670
WINDOW_HEIGHT = 1200
FPS = 60

# Scale factor (2670x1200 is 6.675x 400x800)
SCALE = 6.675

GRAVITY = 0.5 * SCALE
KEY_POWER = -12 * SCALE
PIPE_GAP = int(150 * SCALE)
PIPE_WIDTH = int(80 * SCALE)
PIPE_SPEED = int(-6 * SCALE)
PIPE_SPAWN_RATE = 90

PLAYER_SIZE = int(40 * SCALE)
PLAYER_START_X = int(60 * SCALE)
PLAYER_START_Y = WINDOW_HEIGHT // 2 - int(150 * SCALE)

GROUND_HEIGHT = int(100 * SCALE)
GROUND_Y = WINDOW_HEIGHT - GROUND_HEIGHT

# Colors
SKY_BLUE = (135, 206, 235)
GROUND_COLOR = (34, 139, 34)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
