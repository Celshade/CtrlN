import sys
import random

import pygame

from achievements import Achievements
from background import Background
from objects import Orb, Tree, BirdPerched
from player import Player
from profiles import Profile
from counter import Counter
from config import (
    GameState, FPS, SCALE,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    ORB_SPAWN_RATE, ORB_SIZE,
    TREE_SPAWN_RATE, TREE_SPACING,
    GROUND_Y, PLAYER_SIZE,
    BLACK, WHITE, RED, PERCHED_BIRD_SPAWN_CHANCE,
    TUTORIAL_DURATION, TUTORIAL_SPAWN_MULTIPLIER, TUTORIAL_PAUSE_FRAMES, YELLOW,
    SHIELD_EXPLANATION_PAUSE_FRAMES, MIN_SPAWN_GAP
)

# Frames to display each achievement notification banner
NOTIFICATION_DURATION = 180  # ~3 seconds at 60 FPS


# =================== #
# ### GAME ENGINE ### #
# =================== #
class Game:
    def __init__(self, player_id: str = "player1") -> None:
        print("Creating window...")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                              pygame.SHOWN)
        pygame.display.set_caption("Clacky Key")  # window title
        print("Window created!")

        self.clock = pygame.time.Clock()  # init game clock
        self.font_large = pygame.font.Font(None, int(36 * SCALE))
        self.font_small = pygame.font.Font(None, int(36 * SCALE))
        # 50% smaller for tutorials
        self.font_tutorial = pygame.font.Font(None, int(18 * SCALE))

        # Menu and scoring
        self.state = GameState.MENU
        self.score = 0
        self.high_score = 0

        # Init counter display
        self.counter = Counter()

        # Tutorial assets
        self.tutorial_image = pygame.image.load("assets/tutorial.png")

        # Init player and prep object vars
        self.player = Player()
        self.orbs = []
        self.orb_timer = 0
        self.trees = []
        self.tree_timer = 0
        self.perched_birds = []

        # spawn rates
        self.orb_spawn_rate = None
        self.tree_spawn_rate = None

        # Load player profile and init achievement tracker from it
        self.profile = Profile.load_by_id(player_id)
        self.achievements = Achievements(
            unlocked=self.profile.achievements,
            stats=self.profile.achievement_stats
        )
        self.shield_used_this_game = False
        self.notification_queue: list[str] = []
        self.notification_frames = 0

        # Tutorial tracking
        self.tutorial_active = False
        self.frames_since_start = 0
        self.shield_explanation_active = False
        self.shield_explanation_frames = 0
        self.shield_explanation_shown = False

        # Load background
        self.background = Background()

    def handle_gamestate(self) -> None:
        if self.state == GameState.MENU:
            self.restart_game()
        elif self.state == GameState.PLAYING:
            # Check if we can interrupt a tutorial pause
            if self.frames_since_start <= TUTORIAL_PAUSE_FRAMES:
                # Skip initial tutorial pause
                self.frames_since_start = TUTORIAL_PAUSE_FRAMES + 1
            elif self.shield_explanation_active:
                # Skip shield explanation pause
                self.shield_explanation_active = False
            else:
                # Normal gameplay - trigger jump
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
        self.shield_used_this_game = False
        self.counter = Counter()
        self.player = Player()
        self.orbs = []
        self.orb_timer = 0
        self.trees = []
        self.tree_timer = 0
        self.perched_birds = []
        # Reset parallax offsets for all layers
        self.background.reset()

        # Initialize tutorial
        self.tutorial_active = True
        self.frames_since_start = 0
        self.shield_explanation_active = False
        self.shield_explanation_frames = 0
        self.shield_explanation_shown = False


    def _get_rightmost_obstacle_x(self) -> float:
        """Get the x position of the rightmost orb."""
        rightmost = 0

        for orb in self.orbs:
            rightmost = max(rightmost, orb.x_pos + ORB_SIZE)

        return rightmost

    def _get_spawn_rate(self, object_type: str, score: int) -> int:
        rates = {"orb": ORB_SPAWN_RATE, "tree": TREE_SPAWN_RATE}
        rate = rates[object_type]

        # Tutorial phase: slower spawn rate
        if self.tutorial_active:
            rate = int(rate * TUTORIAL_SPAWN_MULTIPLIER)

        # Three-phase difficulty progression:
        # Phase 1 (Score 0-150): Smooth scaling to 2.5x difficulty
        # (multiplier 1.0 → 0.4)
        # Phase 2 (Score 150-300): Maintains 2.5x difficulty (multiplier 0.4)
        # Phase 3 (Score 300+): Continue scaling to 4x difficulty
        # (multiplier 0.4 → 0.25)
        if score < 150:
            # Linear progression to 2.5x cap
            difficulty_multiplier = 1.0 - score / 250
        elif score < 300:
            # Maintain 2.5x plateau
            difficulty_multiplier = 0.4
        else:
            # Continue scaling beyond 300 to reach 4x at score 450+
            difficulty_multiplier = max(0.25, 0.4 - (score - 300) / 1000)

        return int(rate * difficulty_multiplier)


    def update(self) -> None:
        if self.state != GameState.PLAYING:
            return

        self.frames_since_start += 1

        # Pause at game start for tutorial
        if self.frames_since_start <= TUTORIAL_PAUSE_FRAMES:
            return

        # Check if we reached 5 points and should show shield explanation
        if self.score >= 5 and not self.shield_explanation_shown:
            self.shield_explanation_active = True
            self.shield_explanation_shown = True
            self.shield_explanation_frames = 0

        # Pause for shield explanation
        if self.shield_explanation_active:
            self.shield_explanation_frames += 1
            if self.shield_explanation_frames > SHIELD_EXPLANATION_PAUSE_FRAMES:
                self.shield_explanation_active = False
            return

        self.player.update()  # Update the Player

        # Update parallax background layers
        self.background.update()

        # Spawn orbs (1-3 at a time with minimum spacing from other orbs)
        self.orb_spawn_rate = self._get_spawn_rate(object_type="orb",
                                                   score=self.score)
        self.orb_timer += 1
        if self.orb_timer >= self.orb_spawn_rate:
            # Check if there's enough gap since last orb
            rightmost = self._get_rightmost_obstacle_x()
            if WINDOW_WIDTH - rightmost >= MIN_SPAWN_GAP:
                # Spawn 1-3 orbs at various heights
                num_orbs = random.randint(1, 3)
                for i in range(num_orbs):
                    # Offset each orb horizontally
                    orb_x = WINDOW_WIDTH + (i * ORB_SIZE * 0.8)
                    self.orbs.append(Orb(orb_x))
                self.orb_timer = 0

        # Spawn trees (1-3 at a time at random intervals - no gap constraint)
        self.tree_spawn_rate = self._get_spawn_rate(object_type="tree",
                                                    score=self.score)
        self.tree_timer += 1
        if self.tree_timer >= self.tree_spawn_rate:
            # Spawn 1-3 trees
            num_trees = random.randint(1, 3)
            for i in range(num_trees):
                # Offset each tree horizontally
                tree_x = WINDOW_WIDTH + (i * TREE_SPACING)
                tree = Tree(tree_x)
                self.trees.append(tree)
                # Randomly spawn a perched bird on this tree
                if random.random() < PERCHED_BIRD_SPAWN_CHANCE:
                    bird = BirdPerched(tree)
                    self.perched_birds.append(bird)
            self.tree_timer = 0

        # Update orbs
        for orb in self.orbs:
            orb.update()
            if orb.x_pos < self.player.x_pos and not orb.scored:
                orb.scored = True
                self.score += 1
                self.counter.update_score(self.score)
                self._notify(self.achievements.increment("yellow_birds_dodged"))

        # Update trees
        for tree in self.trees:
            tree.update()

        # Update perched birds
        for bird in self.perched_birds:
            bird.update()
            if bird.x_pos < self.player.x_pos and not bird.scored:
                bird.scored = True
                self.score += 1
                self.counter.update_score(self.score)
                stat = "red_birds_dodged" if bird.is_red else "yellow_birds_dodged"
                self._notify(self.achievements.increment(stat))

        # Update counter animations
        self.counter.update()

        # Check for shield earnings based on score (triggers animations)
        if self.player.update_shields(self.score):
            self._notify(self.achievements.increment("shields_regenerated"))

        # End tutorial phase when score reaches threshold
        if self.tutorial_active and self.score >= TUTORIAL_DURATION:
            self.tutorial_active = False

        # Remove off-screen orbs
        self.orbs = [o for o in self.orbs if not o.is_off_screen()]

        # Remove off-screen trees
        self.trees = [t for t in self.trees if not t.is_off_screen()]

        # Remove off-screen perched birds
        self.perched_birds = [
            b for b in self.perched_birds if not b.is_off_screen()
        ]

        # Check collisions with orbs
        orb_to_remove = None
        for orb in self.orbs:
            if orb.collides_with(self.player):
                if self.player.has_shield():
                    self.player.destroy_shield()
                    self.shield_used_this_game = True
                    self._notify(self.achievements.increment("shields_used"))
                    orb_to_remove = orb  # Mark orb for removal
                    break
                elif self.player.is_invulnerable():
                    # Skip collision during invulnerability period
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
                if self.player.has_shield():
                    self.player.destroy_shield()
                    self.shield_used_this_game = True
                    self._notify(self.achievements.increment("shields_used"))
                    self._notify(self.achievements.increment("trees_hit"))
                    tree_to_remove = tree  # Mark tree for removal
                    break
                elif self.player.is_invulnerable():
                    # Skip collision during invulnerability period
                    break
                else:
                    self._notify(self.achievements.increment("trees_hit"))
                    self.end_game()
                    return

        # Remove the tree that hit the shield
        if tree_to_remove:
            self.trees.remove(tree_to_remove)
            return

        # Check collisions with perched birds
        bird_to_remove = None
        for bird in self.perched_birds:
            if bird.collides_with(self.player):
                perched_stat = "red_perched_hit" if bird.is_red else "yellow_perched_hit"
                if self.player.has_shield():
                    self.player.destroy_shield()
                    self.shield_used_this_game = True
                    self._notify(self.achievements.increment("shields_used"))
                    self._notify(self.achievements.increment(perched_stat))
                    bird_to_remove = bird  # Mark bird for removal
                    break
                elif self.player.is_invulnerable():
                    # Skip collision during invulnerability period
                    break
                else:
                    self._notify(self.achievements.increment(perched_stat))
                    self.end_game()
                    return

        # Remove the perched bird that hit the shield
        if bird_to_remove:
            self.perched_birds.remove(bird_to_remove)
            return

        if self.player.is_dead():
            # Track ground vs ceiling crash
            if self.player.y_pos + self.player.size >= GROUND_Y:
                self._notify(self.achievements.increment("ground_crashes"))
            else:
                self._notify(self.achievements.increment("ceiling_crashes"))
            if self.player.has_shield():
                self.player.destroy_shield()
                self.shield_used_this_game = True
                self._notify(self.achievements.increment("shields_used"))
                # Clamp player position back in bounds
                self.player.y_pos = max(0, min(self.player.y_pos,
                                               GROUND_Y - PLAYER_SIZE))
                self.player.rect.topleft = (self.player.x_pos,
                                            self.player.y_pos)
                return
            elif self.player.is_invulnerable():
                # Don't end game during invulnerability, clamp player back
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
        # Achievement checks at game-over
        self._notify(self.achievements.increment("games_played"))
        self._notify(self.achievements.check_game_score(
            self.score, self.shield_used_this_game
        ))
        # Sync achievements back to profile and persist
        self._save_profile()

    def _notify(self, newly_unlocked: list[str]) -> None:
        """Push newly unlocked achievement IDs onto the notification queue."""
        self.notification_queue.extend(newly_unlocked)

    def _save_profile(self) -> None:
        """Sync achievement data back to the profile and write to disk."""
        self.profile.achievements = self.achievements.to_list()
        self.profile.achievement_stats = self.achievements.stats
        self.profile.games_played = self.achievements.stats.get("games_played",
                                                                 self.profile.games_played)
        self.profile.save_to_file()

    def draw(self) -> None:
        # Draw background layers in order from back to front
        self.background.draw(self.screen)

        # Draw orbs
        for orb in self.orbs:
            orb.draw(self.screen)
        # Draw trees
        for tree in self.trees:
            tree.draw(self.screen)
        # Draw perched birds
        for bird in self.perched_birds:
            bird.draw(self.screen)


        # # Draw ground
        # pygame.draw.rect(self.screen, GROUND_COLOR,
        #                  (0, GROUND_Y, WINDOW_WIDTH, GROUND_HEIGHT))

        # Draw player
        self.player.draw(self.screen, self.score)

        # Draw UI
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.counter.draw(self.screen)

            # Draw tutorial elements
            self.draw_tutorial()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()

        # Draw achievement notification banner (shown in any state)
        self.draw_achievement_notification()

        # Flush display
        pygame.display.flip()

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

    def draw_tutorial(self) -> None:
        """Draw tutorial instructions and pause overlay during warm-up."""
        # Show pause overlay and instructions during initial pause
        if self.frames_since_start <= TUTORIAL_PAUSE_FRAMES:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            title = self.font_tutorial.render("Get Ready!", True, YELLOW)
            instruction = self.font_tutorial.render(
                "Press SPACE or CLICK to Jump", True, WHITE
            )

            self.screen.blit(
                title,
                (WINDOW_WIDTH // 2 - title.get_width() // 2,
                 WINDOW_HEIGHT // 2 - 150)
            )
            self.screen.blit(
                instruction,
                (WINDOW_WIDTH // 2 - instruction.get_width() // 2,
                 WINDOW_HEIGHT // 2 + 50)
            )

        # Show shield explanation pause
        elif self.shield_explanation_active:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            shield_tutorial_text = self.font_tutorial.render(
                "Every 5 points, a shield charge will regenerate.",
                True,
                WHITE
            )
            self.screen.blit(shield_tutorial_text, (20, WINDOW_HEIGHT - 100))

        # Show tutorial progress indicator while in tutorial phase
        elif self.tutorial_active:
            # tutorial_text = self.font_tutorial.render(
            #     f"TUTORIAL: Reach {TUTORIAL_DURATION} to Continue",
            #     True,
            #     YELLOW
            # )
            # self.screen.blit(tutorial_text, (20, WINDOW_HEIGHT - 100))
            # Render and display tutorial image - left-aligned at bottom
            img_rect = self.tutorial_image.get_rect(
                bottomleft=(-150, WINDOW_HEIGHT + 175)
            )
            self.screen.blit(self.tutorial_image, img_rect)

            progress_text = self.font_tutorial.render(
                f"Progress: {self.score}/{TUTORIAL_DURATION}",
                True,
                YELLOW
            )
            self.screen.blit(progress_text, (10, WINDOW_HEIGHT - 50))

    def draw_achievement_notification(self) -> None:
        """Render the topmost queued achievement banner, if any."""
        if not self.notification_queue:
            return

        self.notification_frames += 1
        if self.notification_frames > NOTIFICATION_DURATION:
            self.notification_queue.pop(0)
            self.notification_frames = 0
            if not self.notification_queue:
                return

        aid = self.notification_queue[0]
        from achievements import ACHIEVEMENT_REGISTRY
        entry = ACHIEVEMENT_REGISTRY.get(aid)
        if entry is None:
            return

        label = f"Achievement unlocked: {entry.name}"
        text_surf = self.font_tutorial.render(label, True, BLACK)
        padding = 12
        banner_w = text_surf.get_width() + padding * 2
        banner_h = text_surf.get_height() + padding * 2
        banner_x = WINDOW_WIDTH // 2 - banner_w // 2
        banner_y = 20

        banner = pygame.Surface((banner_w, banner_h), pygame.SRCALPHA)
        banner.fill((255, 215, 0, 210))  # gold, semi-transparent
        self.screen.blit(banner, (banner_x, banner_y))
        self.screen.blit(text_surf, (banner_x + padding, banner_y + padding))

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
            if frame % 30 == 0:
                debug_str = (
                    f"Frame {frame}: State={self.state.name} "
                    f"Score={self.score} Orbs={len(self.orbs)} "
                    f"Trees={len(self.trees)} "
                    f"PerchedBirds={len(self.perched_birds)}"
                )
                print(debug_str)

        print("\nShutting down...")
        self._save_profile()
        pygame.quit()
        sys.exit()
