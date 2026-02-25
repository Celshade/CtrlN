"""Shared pytest configuration and fixtures."""

import pytest
import sys


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
