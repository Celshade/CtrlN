import pygame

from config import *


# ==================== #
# ### Player Class ### #
# ==================== #
class Player:
    def __init__(self) -> None:
        self.x_pos = PLAYER_START_X
        self.y_pos = PLAYER_START_Y
        self.vel = 0
        self.size = PLAYER_SIZE

        # Load player sprite
        self.image = pygame.image.load("assets/player.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))

    def update(self) -> None:
        self.vel += GRAVITY
        self.y_pos += self.vel
        self.rect.topleft = (self.x_pos, self.y_pos)

    def keypress(self) -> None:
        self.vel = KEY_POWER

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)

    def is_dead(self) -> bool:
        return self.y_pos + self.size >= GROUND_Y or self.y_pos < 0
