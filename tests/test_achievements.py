"""Tests for src/ctrln/achievements.py"""

from datetime import date, timedelta
from unittest.mock import patch

import pytest

from ctrln.achievements import (
    ACHIEVEMENT_REGISTRY,
    Achievements,
    _BY_KIND,
    _BY_STAT,
    _DEFAULT_STATS,
)


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def _iso(d: date) -> str:
    return d.isoformat()


# ------------------------------------------------------------------ #
# Module-level index sanity checks                                    #
# ------------------------------------------------------------------ #

class TestIndexes:
    def test_by_kind_keys_are_valid_kinds(self):
        valid = {"stat", "game_score", "no_shield", "rank", "store", "manual"}
        assert set(_BY_KIND.keys()).issubset(valid)

    def test_by_kind_covers_all_registry_entries(self):
        indexed = sum(len(v) for v in _BY_KIND.values())
        assert indexed == len(ACHIEVEMENT_REGISTRY)

    def test_by_stat_only_contains_entries_with_stat_key(self):
        for entries in _BY_STAT.values():
            for _aid, entry in entries:
                assert entry.stat_key is not None

    def test_by_stat_all_stat_type_entries_present(self):
        expected = {
            aid
            for aid, e in ACHIEVEMENT_REGISTRY.items()
            if e.stat_key is not None
        }
        found = {
            aid
            for entries in _BY_STAT.values()
            for aid, _ in entries
        }
        assert found == expected

    def test_stat_entries_in_correct_bucket(self):
        for stat_key, entries in _BY_STAT.items():
            for _aid, entry in entries:
                assert entry.stat_key == stat_key


# ------------------------------------------------------------------ #
# Achievements.__init__                                               #
# ------------------------------------------------------------------ #

class TestInit:
    def test_defaults_when_nothing_passed(self):
        a = Achievements()
        assert a.unlocked == set()
        assert a.stats == _DEFAULT_STATS

    def test_unlocked_list_is_converted_to_set(self):
        a = Achievements(unlocked=["games_played_10", "games_played_50"])
        assert a.unlocked == {"games_played_10", "games_played_50"}

    def test_none_unlocked_gives_empty_set(self):
        assert Achievements(unlocked=None).unlocked == set()

    def test_stats_merged_with_defaults(self):
        a = Achievements(stats={"games_played": 42})
        assert a.stats["games_played"] == 42
        # Other default keys still present
        assert a.stats["daily_streak"] == 0

    def test_extra_stat_keys_preserved(self):
        a = Achievements(stats={"custom_key": 7})
        assert a.stats["custom_key"] == 7

    def test_none_stats_gives_defaults(self):
        assert Achievements(stats=None).stats == _DEFAULT_STATS


# ------------------------------------------------------------------ #
# record_play                                                         #
# ------------------------------------------------------------------ #

class TestRecordPlay:
    TODAY = date(2026, 3, 1)
    YESTERDAY = TODAY - timedelta(days=1)
    TWO_DAYS_AGO = TODAY - timedelta(days=2)

    def _make(self, last_played: str = "", streak: int = 0) -> Achievements:
        return Achievements(stats={
            "last_played": last_played,
            "daily_streak": streak,
        })

    def _call(self, a: Achievements) -> list[str]:
        with patch(
            "ctrln.achievements.datetime"
        ) as mock_dt:
            mock_dt.now.return_value.date.return_value = self.TODAY
            return a.record_play()

    def test_first_play_sets_streak_to_one(self):
        a = self._make()
        self._call(a)
        assert a.stats["daily_streak"] == 1

    def test_first_play_sets_last_played(self):
        a = self._make()
        self._call(a)
        assert a.stats["last_played"] == _iso(self.TODAY)

    def test_same_day_does_not_change_streak(self):
        a = self._make(last_played=_iso(self.TODAY), streak=3)
        result = self._call(a)
        assert a.stats["daily_streak"] == 3
        assert result == []

    def test_same_day_refreshes_last_played(self):
        a = self._make(last_played=_iso(self.TODAY), streak=3)
        self._call(a)
        assert a.stats["last_played"] == _iso(self.TODAY)

    def test_consecutive_day_increments_streak(self):
        a = self._make(last_played=_iso(self.YESTERDAY), streak=4)
        self._call(a)
        assert a.stats["daily_streak"] == 5

    def test_gap_resets_streak_to_one(self):
        a = self._make(last_played=_iso(self.TWO_DAYS_AGO), streak=10)
        self._call(a)
        assert a.stats["daily_streak"] == 1

    def test_returns_newly_unlocked_streak_achievements(self):
        # daily_streak_2 threshold is 2; start at streak=1, yesterday
        a = self._make(last_played=_iso(self.YESTERDAY), streak=1)
        result = self._call(a)
        assert "daily_streak_2" in result

    def test_already_unlocked_streak_not_returned(self):
        a = Achievements(
            unlocked=["daily_streak_2"],
            stats={"last_played": _iso(self.YESTERDAY), "daily_streak": 1},
        )
        result = self._call(a)
        assert "daily_streak_2" not in result


# ------------------------------------------------------------------ #
# increment                                                           #
# ------------------------------------------------------------------ #

class TestIncrement:
    def test_increments_stat_by_one(self):
        a = Achievements()
        a.increment("games_played")
        assert a.stats["games_played"] == 1

    def test_increments_by_custom_amount(self):
        a = Achievements()
        a.increment("games_played", 5)
        assert a.stats["games_played"] == 5

    def test_triggers_unlock_at_threshold(self):
        a = Achievements(stats={"games_played": 9})
        result = a.increment("games_played")
        assert "games_played_10" in result
        assert "games_played_10" in a.unlocked

    def test_does_not_re_unlock(self):
        a = Achievements(
            unlocked=["games_played_10"],
            stats={"games_played": 9},
        )
        result = a.increment("games_played")
        assert "games_played_10" not in result

    def test_no_unlocks_when_below_threshold(self):
        a = Achievements(stats={"games_played": 5})
        result = a.increment("games_played")
        assert result == []

    def test_works_for_new_stat_key(self):
        a = Achievements()
        a.increment("yellow_birds_dodged", 50)
        assert a.stats["yellow_birds_dodged"] == 50

    def test_multiple_thresholds_crossed_in_one_increment(self):
        # Jump from 0 to 1000 should unlock all games_played tiers
        a = Achievements(stats={"games_played": 0})
        result = a.increment("games_played", 1000)
        tiers = [
            "games_played_10", "games_played_50", "games_played_100",
            "games_played_150", "games_played_250", "games_played_500",
            "games_played_1000",
        ]
        for t in tiers:
            assert t in result, f"{t} missing from result"


# ------------------------------------------------------------------ #
# check_game_score                                                    #
# ------------------------------------------------------------------ #

class TestCheckGameScore:
    def test_game_score_unlocked_at_threshold(self):
        a = Achievements()
        result = a.check_game_score(50, shield_used=True)
        assert "score_50_game" in result

    def test_game_score_not_unlocked_below_threshold(self):
        a = Achievements()
        result = a.check_game_score(49, shield_used=True)
        assert "score_50_game" not in result

    def test_no_shield_unlocked_without_shield(self):
        a = Achievements()
        result = a.check_game_score(10, shield_used=False)
        assert "no_shield_10" in result

    def test_no_shield_not_unlocked_with_shield(self):
        a = Achievements()
        result = a.check_game_score(10, shield_used=True)
        assert "no_shield_10" not in result

    def test_already_unlocked_skipped(self):
        a = Achievements(unlocked=["score_50_game"])
        result = a.check_game_score(50, shield_used=False)
        assert "score_50_game" not in result

    def test_multiple_score_milestones_at_once(self):
        a = Achievements()
        result = a.check_game_score(200, shield_used=True)
        assert "score_50_game" in result
        assert "score_100_game" in result
        assert "score_200_game" in result
        assert "score_300_game" not in result

    def test_no_shield_and_game_score_both_returned(self):
        a = Achievements()
        result = a.check_game_score(50, shield_used=False)
        assert "score_50_game" in result
        assert "no_shield_50" in result


# ------------------------------------------------------------------ #
# check_rank                                                          #
# ------------------------------------------------------------------ #

class TestCheckRank:
    def test_unlocks_exact_rank(self):
        a = Achievements()
        result = a.check_rank(5)   # Bronze threshold=5
        assert "reach_bronze" in result

    def test_unlocks_all_lower_rank_ids(self):
        # rank_id=0 (Prestige) should unlock everything rank_id <= threshold
        a = Achievements()
        result = a.check_rank(0)
        for aid in [
            "reach_bronze", "reach_silver", "reach_gold",
            "reach_platinum", "reach_diamond", "reach_prestige",
        ]:
            assert aid in result, f"{aid} missing"

    def test_does_not_unlock_higher_rank(self):
        a = Achievements()
        result = a.check_rank(4)   # Silver; Bronze threshold=5, 4<=5 → unlocked
        assert "reach_diamond" not in result  # threshold=1, 4>1

    def test_already_unlocked_skipped(self):
        a = Achievements(unlocked=["reach_bronze"])
        result = a.check_rank(5)
        assert "reach_bronze" not in result


# ------------------------------------------------------------------ #
# unlock                                                              #
# ------------------------------------------------------------------ #

class TestUnlock:
    def test_unlocks_known_achievement(self):
        a = Achievements()
        result = a.unlock("active_shield_3rd_charge")
        assert result == ["active_shield_3rd_charge"]
        assert "active_shield_3rd_charge" in a.unlocked

    def test_returns_empty_if_already_unlocked(self):
        a = Achievements(unlocked=["active_shield_3rd_charge"])
        result = a.unlock("active_shield_3rd_charge")
        assert result == []

    def test_returns_empty_for_unknown_id(self):
        a = Achievements()
        result = a.unlock("does_not_exist")
        assert result == []

    def test_does_not_add_unknown_id_to_unlocked(self):
        a = Achievements()
        a.unlock("does_not_exist")
        assert "does_not_exist" not in a.unlocked


# ------------------------------------------------------------------ #
# to_list                                                             #
# ------------------------------------------------------------------ #

class TestToList:
    def test_returns_sorted_list(self):
        a = Achievements(
            unlocked=["score_100_game", "games_played_10", "reach_bronze"]
        )
        result = a.to_list()
        assert result == sorted(result)

    def test_empty_unlocked_returns_empty_list(self):
        assert Achievements().to_list() == []

    def test_all_ids_present(self):
        ids = ["score_100_game", "no_shield_10", "reach_gold"]
        a = Achievements(unlocked=ids)
        assert set(a.to_list()) == set(ids)


# ------------------------------------------------------------------ #
# _unlock_matching                                                    #
# ------------------------------------------------------------------ #

class TestUnlockMatching:
    def test_returns_empty_when_predicate_always_false(self):
        a = Achievements()
        candidates = list(ACHIEVEMENT_REGISTRY.items())
        result = a._unlock_matching(candidates, lambda _: False)
        assert result == []

    def test_unlocks_when_predicate_true(self):
        a = Achievements()
        candidates = [("games_played_10", ACHIEVEMENT_REGISTRY["games_played_10"])]
        result = a._unlock_matching(candidates, lambda _: True)
        assert result == ["games_played_10"]
        assert "games_played_10" in a.unlocked

    def test_skips_already_unlocked(self):
        a = Achievements(unlocked=["games_played_10"])
        candidates = [("games_played_10", ACHIEVEMENT_REGISTRY["games_played_10"])]
        result = a._unlock_matching(candidates, lambda _: True)
        assert result == []

    def test_empty_candidates_returns_empty(self):
        a = Achievements()
        assert a._unlock_matching([], lambda _: True) == []


# ------------------------------------------------------------------ #
# _check_stat_achievements                                            #
# ------------------------------------------------------------------ #

class TestCheckStatAchievements:
    def test_returns_matching_achievements_at_threshold(self):
        a = Achievements(stats={"games_played": 10})
        result = a._check_stat_achievements("games_played")
        assert "games_played_10" in result

    def test_does_not_return_above_threshold_achievement(self):
        a = Achievements(stats={"games_played": 10})
        result = a._check_stat_achievements("games_played")
        assert "games_played_50" not in result

    def test_unknown_stat_returns_empty(self):
        a = Achievements()
        assert a._check_stat_achievements("nonexistent_stat") == []

    def test_already_unlocked_not_returned(self):
        a = Achievements(
            unlocked=["games_played_10"],
            stats={"games_played": 10},
        )
        result = a._check_stat_achievements("games_played")
        assert "games_played_10" not in result
