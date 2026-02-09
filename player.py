import pygame
from PIL import Image

from config import (PLAYER_START_X, PLAYER_START_Y, PLAYER_SIZE,
                    GRAVITY, KEY_POWER, GROUND_Y, FPS)


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
        self.mask = pygame.mask.from_surface(self.image)

        # Load keypress animation frames once at initialization
        self.keypress_animation_frames = self._load_keypress_animation()
        self.animation_frame = 0
        self.playing_animation = False

        # Load shield sprite
        self.shield_image = pygame.image.load("assets/shield.png")
        self.shield_image = pygame.transform.scale(self.shield_image,
                                                   (self.size, self.size))

        # Shield state
        self.shield_charges = 0  # Current number of shields (0-2 max)
        self.next_shield_threshold = 5  # Score at which we grant the next shield

    def _load_keypress_animation(self):
        """Load and cache all frames from the keypress animation webp."""
        frames = []
        try:
            pil_image = Image.open("assets/keypress_thruster_fx.webP")

            try:
                while True:
                    frame = pil_image.convert("RGBA")
                    frame = frame.resize((self.size, self.size),
                                         Image.Resampling.LANCZOS)
                    pygame_frame = pygame.image.fromstring(
                        frame.tobytes(), frame.size, frame.mode
                    )
                    frames.append(pygame_frame)
                    pil_image.seek(pil_image.tell() + 1)
            except EOFError:
                pass  # End of frames
        except Exception as e:
            print(f"Warning: Could not load keypress animation: {e}")
        return frames

    def update(self) -> None:
        self.vel += GRAVITY
        self.y_pos += self.vel
        self.rect.topleft = (self.x_pos, self.y_pos)

        # Update animation frame
        if self.playing_animation:
            self.animation_frame += 1
            if self.animation_frame >= len(self.keypress_animation_frames):
                self.playing_animation = False
                self.animation_frame = 0

    def keypress(self) -> None:
        self.vel = KEY_POWER
        # Trigger the keypress animation
        if self.keypress_animation_frames:
            self.animation_frame = 0
            self.playing_animation = True

    def has_shield(self, score) -> bool:
        """Check if shield is currently active."""
        # Grant a new shield when reaching next threshold (capped at 2)
        if score >= self.next_shield_threshold and self.shield_charges < 2:
            self.shield_charges += 1
            self.next_shield_threshold += 5

        return self.shield_charges > 0

    def destroy_shield(self) -> None:
        """Destroy the shield when hit."""
        if self.shield_charges > 0:
            self.shield_charges -= 1

    def draw(self, screen, score=0) -> None:
        # Only draw player sprite if animation is not active
        if not self.playing_animation:
            screen.blit(self.image, self.rect)

        # Draw shield if active (score >= 5 and not broken)
        if self.has_shield(score):
            screen.blit(self.shield_image, self.rect)

        # Draw keypress animation if active
        if (self.playing_animation
            and self.animation_frame < len(self.keypress_animation_frames)
        ):
            current_frame = self.keypress_animation_frames[self.animation_frame]
            anim_rect = current_frame.get_rect(
                center=(self.rect.centerx, self.rect.centery)
            )
            screen.blit(current_frame, anim_rect)

    def is_dead(self) -> bool:
        return self.y_pos + self.size >= GROUND_Y or self.y_pos < 0
