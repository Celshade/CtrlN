"""Create a player xp/rank system"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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
        "unlocks": ["role", "server_access", "prestige", "stabilizers"]
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

# TODO Figure out database solution for persistent player data storage
#   (e.g., SQLite, JSON files, or in-memory with periodic saves)
# In-memory player data storage (can be replaced with database)
_player_data: Dict[str, Dict] = {}


def calculate_rank(xp: int) -> int:
    """
    Determine a player's rank based on total XP earned.

    Args:
        xp: Total experience points

    Returns:
        int: Rank ID (0-7), where 1=Diamond (highest), 0=Unranked
    """
    if xp == 0:
        return 0

    # Iterate through ranks from 1 (Diamond) to 7 (Bamboo)
    # and return the first rank player qualifies for
    for rank_id in range(1, 8):
        if xp >= RANKS[rank_id]["min_points"]:
            return rank_id

    return 7  # Default to Bamboo


def get_rank_progress(xp: int) -> Dict:
    """
    Calculate current rank, XP towards next rank, and progress.

    Args:
        xp: Total experience points

    Returns:
        dict: Rank progress information
    """
    current_rank = calculate_rank(xp)
    current_rank_name = RANKS[current_rank]["name"]

    # Handle Unranked special case
    if current_rank == 0:
        return {
            "current_rank": 0,
            "current_rank_name": "Unranked",
            "xp_in_rank": 0,
            "xp_to_next_rank": 500,
            "progress_percent": 0.0,
            "next_rank": 7
        }

    # Handle Diamond (highest rank)
    if current_rank == 1:
        current_min = RANKS[1]["min_points"]
        return {
            "current_rank": current_rank,
            "current_rank_name": current_rank_name,
            "xp_in_rank": xp - current_min,
            "xp_to_next_rank": 0,
            "progress_percent": 100.0,
            "next_rank": None
        }

    # All other ranks
    current_min = RANKS[current_rank]["min_points"]
    next_min = RANKS[current_rank - 1]["min_points"]

    xp_in_rank = xp - current_min
    xp_to_next = next_min - current_min
    progress_percent = (xp_in_rank / xp_to_next) * 100

    return {
        "current_rank": current_rank,
        "current_rank_name": current_rank_name,
        "xp_in_rank": xp_in_rank,
        "xp_to_next_rank": xp_to_next - xp_in_rank,
        "progress_percent": min(progress_percent, 100.0),
        "next_rank": current_rank - 1
    }


def award_xp(player_id: str, xp_amount: int) -> Dict:
    """
    Award XP to a player and check for rank promotions.

    Args:
        player_id: Unique player identifier
        xp_amount: XP to award

    Returns:
        dict: Award result with rank up information
    """
    # Load or initialize player data
    player = load_player_rank_data(player_id)

    old_rank = calculate_rank(player["total_xp"])
    player["total_xp"] += xp_amount
    new_rank = calculate_rank(player["total_xp"])

    rank_up = new_rank != old_rank and new_rank < old_rank

    player["current_rank"] = new_rank

    # Save updated data
    save_player_rank_data(player_id, player)

    return {
        "xp_awarded": xp_amount,
        "new_total_xp": player["total_xp"],
        "old_rank": old_rank,
        "new_rank": new_rank,
        "rank_up": rank_up,
        "rank_name": RANKS[new_rank]["name"]
    }


def get_rank_unlocks(rank: int) -> List[str]:
    """
    Retrieve features/cosmetics unlocked at a given rank.

    Args:
        rank: Rank ID (0-7)

    Returns:
        list: Feature names unlocked at this rank
    """
    if rank in RANKS:
        return RANKS[rank]["unlocks"]
    return []


def get_all_unlocks(xp: int) -> List[str]:
    """
    Get all unlocks available to a player at their current XP level.

    Args:
        xp: Player's total experience points

    Returns:
        list: All feature/cosmetic unlocks available
    """
    current_rank = calculate_rank(xp)
    unlocks = []

    # If Unranked, return minimal starter unlocks only
    if current_rank == 0:
        return []

    # Collect unlocks from current rank down to Bamboo
    for rank_id in range(current_rank, 7, 1):
        unlocks.extend(RANKS[rank_id]["unlocks"])

    # Always include Bamboo basic access
    unlocks.extend(RANKS[7]["unlocks"])

    return list(set(unlocks))  # Remove duplicates


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


def display_player_progress(
    player_id: str,
    player_xp: int
) -> str:
    """
    Display a player's current rank, XP progress, and next rank info.

    Args:
        player_id: Player identifier
        player_xp: Player's total XP

    Returns:
        str: Formatted progress display
    """
    progress = get_rank_progress(player_xp)
    current_rank = progress["current_rank"]
    current_name = progress["current_rank_name"]

    output = f"{'PLAYER STATS':^80}\n"
    output += "=" * 80 + "\n"
    output += f"Player ID: {player_id}\n"
    output += f"Rank: {current_name} (Rank {current_rank})\n"
    output += f"Total XP: {player_xp:,}\n"

    if progress["next_rank"] is not None:
        next_rank_name = RANKS[progress["next_rank"]]["name"]
        next_min = RANKS[progress["next_rank"]]["min_points"]

        output += f"Next Rank: {next_rank_name} ({next_min:,}+ XP)\n"

        # Create progress bar
        bar_length = 50
        filled_length = int(
            bar_length * progress["progress_percent"] / 100
        )
        bar = "█" * filled_length + "░" * (bar_length - filled_length)

        output += f"Progress: {bar} "
        output += f"{progress['progress_percent']:.0f}% "
        output += f"({progress['xp_to_next_rank']:,} XP to next)\n"
    else:
        output += "Next Rank: None (Maximum rank achieved!)\n"
        output += "Progress: ██████████████████ 100%\n"

    return output


def reset_player_rank(player_id: str) -> Dict:
    """
    Reset player's XP and rank (for seasonal resets or events).

    Args:
        player_id: Player identifier

    Returns:
        dict: Reset result information
    """
    player = load_player_rank_data(player_id)

    reset_xp = player["total_xp"]
    previous_rank = player["current_rank"]

    player["total_xp"] = 0
    player["current_rank"] = 0

    save_player_rank_data(player_id, player)

    return {
        "reset_xp": reset_xp,
        "new_xp": 0,
        "previous_rank": previous_rank,
        "new_rank": 0
    }


def handle_rank_up(
    player_id: str,
    old_rank: int,
    new_rank: int
) -> Dict:
    """
    Handle logic when a player ranks up (promotions).

    Args:
        player_id: Player identifier
        old_rank: Previous rank
        new_rank: New rank

    Returns:
        dict: Rank up handling result
    """
    unlocked_features = get_rank_unlocks(new_rank)
    rank_name = RANKS[new_rank]["name"]

    notification = (
        f"Rank up! You've been promoted to {rank_name}! "
        f"You unlocked: {', '.join(unlocked_features)}"
    )

    return {
        "promotion": True,
        "rank_name": rank_name,
        "unlocked_features": unlocked_features,
        "notification": notification
    }


def save_player_rank_data(player_id: str, rank_data: Dict) -> bool:
    """
    Persist player XP and rank data to storage.

    Args:
        player_id: Player identifier
        rank_data: Player's current rank data

    Returns:
        bool: Success status
    """
    try:
        # Store in memory
        _player_data[player_id] = rank_data

        # Also persist to JSON file for durability
        data_dir = Path("player_data")
        data_dir.mkdir(exist_ok=True)

        file_path = data_dir / f"{player_id}.json"
        with open(file_path, "w") as f:
            json.dump(rank_data, f, indent=2)

        return True
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error saving player data: {e}")
        return False

# FIXME Why are we using dict.copy()?
def load_player_rank_data(player_id: str) -> Dict:
    """
    Load player's saved XP and rank data from storage.

    Args:
        player_id: Player identifier

    Returns:
        dict: Player's rank data or defaults for new player
    """
    # Check memory first
    if player_id in _player_data:
        return _player_data[player_id].copy()

    # Try to load from file
    # TODO Are we making use of Path()? Benefit over just a str?
    data_dir = Path("player_data")
    file_path = data_dir / f"{player_id}.json"

    if file_path.exists():
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                _player_data[player_id] = data
                return data.copy()
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading player data: {e}")

    # Return defaults for new player (Unranked)
    default_data = {
        "player_id": player_id,
        "current_xp": 0,
        "total_xp": 0,
        "current_rank": 0
    }
    _player_data[player_id] = default_data
    return default_data.copy()
