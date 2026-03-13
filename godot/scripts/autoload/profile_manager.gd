extends Node
## Manages player profile persistence (JSON save/load).

const SAVE_DIR := "user://player_data/"
const DEFAULT_ID := "player1"

var current_profile: Dictionary = {}


func _ready() -> void:
	var dir := DirAccess.open("user://")
	if dir and not dir.dir_exists("player_data"):
		dir.make_dir("player_data")
	load_profile(DEFAULT_ID)


func load_profile(player_id: String) -> Dictionary:
	var path := SAVE_DIR + player_id + ".json"
	if FileAccess.file_exists(path):
		var f := FileAccess.open(path, FileAccess.READ)
		var json := JSON.new()
		if json.parse(f.get_as_text()) == OK:  # TODO test mobile persistance
			current_profile = json.data
			return current_profile
	# Default new profile
	current_profile = _default_profile(player_id)
	return current_profile


func save_profile() -> void:
	var path: String = SAVE_DIR + str(current_profile.get("id", DEFAULT_ID)) + ".json"
	var f := FileAccess.open(path, FileAccess.WRITE)
	f.store_string(JSON.stringify(current_profile, "\t"))


func _default_profile(player_id: String) -> Dictionary:
	return {
		"id": player_id,
		"name": "Unknown",
		"season_xp": 0,
		"total_xp": 0,
		"rank": -1,
		"highest_rank": 8,
		"prestige": 0,
		"seasons_played": 0,
		"games_played": 0,
		"games_per_character": {},
		"achievements": [],
		"achievement_stats": {},
	}


func get_rank() -> int:
	return int(current_profile.get("rank", -1))


func get_total_xp() -> int:
	return int(current_profile.get("total_xp", 0))


func add_xp(amount: int) -> Dictionary:
	var old_rank := get_rank()
	current_profile["total_xp"] = get_total_xp() + amount
	current_profile["season_xp"] = int(current_profile.get("season_xp", 0)) + amount
	var new_rank := _calculate_rank(get_total_xp())
	current_profile["rank"] = new_rank
	if new_rank != -1 and new_rank < int(current_profile.get("highest_rank", 8)):
		current_profile["highest_rank"] = new_rank
	return {"old_rank": old_rank, "new_rank": new_rank, "rank_up": new_rank < old_rank}


func _calculate_rank(total_xp: int) -> int:
	# Ranks: 0=Prestige(15000), 1=Diamond(10000), 2=Platinum(7500),
	# 3=Gold(5000), 4=Silver(3000), 5=Bronze(1500), 6=Iron(500), 7=Bamboo(100)
	var thresholds := [15000, 10000, 7500, 5000, 3000, 1500, 500, 100]
	for i in range(thresholds.size()):
		if total_xp >= thresholds[i]:
			return i
	return -1


func increment_games_played(character_id: String) -> void:
	current_profile["games_played"] = int(current_profile.get("games_played", 0)) + 1
	if not current_profile.has("games_per_character"):
		current_profile["games_per_character"] = {}
	var gpc: Dictionary = current_profile["games_per_character"]
	gpc[character_id] = int(gpc.get(character_id, 0)) + 1


func get_unlocked_characters() -> Array[String]:
	var rank := get_rank()
	var unlocked: Array[String] = ["black", "dark_green", "blue", "red"]
	# TODO: Re-enable locked characters when system is implemented
	# if rank <= 7 and rank >= 0:
	# 	unlocked.append_array(["yellow", "purple"])
	# if rank <= 6 and rank >= 0:
	# 	unlocked.append_array(["green", "orange"])
	# if rank <= 4 and rank >= 0:
	# 	unlocked.append("grey")
	# if rank <= 3 and rank >= 0:
	# 	unlocked.append("white")
	return unlocked
