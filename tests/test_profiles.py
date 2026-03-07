"""Tests for src/clackykey/profiles.py"""

import json
from pathlib import Path

import pytest

from clackykey.profiles import Profile


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def _make(**kwargs) -> Profile:
    """Minimal valid Profile; override any field via kwargs."""
    defaults = dict(
        player_id="p1",
        player_name="Tester",
        current_xp=0,
        total_xp=0,
        rank=7,
    )
    defaults.update(kwargs)
    return Profile(**defaults)


def _write_json(path: Path, data: dict) -> str:
    path.write_text(json.dumps(data))
    return str(path)


# ------------------------------------------------------------------ #
# Profile.__init__ — valid construction                               #
# ------------------------------------------------------------------ #

class TestProfileInit:
    def test_minimal_construction(self):
        p = _make()
        assert p.player_id == "p1"
        assert p.player_name == "Tester"
        assert p.current_xp == 0
        assert p.total_xp == 0
        assert p.rank == 7

    def test_optional_defaults(self):
        p = _make()
        assert p.highest_rank == 0
        assert p.prestige == 0
        assert p.seasons_played == 0
        assert p.games_played == 0
        assert p.achievements == []
        assert p.achievement_stats == {}

    def test_explicit_optional_fields(self):
        p = _make(
            highest_rank=3,
            prestige=1,
            seasons_played=5,
            games_played=100,
            achievements=["games_played_10"],
            achievement_stats={"games_played": 100},
        )
        assert p.highest_rank == 3
        assert p.prestige == 1
        assert p.seasons_played == 5
        assert p.games_played == 100
        assert p.achievements == ["games_played_10"]
        assert p.achievement_stats == {"games_played": 100}

    def test_none_achievements_defaults_to_empty_list(self):
        p = _make(achievements=None)
        assert p.achievements == []

    def test_none_achievement_stats_defaults_to_empty_dict(self):
        p = _make(achievement_stats=None)
        assert p.achievement_stats == {}


# ------------------------------------------------------------------ #
# Profile.__init__ — validation errors                                #
# ------------------------------------------------------------------ #

class TestProfileInitValidation:
    @pytest.mark.parametrize("bad", ["", 0, None, 1.5, []])
    def test_invalid_player_id(self, bad):
        with pytest.raises((ValueError, TypeError)):
            _make(player_id=bad)

    @pytest.mark.parametrize("bad", ["", 0, None, 1.5])
    def test_invalid_player_name(self, bad):
        with pytest.raises((ValueError, TypeError)):
            _make(player_name=bad)

    @pytest.mark.parametrize("bad", [-1, -100, "x", 1.5, None])
    def test_invalid_current_xp(self, bad):
        with pytest.raises((ValueError, TypeError)):
            _make(current_xp=bad)

    @pytest.mark.parametrize("bad", [-1, "x", None])
    def test_invalid_total_xp(self, bad):
        with pytest.raises((ValueError, TypeError)):
            _make(total_xp=bad)

    @pytest.mark.parametrize("bad", [-2, "x", None])
    def test_invalid_rank(self, bad):
        with pytest.raises((ValueError, TypeError)):
            _make(rank=bad)

    @pytest.mark.parametrize("bad", [-1, "x"])
    def test_invalid_highest_rank(self, bad):
        with pytest.raises((ValueError, TypeError)):
            _make(highest_rank=bad)

    @pytest.mark.parametrize("bad", [-1, "x"])
    def test_invalid_prestige(self, bad):
        with pytest.raises((ValueError, TypeError)):
            _make(prestige=bad)

    @pytest.mark.parametrize("bad", [-1, "x"])
    def test_invalid_seasons_played(self, bad):
        with pytest.raises((ValueError, TypeError)):
            _make(seasons_played=bad)

    @pytest.mark.parametrize("bad", [-1, "x"])
    def test_invalid_games_played(self, bad):
        with pytest.raises((ValueError, TypeError)):
            _make(games_played=bad)

    def test_invalid_achievements_type(self):
        with pytest.raises(ValueError):
            _make(achievements="not_a_list")

    def test_invalid_achievement_stats_type(self):
        with pytest.raises(ValueError):
            _make(achievement_stats="not_a_dict")


# ------------------------------------------------------------------ #
# Property setters                                                    #
# ------------------------------------------------------------------ #

class TestPropertySetters:
    def test_set_current_xp(self):
        p = _make()
        p.current_xp = 500
        assert p.current_xp == 500

    def test_set_current_xp_zero(self):
        p = _make(current_xp=10)
        p.current_xp = 0
        assert p.current_xp == 0

    def test_set_current_xp_negative_raises(self):
        p = _make()
        with pytest.raises(ValueError):
            p.current_xp = -1

    def test_set_total_xp(self):
        p = _make()
        p.total_xp = 1000
        assert p.total_xp == 1000

    def test_set_rank(self):
        p = _make()
        p.rank = 3
        assert p.rank == 3

    def test_set_rank_negative_raises(self):
        p = _make()
        with pytest.raises(ValueError):
            p.rank = -2

    def test_set_achievements(self):
        p = _make()
        p.achievements = ["games_played_10"]
        assert p.achievements == ["games_played_10"]

    def test_set_achievements_non_list_raises(self):
        p = _make()
        with pytest.raises(ValueError):
            p.achievements = "not_a_list"

    def test_set_achievement_stats(self):
        p = _make()
        p.achievement_stats = {"games_played": 42}
        assert p.achievement_stats["games_played"] == 42

    def test_set_achievement_stats_non_dict_raises(self):
        p = _make()
        with pytest.raises(ValueError):
            p.achievement_stats = [1, 2, 3]


# ------------------------------------------------------------------ #
# load_from_json                                                      #
# ------------------------------------------------------------------ #

class TestLoadFromJson:
    def _base_data(self) -> dict:
        return {
            "id": "player1",
            "name": "Alice",
            "current_xp": 200,
            "total_xp": 1500,
            "rank": 5,
        }

    def test_loads_required_fields(self, tmp_path):
        path = _write_json(tmp_path / "p.json", self._base_data())
        p = Profile.load_from_json(path)
        assert p.player_id == "player1"
        assert p.player_name == "Alice"
        assert p.current_xp == 200
        assert p.total_xp == 1500
        assert p.rank == 5

    def test_optional_fields_default_when_absent(self, tmp_path):
        path = _write_json(tmp_path / "p.json", self._base_data())
        p = Profile.load_from_json(path)
        assert p.highest_rank == 0
        assert p.prestige == 0
        assert p.seasons_played == 0
        assert p.games_played == 0
        assert p.achievements == []
        assert p.achievement_stats == {}

    def test_loads_optional_fields_when_present(self, tmp_path):
        data = self._base_data()
        data.update({
            "highest_rank": 3,
            "prestige": 1,
            "seasons_played": 4,
            "games_played": 80,
            "achievements": ["reach_bronze"],
            "achievement_stats": {"games_played": 80},
        })
        path = _write_json(tmp_path / "p.json", data)
        p = Profile.load_from_json(path)
        assert p.highest_rank == 3
        assert p.prestige == 1
        assert p.achievements == ["reach_bronze"]
        assert p.achievement_stats == {"games_played": 80}

    def test_missing_required_field_raises_value_error(self, tmp_path):
        data = self._base_data()
        del data["rank"]
        path = _write_json(tmp_path / "p.json", data)
        with pytest.raises(ValueError, match="Missing required field"):
            Profile.load_from_json(path)

    def test_file_not_found_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            Profile.load_from_json(str(tmp_path / "nonexistent.json"))

    def test_malformed_json_raises_value_error(self, tmp_path):
        path = tmp_path / "bad.json"
        path.write_text("{not valid json")
        with pytest.raises(ValueError, match="Malformed JSON"):
            Profile.load_from_json(str(path))

    def test_invalid_field_type_raises_value_error(self, tmp_path):
        data = self._base_data()
        data["current_xp"] = "not_an_int"
        path = _write_json(tmp_path / "p.json", data)
        with pytest.raises(ValueError):
            Profile.load_from_json(path)


# ------------------------------------------------------------------ #
# save_to_file                                                        #
# ------------------------------------------------------------------ #

class TestSaveToFile:
    def test_saves_and_reloads(self, tmp_path):
        p = _make(
            player_id="save_test",
            player_name="Bob",
            current_xp=100,
            total_xp=500,
            rank=6,
            achievements=["games_played_10"],
        )
        path = str(tmp_path / "save_test.json")
        assert p.save_to_file(path) is True
        loaded = Profile.load_from_json(path)
        assert loaded.player_id == "save_test"
        assert loaded.player_name == "Bob"
        assert loaded.current_xp == 100
        assert loaded.achievements == ["games_played_10"]

    def test_returns_true_on_success(self, tmp_path):
        p = _make()
        assert p.save_to_file(str(tmp_path / "out.json")) is True

    def test_returns_false_on_bad_path(self):
        p = _make()
        result = p.save_to_file("/nonexistent_dir/__bad__/out.json")
        assert result is False

    def test_full_round_trip_preserves_all_fields(self, tmp_path):
        p = _make(
            highest_rank=2,
            prestige=1,
            seasons_played=3,
            games_played=50,
            achievements=["reach_bronze", "no_shield_10"],
            achievement_stats={"games_played": 50, "daily_streak": 5},
        )
        path = str(tmp_path / "rt.json")
        p.save_to_file(path)
        rt = Profile.load_from_json(path)
        assert rt.highest_rank == 2
        assert rt.prestige == 1
        assert rt.seasons_played == 3
        assert rt.games_played == 50
        assert set(rt.achievements) == {"reach_bronze", "no_shield_10"}
        assert rt.achievement_stats["daily_streak"] == 5

    def test_save_with_data_dict_updates_before_saving(self, tmp_path):
        p = _make(current_xp=0)
        path = str(tmp_path / "update.json")
        p.save_to_file(path, data={"current_xp": 999})
        loaded = Profile.load_from_json(path)
        assert loaded.current_xp == 999


# ------------------------------------------------------------------ #
# load_by_id                                                          #
# ------------------------------------------------------------------ #

class TestLoadById:
    def test_returns_default_profile_when_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        p = Profile.load_by_id("missing_player")
        assert p.player_id == "missing_player"
        assert p.player_name == "Unknown"
        assert p.current_xp == 0
        assert p.rank == -1

    def test_loads_existing_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        data_dir = tmp_path / "player_data"
        data_dir.mkdir()
        _write_json(data_dir / "alice.json", {
            "id": "alice",
            "name": "Alice",
            "current_xp": 300,
            "total_xp": 300,
            "rank": 5,
        })
        p = Profile.load_by_id("alice")
        assert p.player_name == "Alice"
        assert p.current_xp == 300


# ------------------------------------------------------------------ #
# update_profile                                                      #
# ------------------------------------------------------------------ #

class TestUpdateProfile:
    def test_updates_existing_attribute(self):
        p = _make(current_xp=0)
        p.update_profile({"current_xp": 250})
        assert p.current_xp == 250

    def test_updates_multiple_attributes(self):
        p = _make()
        p.update_profile({"current_xp": 100, "games_played": 5})
        assert p.current_xp == 100
        assert p.games_played == 5

    def test_unknown_keys_are_silently_ignored(self):
        p = _make()
        p.update_profile({"nonexistent_field": 99})  # should not raise

    def test_validation_still_enforced_via_setter(self):
        p = _make()
        with pytest.raises(ValueError):
            p.update_profile({"current_xp": -5})
