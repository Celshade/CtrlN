"""Tests for ranked character unlock system."""

import pytest

from characters import CHARACTER_ROSTER, CHARACTER_ORDER
from ranks import get_unlocked_characters, RANKS


class TestCharacterUnlocks:
    """Test suite for character unlock progression by rank."""

    def test_base_characters_always_unlocked(self):
        """Base characters should be available at all ranks."""
        base_chars = {"black", "dark_green", "blue", "red"}

        for rank_id in RANKS:
            unlocked = get_unlocked_characters(rank_id)
            assert base_chars.issubset(
                unlocked
            ), f"Base chars not unlocked at rank {rank_id}"

    def test_unranked_only_has_base_characters(self):
        """Unranked (-1) should only have base characters."""
        unlocked = get_unlocked_characters(-1)
        assert unlocked == {
            "black", "dark_green", "blue", "red"
        }, "Unranked should only have base characters"

    def test_bamboo_unlocks_yellow_and_purple(self):
        """Rank 7 (Bamboo) should unlock yellow and purple."""
        unlocked = get_unlocked_characters(7)
        assert "yellow" in unlocked, "Yellow not unlocked at Bamboo"
        assert "purple" in unlocked, "Purple not unlocked at Bamboo"
        assert len(unlocked) == 6, "Bamboo should have 6 characters"

    def test_iron_unlocks_green_and_orange(self):
        """Rank 6 (Iron) should unlock green and orange."""
        unlocked = get_unlocked_characters(6)
        assert "green" in unlocked, "Green not unlocked at Iron"
        assert "orange" in unlocked, "Orange not unlocked at Iron"
        # Cumulative: base + bamboo + iron = 8
        assert len(unlocked) == 8, "Iron should have 8 characters"

    def test_silver_unlocks_grey(self):
        """Rank 4 (Silver) should unlock grey."""
        unlocked = get_unlocked_characters(4)
        assert "grey" in unlocked, "Grey not unlocked at Silver"
        # Cumulative: base + bamboo + iron + silver = 9
        assert len(unlocked) == 9, "Silver should have 9 characters"

    def test_gold_unlocks_white(self):
        """Rank 3 (Gold) should unlock white."""
        unlocked = get_unlocked_characters(3)
        assert "white" in unlocked, "White not unlocked at Gold"
        # Cumulative: base + bamboo + iron + silver + gold = 10
        assert len(unlocked) == 10, "Gold should have 10 characters"

    def test_higher_tiers_gain_lower_tier_characters(self):
        """Higher tiers (lower rank numbers) should have all lower tier
        characters in this cumulative system."""
        unlocked_gold = get_unlocked_characters(3)
        unlocked_bamboo = get_unlocked_characters(7)

        # Gold should have everything Bamboo has, plus more
        assert "yellow" in unlocked_gold, "Gold should have yellow"
        assert "purple" in unlocked_gold, "Gold should have purple"

        # Bamboo should also have them
        assert "yellow" in unlocked_bamboo
        assert "purple" in unlocked_bamboo

        # Gold should have more characters than Bamboo
        assert len(unlocked_gold) > len(unlocked_bamboo)

    def test_prestige_no_additional_character_unlock(self):
        """Prestige tier (rank 0) doesn't add new characters beyond
        what lower tiers have."""
        unlocked_prestige = get_unlocked_characters(0)
        unlocked_gold = get_unlocked_characters(3)
        # Prestige should have the same characters as Gold
        assert unlocked_prestige == unlocked_gold

    def test_diamond_no_additional_character_unlock(self):
        """Diamond tier (rank 1) doesn't add new characters beyond
        what lower tiers have."""
        unlocked_diamond = get_unlocked_characters(1)
        unlocked_gold = get_unlocked_characters(3)
        # Diamond should have the same characters as Gold
        assert unlocked_diamond == unlocked_gold

    def test_no_unlock_path_characters(self):
        """Aqua, sunset, silver, gold should not be accessible at any
        rank."""
        no_path = {"aqua", "sunset", "silver", "gold"}

        for rank_id in RANKS:
            unlocked = get_unlocked_characters(rank_id)
            overlap = no_path & unlocked
            assert (
                not overlap
            ), f"Character(s) {overlap} should not unlock at rank {rank_id}"

    def test_all_unlocked_characters_exist_in_roster(self):
        """All returned unlocked characters should exist in roster."""
        for rank_id in RANKS:
            unlocked = get_unlocked_characters(rank_id)
            for char_id in unlocked:
                assert (
                    char_id in CHARACTER_ROSTER
                ), f"Unknown character '{char_id}' unlocked at rank {rank_id}"

    def test_unlocked_set_size_progression(self):
        """Verify the expected size progression of unlocked characters."""
        expected_sizes = {
            -1: 4,   # Unranked: 4 base
            7: 6,    # Bamboo: 4 base + yellow + purple
            6: 8,    # Iron: 4 base + yellow + purple + green + orange
            5: 8,    # Bronze: same as Iron (no new char unlock)
            4: 9,    # Silver: + grey
            3: 10,   # Gold: + white (all rankable chars)
            2: 10,   # Platinum: same as Gold (no char unlock)
            1: 10,   # Diamond: same as Gold (no char unlock)
            0: 10,   # Prestige: same as Gold (no char unlock)
        }

        for rank_id, expected_size in expected_sizes.items():
            unlocked = get_unlocked_characters(rank_id)
            assert len(
                unlocked
            ) == expected_size, (
                f"Rank {rank_id}: expected {expected_size} characters, "
                f"got {len(unlocked)} - {sorted(unlocked)}"
            )

    def test_total_playable_characters(self):
        """Verify total character count."""
        assert (
            len(CHARACTER_ROSTER) == 14
        ), "Should have 14 total characters"

    def test_character_roster_has_required_characters(self):
        """Verify all expected characters exist in roster."""
        required = {
            "black", "dark_green", "blue", "red",  # base
            "yellow", "purple", "green", "orange", "white", "grey",  # ranked
            "aqua", "sunset", "silver", "gold",  # no current unlock
        }

        assert (
            required == set(CHARACTER_ROSTER.keys())
        ), f"Character roster mismatch: {set(CHARACTER_ROSTER.keys())}"
