extends Node
## Tracks achievement unlocks & lifetime stats.

signal achievement_unlocked(achievement_id: String)

# Achievement definitions: id -> {name, description, kind, stat_key, threshold}
var registry: Dictionary = {}
var unlocked: Array = []
var stats: Dictionary = {}


func _ready() -> void:
	_build_registry()
	# Load from profile
	unlocked = ProfileManager.current_profile.get("achievements", []).duplicate()
	stats = ProfileManager.current_profile.get("achievement_stats", {}).duplicate()
	_ensure_default_stats()


func _ensure_default_stats() -> void:
	var defaults := [
		"yellow_birds_dodged", "yellow_perched_hit", "red_birds_dodged",
		"red_perched_hit", "trees_hit", "ground_crashes", "ceiling_crashes",
		"shields_regenerated", "shields_used", "games_played", "daily_streak",
	]
	for key in defaults:
		if not stats.has(key):
			stats[key] = 0
	if not stats.has("last_played"):
		stats["last_played"] = ""


func _build_registry() -> void:
	# Combat
	_reg("yellow_birds_dodged_50", "Bird Dodger", "stat", "yellow_birds_dodged", 50)
	_reg("yellow_perched_hit_10", "Tree Sniper", "stat", "yellow_perched_hit", 10)
	_reg("red_birds_dodged_25", "Red Evader", "stat", "red_birds_dodged", 25)
	_reg("red_perched_hit_10", "Red Hunter", "stat", "red_perched_hit", 10)
	_reg("trees_hit_10", "Lumberjack", "stat", "trees_hit", 10)
	_reg("ground_crashes_10", "Ground Pounder", "stat", "ground_crashes", 10)
	_reg("ceiling_crashes_10", "Sky Scraper", "stat", "ceiling_crashes", 10)
	_reg("shields_regenerated_25", "Shield Master", "stat", "shields_regenerated", 25)
	_reg("shields_used_10", "Shield User", "stat", "shields_used", 10)
	# Games played
	for t in [10, 50, 100, 150, 250, 500, 1000]:
		_reg("games_played_%d" % t, "%d Games" % t, "stat", "games_played", t)
	# Score milestones
	for t in [50, 100, 200, 300, 400, 500]:
		_reg("score_%d_game" % t, "Score %d" % t, "game_score", "", t)
	# No-shield runs
	for t in [10, 50, 100, 150]:
		_reg("no_shield_%d" % t, "No Shield %d" % t, "no_shield_score", "", t)
	# Rank achievements
	var rank_names := {5: "Bronze", 4: "Silver", 3: "Gold", 2: "Platinum", 1: "Diamond", 0: "Prestige"}
	for rank_id in rank_names:
		_reg("reach_%s" % rank_names[rank_id].to_lower(), "Reach %s" % rank_names[rank_id], "rank", "", rank_id)


func _reg(id: String, name: String, kind: String, stat_key: String, threshold: int) -> void:
	registry[id] = {"name": name, "kind": kind, "stat_key": stat_key, "threshold": threshold}


func increment(stat_key: String, amount: int = 1) -> Array[String]:
	stats[stat_key] = int(stats.get(stat_key, 0)) + amount
	var newly: Array[String] = []
	for aid in registry:
		if aid in unlocked:
			continue
		var entry: Dictionary = registry[aid]
		if entry["kind"] == "stat" and entry["stat_key"] == stat_key:
			if int(stats.get(stat_key, 0)) >= entry["threshold"]:
				_unlock(aid)
				newly.append(aid)
	return newly


func check_game_score(score: int, shield_used: bool) -> Array[String]:
	var newly: Array[String] = []
	for aid in registry:
		if aid in unlocked:
			continue
		var entry: Dictionary = registry[aid]
		if entry["kind"] == "game_score" and score >= entry["threshold"]:
			_unlock(aid)
			newly.append(aid)
		elif entry["kind"] == "no_shield_score" and not shield_used and score >= entry["threshold"]:
			_unlock(aid)
			newly.append(aid)
	return newly


func check_rank(rank: int) -> Array[String]:
	var newly: Array[String] = []
	if rank == -1:
		return newly
	for aid in registry:
		if aid in unlocked:
			continue
		var entry: Dictionary = registry[aid]
		if entry["kind"] == "rank" and rank <= entry["threshold"]:
			_unlock(aid)
			newly.append(aid)
	return newly


func record_play() -> Array[String]:
	var today := Time.get_date_string_from_system()
	var last := str(stats.get("last_played", ""))
	if last == today:
		return []
	# Check streak (simplified - no gap calculation, just consecutive days)
	if last != "":
		stats["daily_streak"] = int(stats.get("daily_streak", 0)) + 1
	else:
		stats["daily_streak"] = 1
	stats["last_played"] = today
	return increment("games_played")


func _unlock(aid: String) -> void:
	if aid not in unlocked:
		unlocked.append(aid)
		achievement_unlocked.emit(aid)


func sync_to_profile() -> void:
	ProfileManager.current_profile["achievements"] = unlocked.duplicate()
	ProfileManager.current_profile["achievement_stats"] = stats.duplicate()


func get_achievement_name(aid: String) -> String:
	if registry.has(aid):
		return registry[aid]["name"]
	return aid
