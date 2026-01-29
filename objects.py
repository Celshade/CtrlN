import random

import pygame

from config import *


# ==================== #
# ### GAME OBJECTS ### #
# ==================== #
class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_start = random.randint(80, GROUND_Y - PIPE_GAP - 80)
        self.gap_end = self.gap_start + PIPE_GAP
        self.scored = False

    def update(self):
        self.x += PIPE_SPEED

    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.gap_start))
        pygame.draw.rect(screen, BLACK,
                         (self.x, 0, PIPE_WIDTH, self.gap_start), 2)
        # Bottom pipe
        pygame.draw.rect(screen, GREEN,
            (self.x, self.gap_end, PIPE_WIDTH, GROUND_Y - self.gap_end))
        pygame.draw.rect(screen, BLACK,
            (self.x, self.gap_end, PIPE_WIDTH, GROUND_Y - self.gap_end), 2)

    def is_off_screen(self):
        return self.x < -PIPE_WIDTH

    def collides_with(self, player):
        player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_start)
        bottom_rect = pygame.Rect(self.x, self.gap_end,
                                  PIPE_WIDTH, GROUND_Y - self.gap_end)

        # NOTE
        return (player_rect.colliderect(top_rect)
                or player_rect.colliderect(bottom_rect))
