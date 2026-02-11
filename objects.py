import random

import pygame
from PIL import Image

from player import Player
from config import (
    GROUND_Y, ORB_SIZE, OBJECT_SPEED, ORB_MIN_MARGIN, ORB_MAX_MARGIN, ORANGE,
    TREE_SIZE, OBJECT_SPEED, PERCHED_BIRD_SIZE
)



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
            self.image = pygame.transform.scale(tree_image,
                                                (TREE_SIZE, TREE_SIZE))
        except Exception as e:
            print(f"Warning: Could not load tree image: {e}")
            # Fallback to a simple rectangle if image fails
            self.image = pygame.Surface((TREE_SIZE, TREE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(self.image,
                             (139, 69, 19), (0, 0, TREE_SIZE, TREE_SIZE))

        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        self.x_pos += OBJECT_SPEED
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


class BirdPerched:
    """A bird perched at the tip of a tree, with a chance to fly."""
    # Class-level animation frames (shared across all flying birds)
    flying_animation_frames = []

    def __init__(self, tree: 'Tree') -> None:
        # Load flying animation frames once on first instantiation
        if not BirdPerched.flying_animation_frames:
            BirdPerched.flying_animation_frames = self._load_flying_animation()

        self.tree = tree
        self.scored = False

        # 33% chance to start flying
        self.is_flying = random.random() < 0.33

        if self.is_flying:
            # Flying state
            self.animation_frame = 0
            self.animation_counter = 0
            self.x_pos = self.tree.x_pos + (TREE_SIZE - PERCHED_BIRD_SIZE) // 2
            self.y_pos = self.tree.y_pos - PERCHED_BIRD_SIZE + 43
            self.y_start = self.y_pos
            self.transition_frame = 0  # Counter for 5-frame transition
            self.y_distance_per_frame = 200 / 10  # 20 pixels per frame

            # Use flying animation
            if BirdPerched.flying_animation_frames:
                self.image = BirdPerched.flying_animation_frames[0]
            else:
                # Fallback
                self.image = pygame.Surface((PERCHED_BIRD_SIZE, PERCHED_BIRD_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(self.image, (255, 200, 0), (0, 0, PERCHED_BIRD_SIZE, PERCHED_BIRD_SIZE))
        else:
            # Perched state - original behavior
            # Load and scale the perched bird image
            try:
                bird_image = pygame.image.load("assets/BirdPerched.png")
                self.image = pygame.transform.scale(bird_image,
                                                    (PERCHED_BIRD_SIZE, PERCHED_BIRD_SIZE))
            except Exception as e:
                print(f"Warning: Could not load perched bird image: {e}")
                # Fallback to a simple rectangle if image fails
                self.image = pygame.Surface((PERCHED_BIRD_SIZE, PERCHED_BIRD_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(self.image,
                                 (255, 200, 0), (0, 0, PERCHED_BIRD_SIZE, PERCHED_BIRD_SIZE))

            self.update_position()

        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        self.mask = pygame.mask.from_surface(self.image)

    def _load_flying_animation(self):
        """Load and cache all frames from BirdFlying.gif."""
        frames = []
        try:
            pil_image = Image.open("assets/BirdFlying.gif")

            try:
                while True:
                    frame = pil_image.convert("RGBA")
                    frame = frame.resize((ORB_SIZE, ORB_SIZE),
                                         Image.Resampling.LANCZOS)
                    pygame_frame = pygame.image.fromstring(
                        frame.tobytes(), frame.size, frame.mode
                    )
                    frames.append(pygame_frame)
                    pil_image.seek(pil_image.tell() + 1)
            except EOFError:
                pass  # End of frames
        except Exception as e:
            print(f"Warning: Could not load bird flying animation: {e}")
        return frames

    def update_position(self) -> None:
        """Update bird position based on tree position (at the tip)."""
        # Position bird at the tip of the tree (center-top area)
        self.x_pos = self.tree.x_pos + (TREE_SIZE - PERCHED_BIRD_SIZE) // 2
        self.y_pos = self.tree.y_pos - PERCHED_BIRD_SIZE + 43  # Slightly above the tree top
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))

    def update(self) -> None:
        """Update bird state."""
        if self.is_flying:
            # Flying behavior
            self.x_pos += OBJECT_SPEED
            self.rect.x = int(self.x_pos)

            # Move up over 7 frames
            if self.transition_frame < 7:
                self.y_pos -= self.y_distance_per_frame
                self.transition_frame += 1

            # Animate bird (cycle through frames)
            if BirdPerched.flying_animation_frames:
                self.animation_counter += 1
                if self.animation_counter >= 2:  # Each frame lasts 2 updates
                    self.animation_counter = 0
                    self.animation_frame = (self.animation_frame + 1) % len(BirdPerched.flying_animation_frames)
                    self.image = BirdPerched.flying_animation_frames[self.animation_frame]
                    # Update rect and mask with new frame
                    self.rect = self.image.get_rect(
                        topleft=(self.x_pos, self.y_pos)
                    )
                    self.mask = pygame.mask.from_surface(self.image)
        else:
            # Perched behavior - follow the tree
            self.update_position()

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)

    def is_off_screen(self) -> bool:
        return self.x_pos < -PERCHED_BIRD_SIZE

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


#   or just create separate classes for each instance of a flying obj (Bird)
class Orb:
    # Class-level animation frames (shared across all orbs)
    animation_frames = []

    def __init__(self, x_pos) -> None:
        # Load animation frames once on first instantiation
        if not Orb.animation_frames:
            Orb.animation_frames = self._load_bird_animation()

        self.x_pos = x_pos
        # Position orb randomly with margins
        min_y = ORB_MIN_MARGIN
        max_y = GROUND_Y - ORB_SIZE - ORB_MAX_MARGIN
        self.y_pos = random.randint(min_y, max_y)
        self.scored = False

        # Animation state
        self.animation_frame = 0
        self.animation_counter = 0

        # Use first frame for initial rect
        if Orb.animation_frames:
            self.image = Orb.animation_frames[0]
        else:
            # Fallback to orange circle if animation fails to load
            self.image = pygame.Surface((ORB_SIZE, ORB_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(self.image, ORANGE,
                              (ORB_SIZE // 2, ORB_SIZE // 2), ORB_SIZE // 2)

        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        self.mask = pygame.mask.from_surface(self.image)

    def _load_bird_animation(self):
        """Load and cache all frames from BirdFlying.gif."""
        frames = []
        try:
            pil_image = Image.open("assets/BirdFlying.gif")

            try:
                while True:
                    frame = pil_image.convert("RGBA")
                    frame = frame.resize((ORB_SIZE, ORB_SIZE),
                                         Image.Resampling.LANCZOS)
                    pygame_frame = pygame.image.fromstring(
                        frame.tobytes(), frame.size, frame.mode
                    )
                    frames.append(pygame_frame)
                    pil_image.seek(pil_image.tell() + 1)
            except EOFError:
                pass  # End of frames
        except Exception as e:
            print(f"Warning: Could not load bird animation: {e}")
        return frames

    def update(self) -> None:
        self.x_pos += OBJECT_SPEED
        self.rect.x = int(self.x_pos)

        # Animate bird (cycle through frames)
        if Orb.animation_frames:
            self.animation_counter += 1
            if self.animation_counter >= 2:  # Each frame lasts 2 updates
                self.animation_counter = 0
                self.animation_frame = (self.animation_frame + 1) % len(Orb.animation_frames)
                self.image = Orb.animation_frames[self.animation_frame]
                # Update rect and mask with new frame
                self.rect = self.image.get_rect(
                    topleft=(self.x_pos, self.y_pos)
                )
                self.mask = pygame.mask.from_surface(self.image)

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
