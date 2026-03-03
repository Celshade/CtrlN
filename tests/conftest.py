"""Shared pytest configuration and fixtures."""

import sys
from pathlib import Path

import pytest

# Source modules use bare imports (e.g. `from ranks import RANKS`) that
# require src/clackykey itself to be on sys.path in addition to src/.
_PKG_DIR = Path(__file__).parent.parent / "src" / "clackykey"
if str(_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_PKG_DIR))


@pytest.fixture
def sample_profile():
    """Create a sample profile for testing."""
    from clackykey.profiles import Profile

    return Profile(
        player_id="test_player",
        player_name="Test Player",
        current_xp=100,
        total_xp=500,
        rank=2,
        highest_rank=3,
        prestige=0,
        games_played=0,
        seasons_played=1,
        achievements=["ach1", "ach2"]
    )


@pytest.fixture
def sample_player(sample_profile):
    """Create a sample player for testing."""
    from clackykey.player import Player

    return Player(profile=sample_profile)
