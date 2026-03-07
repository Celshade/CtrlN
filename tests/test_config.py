"""Tests for src/ctrln/config.py"""

import pytest

from ctrln.config import (
    BLACK,
    FPS,
    GRAVITY,
    GREEN,
    GROUND_HEIGHT,
    GROUND_Y,
    KEY_POWER,
    OBJECT_SPEED,
    ORANGE,
    PLAYER_SIZE,
    PLAYER_START_X,
    PLAYER_START_Y,
    RED,
    SCALE,
    SKY_BLUE,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    YELLOW,
    GameState,
)


# ------------------------------------------------------------------ #
# GameState enum                                                      #
# ------------------------------------------------------------------ #

class TestGameState:
    def test_all_states_exist(self):
        assert hasattr(GameState, "CHARACTER_SELECT")
        assert hasattr(GameState, "MENU")
        assert hasattr(GameState, "PLAYING")
        assert hasattr(GameState, "GAME_OVER")

    def test_states_are_distinct(self):
        values = [s.value for s in GameState]
        assert len(values) == len(set(values))

    def test_states_are_comparable(self):
        assert GameState.MENU != GameState.PLAYING
        assert GameState.PLAYING == GameState.PLAYING


# ------------------------------------------------------------------ #
# Window / display constants                                          #
# ------------------------------------------------------------------ #

class TestWindowConstants:
    def test_positive_dimensions(self):
        assert WINDOW_WIDTH > 0
        assert WINDOW_HEIGHT > 0

    def test_width_greater_than_height(self):
        """Landscape orientation assumed by the layout code."""
        assert WINDOW_WIDTH > WINDOW_HEIGHT

    def test_fps_positive(self):
        assert FPS > 0

    def test_scale_positive(self):
        assert SCALE > 0


# ------------------------------------------------------------------ #
# Derived / computed constants                                        #
# ------------------------------------------------------------------ #

class TestDerivedConstants:
    def test_ground_y_below_center(self):
        assert GROUND_Y > WINDOW_HEIGHT // 2

    def test_ground_y_plus_height_equals_window_height(self):
        assert GROUND_Y + GROUND_HEIGHT == WINDOW_HEIGHT

    def test_player_size_scaled(self):
        assert PLAYER_SIZE == int(25 * SCALE)

    def test_player_start_positions_on_screen(self):
        assert 0 <= PLAYER_START_X < WINDOW_WIDTH
        assert 0 <= PLAYER_START_Y < WINDOW_HEIGHT


# ------------------------------------------------------------------ #
# Physics constants                                                   #
# ------------------------------------------------------------------ #

class TestPhysicsConstants:
    def test_gravity_positive(self):
        assert GRAVITY > 0

    def test_key_power_negative(self):
        """Key press impulse should push the player upward (negative Y)."""
        assert KEY_POWER < 0

    def test_object_speed_negative(self):
        """Objects move left (negative X direction)."""
        assert OBJECT_SPEED < 0


# ------------------------------------------------------------------ #
# Color constants                                                     #
# ------------------------------------------------------------------ #

def _valid_rgb(color) -> bool:
    return (
        isinstance(color, tuple)
        and len(color) == 3
        and all(isinstance(c, int) and 0 <= c <= 255 for c in color)
    )


class TestColors:
    @pytest.mark.parametrize("color,name", [
        (WHITE,    "WHITE"),
        (BLACK,    "BLACK"),
        (RED,      "RED"),
        (GREEN,    "GREEN"),
        (YELLOW,   "YELLOW"),
        (SKY_BLUE, "SKY_BLUE"),
        (ORANGE,   "ORANGE"),
    ])
    def test_colors_are_valid_rgb(self, color, name):
        assert _valid_rgb(color), f"{name} is not a valid RGB tuple"

    def test_white_is_255_255_255(self):
        assert WHITE == (255, 255, 255)

    def test_black_is_0_0_0(self):
        assert BLACK == (0, 0, 0)

    def test_colors_are_distinct(self):
        colors = [WHITE, BLACK, RED, GREEN, YELLOW, SKY_BLUE, ORANGE]
        assert len(colors) == len(set(colors))
