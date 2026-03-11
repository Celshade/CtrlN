import pygame

from achievements import ACHIEVEMENT_REGISTRY
from config import (
    SCALE,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    BLACK, WHITE, RED,
)

# Frames to display each achievement notification banner (~3 s at 60 FPS)
NOTIFICATION_DURATION = 180


# ============= #
# ### UI HUD ### #
# ============= #
class UI:
    """Stateless renderer for menu, game-over, and achievement notification HUD."""

    def __init__(self) -> None:
        self.font_large = pygame.font.Font(None, int(36 * SCALE))
        self.font_small = pygame.font.Font(None, int(36 * SCALE))
        self.font_tutorial = pygame.font.Font(None, int(18 * SCALE))

    # ------------------------------------------------------------------ #
    # Screen overlays                                                      #
    # ------------------------------------------------------------------ #

    def draw_menu(self, screen: pygame.Surface, high_score: int) -> None:
        title1 = self.font_large.render("Clacky", True, BLACK)
        title2 = self.font_large.render("Key", True, BLACK)
        subtitle = self.font_small.render("Press SPACE to Start", True, BLACK)
        high_score_text = self.font_small.render(
            f"High Score: {high_score}", True, BLACK
        )

        screen.blit(title1,
                    (WINDOW_WIDTH // 2 - title1.get_width() // 2, 100))
        screen.blit(title2,
                    (WINDOW_WIDTH // 2 - title2.get_width() // 2, 250))
        screen.blit(subtitle,
                    (WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 450))
        screen.blit(
            high_score_text,
            (WINDOW_WIDTH // 2 - high_score_text.get_width() // 2, 1025)
        )

    def draw_game_over(
        self, screen: pygame.Surface, score: int, high_score: int
    ) -> None:
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        game_over = self.font_large.render("Game Over", True, RED)
        score_text = self.font_small.render(f"Score: {score}", True, WHITE)
        high_score_surf = self.font_small.render(
            f"High Score: {high_score}", True, WHITE
        )
        restart = self.font_small.render("Press SPACE to Restart", True, WHITE)

        y = 250
        screen.blit(
            game_over,
            (WINDOW_WIDTH // 2 - game_over.get_width() // 2, y)
        )
        screen.blit(
            score_text,
            (WINDOW_WIDTH // 2 - score_text.get_width() // 2, y + 625)
        )
        screen.blit(
            high_score_surf,
            (WINDOW_WIDTH // 2 - high_score_surf.get_width() // 2, y + 775)
        )
        screen.blit(
            restart,
            (WINDOW_WIDTH // 2 - restart.get_width() // 2, y + 220)
        )

    def draw_achievement_notification(
        self,
        screen: pygame.Surface,
        queue: list[str],
        frames: int,
    ) -> int:
        """Render the topmost queued achievement banner.

        Mutates *queue* in-place (pops expired entries).
        Returns the updated frame counter for the caller to store.
        """
        if not queue:
            return 0

        frames += 1
        if frames > NOTIFICATION_DURATION:
            queue.pop(0)
            frames = 0
            if not queue:
                return 0

        aid = queue[0]
        entry = ACHIEVEMENT_REGISTRY.get(aid)
        if entry is None:
            return frames

        label = f"Achievement unlocked: {entry.name}"
        text_surf = self.font_tutorial.render(label, True, BLACK)
        padding = 12
        banner_w = text_surf.get_width() + padding * 2
        banner_h = text_surf.get_height() + padding * 2
        banner_x = WINDOW_WIDTH // 2 - banner_w // 2
        banner_y = 20

        banner = pygame.Surface((banner_w, banner_h), pygame.SRCALPHA)
        banner.fill((255, 215, 0, 210))  # gold, semi-transparent
        screen.blit(banner, (banner_x, banner_y))
        screen.blit(text_surf, (banner_x + padding, banner_y + padding))

        return frames
