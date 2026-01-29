import pygame

from config import *  # TODO refine


# ==================== #
# ### Player Class ### #
# ==================== #
class Player:
    def __init__(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.vel = 0
        self.size = PLAYER_SIZE

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel

    def keypress(self):
        self.vel = KEY_POWER

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(
            screen, BLACK, (self.x, self.y, self.size, self.size), 2
        )

    def is_dead(self):
        return self.y + self.size >= GROUND_Y or self.y < 0
