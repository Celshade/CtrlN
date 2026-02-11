from enum import Enum


# ===================== #
# ### CONFIGURATION ### #
# ===================== #

# Game settings
# Display at actual Solana Seeker phone dimensions (base resolution)
WINDOW_WIDTH = 890
WINDOW_HEIGHT = 400
FPS = 60

# Scale factor (base 890x400 is the Solana Seeker display, 2670x1200 is 3x)
SCALE = 3.0

# Player
KEY_POWER = -8
PLAYER_SIZE = int(25 * SCALE)
PLAYER_START_X = int(50 * SCALE)
PLAYER_START_Y = WINDOW_HEIGHT // 2 - PLAYER_SIZE // 2

# Orbs (obstacles)  # FIXME birds
OBJECT_SPEED = int(-8 * SCALE)  # NOTE lower => faster
ORB_SIZE = int(PLAYER_SIZE * 0.5)
ORB_SPAWN_RATE = 30
ORB_MIN_MARGIN = int(25 * SCALE)  # NOTE: drastically affects game difficulty
ORB_MAX_MARGIN = int(25 * SCALE)  # NOTE: drastically affects game difficulty

# Constraints
GRAVITY = 0.69
GROUND_HEIGHT = int(12.5 * SCALE)
GROUND_Y = WINDOW_HEIGHT - GROUND_HEIGHT

# Trees (obstacles)
TREE_SIZE = int(PLAYER_SIZE * 1.5)
TREE_SPAWN_RATE = 60
TREE_SPACING = int(TREE_SIZE * 0.8)  # Horizontal spacing between trees in a group

# Perched Birds (obstacles on trees)
PERCHED_BIRD_SIZE = int(PLAYER_SIZE * 1)
PERCHED_BIRD_SPAWN_CHANCE = 0.4  # 40% chance of a bird on each tree

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
SKY_BLUE = (135, 206, 235)
ORANGE = (255, 165, 0)
# GROUND_COLOR = (34, 139, 34)


# NOTE: Breakout into a types module if we generate more than one state/type
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
