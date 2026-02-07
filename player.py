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

        # Load keypress animation frames once at initialization
        self.keypress_animation_frames = self._load_keypress_animation()
        self.animation_frame = 0
        self.playing_animation = False

    def _load_keypress_animation(self):
        """Load and cache all frames from the keypress animation webp."""
        frames = []
        try:
            pil_image = Image.open("assets/keypress_with_thruster+fx.webP")

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

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)

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
