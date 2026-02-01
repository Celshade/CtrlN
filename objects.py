import random

import pygame

from player import Player
from config import (WINDOW_HEIGHT, GROUND_Y, PIPE_GAP, PIPE_WIDTH,
                    PIPE_MIN_MARGIN, PIPE_MAX_MARGIN, PIPE_SPEED)


# ==================== #
# ### GAME OBJECTS ### #
# ==================== #
class Pipe:
    def __init__(self, x_pos) -> None:
        self.x_pos = x_pos
        # Position gap randomly with margins
        min_gap = PIPE_MIN_MARGIN
        max_gap = GROUND_Y - PIPE_GAP - PIPE_MAX_MARGIN
        self.gap_start = random.randint(min_gap, max_gap)
        self.gap_end = self.gap_start + PIPE_GAP
        self.scored = False

        # Load pipe sprite
        self.pipe_image = pygame.image.load("assets/pipe.png")
        # Scale the pipe image to fit the PIPE_WIDTH
        self.pipe_image = pygame.transform.scale(
            self.pipe_image, (PIPE_WIDTH, WINDOW_HEIGHT)
        )

    def update(self) -> None:
        self.x_pos += PIPE_SPEED

    def draw(self, screen) -> None:
        # Top pipe - scale to gap_start height
        top_pipe = pygame.transform.scale(self.pipe_image,
                                          (PIPE_WIDTH, self.gap_start))
        screen.blit(top_pipe, (self.x_pos, 0))

        # Bottom pipe - scale to the height needed
        bottom_height = GROUND_Y - self.gap_end
        bottom_pipe = pygame.transform.scale(self.pipe_image,
                                             (PIPE_WIDTH, bottom_height))
        screen.blit(bottom_pipe, (self.x_pos, self.gap_end))

    def is_off_screen(self) -> int:
        return self.x_pos < -PIPE_WIDTH

    def collides_with(self, player: Player) -> bool:
        # NOTE: player is effectively a 68x68 square for now
        # TODO: Add sprite masking for more accurate collision?
        player_rect = pygame.Rect(player.x_pos, player.y_pos,
                                  player.size, player.size)
        top_rect = pygame.Rect(self.x_pos, 0, PIPE_WIDTH, self.gap_start)
        bottom_rect = pygame.Rect(self.x_pos, self.gap_end,
                                  PIPE_WIDTH, GROUND_Y - self.gap_end)

        return (player_rect.colliderect(top_rect)
                or player_rect.colliderect(bottom_rect))
