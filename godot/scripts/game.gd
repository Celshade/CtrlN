extends Node2D
## Main game controller — state machine, input, scoring, collision.

const PlayerScene := preload("res://scenes/player.tscn")
const OrbScene := preload("res://scenes/orb.tscn")
const TreeScene := preload("res://scenes/tree_obstacle.tscn")
const BirdPerchedScene := preload("res://scenes/bird_perched.tscn")
const CharacterSelectScene := preload("res://scenes/character_select.tscn")
const LoginScreenScene := preload("res://scenes/login_screen.tscn")

# Nodes
@onready var background_node := $Background
@onready var obstacles_node := $Obstacles
@onready var player_parent := $Player
@onready var ui_layer := $UI
@onready var notification_label := $UI/NotificationLabel
@onready var notification_timer := $UI/NotificationTimer
@onready var counter_node := $UI/Counter

@onready var tut_progress_label: Label = $UI/TutProgressLabel
@onready var tutorial_image: TextureRect = $UI/TutorialImage
@onready var dark_overlay: ColorRect = $UI/DarkOverlay
@onready var tutorial_label: Label = $UI/TutorialLabel
@onready var tutorial_sub_label: Label = $UI/TutorialSubLabel
@onready var game_over_label: Label = $UI/GameOverLabel
@onready var game_over_restart_label: Label = $UI/GameOverRestartLabel
@onready var menu_label: Label = $UI/MenuLabel

# State
var state: int = GameConfig.GameState.CHARACTER_SELECT
var score: int = 0
var high_score: int = 0
var shield_used_this_game := false

# References
var player = null
var spawner: Node = null
var background: Node = null
var tutorial: Node = null
var counter: Node = null
var char_select: Node = null
var login_screen: Node = null

var selected_character_id := "black"
var selected_asset_path := "res://assets/characters/black/player_black_ig.png"

# Notification queue
var notification_queue: Array[String] = []

# Background layers
var bg_layers: Array[Dictionary] = []


func _ready() -> void:
	notification_timer.timeout.connect(_on_notification_timeout)
	AchievementManager.achievement_unlocked.connect(_on_achievement_unlocked)
	_setup_background()
	_show_login_screen()


func _setup_background() -> void:
	var layer_defs := [
		["sky_and_grass", "res://assets/level_one/sky_and_grass.png", 0.0],
		["big_clouds", "res://assets/level_one/big_clouds.png", 0.025],
		["mountains", "res://assets/level_one/mountains.png", 0.0],
		["little_clouds", "res://assets/level_one/little_clouds.png", 0.05],
		["background", "res://assets/level_one/background.png", 0.04],
		["middleground_back", "res://assets/level_one/middleground_back.png", 0.0625],
		["middleground_middle", "res://assets/level_one/middleground_middle.png", 0.08],
		["middleground_front", "res://assets/level_one/middleground_front.png", 0.2],
		["ground", "res://assets/level_one/ground.png", 1.0],
	]
	for def_arr in layer_defs:
		var tex := load(def_arr[1]) as Texture2D
		if tex == null:
			continue
		var sprite1 := Sprite2D.new()
		sprite1.texture = tex
		sprite1.centered = false
		# Scale to fill viewport
		var sx := float(GameConfig.WINDOW_WIDTH) / tex.get_width()
		var sy := float(GameConfig.WINDOW_HEIGHT) / tex.get_height()
		sprite1.scale = Vector2(sx, sy)
		background_node.add_child(sprite1)

		var sprite2 := Sprite2D.new()
		sprite2.texture = tex
		sprite2.centered = false
		sprite2.scale = Vector2(sx, sy)
		sprite2.position.x = GameConfig.WINDOW_WIDTH
		background_node.add_child(sprite2)

		bg_layers.append({
			"speed": def_arr[2] as float,
			"offset": 0.0,
			"sprite1": sprite1,
			"sprite2": sprite2,
		})


func _update_background() -> void:
	for layer in bg_layers:
		if layer["speed"] == 0.0:
			continue
		layer["offset"] += GameConfig.OBJECT_SPEED * layer["speed"]
		if layer["offset"] < -GameConfig.WINDOW_WIDTH:
			layer["offset"] += GameConfig.WINDOW_WIDTH
		var off := layer["offset"] as float
		(layer["sprite1"] as Sprite2D).position.x = off
		(layer["sprite2"] as Sprite2D).position.x = off + GameConfig.WINDOW_WIDTH


func _reset_background() -> void:
	for layer in bg_layers:
		layer["offset"] = 0.0
		(layer["sprite1"] as Sprite2D).position.x = 0.0
		(layer["sprite2"] as Sprite2D).position.x = GameConfig.WINDOW_WIDTH


# ── Login Screen ─────────────────────────────────────────────────

func _show_login_screen() -> void:
	state = GameConfig.GameState.LOGIN
	if login_screen:
		login_screen.queue_free()
	login_screen = LoginScreenScene.instantiate()
	login_screen.guest_pressed.connect(_on_login_guest)
	login_screen.login_succeeded.connect(_on_login_login)
	login_screen.login_failed.connect(_on_login_error)
	login_screen.store_pressed.connect(_on_login_store)
	login_screen.website_pressed.connect(_on_login_website)
	ui_layer.add_child(login_screen)


func _dismiss_login_screen() -> void:
	if login_screen:
		login_screen.queue_free()
		login_screen = null


func _on_login_guest() -> void:
	_dismiss_login_screen()
	_show_character_select()


func _on_login_login(profile: Dictionary) -> void:
	# TODO: merge Matrica profile data into ProfileManager
	print("Matrica login: ", profile.get("username", "unknown"))
	_dismiss_login_screen()
	_show_character_select()


func _on_login_error(reason: String) -> void:
	push_warning("Matrica login failed: " + reason)


func _on_login_store() -> void:
	OS.shell_open("https://ctrln.art/store")


func _on_login_website() -> void:
	OS.shell_open("https://ctrln.art")


# ── Character Select ──────────────────────────────────────────────

func _show_character_select() -> void:
	state = GameConfig.GameState.CHARACTER_SELECT
	if char_select:
		char_select.queue_free()
	char_select = CharacterSelectScene.instantiate()
	char_select.character_confirmed.connect(_on_character_confirmed)
	ui_layer.add_child(char_select)


func _on_character_confirmed(character_id: String, asset_path: String) -> void:
	selected_character_id = character_id
	selected_asset_path = asset_path
	if char_select:
		char_select.queue_free()
		char_select = null
	restart_game()


# ── Game Flow ─────────────────────────────────────────────────────

func restart_game() -> void:
	state = GameConfig.GameState.PLAYING
	score = 0
	shield_used_this_game = false

	# Clear obstacles
	for child in obstacles_node.get_children():
		child.queue_free()

	# Spawn player
	if player:
		player.queue_free()
	player = PlayerScene.instantiate()
	player_parent.add_child(player)
	player.setup(selected_character_id, selected_asset_path)

	_reset_background()
	_reset_tutorial()
	_reset_spawner()
	_update_ui()


func end_game() -> void:
	state = GameConfig.GameState.GAME_OVER
	if score > high_score:
		high_score = score
	# Award XP
	var result := ProfileManager.add_xp(score)
	# Achievement checks
	_notify_all(AchievementManager.record_play())
	_notify_all(AchievementManager.increment("games_played"))
	_notify_all(AchievementManager.check_game_score(score, shield_used_this_game))
	_notify_all(AchievementManager.check_rank(result["new_rank"]))
	# Save
	AchievementManager.sync_to_profile()
	ProfileManager.increment_games_played(selected_character_id)
	ProfileManager.save_profile()
	_update_ui()


# ── Input ────────────────────────────────────────────────────────

func _unhandled_input(event: InputEvent) -> void:
	if state == GameConfig.GameState.CHARACTER_SELECT:
		return  # Handled by char_select scene

	if event.is_action_pressed("jump"):
		match state:
			GameConfig.GameState.MENU:
				restart_game()
			GameConfig.GameState.PLAYING:
				if not _tutorial_skip_pause():
					if player:
						player.do_jump()
			GameConfig.GameState.GAME_OVER:
				state = GameConfig.GameState.MENU
				_update_ui()

	if event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE:
		get_tree().quit()


# ── Tutorial ──────────────────────────────────────────────────────

var tutorial_active := false
var tutorial_frames_since_start := 0
var tutorial_shield_explanation_active := false
var tutorial_shield_explanation_frames := 0
var tutorial_shield_explanation_shown := false


func _reset_tutorial() -> void:
	tutorial_active = true
	tutorial_frames_since_start = 0
	tutorial_shield_explanation_active = false
	tutorial_shield_explanation_frames = 0
	tutorial_shield_explanation_shown = false


func _tutorial_update() -> bool:
	tutorial_frames_since_start += 1
	if tutorial_frames_since_start <= GameConfig.TUTORIAL_PAUSE_FRAMES:
		return true
	if score >= 5 and not tutorial_shield_explanation_shown:
		tutorial_shield_explanation_active = true
		tutorial_shield_explanation_shown = true
		tutorial_shield_explanation_frames = 0
	if tutorial_shield_explanation_active:
		tutorial_shield_explanation_frames += 1
		if tutorial_shield_explanation_frames > GameConfig.SHIELD_EXPLANATION_PAUSE_FRAMES:
			tutorial_shield_explanation_active = false
		else:
			return true  # pause physics while shield explanation is showing
	if tutorial_active and score >= GameConfig.TUTORIAL_DURATION:
		tutorial_active = false
	return false


func _tutorial_skip_pause() -> bool:
	if tutorial_frames_since_start <= GameConfig.TUTORIAL_PAUSE_FRAMES:
		tutorial_frames_since_start = GameConfig.TUTORIAL_PAUSE_FRAMES + 1
		return true
	elif tutorial_shield_explanation_active:
		tutorial_shield_explanation_active = false
		return true
	return false


# ── Spawner ───────────────────────────────────────────────────────

var orb_timer := 0
var tree_timer := 0


func _reset_spawner() -> void:
	orb_timer = 0
	tree_timer = 0


func _get_spawn_rate(object_type: String) -> int:
	var rate := GameConfig.ORB_SPAWN_RATE if object_type == "orb" else GameConfig.TREE_SPAWN_RATE
	if tutorial_active:
		rate = int(rate * GameConfig.TUTORIAL_SPAWN_MULTIPLIER)
	var multiplier: float
	if score < 150:
		multiplier = 1.0 - score / 250.0
	elif score < 300:
		multiplier = 0.4
	else:
		multiplier = maxf(0.25, 0.4 - (score - 300) / 1000.0)
	return int(rate * multiplier)


func _get_rightmost_orb_x() -> float:
	var rightmost := 0.0
	for child in obstacles_node.get_children():
		if child.is_in_group("orbs"):
			rightmost = maxf(rightmost, child.position.x + GameConfig.ORB_SIZE)
	return rightmost


func _spawn_obstacles() -> void:
	# Spawn orbs
	var orb_rate := _get_spawn_rate("orb")
	orb_timer += 1
	if orb_timer >= orb_rate:
		var rightmost := _get_rightmost_orb_x()
		if GameConfig.WINDOW_WIDTH - rightmost >= GameConfig.MIN_SPAWN_GAP:
			var num_orbs := randi_range(1, 3)
			for i in range(num_orbs):
				var orb := OrbScene.instantiate()
				orb.position.x = GameConfig.WINDOW_WIDTH + i * GameConfig.ORB_SIZE * 0.8
				orb.position.y = randf_range(GameConfig.ORB_MIN_MARGIN, GameConfig.GROUND_Y - GameConfig.ORB_SIZE - GameConfig.ORB_MAX_MARGIN)
				orb.add_to_group("orbs")
				obstacles_node.add_child(orb)
			orb_timer = 0

	# Spawn trees
	var tree_rate := _get_spawn_rate("tree")
	tree_timer += 1
	if tree_timer >= tree_rate:
		var num_trees := randi_range(1, 3)
		for i in range(num_trees):
			var tree_x := GameConfig.WINDOW_WIDTH + i * GameConfig.TREE_SPACING
			var tree := TreeScene.instantiate()
			tree.position.x = tree_x
			tree.position.y = GameConfig.GROUND_Y - GameConfig.TREE_SIZE - 10
			tree.add_to_group("trees")
			obstacles_node.add_child(tree)
			if randf() < GameConfig.PERCHED_BIRD_SPAWN_CHANCE:
				var bird := BirdPerchedScene.instantiate()
				bird.setup(tree)
				bird.add_to_group("birds")
				obstacles_node.add_child(bird)
		tree_timer = 0


# ── Per-Frame Update ──────────────────────────────────────────────

func _physics_process(_delta: float) -> void:
	if state != GameConfig.GameState.PLAYING:
		return
	if _tutorial_update():
		_update_ui()
		return

	# Update background
	_update_background()

	# Spawn new obstacles
	_spawn_obstacles()

	# Move & prune obstacles, check scoring
	var to_remove: Array[Node] = []
	for child in obstacles_node.get_children():
		child.position.x += GameConfig.OBJECT_SPEED

		# Score when obstacle passes player
		if child.position.x < GameConfig.PLAYER_START_X and not child.get_meta("scored", false):
			child.set_meta("scored", true)
			score += 1
			if child.is_in_group("orbs"):
				_notify_all(AchievementManager.increment("yellow_birds_dodged"))
			elif child.is_in_group("birds"):
				if child.get_meta("is_red", false):
					_notify_all(AchievementManager.increment("red_birds_dodged"))
				else:
					_notify_all(AchievementManager.increment("yellow_birds_dodged"))

		# Prune off-screen
		if child.position.x < -GameConfig.PERCHED_BIRD_SIZE:
			to_remove.append(child)

	for node in to_remove:
		node.queue_free()

	# Update player
	if player:
		player.do_update()
		# Shield earnings
		if player.update_shields(score):
			_notify_all(AchievementManager.increment("shields_regenerated"))

		# Collision detection
		if _check_collisions():
			return

		# Death check (out of bounds)
		if player.is_dead():
			if player.position.y + GameConfig.PLAYER_SIZE >= GameConfig.GROUND_Y:
				_notify_all(AchievementManager.increment("ground_crashes"))
			else:
				_notify_all(AchievementManager.increment("ceiling_crashes"))
			if player.has_shield():
				player.destroy_shield()
				shield_used_this_game = true
				_notify_all(AchievementManager.increment("shields_used"))
				player.position.y = clampf(player.position.y, 0, GameConfig.GROUND_Y - GameConfig.PLAYER_SIZE)
				return
			elif player.is_invulnerable():
				player.position.y = clampf(player.position.y, 0, GameConfig.GROUND_Y - GameConfig.PLAYER_SIZE)
				return
			else:
				end_game()

	_update_ui()


func _check_collisions() -> bool:
	if player == null:
		return false

	# Pixel-accurate player hitbox: key cap area within the 75×75 sprite cell.
	var player_rect := Rect2(
		player.position + GameConfig.PLAYER_HITBOX_OFFSET,
		GameConfig.PLAYER_HITBOX_SIZE
	)

	for child in obstacles_node.get_children():
		var obs_rect := _get_obstacle_hitbox(child)

		if not player_rect.intersects(obs_rect):
			continue

		# Collision detected!
		if player.has_shield():
			player.destroy_shield()
			shield_used_this_game = true
			_notify_all(AchievementManager.increment("shields_used"))
			if child.is_in_group("trees"):
				_notify_all(AchievementManager.increment("trees_hit"))
			elif child.is_in_group("birds"):
				var stat := "red_perched_hit" if child.get_meta("is_red", false) else "yellow_perched_hit"
				_notify_all(AchievementManager.increment(stat))
			child.queue_free()
			return true
		elif player.is_invulnerable():
			return true
		else:
			if child.is_in_group("trees"):
				_notify_all(AchievementManager.increment("trees_hit"))
			elif child.is_in_group("birds"):
				var stat := "red_perched_hit" if child.get_meta("is_red", false) else "yellow_perched_hit"
				_notify_all(AchievementManager.increment(stat))
			end_game()
			return true

	return false


## Returns the world-space Rect2 matching the visible/opaque pixels of each obstacle.
## This replaces the old AABB-only _get_obstacle_size() for pixel-accurate collision.
func _get_obstacle_hitbox(node: Node) -> Rect2:
	if node.is_in_group("orbs"):
		return Rect2(node.position + GameConfig.ORB_HITBOX_OFFSET, GameConfig.ORB_HITBOX_SIZE)
	elif node.is_in_group("trees"):
		return Rect2(node.position + GameConfig.TREE_HITBOX_OFFSET, GameConfig.TREE_HITBOX_SIZE)
	elif node.is_in_group("birds"):
		return node.get_hitbox_rect()
	return Rect2(node.position, Vector2(50, 50))


# ── UI ────────────────────────────────────────────────────────────

func _update_ui() -> void:
	_refresh_ui()


func _refresh_ui() -> void:
	# Hide all UI elements first
	counter_node.visible = false
	tut_progress_label.visible = false
	tutorial_image.visible = false
	dark_overlay.visible = false
	tutorial_label.visible = false
	tutorial_sub_label.visible = false
	game_over_label.visible = false
	game_over_restart_label.visible = false
	menu_label.visible = false

	match state:
		GameConfig.GameState.MENU:
			menu_label.text = "CKEY: Ctrl+N\n\nPress SPACE to Start\nHigh Score: %d" % high_score
			menu_label.visible = true

		GameConfig.GameState.PLAYING:
			counter_node.set_score(score)
			counter_node.visible = true
			if tutorial_frames_since_start <= GameConfig.TUTORIAL_PAUSE_FRAMES:
				dark_overlay.color = Color(0, 0, 0, 0.6)
				dark_overlay.visible = true
				tutorial_label.text = "Get Ready!"
				tutorial_label.add_theme_color_override("font_color", Color.YELLOW)
				tutorial_label.visible = true
				tutorial_sub_label.text = "Press SPACE or TAP to Jump"
				tutorial_sub_label.visible = true
			elif tutorial_shield_explanation_active:
				dark_overlay.color = Color(0, 0, 0, 0.6)
				dark_overlay.visible = true
				tutorial_label.text = "Every 5 points, a shield\ncharge will regenerate."
				tutorial_label.add_theme_color_override("font_color", Color.WHITE)
				tutorial_label.visible = true
			else:
				if tutorial_active:
					tutorial_image.visible = true
					tut_progress_label.text = "Progress: %d/%d" % [score, GameConfig.TUTORIAL_DURATION]
					tut_progress_label.visible = true

		GameConfig.GameState.GAME_OVER:
			dark_overlay.color = Color(0, 0, 0, 0.8)
			dark_overlay.visible = true
			game_over_label.text = "Game Over\n\nScore: %d\nHigh Score: %d" % [score, high_score]
			game_over_label.visible = true
			game_over_restart_label.visible = true


# ── Notifications ─────────────────────────────────────────────────

func _notify_all(newly: Array) -> void:
	for aid in newly:
		notification_queue.append(aid)
	_show_next_notification()


func _on_achievement_unlocked(_aid: String) -> void:
	pass  # Handled via _notify_all already


func _show_next_notification() -> void:
	if notification_queue.is_empty() or notification_label.visible:
		return
	var aid: String = notification_queue.pop_front()
	notification_label.text = "Achievement: %s" % AchievementManager.get_achievement_name(aid)
	notification_label.visible = true
	notification_timer.start()


func _on_notification_timeout() -> void:
	notification_label.visible = false
	_show_next_notification()
