import sys

import pygame

from achievements import Achievements
from background import Background
from character_select import CharacterSelect
from characters import CHARACTER_ROSTER, CHARACTER_ORDER
from player import Player
from profiles import Profile
from counter import Counter
from spawner import Spawner
from tutorial import Tutorial
from ui import UI
from counter import Counter
from spawner import Spawner
from tutorial import Tutorial
from ui import UI
from config import (
    GameState, FPS,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    GROUND_Y, PLAYER_SIZE,
)


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

        # Menu and scoring
        self.state = GameState.CHARACTER_SELECT
        self.score = 0
        self.high_score = 0

        # Init subsystems
        self.counter = Counter()
        self.player = Player()
        self.background = Background()
        self.spawner = Spawner()
        self.ui = UI()
        self.tutorial = Tutorial()

        # Load player profile and init achievement tracker from it
        self.profile = Profile.load_by_id(player_id)
        self.achievements = Achievements(
            unlocked=self.profile.achievements,
            stats=self.profile.achievement_stats
        )

        # Create character select with player's current rank
        self.char_select = CharacterSelect(player_rank=self.profile.rank)
        self.selected_character = CHARACTER_ROSTER[CHARACTER_ORDER[0]]
        self.shield_used_this_game = False
        self.notification_queue: list[str] = []
        self.notification_frames = 0

    def handle_gamestate(self) -> None:
        if self.state == GameState.MENU:
            self.restart_game()
        elif self.state == GameState.PLAYING:
            # Let the tutorial skip its current pause; if nothing was skipped
            # it means we're in normal gameplay so trigger a jump.
            if not self.tutorial.skip_pause():
                self.player.keypress()
        elif self.state == GameState.GAME_OVER:
            self.state = GameState.MENU

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif self.state == GameState.CHARACTER_SELECT:
                    if event.key == pygame.K_LEFT:
                        self.char_select.navigate(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.char_select.navigate(1)
                    elif event.key == pygame.K_UP:
                        self.char_select.navigate_row(-1)
                    elif event.key == pygame.K_DOWN:
                        self.char_select.navigate_row(1)
                    elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self._confirm_character()
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.handle_gamestate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.CHARACTER_SELECT:
                    slot = self.char_select.icon_slot_at(event.pos)
                    if slot is not None:
                        self.char_select.selected_id = slot
                    elif self.char_select.is_play_clicked(event.pos):
                        self._confirm_character()
                else:
                    self.handle_gamestate()
        return True

    def restart_game(self) -> None:
        self.state = GameState.PLAYING
        self.score = 0
        self.shield_used_this_game = False
        self.counter = Counter()
        self.player = Player(profile=self.profile, 
                             character_id=self.selected_character.id,
                             asset_path=self.selected_character.asset_path)
        self.background.reset()
        self.spawner.reset()
        self.tutorial.reset()

    def _confirm_character(self) -> None:
        """Lock in the highlighted character and start the game."""
        self.selected_character = self.char_select.selected
        self.restart_game()




    def update(self) -> None:
        if self.state != GameState.PLAYING:
            return

        # Tutorial handles its own frame counting; returns True when paused
        if self.tutorial.update(self.score):
            return

        self.player.update()
        self.background.update()
        self.spawner.update(self.score, self.tutorial.active)

        # Score orbs that have passed the player
        for orb in self.spawner.orbs:
            if orb.x_pos < self.player.x_pos and not orb.scored:
                orb.scored = True
                self.score += 1
                self.counter.update_score(self.score)
                self._notify(self.achievements.increment("yellow_birds_dodged"))

        # Score perched birds that have passed the player
        for bird in self.spawner.perched_birds:
            if bird.x_pos < self.player.x_pos and not bird.scored:
                bird.scored = True
                self.score += 1
                self.counter.update_score(self.score)
                stat = "red_birds_dodged" if bird.is_red else "yellow_birds_dodged"
                self._notify(self.achievements.increment(stat))

        self.counter.update()

        # Check for shield earnings based on score (triggers animations)
        if self.player.update_shields(self.score):
            self._notify(self.achievements.increment("shields_regenerated"))

        # Check collisions with orbs
        orb_to_remove = None
        for orb in self.spawner.orbs:
            if orb.collides_with(self.player):
                if self.player.has_shield():
                    self.player.destroy_shield()
                    self.shield_used_this_game = True
                    self._notify(self.achievements.increment("shields_used"))
                    orb_to_remove = orb
                    break
                elif self.player.is_invulnerable():
                    break
                else:
                    self.end_game()
                    return

        if orb_to_remove:
            self.spawner.orbs.remove(orb_to_remove)
            return

        # Check collisions with trees
        tree_to_remove = None
        for tree in self.spawner.trees:
            if tree.collides_with(self.player):
                if self.player.has_shield():
                    self.player.destroy_shield()
                    self.shield_used_this_game = True
                    self._notify(self.achievements.increment("shields_used"))
                    self._notify(self.achievements.increment("trees_hit"))
                    tree_to_remove = tree
                    break
                elif self.player.is_invulnerable():
                    break
                else:
                    self._notify(self.achievements.increment("trees_hit"))
                    self.end_game()
                    return

        if tree_to_remove:
            self.spawner.trees.remove(tree_to_remove)
            return

        # Check collisions with perched birds
        bird_to_remove = None
        for bird in self.spawner.perched_birds:
            if bird.collides_with(self.player):
                perched_stat = "red_perched_hit" if bird.is_red else "yellow_perched_hit"
                if self.player.has_shield():
                    self.player.destroy_shield()
                    self.shield_used_this_game = True
                    self._notify(self.achievements.increment("shields_used"))
                    self._notify(self.achievements.increment(perched_stat))
                    bird_to_remove = bird
                    break
                elif self.player.is_invulnerable():
                    break
                else:
                    self._notify(self.achievements.increment(perched_stat))
                    self.end_game()
                    return

        if bird_to_remove:
            self.spawner.perched_birds.remove(bird_to_remove)
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
        # Award XP based on score (1 XP per point)
        xp_earned = self.score
        self.player.add_xp(xp_earned)
        # Achievement checks at game-over
        self._notify(self.achievements.record_play())
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
        # Increment games played for this character
        if self.player.character_id:
            if self.player.character_id not in self.profile.games_per_character:
                self.profile.games_per_character[self.player.character_id] = 0
            self.profile.games_per_character[self.player.character_id] += 1
        # Sync player progression data
        self.profile.current_xp = self.player.season_xp
        self.profile.total_xp = self.player.total_xp
        self.profile.rank = self.player.rank
        self.profile.highest_rank = self.player.highest_rank
        self.profile.prestige = self.player.prestige
        self.profile.seasons_played = self.player.seasons_played
        self.profile.save_to_file()

    def draw(self) -> None:
        self.background.draw(self.screen)

        if self.state == GameState.CHARACTER_SELECT:
            self.char_select.draw(self.screen)
            pygame.display.flip()
            return

        self.spawner.draw(self.screen)
        self.player.draw(self.screen, self.score)

        if self.state == GameState.MENU:
            self.ui.draw_menu(self.screen, self.high_score)
        elif self.state == GameState.PLAYING:
            self.counter.draw(self.screen)
            self.tutorial.draw(self.screen, self.score)
        elif self.state == GameState.GAME_OVER:
            self.ui.draw_game_over(self.screen, self.score, self.high_score)

        # Achievement notification banner (shown in any non-select state)
        self.notification_frames = self.ui.draw_achievement_notification(
            self.screen, self.notification_queue, self.notification_frames
        )

        pygame.display.flip()

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
                    f"Score={self.score} "
                    f"Orbs={len(self.spawner.orbs)} "
                    f"Trees={len(self.spawner.trees)} "
                    f"PerchedBirds={len(self.spawner.perched_birds)}"
                )
                print(debug_str)

        print("\nShutting down...")
        self._save_profile()
        pygame.quit()
        sys.exit()
