import random

import pygame

from player import Player
from config import (GROUND_Y, ORB_SIZE, ORB_SPEED,
                    ORB_MIN_MARGIN, ORB_MAX_MARGIN, ORANGE)


# ==================== #
# ### GAME OBJECTS ### #
# ==================== #
class Orb:
    def __init__(self, x_pos) -> None:
        self.x_pos = x_pos
        # Position orb randomly with margins
        min_y = ORB_MIN_MARGIN
        max_y = GROUND_Y - ORB_SIZE - ORB_MAX_MARGIN
        self.y_pos = random.randint(min_y, max_y)
        self.scored = False

        # Create orange circle sprite
        self.image = pygame.Surface((ORB_SIZE, ORB_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ORANGE,
                          (ORB_SIZE // 2, ORB_SIZE // 2), ORB_SIZE // 2)
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        self.x_pos += ORB_SPEED
        self.rect.x = int(self.x_pos)

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)

    def is_off_screen(self) -> bool:
        return self.x_pos < -ORB_SIZE

    def collides_with(self, player: Player) -> bool:
        # Check rect collision first (broad phase)
        player_rect = pygame.Rect(player.x_pos, player.y_pos,
                                  player.size, player.size)

        if player_rect.colliderect(self.rect):
            # Use mask collision for accurate detection
            offset_x = int(self.x_pos - player.x_pos)
            offset_y = int(self.y_pos - player.y_pos)
            return player.mask.overlap(self.mask, (offset_x, offset_y))

        return False
