"""Rank system definitions and utilities.

Defines rank progression tiers, XP thresholds, and feature unlocks.
For player profile management, see profiles.py
"""

from typing import List

# XP Rank definitions with thresholds and unlocks
# NOTE ranks reset every "season" (can be triggered manually or on a schedule)
# NOTE "<color>_key", "role", "server_access" will persist even in season reset
RANKS = {
    0: {
        "name": "Unranked",
        "min_points": None,
        "unlocks": ["basic_access"]
    },
    1: {
        "name": "Diamond",
        "min_points": 10000,
        "unlocks": ["role", "server_access", "prestige", "shield_stabilizers"]
    },
    2: {
        "name": "Platinum",
        "min_points": 7500,
        "unlocks": ["role", "shield_strength+1"]
    },
    3: {
        "name": "Gold",
        "min_points": 5000,
        "unlocks": ["role", "gold_key", "shield_boost+1", "xp_boost+5%"]
    },
    4: {
        "name": "Silver",
        "min_points": 3000,
        "unlocks": ["role", "silver_key", "leaderboard_access", "xp_boost+2%"]
    },
    5: {
        "name": "Bronze",
        "min_points": 1500,
        "unlocks": ["role", "shield_charge+1", "game_stats"]
    },
    6: {
        "name": "Iron",
        "min_points": 500,
        "unlocks": ["green_key", "orange_key"]
    },
    7: {
        "name": "Bamboo",
        "min_points": 100,
        "unlocks": ["yellow_key", "purple_key"]
    }
}


def get_rank_unlocks(rank: int) -> List[str]:
    """Retrieve features/cosmetics unlocked at a given rank.

    Args:
        rank: Rank ID (0-7)

    Returns:
        list: Feature names unlocked at this rank
    """
    if rank in RANKS:
        return RANKS[rank]["unlocks"]
    return []


def display_rank_progression() -> str:
    """
    Display formatted rank progression table with XP requirements.

    Returns:
        str: Formatted table showing all ranks
    """
    output = "RANK PROGRESSION\n"
    output += "=" * 80 + "\n"
    output += f"{'Rank':<15} {'Name':<15} {'Min XP':<12} "
    output += f"{'XP to Next':<12}\n"
    output += "-" * 80 + "\n"

    rank_order = [1, 2, 3, 4, 5, 6, 7, 0]

    for rank_id in rank_order:
        if rank_id == 0:
            output += f"{'0':<15} {'Unranked':<15} {'N/A':<12} "
            output += f"{'0':<12}\n"
        elif rank_id == 1:
            output += f"{'1':<15} {'Diamond':<15} {'10,000':<12} "
            output += f"{'—':<12}\n"
        else:
            min_xp = RANKS[rank_id]["min_points"]
            if rank_id > 1:
                next_rank_min = RANKS[rank_id - 1]["min_points"]
            else:
                next_rank_min = 0
            xp_to_next = next_rank_min - min_xp

            output += f"{rank_id:<15} "
            output += f"{RANKS[rank_id]['name']:<15} "
            output += f"{min_xp:>10,}  "
            output += f"{xp_to_next:>10,}\n"

    return output
