"""Tests for src/ctrln/ranks.py"""

import pytest

from ctrln.ranks import RANKS, display_rank_progression, get_rank_unlocks


# ------------------------------------------------------------------ #
# RANKS structure                                                     #
# ------------------------------------------------------------------ #

class TestRanksStructure:
    EXPECTED_IDS = {-1, 0, 1, 2, 3, 4, 5, 6, 7}

    def test_all_rank_ids_present(self):
        assert set(RANKS.keys()) == self.EXPECTED_IDS

    def test_every_rank_has_name(self):
        for rid, data in RANKS.items():
            assert "name" in data, f"rank {rid} missing 'name'"
            assert isinstance(data["name"], str)
            assert data["name"]

    def test_every_rank_has_unlocks(self):
        for rid, data in RANKS.items():
            assert "unlocks" in data, f"rank {rid} missing 'unlocks'"
            assert isinstance(data["unlocks"], list)

    def test_every_rank_has_min_points(self):
        for rid, data in RANKS.items():
            assert "min_points" in data, f"rank {rid} missing 'min_points'"

    def test_unranked_min_points_is_none(self):
        assert RANKS[-1]["min_points"] is None

    def test_ranked_tiers_have_integer_min_points(self):
        for rid in [0, 1, 2, 3, 4, 5, 6, 7]:
            mp = RANKS[rid]["min_points"]
            assert isinstance(mp, int), (
                f"rank {rid} min_points should be int, got {type(mp)}"
            )

    def test_higher_tiers_require_more_xp(self):
        """Lower rank_id == higher tier; thresholds should be ascending."""
        ordered = sorted(
            [(rid, RANKS[rid]["min_points"])
             for rid in range(1, 8)],  # 1=Diamond … 7=Bamboo
            key=lambda x: x[0],
        )
        for i in range(len(ordered) - 1):
            lower_id, lower_xp = ordered[i]
            higher_id, higher_xp = ordered[i + 1]
            assert higher_xp < lower_xp, (
                f"rank {higher_id} (min={higher_xp}) should be < "
                f"rank {lower_id} (min={lower_xp})"
            )

    def test_specific_rank_names(self):
        expected = {
            -1: "Unranked",
            0: "Prestige",
            1: "Diamond",
            2: "Platinum",
            3: "Gold",
            4: "Silver",
            5: "Bronze",
            6: "Iron",
            7: "Bamboo",
        }
        for rid, name in expected.items():
            assert RANKS[rid]["name"] == name

    def test_unranked_has_basic_shield_unlock(self):
        assert "basic_shield" in RANKS[-1]["unlocks"]

    def test_prestige_threshold(self):
        assert RANKS[0]["min_points"] == 15000


# ------------------------------------------------------------------ #
# get_rank_unlocks                                                    #
# ------------------------------------------------------------------ #

class TestGetRankUnlocks:
    def test_returns_list_for_valid_rank(self):
        result = get_rank_unlocks(5)
        assert isinstance(result, list)

    def test_known_unlocks_present(self):
        result = get_rank_unlocks(-1)
        assert "basic_shield" in result
        assert "thrusters" in result

    def test_returns_empty_list_for_unknown_rank(self):
        assert get_rank_unlocks(99) == []
        assert get_rank_unlocks(-2) == []

    def test_all_valid_ranks_return_non_empty(self):
        for rid in RANKS:
            assert get_rank_unlocks(rid), (
                f"rank {rid} returned empty unlocks list"
            )

    def test_prestige_unlock_at_rank_0(self):
        assert "prestige" in get_rank_unlocks(0)

    def test_bronze_shield_charge_plus1(self):
        assert "shield_charge+1" in get_rank_unlocks(5)


# ------------------------------------------------------------------ #
# display_rank_progression                                            #
# ------------------------------------------------------------------ #

class TestDisplayRankProgression:
    def test_returns_string(self):
        assert isinstance(display_rank_progression(), str)

    def test_contains_all_rank_names(self):
        output = display_rank_progression()
        for rid, data in RANKS.items():
            assert data["name"] in output, (
                f"'{data['name']}' not found in progression table"
            )

    def test_contains_header(self):
        assert "RANK PROGRESSION" in display_rank_progression()

    def test_output_is_multi_line(self):
        assert display_rank_progression().count("\n") > 5
