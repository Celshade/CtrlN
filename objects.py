import random

import pygame

from player import Player
from config import (GROUND_Y, ORB_SIZE, ORB_SPEED,
                    ORB_MIN_MARGIN, ORB_MAX_MARGIN, ORANGE,
                    TREE_SIZE, TREE_SPEED,
                    WINDOW_WIDTH)



# ==================== #
# ### GAME OBJECTS ### #
# ==================== #
class Tree:
    def __init__(self, x_pos) -> None:
        self.x_pos = x_pos
        # Position tree so its bottom aligns with the ground
        self.y_pos = GROUND_Y - TREE_SIZE - 10

        # Load tree sprite
        try:
            tree_image = pygame.image.load("assets/tree_obj.png")
            self.image = pygame.transform.scale(tree_image, (TREE_SIZE, TREE_SIZE))
        except Exception as e:
            print(f"Warning: Could not load tree image: {e}")
            # Fallback to a simple rectangle if image fails
            self.image = pygame.Surface((TREE_SIZE, TREE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (139, 69, 19), (0, 0, TREE_SIZE, TREE_SIZE))

        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        self.x_pos += TREE_SPEED
        self.rect.x = int(self.x_pos)

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)

    def is_off_screen(self) -> bool:
        return self.x_pos < -TREE_SIZE

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
