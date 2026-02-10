import sys

import pygame

from objects import Orb, Tree
from player import Player
from config import (
    GameState, FPS, SCALE,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    ORB_SPEED, ORB_SPAWN_RATE,
    TREE_SPEED, TREE_SPAWN_RATE,
    GROUND_Y, PLAYER_SIZE,
    BLACK, WHITE, RED
)


# =================== #
# ### GAME ENGINE ### #
# =================== #
class Game:
    def __init__(self) -> None:
        print("Creating window...")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                              pygame.SHOWN)
        pygame.display.set_caption("Clacky Key")  # window title
        print("Window created!")

        self.clock = pygame.time.Clock()  # init game clock
        self.font_large = pygame.font.Font(None, int(36 * SCALE))
        self.font_small = pygame.font.Font(None, int(36 * SCALE))

        # Menu and scoring
        self.state = GameState.MENU
        self.score = 0
        self.high_score = 0

        # Init player and prep object vars
        self.player = Player()
        self.orbs = []
        self.orb_timer = 0
        self.trees = []
        self.tree_timer = 0

        # Load background layers with parallax support
        # Format: {"image": loaded_image, "speed": parallax_speed, "offset": current_offset}
        self.bg_layers = [
            {
                "name": "sky_and_grass",
                "image": pygame.transform.scale(
                    pygame.image.load("assets/sky_and_grass.png"),
                    (WINDOW_WIDTH, WINDOW_HEIGHT)
                ),
                "speed": 0.0,  # Static - no parallax
                "offset": 0
            },
            {
                "name": "big_clouds",
                "image": pygame.transform.scale(
                    pygame.image.load("assets/big_clouds.png"),
                    (WINDOW_WIDTH, WINDOW_HEIGHT)
                ),
                "speed": 0.025,
                "offset": 0
            },
            {
                "name": "mountains",
                "image": pygame.transform.scale(
                    pygame.image.load("assets/mountains.png"),
                    (WINDOW_WIDTH, WINDOW_HEIGHT)
                ),
                "speed": 0.0,  # Static - no parallax
                "offset": 0
            },
            {
                "name": "little_clouds",
                "image": pygame.transform.scale(
                    pygame.image.load("assets/little_clouds.png"),
                    (WINDOW_WIDTH, WINDOW_HEIGHT)
                ),
                "speed": 0.05,
                "offset": 0
            },
            {
                "name": "background",
                "image": pygame.transform.scale(
                    pygame.image.load("assets/background.png"),
                    (WINDOW_WIDTH, WINDOW_HEIGHT)
                ),
                "speed": 0.04,
                "offset": 0
            },
            {
                "name": "middleground_dark",
                "image": pygame.transform.scale(
                    pygame.image.load("assets/middleground_dark.png"),
                    (WINDOW_WIDTH, WINDOW_HEIGHT)
                ),
                "speed": 0.0625,
                "offset": 0
            },
            {
                "name": "middleground_light",
                "image": pygame.transform.scale(
                    pygame.image.load("assets/middleground_light.png"),
                    (WINDOW_WIDTH, WINDOW_HEIGHT)
                ),
                "speed": 0.08,
                "offset": 0
            },
            {
                "name": "foreground",
                "image": pygame.transform.scale(
                    pygame.image.load("assets/foreground.png"),
                    (WINDOW_WIDTH, WINDOW_HEIGHT)
                ),
                "speed": 0.2,
                "offset": 0
            },
            {
                "name": "ground",
                "image": pygame.transform.scale(
                    pygame.image.load("assets/ground.png"),
                    (WINDOW_WIDTH, WINDOW_HEIGHT)
                ),
                "speed": 0.5,
                "offset": 0
            }
        ]

    def handle_gamestate(self) -> None:
        if self.state == GameState.MENU:
            self.restart_game()
        elif self.state == GameState.PLAYING:
            self.player.keypress()
        elif self.state == GameState.GAME_OVER:
            self.state = GameState.MENU

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            # Handle quit
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                # Handle escape
                if event.key == pygame.K_ESCAPE:
                    return False
                # Handle keyboard movement
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.handle_gamestate()
            # Handle mouse movement
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_gamestate()
        return True

    def restart_game(self) -> None:
        # Reset game vars
        self.state = GameState.PLAYING
        self.score = 0
        self.player = Player()
        self.orbs = []
        self.orb_timer = 0
        self.trees = []
        self.tree_timer = 0
        # Reset parallax offsets for all layers
        for layer in self.bg_layers:
            layer["offset"] = 0

    def update(self) -> None:
        if self.state != GameState.PLAYING:
            return

        self.player.update()  # Update the Player

        # Update parallax background layers
        for layer in self.bg_layers:
            if layer["speed"] > 0:  # Only update if not static
                layer["offset"] += ORB_SPEED * layer["speed"]
                # Wrap the layer offset for seamless scrolling
                if layer["offset"] < -WINDOW_WIDTH:
                    layer["offset"] += WINDOW_WIDTH

        # Spawn orbs
        self.orb_timer += 1
        if self.orb_timer >= ORB_SPAWN_RATE:
            self.orbs.append(Orb(WINDOW_WIDTH))
            self.orb_timer = 0

        # Spawn trees
        self.tree_timer += 1
        if self.tree_timer >= TREE_SPAWN_RATE:
            self.trees.append(Tree(WINDOW_WIDTH))
            self.tree_timer = 0

        # Update orbs
        for orb in self.orbs:
            orb.update()
            if orb.x_pos < self.player.x_pos and not orb.scored:
                orb.scored = True
                self.score += 1

        # Update trees
        for tree in self.trees:
            tree.update()

        # Remove off-screen orbs
        self.orbs = [o for o in self.orbs if not o.is_off_screen()]

        # Remove off-screen trees
        self.trees = [t for t in self.trees if not t.is_off_screen()]

        # Check collisions with orbs
        orb_to_remove = None
        for orb in self.orbs:
            if orb.collides_with(self.player):
                if self.player.has_shield(self.score):
                    self.player.destroy_shield()
                    orb_to_remove = orb  # Mark orb for removal
                    break
                else:
                    self.end_game()
                    return

        # Remove the orb that hit the shield
        if orb_to_remove:
            self.orbs.remove(orb_to_remove)
            return

        # Check collisions with trees
        tree_to_remove = None
        for tree in self.trees:
            if tree.collides_with(self.player):
                if self.player.has_shield(self.score):
                    self.player.destroy_shield()
                    tree_to_remove = tree  # Mark tree for removal
                    break
                else:
                    self.end_game()
                    return

        # Remove the tree that hit the shield
        if tree_to_remove:
            self.trees.remove(tree_to_remove)
            return

        if self.player.is_dead():
            if self.player.has_shield(self.score):
                self.player.destroy_shield()
                # Clamp player position back in bounds
                self.player.y_pos = max(0, min(self.player.y_pos,
                                               GROUND_Y - PLAYER_SIZE))
                self.player.rect.topleft = (self.player.x_pos,
                                            self.player.y_pos)
                return
            else:
                self.end_game()

    def end_game(self) -> None:
        self.state = GameState.GAME_OVER
        if self.score > self.high_score:
            self.high_score = self.score

    def draw(self) -> None:
        # Draw background layers in order from back to front
        for layer in self.bg_layers:
            offset = int(layer["offset"])
            # Static layers only need to be drawn once
            if layer["speed"] == 0.0:
                self.screen.blit(layer["image"], (0, 0))
            else:
                # Parallax layers - draw with wrapping for seamless scrolling
                self.screen.blit(layer["image"], (offset, 0))
                self.screen.blit(layer["image"], (offset + WINDOW_WIDTH, 0))

        # Draw orbs
        for orb in self.orbs:
            orb.draw(self.screen)
        # Draw trees
        for tree in self.trees:
            tree.draw(self.screen)


        # # Draw ground
        # pygame.draw.rect(self.screen, GROUND_COLOR,
        #                  (0, GROUND_Y, WINDOW_WIDTH, GROUND_HEIGHT))

        # Draw player
        self.player.draw(self.screen, self.score)

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

    def draw_menu(self) -> None:
        title1 = self.font_large.render("Clacky", True, BLACK)
        title2 = self.font_large.render("Key", True, BLACK)
        subtitle = self.font_small.render("Press SPACE to Start", True, BLACK)
        high_score_text = self.font_small.render(
            f"High Score: {self.high_score}", True, BLACK
        )

        self.screen.blit(title1,
                         (WINDOW_WIDTH // 2 - title1.get_width() // 2, 100))
        self.screen.blit(title2,
                         (WINDOW_WIDTH // 2 - title2.get_width() // 2, 250))
        self.screen.blit(subtitle,
                         (WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 450))
        self.screen.blit(
            high_score_text,
            (WINDOW_WIDTH // 2 - high_score_text.get_width() // 2, 1025)
        )

    def draw_game_over(self) -> None:
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
            (WINDOW_WIDTH // 2 - score_text.get_width() // 2, y + 625)
        )
        self.screen.blit(
            high_score,
            (WINDOW_WIDTH // 2 - high_score.get_width() // 2, y + 775)
        )
        self.screen.blit(
            restart,
            (WINDOW_WIDTH // 2 - restart.get_width() // 2, y + 220)
        )

    def run(self) -> None:
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
