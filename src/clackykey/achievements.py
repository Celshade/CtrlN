from datetime import date, datetime, timezone
from typing import NamedTuple


# Achievement types:
#   "stat"       - a lifetime counter crosses a threshold (checked increment())
#   "game_score" - score in a single game (checked at game-over)
#   "no_shield"  - reach score X in one game without using a shield
#   "rank"       - reach a specific rank
#   "store"      - triggered by a store/upgrade event
#   "manual"     - checked explicitly (3rd-charge shield deploy, etc.)
#
# NOTE: Thresholds for #67-75 (stat-based combat events) are marked TODO and
#       should be tuned once playtesting data is available.


class Achievement(NamedTuple):
    name: str               # Display name
    description: str        # Flavour / UI text
    kind: str               # Achievement type (see types above)
    stat_key: str | None    # stats dict key; None for event-driven types
    threshold: int | None   # Value to reach; None if checked externally


ACHIEVEMENT_REGISTRY: dict[str, Achievement] = {
    # ------------------------------------------------------------------ #
    # Combat / Obstacle (#67-75)                                         #
    # ------------------------------------------------------------------ #
    # #67
    "yellow_birds_dodged": Achievement(
        name="Ghost Feathers",
        description="Dodge yellow birds",
        kind="stat",
        stat_key="yellow_birds_dodged",
        threshold=50,                               # TODO: tune threshold
    ),
    # #68
    "yellow_perched_hit": Achievement(
        name="Woodpecker",
        description="Collide with yellow perched birds",
        kind="stat",
        stat_key="yellow_perched_hit",
        threshold=10,                               # TODO: tune threshold
    ),
    # #69
    "red_birds_dodged": Achievement(
        name="Seeing Red",
        description="Dodge red birds",
        kind="stat",
        stat_key="red_birds_dodged",
        threshold=25,                               # TODO: tune threshold
    ),
    # #70
    "red_perched_hit": Achievement(
        name="Crimson Crash",
        description="Collide with red perched birds",
        kind="stat",
        stat_key="red_perched_hit",
        threshold=10,                               # TODO: tune threshold
    ),
    # #71
    "trees_hit": Achievement(
        name="Bark Buster",
        description="Collide with trees",
        kind="stat",
        stat_key="trees_hit",
        threshold=10,                               # TODO: tune threshold
    ),
    # #72
    "ground_crashes": Achievement(
        name="Face Plant",
        description="Crash into the ground",
        kind="stat",
        stat_key="ground_crashes",
        threshold=10,                               # TODO: tune threshold
    ),
    # #73
    "ceiling_crashes": Achievement(
        name="Sky High",
        description="Crash into the ceiling",
        kind="stat",
        stat_key="ceiling_crashes",
        threshold=10,                               # TODO: tune threshold
    ),
    # #74
    "shields_regenerated": Achievement(
        name="Recharged",
        description="Regenerate shield charges",
        kind="stat",
        stat_key="shields_regenerated",
        threshold=25,                               # TODO: tune threshold
    ),
    # #75
    "shields_used": Achievement(
        name="Guardian",
        description="Use shield charges",
        kind="stat",
        stat_key="shields_used",
        threshold=10,                               # TODO: tune threshold
    ),

    # ------------------------------------------------------------------ #
    # No-shield score runs (#76-79)                                      #
    # ------------------------------------------------------------------ #
    # #76
    "no_shield_10": Achievement(
        name="Unprotected I",
        description="Reach 10 points in one game without using a shield",
        kind="no_shield",
        stat_key=None,
        threshold=10,
    ),
    # #77
    "no_shield_50": Achievement(
        name="Unprotected II",
        description="Reach 50 points in one game without using a shield",
        kind="no_shield",
        stat_key=None,
        threshold=50,
    ),
    # #78
    "no_shield_100": Achievement(
        name="Unprotected III",
        description="Reach 100 points in one game without using a shield",
        kind="no_shield",
        stat_key=None,
        threshold=100,
    ),
    # #79
    "no_shield_150": Achievement(
        name="Unprotected IV",
        description="Reach 150 points in one game without using a shield",
        kind="no_shield",
        stat_key=None,
        threshold=150,
    ),

    # ------------------------------------------------------------------ #
    # Games played (#80-86)                                              #
    # ------------------------------------------------------------------ #
    # #80
    "games_played_10": Achievement(
        name="Just Getting Started",
        description="Play 10 games",
        kind="stat",
        stat_key="games_played",
        threshold=10,
    ),
    # #81
    "games_played_50": Achievement(
        name="Regular",
        description="Play 50 games",
        kind="stat",
        stat_key="games_played",
        threshold=50,
    ),
    # #82
    "games_played_100": Achievement(
        name="Century",
        description="Play 100 games",
        kind="stat",
        stat_key="games_played",
        threshold=100,
    ),
    # #83
    "games_played_150": Achievement(
        name="Devoted",
        description="Play 150 games",
        kind="stat",
        stat_key="games_played",
        threshold=150,
    ),
    # #84
    "games_played_250": Achievement(
        name="Persistent",
        description="Play 250 games",
        kind="stat",
        stat_key="games_played",
        threshold=250,
    ),
    # #85
    "games_played_500": Achievement(
        name="Veteran",
        description="Play 500 games",
        kind="stat",
        stat_key="games_played",
        threshold=500,
    ),
    # #86
    "games_played_1000": Achievement(
        name="Legendary",
        description="Play 1000 games",
        kind="stat",
        stat_key="games_played",
        threshold=1000,
    ),

    # ------------------------------------------------------------------ #
    # Store / Shield enhancements (#87-88)                               #
    # ------------------------------------------------------------------ #
    # #87
    "shield_enhancement_1": Achievement(
        name="Upgraded",
        description="Unlock a shield enhancement",
        kind="store",
        stat_key=None,
        threshold=1,
    ),
    # #88
    "shield_enhancement_all": Achievement(
        name="Full Arsenal",
        description="Unlock all shield enhancements",
        kind="store",
        stat_key=None,
        threshold=None,             # checked externally
    ),

    # ------------------------------------------------------------------ #
    # Progression (#92)                                                  #
    # ------------------------------------------------------------------ #
    # Rank achievements (#93-98)                                         #
    # rank IDs: 5=Bronze, 4=Silver, 3=Gold, 2=Platinum, 1=Diamond,       #
    #           0=Prestige                                               #
    # ------------------------------------------------------------------ #
    # #93
    "reach_bronze": Achievement(
        name="Bronze",
        description="Reach Bronze rank",
        kind="rank",
        stat_key=None,
        threshold=5,
    ),
    # #94
    "reach_silver": Achievement(
        name="Silver",
        description="Reach Silver rank",
        kind="rank",
        stat_key=None,
        threshold=4,
    ),
    # #95
    "reach_gold": Achievement(
        name="Gold",
        description="Reach Gold rank",
        kind="rank",
        stat_key=None,
        threshold=3,
    ),
    # #96
    "reach_platinum": Achievement(
        name="Platinum",
        description="Reach Platinum rank",
        kind="rank",
        stat_key=None,
        threshold=2,
    ),
    # #97
    "reach_diamond": Achievement(
        name="Diamond",
        description="Reach Diamond rank",
        kind="rank",
        stat_key=None,
        threshold=1,
    ),
    # #98
    "reach_prestige": Achievement(
        name="Beyond the Top",
        description="Reach Prestige rank",
        kind="rank",
        stat_key=None,
        threshold=0,
    ),

    # ------------------------------------------------------------------ #
    # Store / Energy (#99-101)                                           #
    # ------------------------------------------------------------------ #
    # #99
    "top_off_energy": Achievement(
        name="Full Tank",
        description="Top off energy",
        kind="store",
        stat_key=None,
        threshold=1,
    ),
    # #99
    "buy_keycap": Achievement(
        name="Keycapper",
        description="Buy a keycap from the store",
        kind="store",
        stat_key=None,
        threshold=1,
    ),
    # #100
    "buy_thruster": Achievement(
        name="Thruster",
        description="Buy a thruster from the store",
        kind="store",
        stat_key=None,
        threshold=1,
    ),

    # ------------------------------------------------------------------ #
    # Single-game events (#102)                                          #
    # ------------------------------------------------------------------ #
    # #102
    "active_shield_3rd_charge": Achievement(
        name="Triple Threat",
        description="Deploy an active shield using the 3rd charge",
        kind="manual",
        stat_key=None,
        threshold=1,
    ),

    # ------------------------------------------------------------------ #
    # Single-game score milestones (#103-108)                            #
    # ------------------------------------------------------------------ #
    # #103
    "score_50_game": Achievement(
        name="Half Century",
        description="Reach 50 points in one game",
        kind="game_score",
        stat_key=None,
        threshold=50,
    ),
    # #104
    "score_100_game": Achievement(
        name="Century",
        description="Reach 100 points in one game",
        kind="game_score",
        stat_key=None,
        threshold=100,
    ),
    # #105
    "score_200_game": Achievement(
        name="Double Century",
        description="Reach 200 points in one game",
        kind="game_score",
        stat_key=None,
        threshold=200,
    ),
    # #106
    "score_300_game": Achievement(
        name="Triple Century",
        description="Reach 300 points in one game",
        kind="game_score",
        stat_key=None,
        threshold=300,
    ),
    # #107
    "score_400_game": Achievement(
        name="Quadruple Century",
        description="Reach 400 points in one game",
        kind="game_score",
        stat_key=None,
        threshold=400,
    ),
    # #108
    "score_500_game": Achievement(
        name="Quintuple Century",
        description="Reach 500 points in one game",
        kind="game_score",
        stat_key=None,
        threshold=500,
    ),

    # ------------------------------------------------------------------ #
    # Daily streak (#109-113)                                            #
    # Consecutive days with at least one game played                     #
    # ------------------------------------------------------------------ #
    # #109
    "daily_streak_2": Achievement(
        name="Two-Day Streak",
        description="Play at least one game per day for 2 consecutive days",
        kind="stat",
        stat_key="daily_streak",
        threshold=2,
    ),
    # #110
    "daily_streak_5": Achievement(
        name="Five-Day Streak",
        description="Play at least one game per day for 5 consecutive days",
        kind="stat",
        stat_key="daily_streak",
        threshold=5,
    ),
    # #111
    "daily_streak_10": Achievement(
        name="Ten-Day Streak",
        description="Play at least one game per day for 10 consecutive days",
        kind="stat",
        stat_key="daily_streak",
        threshold=10,
    ),
    # #112
    "daily_streak_20": Achievement(
        name="Twenty-Day Streak",
        description="Play at least one game per day for 20 consecutive days",
        kind="stat",
        stat_key="daily_streak",
        threshold=20,
    ),
    # #113
    "daily_streak_30": Achievement(
        name="Thirty-Day Streak",
        description="Play at least one game per day for 30 consecutive days",
        kind="stat",
        stat_key="daily_streak",
        threshold=30,
    ),
}


# Default lifetime stat counters — all keys that stat-based achievements use.
# Integer counters are checked by achievement thresholds.
# "last_played" is an ISO-8601 UTC date string ("YYYY-MM-DD") or "" if never
# recorded; it is managed exclusively by record_play().
_DEFAULT_STATS: dict[str, int | str] = {
    "yellow_birds_dodged": 0,
    "yellow_perched_hit":  0,
    "red_birds_dodged":    0,
    "red_perched_hit":     0,
    "trees_hit":           0,
    "ground_crashes":      0,
    "ceiling_crashes":     0,
    "shields_regenerated": 0,
    "shields_used":        0,
    "games_played":        0,
    "daily_streak":        0,
    "last_played":         "",   # ISO UTC date of last save(); "" = never
}


class Achievements:
    """Tracks unlocked achievements and lifetime stats for a player.

    Intended to be instantiated once per player session and kept in sync
    with their Profile. All methods that can unlock achievements return
    a list of newly-unlocked achievement IDs so callers can queue
    notifications.
    """

    def __init__(self,
                 unlocked: list[str] | None = None,
                 stats: dict[str, int] | None = None) -> None:
        """Initialize achievement tracker.

        Args:
            unlocked: List of already-earned achievement IDs (from
                Profile). Defaults to empty.
            stats: Persisted lifetime stat counters (from Profile).
                Missing keys are filled with defaults.
        """
        self.unlocked: set[str] = set(unlocked or [])
        self.stats: dict[str, int | str] = {**_DEFAULT_STATS, **(stats or {})}

    # ------------------------------------------------------------------ #
    # Public API                                                          #
    # ------------------------------------------------------------------ #

    def record_play(self) -> list[str]:
        """Update ``last_played`` and advance ``daily_streak`` if applicable.

        Call this once per session when the profile is saved (e.g. game-over).
        Day boundaries are determined in UTC.  Rules:

        * Same UTC day as last call → timestamp refreshed, streak unchanged.
        * Next consecutive UTC day   → streak incremented by 1.
        * Gap of 2+ days             → streak reset to 1.
        * Never called before        → streak set to 1.

        Returns:
            List of newly-unlocked achievement IDs (may be empty).
        """
        today = datetime.now(timezone.utc).date()
        last_raw = self.stats.get("last_played", "")

        if last_raw:
            last_date = date.fromisoformat(str(last_raw))
            delta = (today - last_date).days
            if delta == 0:
                # Same day — refresh timestamp, no streak change
                self.stats["last_played"] = today.isoformat()
                return []
            elif delta == 1:
                # Consecutive day — advance streak
                self.stats["daily_streak"] = (
                    int(self.stats.get("daily_streak", 0)) + 1
                )
            else:
                # Streak broken — reset
                self.stats["daily_streak"] = 1
        else:
            # First recorded play
            self.stats["daily_streak"] = 1

        self.stats["last_played"] = today.isoformat()
        return self._check_stat_achievements("daily_streak")

    def increment(self, stat: str, amount: int = 1) -> list[str]:
        """Increment a lifetime stat counter and check for new unlocks.

        Args:
            stat: Key in self.stats to increment.
            amount: Amount to add (default 1).

        Returns:
            List of newly-unlocked achievement IDs (may be empty).
        """
        self.stats[stat] = self.stats.get(stat, 0) + amount
        return self._check_stat_achievements(stat)

    # FIXME I think this needs to be refactored for achievements that can be
    # unlocked mid game (e.g. hit 10 points without using a shield but game
    # isn't over yet and they use a shield charge later on)
    def check_game_score(self, score: int, shield_used: bool) -> list[str]:
        """Check single-game score achievements at game-over.

        Checks both ``game_score`` achievements (score milestones) and
        ``no_shield`` achievements (score milestones without using a
        shield this game).

        Args:
            score: Final score for the game just ended.
            shield_used: Whether the player used a shield charge this game.

        Returns:
            List of newly-unlocked achievement IDs (may be empty).
        """
        newly_unlocked = []
        for aid, entry in ACHIEVEMENT_REGISTRY.items():
            if aid in self.unlocked:
                continue
            if entry.kind == "game_score" and score >= entry.threshold:
                self.unlocked.add(aid)
                newly_unlocked.append(aid)
            elif (entry.kind == "no_shield"
                  and not shield_used
                  and score >= entry.threshold):
                self.unlocked.add(aid)
                newly_unlocked.append(aid)
        return newly_unlocked

    def check_rank(self, rank_id: int) -> list[str]:
        """Check rank achievements after a rank change.

        Args:
            rank_id: The player's new rank ID (1=Diamond … 7=Bamboo).

        Returns:
            List of newly-unlocked achievement IDs (may be empty).
        """
        newly_unlocked = []
        for aid, entry in ACHIEVEMENT_REGISTRY.items():
            if aid in self.unlocked:
                continue
            # threshold stores the required rank_id; lower id = higher rank,
            # so unlock when the player's rank_id <= the achievement threshold
            if entry.kind == "rank" and rank_id <= entry.threshold:
                self.unlocked.add(aid)
                newly_unlocked.append(aid)
        return newly_unlocked

    def unlock(self, achievement_id: str) -> list[str]:
        """Manually unlock a specific achievement (store / manual types).

        Args:
            achievement_id: Registry key for the achievement to unlock.

        Returns:
            List containing the ID if newly unlocked, else empty list.
        """
        if (achievement_id in ACHIEVEMENT_REGISTRY
                and achievement_id not in self.unlocked):
            self.unlocked.add(achievement_id)
            return [achievement_id]
        return []

    def to_list(self) -> list[str]:
        """Serialize unlocked set for persistence in Profile.

        Returns:
            Sorted list of unlocked achievement IDs.
        """
        return sorted(self.unlocked)

    # ------------------------------------------------------------------ #
    # Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    def _check_stat_achievements(self, stat: str) -> list[str]:
        """Check all stat-type achievements tied to the given stat key.

        Args:
            stat: The stat key that was just incremented.

        Returns:
            List of newly-unlocked achievement IDs (may be empty).
        """
        current = self.stats[stat]
        newly_unlocked = []
        for aid, entry in ACHIEVEMENT_REGISTRY.items():
            if aid in self.unlocked:
                continue
            if (entry.kind == "stat"
                    and entry.stat_key == stat
                    and current >= entry.threshold):
                self.unlocked.add(aid)
                newly_unlocked.append(aid)
        return newly_unlocked
