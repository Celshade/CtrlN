import pygame

from config import (
    SCALE,
    TUTORIAL_DURATION, TUTORIAL_PAUSE_FRAMES,
    SHIELD_EXPLANATION_PAUSE_FRAMES,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    BLACK, WHITE, YELLOW,
)


# ==================== #
# ### TUTORIAL HUD ### #
# ==================== #
class Tutorial:
    """Manages tutorial state and draws tutorial overlays."""

    def __init__(self) -> None:
        self._font = pygame.font.Font(None, int(18 * SCALE))
        self._image = pygame.image.load("assets/tutorial.png")

        self.active = False
        self.frames_since_start = 0
        self.shield_explanation_active = False
        self.shield_explanation_frames = 0
        self.shield_explanation_shown = False

    def reset(self) -> None:
        """Re-initialise all tutorial state for a new game."""
        self.active = True
        self.frames_since_start = 0
        self.shield_explanation_active = False
        self.shield_explanation_frames = 0
        self.shield_explanation_shown = False

    def update(self, score: int) -> bool:
        """Advance tutorial state for one frame.

        Returns True if the game loop should be paused this frame
        (i.e. the tutorial is in a hold/pause phase).
        """
        self.frames_since_start += 1

        # Hold at game start
        if self.frames_since_start <= TUTORIAL_PAUSE_FRAMES:
            return True

        # Trigger shield explanation once at 5 pts
        if score >= 5 and not self.shield_explanation_shown:
            self.shield_explanation_active = True
            self.shield_explanation_shown = True
            self.shield_explanation_frames = 0

        # Hold during shield explanation
        if self.shield_explanation_active:
            self.shield_explanation_frames += 1
            if self.shield_explanation_frames > SHIELD_EXPLANATION_PAUSE_FRAMES:
                self.shield_explanation_active = False
            return True

        # End tutorial phase when score threshold is reached
        if self.active and score >= TUTORIAL_DURATION:
            self.active = False

        return False

    def skip_pause(self) -> bool:
        """Skip whichever pause is currently active.

        Returns True if a pause was actually skipped (caller should NOT
        also trigger a jump), False if no pause was active.
        """
        if self.frames_since_start <= TUTORIAL_PAUSE_FRAMES:
            self.frames_since_start = TUTORIAL_PAUSE_FRAMES + 1
            return True
        elif self.shield_explanation_active:
            self.shield_explanation_active = False
            return True
        return False

    def draw(self, screen: pygame.Surface, score: int) -> None:
        """Draw the appropriate tutorial overlay for the current state."""
        if self.frames_since_start <= TUTORIAL_PAUSE_FRAMES:
            # Initial hold overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            title = self._font.render("Get Ready!", True, YELLOW)
            instruction = self._font.render(
                "Press SPACE or CLICK to Jump", True, WHITE
            )
            screen.blit(
                title,
                (WINDOW_WIDTH // 2 - title.get_width() // 2,
                 WINDOW_HEIGHT // 2 - 150)
            )
            screen.blit(
                instruction,
                (WINDOW_WIDTH // 2 - instruction.get_width() // 2,
                 WINDOW_HEIGHT // 2 + 50)
            )

        elif self.shield_explanation_active:
            # Shield explanation overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            text = self._font.render(
                "Every 5 points, a shield charge will regenerate.",
                True,
                WHITE,
            )
            screen.blit(text, (20, WINDOW_HEIGHT - 100))

        elif self.active:
            # In-progress tutorial: image + progress bar
            img_rect = self._image.get_rect(
                bottomleft=(-150, WINDOW_HEIGHT + 175)
            )
            screen.blit(self._image, img_rect)

            progress_text = self._font.render(
                f"Progress: {score}/{TUTORIAL_DURATION}",
                True,
                YELLOW,
            )
            screen.blit(progress_text, (10, WINDOW_HEIGHT - 50))
