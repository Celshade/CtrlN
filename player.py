import pygame
from PIL import Image

from config import (PLAYER_START_X, PLAYER_START_Y, PLAYER_SIZE,
                    GRAVITY, KEY_POWER, GROUND_Y, FPS, SHIELD_INVULNERABILITY_FRAMES)


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

        # Load shield sprites
        self.shield_image = pygame.image.load("assets/shield_3.2.png")
        self.shield_image = pygame.transform.scale(self.shield_image,
                                                   (self.size, self.size))

        self.shield_image_tier2 = pygame.image.load("assets/shield_3.4.png")
        self.shield_image_tier2 = pygame.transform.scale(self.shield_image_tier2,
                                                         (self.size, self.size))

        # Load shield charge animation frames
        self.shield_charge_animation_frames = self._load_shield_charge_animation("assets/shield_fx3.2.webP")
        self.shield_charge_animation_frames_tier2 = self._load_shield_charge_animation("assets/shield_fx3.4.webP")
        self.shield_animation_frame = 0
        self.playing_shield_animation = False
        self.playing_shield_animation_tier2 = False

        # Shield state
        self.shield_charges = 0  # Current number of shields (0-2 max)
        self.next_shield_threshold = 5  # Score threshold for next shield

        # Invulnerability tracking
        self.invulnerability_frames = 0  # Frames remaining of invulnerability after shield break

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

    def _load_shield_charge_animation(self, filepath="assets/shield_key_fx3.2.webP"):
        """Load and cache all frames from the shield charge animation webp."""
        frames = []
        try:
            pil_image = Image.open(filepath)

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
            print(f"Warning: Could not load shield charge animation from {filepath}: {e}")
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

        # Update shield charge animation frame (tier 1)
        if self.playing_shield_animation:
            self.shield_animation_frame += 1
            if self.shield_animation_frame >= len(self.shield_charge_animation_frames):
                self.playing_shield_animation = False
                self.shield_animation_frame = 0

        # Update shield charge animation frame (tier 2)
        if self.playing_shield_animation_tier2:
            self.shield_animation_frame += 1
            if self.shield_animation_frame >= len(self.shield_charge_animation_frames_tier2):
                self.playing_shield_animation_tier2 = False
                self.shield_animation_frame = 0

        # Update invulnerability frames
        if self.invulnerability_frames > 0:
            self.invulnerability_frames -= 1

    def keypress(self) -> None:
        self.vel = KEY_POWER
        # Trigger the keypress animation
        if self.keypress_animation_frames:
            self.animation_frame = 0
            self.playing_animation = True

    def has_shield(self) -> bool:
        """Check if shield is currently active (no side effects)."""
        return self.shield_charges > 0

    def is_invulnerable(self) -> bool:
        """Check if player is currently invulnerable after shield break."""
        return self.invulnerability_frames > 0

    def update_shields(self, score) -> None:
        """Grant new shields based on score threshold."""
        # Grant a new shield when reaching next threshold (capped at 2)
        if score >= self.next_shield_threshold and self.shield_charges < 2:
            self.shield_charges += 1
            self.next_shield_threshold += 5

            # Trigger the appropriate shield charge animation based on tier
            if self.shield_charges == 1:
                # First shield charge
                if self.shield_charge_animation_frames:
                    self.shield_animation_frame = 0
                    self.playing_shield_animation = True
                    self.playing_shield_animation_tier2 = False
            elif self.shield_charges == 2:
                # Second shield charge
                if self.shield_charge_animation_frames_tier2:
                    self.shield_animation_frame = 0
                    self.playing_shield_animation = False
                    self.playing_shield_animation_tier2 = True

    def destroy_shield(self) -> None:
        """Destroy the shield when hit."""
        if self.shield_charges > 0:
            self.shield_charges -= 1
            # Reset animation flags when shield is consumed
            self.playing_shield_animation_tier2 = False
            self.playing_shield_animation = False
            # Activate brief invulnerability period after shield break
            self.invulnerability_frames = SHIELD_INVULNERABILITY_FRAMES

    def draw(self, screen, score=0) -> None:
        # Draw player sprite or keypress animation (base layer)
        if (self.playing_animation
            and self.animation_frame < len(self.keypress_animation_frames)
        ):
            current_frame = self.keypress_animation_frames[self.animation_frame]
            anim_rect = current_frame.get_rect(
                center=(self.rect.centerx, self.rect.centery)
            )
            screen.blit(current_frame, anim_rect)
        else:
            screen.blit(self.image, self.rect)

        # Draw shield charge animation if active (on top, highest priority)
        if (self.playing_shield_animation
            and self.shield_animation_frame < len(self.shield_charge_animation_frames)
        ):
            current_frame = self.shield_charge_animation_frames[self.shield_animation_frame]
            anim_rect = current_frame.get_rect(
                center=(self.rect.centerx, self.rect.centery)
            )
            screen.blit(current_frame, anim_rect, special_flags=pygame.BLEND_RGBA_MAX)
        elif (self.playing_shield_animation_tier2
            and self.shield_animation_frame < len(self.shield_charge_animation_frames_tier2)
        ):
            current_frame = self.shield_charge_animation_frames_tier2[self.shield_animation_frame]
            anim_rect = current_frame.get_rect(
                center=(self.rect.centerx, self.rect.centery)
            )
            screen.blit(current_frame, anim_rect, special_flags=pygame.BLEND_RGBA_MAX)

        # Draw shield if it's active - only when no shield charge animation
        if self.shield_charges == 2 and not self.playing_shield_animation_tier2:
            screen.blit(self.shield_image_tier2, self.rect)
        elif self.shield_charges == 1 and not self.playing_shield_animation:
            screen.blit(self.shield_image, self.rect)

    def is_dead(self) -> bool:
        return self.y_pos + self.size >= GROUND_Y or self.y_pos < -14
