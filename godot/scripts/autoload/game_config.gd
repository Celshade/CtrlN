extends Node
## Global game configuration constants.

# Display (base resolution — Solana Seeker phone dimensions)
const WINDOW_WIDTH := 890
const WINDOW_HEIGHT := 400

# Player
const KEY_POWER := -8.0
const PLAYER_SIZE := 75  # 25 * SCALE
const PLAYER_START_X := 150  # 50 * SCALE
const PLAYER_START_Y := 125  # WINDOW_HEIGHT / 2 - PLAYER_SIZE / 2

# Obstacles
const OBJECT_SPEED := -24.0  # -8 * SCALE
const ORB_SIZE := 38  # PLAYER_SIZE * 0.5
const ORB_SPAWN_RATE := 30  # frames
const ORB_MIN_MARGIN := 0
const ORB_MAX_MARGIN := 75  # 25 * SCALE

const TREE_SIZE := 113  # PLAYER_SIZE * 1.5
const TREE_SPAWN_RATE := 60
const TREE_SPACING := 90  # TREE_SIZE * 0.8

const PERCHED_BIRD_SIZE := 300  # PLAYER_SIZE * 4
const PERCHED_BIRD_SPAWN_CHANCE := 0.4

# Physics
const GRAVITY := 0.69
const GROUND_HEIGHT := 38  # 12.5 * SCALE
const GROUND_Y := WINDOW_HEIGHT - GROUND_HEIGHT  # 362

# Tutorial
const TUTORIAL_DURATION := 10
const TUTORIAL_SPAWN_MULTIPLIER := 2.0
const TUTORIAL_PAUSE_FRAMES := 45
const SHIELD_EXPLANATION_PAUSE_FRAMES := 45

# Shields
const SHIELD_INVULNERABILITY_FRAMES := 15

# Spawn gap
const MIN_SPAWN_GAP := 84  # PLAYER_SIZE + 3 * SCALE

# Scale (keeping for reference, but Godot handles scaling via viewport)
const SCALE := 3.0

# ── Collision hitbox offsets (pixel-accurate, derived from sprite alpha bounds) ──
# Player: 150×150 source → 75×75 display.  Measured from player_black.png (idle frame).
# Key cap occupies src (44,15)-(106,77) → display (22,8)-(53,39), size 31×31.
const PLAYER_HITBOX_OFFSET := Vector2(22.0, 8.0)
const PLAYER_HITBOX_SIZE   := Vector2(31.0, 31.0)

# Tree sprite: 79×83 source → 113×113 display.  Opaque region covers ~(6,3)-(102,101).
const TREE_HITBOX_OFFSET := Vector2(6.0, 3.0)
const TREE_HITBOX_SIZE   := Vector2(96.0, 98.0)

# Orb (bird_fly frames): 28×26 source → 38×38 display.  Opaque ~(4,3)-(33,34).
const ORB_HITBOX_OFFSET := Vector2(4.0, 3.0)
const ORB_HITBOX_SIZE   := Vector2(29.0, 31.0)

# Perched bird (static state): BirdPerched.png is 384×256 with opaque pixels only at
# source (240,129)-(255,147).  Scaled to 300×300 → offset ≈ (188,151), size ≈ (12,22).
const PERCHED_BIRD_HITBOX_OFFSET := Vector2(188.0, 151.0)
const PERCHED_BIRD_HITBOX_SIZE   := Vector2(12.0, 22.0)

enum GameState {
	CHARACTER_SELECT,
	MENU,
	PLAYING,
	GAME_OVER,
}
