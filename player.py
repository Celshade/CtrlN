import pygame
import os

from config import *


# ==================== #
# ### Player Class ### #
# ==================== #
class Player:
    def __init__(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.vel = 0
        self.size = PLAYER_SIZE
        
        # Load player sprite
        asset_path = os.path.join(os.path.dirname(__file__), 'assets', 'player.png')
        self.image = pygame.image.load(asset_path)
        self.image = pygame.transform.scale(self.image, (int(self.size), int(self.size)))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.topleft = (self.x, self.y)

    def keypress(self):
        self.vel = KEY_POWER

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_dead(self):
        return self.y + self.size >= GROUND_Y or self.y < 0
