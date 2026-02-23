import json
from pathlib import Path
from typing import Dict, List

# Import rank system
from .ranks import RANKS


class Profile:
    """Data container for player progression tracking.

    Stores player statistics and provides JSON serialization for
    persistence. All progression logic is in the Player class.
    """
    # memory-efficient attribute storage
    __slots__ = ("_player_id", "_player_name", "_current_xp", "_total_xp",
                 "_rank", "_highest_rank", "_prestige", "_seasons_played",
                 "_achievements")

# Getters and Setters with type validation
    @property
    def player_id(self) -> str:
        """Get player ID."""
        return self._player_id

    @player_id.setter
    def player_id(self, value: str) -> None:
        """Set player ID with validation."""
        if not isinstance(value, str) or not value:
            raise ValueError("player_id must be a non-empty string")
        self._player_id = value

    @property
    def player_name(self) -> str:
        """Get player name."""
        return self._player_name

    @player_name.setter
    def player_name(self, value: str) -> None:
        """Set player name with validation."""
        if not isinstance(value, str) or not value:
            raise ValueError("player_name must be a non-empty string")
        self._player_name = value

    @property
    def current_xp(self) -> int:
        """Get current season XP."""
        return self._current_xp

    @current_xp.setter
    def current_xp(self, value: int) -> None:
        """Set current season XP with validation."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("current_xp must be a non-negative integer")
        self._current_xp = value

    @property
    def total_xp(self) -> int:
        """Get total all-time XP."""
        return self._total_xp

    @total_xp.setter
    def total_xp(self, value: int) -> None:
        """Set total all-time XP with validation."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("total_xp must be a non-negative integer")
        self._total_xp = value

    @property
    def rank(self) -> int:
        """Get current rank."""
        return self._rank

    @rank.setter
    def rank(self, value: int) -> None:
        """Set current rank with validation."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("rank must be a non-negative integer")
        self._rank = value

    @property
    def highest_rank(self) -> int:
        """Get highest rank achieved."""
        return self._highest_rank

    @highest_rank.setter
    def highest_rank(self, value: int) -> None:
        """Set highest rank with validation."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("highest_rank must be a non-negative integer")
        self._highest_rank = value

    @property
    def prestige(self) -> int:
        """Get prestige level."""
        return self._prestige

    @prestige.setter
    def prestige(self, value: int) -> None:
        """Set prestige level with validation."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("prestige must be a non-negative integer")
        self._prestige = value

    @property
    def seasons_played(self) -> int:
        """Get number of seasons played."""
        return self._seasons_played

    @seasons_played.setter
    def seasons_played(self, value: int) -> None:
        """Set number of seasons played with validation."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("seasons_played must be a non-negative integer")
        self._seasons_played = value

    @property
    def achievements(self) -> list:
        """Get list of achievements."""
        return self._achievements

    @achievements.setter
    def achievements(self, value: list) -> None:
        """Set achievements with validation."""
        if not isinstance(value, list):
            raise ValueError("achievements must be a list")
        self._achievements = value

    def __init__(self,
                 player_id: str, player_name: str,
                 current_xp: int, total_xp: int,
                 rank: int, highest_rank: int = 0, prestige: int = 0,
                 seasons_played: int = 0, achievements: list = None):
        """Initialize a player profile with validation.

        Args:
            player_id: Unique player identifier.
            player_name: Display name.
            current_xp: XP earned in current season.
            total_xp: All-time XP earned.
            rank: Current rank ID 0-7.
            highest_rank: Best rank achieved (default=0).
            prestige: Prestige level (default=0).
            seasons_played: Number of completed seasons (default=0).
            achievements: List of achievement IDs (default=None=>[]).

        Raises:
            ValueError: If any argument fails type or value validation.
        """
        # Validate primary args
        if not isinstance(player_id, str) or not player_id:
            raise ValueError("player_id must be a non-empty string")
        if not isinstance(player_name, str) or not player_name:
            raise ValueError("player_name must be non-empty string")
        if not isinstance(current_xp, int) or current_xp < 0:
            raise ValueError("current_xp must be a non-negative integer")
        if not isinstance(total_xp, int) or total_xp < 0:
            raise ValueError("total_xp must be a non-negative integer")
        if not isinstance(rank, int) or rank < 0:
            raise ValueError("rank must be a non-negative integer")

        # Validate optional args
        if not isinstance(highest_rank, int) or highest_rank < 0:
            raise ValueError("highest_rank must be a non-negative integer")
        if not isinstance(prestige, int) or prestige < 0:
            raise ValueError("prestige must be a non-negative integer")
        if not isinstance(seasons_played, int) or seasons_played < 0:
            raise ValueError("seasons_played must be a non-negative integer")
        if achievements is None:
            achievements = []
        elif not isinstance(achievements, list):
            raise ValueError("achievements must be a list")

        self.player_id = player_id
        self.player_name = player_name
        self.current_xp = current_xp
        self.total_xp = total_xp
        self.rank = rank
        self.highest_rank = highest_rank
        self.prestige = prestige
        self.seasons_played = seasons_played
        self.achievements = achievements

    @classmethod
    def load_from_json(cls, filename: str) -> 'Profile':
        """Load profile data from a JSON file.

        Loads player profile from JSON with required fields (id, name,
        current_xp, total_xp, rank) and optional fields (highest_rank,
        prestige, seasons_played, achievements).

        Args:
            filename: Path to the JSON profile file.

        Returns:
            Profile: New Profile instance loaded from file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If JSON data is missing required fields or
                has invalid types.
            json.JSONDecodeError: If JSON syntax is invalid.
        """
        try:
            with open(filename, "r") as f:
                data = json.load(f)

            return cls(
                player_id=data["id"],
                player_name=data["name"],
                current_xp=data["current_xp"],
                total_xp=data["total_xp"],
                rank=data["rank"],
                highest_rank=data.get("highest_rank", 0),
                prestige=data.get("prestige", 0),
                seasons_played=data.get("seasons_played", 0),
                achievements=data.get("achievements", [])
            )
        except KeyError as ke:
            raise ValueError(f"Missing required field: {ke}") from ke
        except ValueError as ve:
            raise ValueError(f"Invalid profile data: {ve}") from ve
        except json.JSONDecodeError as je:
            raise ValueError(f"Malformed JSON in {filename}: {je}") from je
        except FileNotFoundError as fe:
            raise FileNotFoundError(f"{filename} not found: {fe}") from fe

    @classmethod
    def load_by_id(cls, player_id: str) -> 'Profile':
        """Load profile using standard player directory location.

        Args:
            player_id: Unique player identifier.

        Returns:
            Profile: New Profile instance loaded from file, or
                default Unranked profile if not found.

        Raises:
            ValueError: If file exists but data is invalid.
        """
        data_dir = Path("player_data")
        filename = str(data_dir / f"{player_id}.json")

        if Path(filename).exists():
            return cls.load_from_json(filename)

        # Return new Unranked profile
        return cls(
            player_id=player_id,
            player_name="Unknown",
            current_xp=0,
            total_xp=0,
            rank=0
        )

    def save_to_file(self, filename: str = None, data: dict = None) -> bool:
        """Persist profile to JSON file.

        Args:
            filename: Path to save file. If None, uses default
                pattern player_data/{player_id}.json
            data: Optional dictionary of profile fields to update
                before saving. If provided, calls update_profile(data).

        Returns:
            bool: Success status.
        """
        try:
            if data is not None:
                self.update_profile(data)

            if filename is None:
                data_dir = Path("player_data")
                data_dir.mkdir(exist_ok=True)
                filename = str(data_dir / f"{self.player_id}.json")

            profile_data = {
                "id": self.player_id,
                "name": self.player_name,
                "current_xp": self.current_xp,
                "total_xp": self.total_xp,
                "rank": self.rank,
                "highest_rank": self.highest_rank,
                "prestige": self.prestige,
                "seasons_played": self.seasons_played,
                "achievements": self.achievements
            }

            with open(filename, "w") as f:
                json.dump(profile_data, f, indent=2)

            return True
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error saving profile: {e}")
            return False

    def update_profile(self, data: dict) -> None:
        """Update profile attributes from a data dictionary.

        Args:
            data: Dictionary containing profile fields to update.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
