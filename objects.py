import random

import pygame

from config import *


# ==================== #
# ### GAME OBJECTS ### #
# ==================== #
class Pipe:
    def __init__(self, x):
        self.x = x
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
            self.pipe_image, (int(PIPE_WIDTH), int(WINDOW_HEIGHT))
        )

    def update(self):
        self.x += PIPE_SPEED

    def draw(self, screen):
        # Top pipe - scale to gap_start height
        top_pipe = pygame.transform.scale(self.pipe_image,
                                          (PIPE_WIDTH, self.gap_start))
        screen.blit(top_pipe, (self.x, 0))

        # Bottom pipe - scale to the height needed
        bottom_height = GROUND_Y - self.gap_end
        bottom_pipe = pygame.transform.scale(self.pipe_image,
                                             (PIPE_WIDTH, bottom_height))
        screen.blit(bottom_pipe, (self.x, self.gap_end))

    def is_off_screen(self):
        return self.x < -PIPE_WIDTH

    def collides_with(self, player):
        # NOTE: player is effectively a 68x68 square for now
        # TODO: Add sprite masking for more accurate collision?
        player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_start)
        bottom_rect = pygame.Rect(self.x, self.gap_end,
                                  PIPE_WIDTH, GROUND_Y - self.gap_end)

        return (player_rect.colliderect(top_rect)
                or player_rect.colliderect(bottom_rect))
