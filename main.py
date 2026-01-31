#!/usr/bin/env python3

import os
import sys

import pygame

from config import *  # TODO refine
from objects import Pipe
from player import Player


# =================== #
# ### ENTRY POINT ### #
# =================== #
def main() -> None:
    # NOTE: if we keep terminal output, implement Rich to make it look good
    # System data
    print(
        f"\n{'=' * 79}",
        "\nGAME - STARTING",
        f"\n{'=' * 79}",
        f"\nDisplay: {os.environ.get('DISPLAY', 'NOT SET')}",
        f"\nPython: {sys.version.split()[0]}"
    )

    # Initialize Pygame
    pygame.init()
    print(f"Pygame initialized")  # System data
    print(f"Display driver: {pygame.display.get_driver()}")  # System data
    print(f"{'=' * 79}\n")

    # Run the game
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"\n[ERROR] {e}")

        import traceback
        traceback.print_exc()
        sys.exit(1)


# =================== #
# ### GAME ENGINE ### #
# =================== #
class Game:
    def __init__(self):
        print("Creating window...")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                              pygame.SHOWN)
        pygame.display.set_caption("Clacky Key")  # window title
        print("Window created!")

        self.clock = pygame.time.Clock()  # init game clock
        self.font_large = pygame.font.Font(None, int(36 * SCALE))
        self.font_small = pygame.font.Font(None, int(36 * SCALE))

        self.state = GameState.MENU
        self.score = 0
        self.high_score = 0

        self.player = Player()  # init player
        self.pipes = []
        self.pipe_timer = 0

        # Load background with parallax support
        bg_path = os.path.join(os.path.dirname(__file__),
                               'assets', 'day_level.gif')
        self.bg_image = pygame.image.load(bg_path)
        self.bg_image = pygame.transform.scale(self.bg_image,
                                               (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_offset = 0  # Parallax offset
        self.parallax_speed = 0.3  # Parallax speed factor

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if self.state == GameState.MENU:
                        self.start_game()
                    elif self.state == GameState.PLAYING:
                        self.player.keypress()
                    elif self.state == GameState.GAME_OVER:
                        self.state = GameState.MENU
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.MENU:
                    self.start_game()
                elif self.state == GameState.PLAYING:
                    self.player.keypress()
                elif self.state == GameState.GAME_OVER:
                    self.state = GameState.MENU
        return True

    def start_game(self):
        self.state = GameState.PLAYING
        self.score = 0
        self.player = Player()
        self.pipes = []
        self.pipe_timer = 0
        self.bg_offset = 0  # Reset parallax offset

    def update(self):
        if self.state != GameState.PLAYING:
            return

        self.player.update()

        # Update parallax background
        self.bg_offset += PIPE_SPEED * self.parallax_speed
        # Wrap the background offset for seamless scrolling
        if self.bg_offset < -WINDOW_WIDTH:
            self.bg_offset += WINDOW_WIDTH

        # Spawn pipes
        self.pipe_timer += 1
        if self.pipe_timer >= PIPE_SPAWN_RATE:
            self.pipes.append(Pipe(WINDOW_WIDTH))
            self.pipe_timer = 0

        # Update pipes
        for pipe in self.pipes:
            pipe.update()
            if pipe.x + PIPE_WIDTH < self.player.x and not pipe.scored:
                pipe.scored = True
                self.score += 1

        # Remove off-screen pipes
        self.pipes = [p for p in self.pipes if not p.is_off_screen()]

        # Check collisions
        for pipe in self.pipes:
            if pipe.collides_with(self.player):
                self.end_game()
                return

        if self.player.is_dead():
            self.end_game()

    def end_game(self):
        self.state = GameState.GAME_OVER
        if self.score > self.high_score:
            self.high_score = self.score

    def draw(self):
        # Draw background with parallax scrolling
        self.screen.blit(self.bg_image, (int(self.bg_offset), 0))
        # Draw second copy of background for seamless scrolling
        self.screen.blit(self.bg_image, (int(self.bg_offset + WINDOW_WIDTH), 0))

        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)

        # Draw ground
        pygame.draw.rect(self.screen, GROUND_COLOR,
                         (0, GROUND_Y, WINDOW_WIDTH, GROUND_HEIGHT))

        # Draw player
        self.player.draw(self.screen)

        # Draw UI
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            score_text = self.font_large.render(str(self.score), True, BLACK)
            self.screen.blit(score_text, (20, 20))
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()

        # Flush display
        pygame.display.flip()
        pygame.display.update()

    def draw_menu(self):
        title1 = self.font_large.render("Clacky", True, BLACK)
        title2 = self.font_large.render("Key", True, BLACK)
        subtitle = self.font_small.render("Press SPACE to Start", True, BLACK)
        high_score_text = self.font_small.render(
            f"High Score: {self.high_score}", True, BLACK
        )

        self.screen.blit(title1,
                         (WINDOW_WIDTH // 2 - title1.get_width() // 2, 150))
        self.screen.blit(title2,
                         (WINDOW_WIDTH // 2 - title2.get_width() // 2, 220))
        self.screen.blit(subtitle,
                         (WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 400))
        self.screen.blit(
            high_score_text,
            (WINDOW_WIDTH // 2 - high_score_text.get_width() // 2, 500)
        )

    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Game over text
        game_over = self.font_large.render("Game Over", True, RED)
        score_text = self.font_small.render(f"Score: {self.score}",
                                            True, WHITE)
        high_score = self.font_small.render(f"High Score: {self.high_score}",
                                            True, WHITE)
        restart = self.font_small.render("Press SPACE to Restart", True, WHITE)

        y = 250
        self.screen.blit(
            game_over,
            (WINDOW_WIDTH // 2 - game_over.get_width() // 2, y)
        )
        self.screen.blit(
            score_text,
            (WINDOW_WIDTH // 2 - score_text.get_width() // 2, y + 80)
        )
        self.screen.blit(
            high_score,
            (WINDOW_WIDTH // 2 - high_score.get_width() // 2, y + 140)
        )
        self.screen.blit(
            restart,
            (WINDOW_WIDTH // 2 - restart.get_width() // 2, y + 220)
        )

    def run(self):
        print("Game loop starting...\n")
        running = True
        frame = 0

        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

            # NOTE: FPS counter
            frame += 1
            if frame % 60 == 0:
                print(f"Frame {frame}: State={self.state.name}",
                      f"Score={self.score}")

        print("\nShutting down...")
        pygame.quit()
        sys.exit()


# =================== #
# ### ENTRY POINT ### #
# =================== #
if __name__ == "__main__":
    main()
