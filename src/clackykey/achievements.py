from typing import NamedTuple


# Achievement types:
#   "stat"       - a lifetime counter crosses a threshold (checked increment())
#   "game_score" - score in a single game (checked at game-over)
#   "no_shield"  - reach score X in one game without using a shield
#   "rank"       - reach a specific rank
#   "store"      - triggered by a store/upgrade event
#   "manual"     - checked explicitly (prestige, 3rd-charge shield deploy, etc.)
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
    # #92
    "prestige": Achievement(
        name="Beyond the Top",
        description="Achieve prestige",
        kind="manual",
        stat_key=None,
        threshold=1,
    ),

    # ------------------------------------------------------------------ #
    # Rank achievements (#93-97)                                         #
    # rank IDs: 5=Bronze, 4=Silver, 3=Gold, 2=Platinum, 1=Diamond        #
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

    # ------------------------------------------------------------------ #
    # Store / Energy (#98-100)                                           #
    # ------------------------------------------------------------------ #
    # #98
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
    # Single-game events (#101)                                          #
    # ------------------------------------------------------------------ #
    # #101
    "active_shield_3rd_charge": Achievement(
        name="Triple Threat",
        description="Deploy an active shield using the 3rd charge",
        kind="manual",
        stat_key=None,
        threshold=1,
    ),

    # ------------------------------------------------------------------ #
    # Single-game score milestones (#102-107)                            #
    # ------------------------------------------------------------------ #
    # #102
    "score_50_game": Achievement(
        name="Half Century",
        description="Reach 50 points in one game",
        kind="game_score",
        stat_key=None,
        threshold=50,
    ),
    # #103
    "score_100_game": Achievement(
        name="Century",
        description="Reach 100 points in one game",
        kind="game_score",
        stat_key=None,
        threshold=100,
    ),
    # #104
    "score_200_game": Achievement(
        name="Double Century",
        description="Reach 200 points in one game",
        kind="game_score",
        stat_key=None,
        threshold=200,
    ),
    # #105
    "score_300_game": Achievement(
        name="Triple Century",
        description="Reach 300 points in one game",
        kind="game_score",
        stat_key=None,
        threshold=300,
    ),
    # #106
    "score_400_game": Achievement(
        name="Quadruple Century",
        description="Reach 400 points in one game",
        kind="game_score",
        stat_key=None,
        threshold=400,
    ),
    # #107
    "score_500_game": Achievement(
        name="Quintuple Century",
        description="Reach 500 points in one game",
        kind="game_score",
        stat_key=None,
        threshold=500,
    ),
}
