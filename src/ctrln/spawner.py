import random

import pygame

from objects import Orb, Tree, BirdPerched
from config import (
    WINDOW_WIDTH,
    ORB_SPAWN_RATE, ORB_SIZE,
    TREE_SPAWN_RATE, TREE_SPACING,
    PERCHED_BIRD_SPAWN_CHANCE,
    TUTORIAL_SPAWN_MULTIPLIER,
    MIN_SPAWN_GAP,
)


# ================== #
# ### OBJ SPAWNER ### #
# ================== #
class Spawner:
    """Manages obstacle spawning, movement, and off-screen pruning."""

    def __init__(self) -> None:
        self.orbs: list[Orb] = []
        self.trees: list[Tree] = []
        self.perched_birds: list[BirdPerched] = []

        self._orb_timer: int = 0
        self._tree_timer: int = 0
        self.orb_spawn_rate: int | None = None
        self.tree_spawn_rate: int | None = None

    def reset(self) -> None:
        """Clear all obstacles and reset spawn timers."""
        self.orbs.clear()
        self.trees.clear()
        self.perched_birds.clear()
        self._orb_timer = 0
        self._tree_timer = 0

    # ------------------------------------------------------------------ #
    # Internal helpers                                                     #
    # ------------------------------------------------------------------ #

    def _get_rightmost_obstacle_x(self) -> float:
        """Return the x position of the rightmost orb's trailing edge."""
        rightmost: float = 0
        for orb in self.orbs:
            rightmost = max(rightmost, orb.x_pos + ORB_SIZE)
        return rightmost

    def _get_spawn_rate(
        self, object_type: str, score: int, tutorial_active: bool
    ) -> int:
        """Calculate the current spawn-rate (in frames) for an object type.

        Three-phase difficulty progression:
          Phase 1 (Score   0–150): Smooth scaling to 2.5× difficulty
                                   (multiplier 1.0 → 0.4)
          Phase 2 (Score 150–300): Maintains 2.5× plateau (multiplier 0.4)
          Phase 3 (Score   300+):  Continue scaling to 4× difficulty
                                   (multiplier 0.4 → 0.25)
        """
        rates = {"orb": ORB_SPAWN_RATE, "tree": TREE_SPAWN_RATE}
        rate = rates[object_type]

        # Tutorial phase: slower spawn rate
        if tutorial_active:
            rate = int(rate * TUTORIAL_SPAWN_MULTIPLIER)

        if score < 150:
            difficulty_multiplier = 1.0 - score / 250
        elif score < 300:
            difficulty_multiplier = 0.4
        else:
            difficulty_multiplier = max(0.25, 0.4 - (score - 300) / 1000)

        return int(rate * difficulty_multiplier)

    # ------------------------------------------------------------------ #
    # Per-frame update                                                     #
    # ------------------------------------------------------------------ #

    def update(self, score: int, tutorial_active: bool) -> None:
        """Spawn new obstacles, move all existing ones, and prune off-screen."""

        # --- Spawn orbs (1–3 at a time; minimum spacing enforced) ---
        self.orb_spawn_rate = self._get_spawn_rate("orb", score, tutorial_active)
        self._orb_timer += 1
        if self._orb_timer >= self.orb_spawn_rate:
            rightmost = self._get_rightmost_obstacle_x()
            if WINDOW_WIDTH - rightmost >= MIN_SPAWN_GAP:
                num_orbs = random.randint(1, 3)
                for i in range(num_orbs):
                    orb_x = WINDOW_WIDTH + (i * ORB_SIZE * 0.8)
                    self.orbs.append(Orb(orb_x))
                self._orb_timer = 0

        # --- Spawn trees (1–3 at a time; no gap constraint) ---
        self.tree_spawn_rate = self._get_spawn_rate("tree", score, tutorial_active)
        self._tree_timer += 1
        if self._tree_timer >= self.tree_spawn_rate:
            num_trees = random.randint(1, 3)
            for i in range(num_trees):
                tree_x = WINDOW_WIDTH + (i * TREE_SPACING)
                tree = Tree(tree_x)
                self.trees.append(tree)
                if random.random() < PERCHED_BIRD_SPAWN_CHANCE:
                    self.perched_birds.append(BirdPerched(tree))
            self._tree_timer = 0

        # --- Move all existing obstacles ---
        for orb in self.orbs:
            orb.update()
        for tree in self.trees:
            tree.update()
        for bird in self.perched_birds:
            bird.update()

        # --- Prune off-screen obstacles ---
        self.orbs = [o for o in self.orbs if not o.is_off_screen()]
        self.trees = [t for t in self.trees if not t.is_off_screen()]
        self.perched_birds = [b for b in self.perched_birds if not b.is_off_screen()]

    # ------------------------------------------------------------------ #
    # Drawing                                                              #
    # ------------------------------------------------------------------ #

    def draw(self, screen: pygame.Surface) -> None:
        for orb in self.orbs:
            orb.draw(screen)
        for tree in self.trees:
            tree.draw(screen)
        for bird in self.perched_birds:
            bird.draw(screen)
