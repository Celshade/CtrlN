extends Control
## Character selection screen — 5×3 grid + featured card.
## Assets used here:
##   - Grid icons:            assets/player_{char_id}.png  (static, loaded via roster 'asset')
##   - Featured card preview: assets/keybounce_{char_id}/keybounce_{char_id}{i}.png
##                            animated at KEYBOUNCE_FPS when that character is highlighted
##                            (falls back to static grid icon if no keybounce folder exists)

signal character_confirmed(character_id: String, asset_path: String)

const GRID_COLS := 5
const GRID_ROWS := 3
const ICON_SIZE := 50
const ICON_GAP := 8
const GRID_X := 40
const GRID_Y := 60

const CARD_X := 420
const CARD_Y := 40
const CARD_W := 200
const CARD_H := 270

const PLAY_BTN_X := 470
const PLAY_BTN_Y := 330
const PLAY_BTN_W := 100
const PLAY_BTN_H := 40

# Character roster (mirrors Python characters.py)
var roster: Array[Dictionary] = []
var character_order: Array[String] = []
var selected_index := 0

# Cached textures (loaded once in _ready)
var _icon_textures: Array[Texture2D] = []
var _locked_key_tex: Texture2D = null

# Keybounce animation for the featured card (character select only)
# Loaded from: assets/keybounce_{char_id}/key_bounce_{char_id}{i}.png
const KEYBOUNCE_FPS := 20.0
var _keybounce_frames: Array[Texture2D] = []
var _keybounce_frame_idx := 0
var _keybounce_frame_timer := 0.0


func _ready() -> void:
	_build_roster()
	_preload_textures()
	selected_index = 0
	_load_keybounce_frames()
	set_process(true)
	queue_redraw()


func _process(delta: float) -> void:
	# Animate keybounce in the featured card
	if _keybounce_frames.size() < 2:
		return
	_keybounce_frame_timer += delta
	if _keybounce_frame_timer >= 1.0 / KEYBOUNCE_FPS:
		_keybounce_frame_timer = 0.0
		_keybounce_frame_idx = (_keybounce_frame_idx + 1) % _keybounce_frames.size()
		queue_redraw()


func _load_keybounce_frames() -> void:
	_keybounce_frames.clear()
	_keybounce_frame_idx = 0
	_keybounce_frame_timer = 0.0
	var char_id: String = roster[selected_index]["id"]
	var i := 1
	while true:
		var path := "res://assets/characters/%s/keybounce/keybounce%d.png" % [char_id, i]
		if ResourceLoader.exists(path):
			_keybounce_frames.append(load(path) as Texture2D)
			i += 1
		else:
			break


func _preload_textures() -> void:
	_icon_textures.resize(roster.size())
	for i in range(roster.size()):
		_icon_textures[i] = load(roster[i]["asset"]) as Texture2D
	_locked_key_tex = load("res://assets/UI/locked_key.png") as Texture2D


func _build_roster() -> void:
	var unlocked := ProfileManager.get_unlocked_characters()
	var defs := [
		{"id": "black", "name": "Black", "asset": "res://assets/characters/black/player_black.png", "ig_asset": "res://assets/characters/black/player_black.png"},
		{"id": "dark_green", "name": "Dark Green", "asset": "res://assets/characters/dark_green/player_dark_green.png"},
		{"id": "blue", "name": "Blue", "asset": "res://assets/characters/blue/player_blue.png"},
		{"id": "red", "name": "Red", "asset": "res://assets/characters/red/player_red.png"},
		{"id": "yellow", "name": "Yellow", "asset": "res://assets/characters/yellow/player_yellow.png"},
		{"id": "purple", "name": "Purple", "asset": "res://assets/characters/purple/player_purple.png"},
		{"id": "green", "name": "Green", "asset": "res://assets/characters/green/player_green.png"},
		{"id": "orange", "name": "Orange", "asset": "res://assets/characters/orange/player_orange.png"},
		{"id": "grey", "name": "Grey", "asset": "res://assets/characters/grey/player_grey.png"},
		{"id": "white", "name": "White", "asset": "res://assets/characters/white/player_white.png"},
		{"id": "aqua", "name": "Aqua", "asset": "res://assets/characters/aqua/player_aqua.png"},
		{"id": "sunset", "name": "Sunset", "asset": "res://assets/characters/sunset/player_sunset.png"},
		{"id": "silver", "name": "Silver", "asset": "res://assets/characters/silver/player_silver.png"},
		{"id": "gold", "name": "Gold", "asset": "res://assets/characters/gold/player_gold.png"},
	]
	for d in defs:
		d["locked"] = d["id"] not in unlocked
		roster.append(d)
		character_order.append(d["id"])


func _gui_input(event: InputEvent) -> void:
	if event.is_action_pressed("navigate_left"):
		_navigate(-1)
	elif event.is_action_pressed("navigate_right"):
		_navigate(1)
	elif event.is_action_pressed("navigate_up"):
		_navigate_row(-1)
	elif event.is_action_pressed("navigate_down"):
		_navigate_row(1)
	elif event.is_action_pressed("confirm"):
		_confirm()
	elif event is InputEventMouseButton and event.pressed:
		var pos: Vector2 = event.position
		# Check grid click
		var slot := _icon_slot_at(pos)
		if slot >= 0 and not roster[slot]["locked"]:
			selected_index = slot
			_load_keybounce_frames()
			queue_redraw()
		# Check play button click
		elif _is_play_clicked(pos):
			_confirm()
	elif event is InputEventScreenTouch and event.pressed:
		var pos: Vector2 = event.position
		var slot := _icon_slot_at(pos)
		if slot >= 0 and not roster[slot]["locked"]:
			selected_index = slot
			_load_keybounce_frames()
			queue_redraw()
		elif _is_play_clicked(pos):
			_confirm()


func _navigate(direction: int) -> void:
	var attempts := roster.size()
	var idx := selected_index
	while attempts > 0:
		idx = (idx + direction + roster.size()) % roster.size()
		if not roster[idx]["locked"]:
			selected_index = idx
			_load_keybounce_frames()
			queue_redraw()
			return
		attempts -= 1


func _navigate_row(direction: int) -> void:
	var target := selected_index + direction * GRID_COLS
	if target < 0 or target >= roster.size():
		return
	if not roster[target]["locked"]:
		selected_index = target
		_load_keybounce_frames()
		queue_redraw()


func _icon_slot_at(pos: Vector2) -> int:
	for i in range(roster.size()):
		var row := i / GRID_COLS
		var col := i % GRID_COLS
		var x := GRID_X + col * (ICON_SIZE + ICON_GAP)
		var y := GRID_Y + row * (ICON_SIZE + ICON_GAP)
		if Rect2(x, y, ICON_SIZE, ICON_SIZE).has_point(pos):
			return i
	return -1


func _is_play_clicked(pos: Vector2) -> bool:
	return Rect2(PLAY_BTN_X, PLAY_BTN_Y, PLAY_BTN_W, PLAY_BTN_H).has_point(pos)


func _confirm() -> void:
	var entry: Dictionary = roster[selected_index]
	if entry["locked"]:
		return
	character_confirmed.emit(entry["id"], entry.get("ig_asset", entry["asset"]))


func _draw() -> void:
	# Background
	draw_rect(Rect2(0, 0, GameConfig.WINDOW_WIDTH, GameConfig.WINDOW_HEIGHT), Color(0.1, 0.1, 0.15, 0.9))

	var font := ThemeDB.fallback_font

	# Title
	draw_string(font, Vector2(GameConfig.WINDOW_WIDTH / 2.0 - 160, 35), "Select Your Character", HORIZONTAL_ALIGNMENT_CENTER, -1, 36, Color.WHITE)

	# Grid
	for i in range(roster.size()):
		var row := i / GRID_COLS
		var col := i % GRID_COLS
		var x := float(GRID_X + col * (ICON_SIZE + ICON_GAP))
		var y := float(GRID_Y + row * (ICON_SIZE + ICON_GAP))
		var rect := Rect2(x, y, ICON_SIZE, ICON_SIZE)

		# Border
		var border_color := Color.GOLD if i == selected_index else Color(0.4, 0.4, 0.4)
		draw_rect(Rect2(x - 3, y - 3, ICON_SIZE + 6, ICON_SIZE + 6), border_color, false, 3.0)

		# Icon
		var entry: Dictionary = roster[i]
		var tex: Texture2D = _icon_textures[i] if i < _icon_textures.size() else null
		if tex:
			if entry["locked"]:
				# Draw greyed-out version
				draw_texture_rect(tex, rect, false, Color(0.25, 0.25, 0.25, 0.7))
				# Dark tint overlay
				draw_rect(rect, Color(0, 0, 0, 0.55))
				# Lock icon filling the tile
				if _locked_key_tex:
					draw_texture_rect(_locked_key_tex, rect, false)
			else:
				draw_texture_rect(tex, rect, false, Color.WHITE)

	# Featured card
	draw_rect(Rect2(CARD_X, CARD_Y, CARD_W, CARD_H), Color(0.15, 0.15, 0.2, 0.9))
	draw_rect(Rect2(CARD_X, CARD_Y, CARD_W, CARD_H), Color.GOLD, false, 2.0)

	var selected: Dictionary = roster[selected_index]
	# Featured card preview: use keybounce animation if available, else fall back to static icon
	var preview_tex: Texture2D
	if _keybounce_frames.size() > 0:
		preview_tex = _keybounce_frames[_keybounce_frame_idx]
	else:
		preview_tex = _icon_textures[selected_index] if selected_index < _icon_textures.size() else null
	if preview_tex:
		var preview_size := 120.0
		var px := CARD_X + (CARD_W - preview_size) / 2.0
		var py := CARD_Y + 20.0
		draw_texture_rect(preview_tex, Rect2(px, py, preview_size, preview_size), false)

	# Character name
	draw_string(font, Vector2(CARD_X + 20, CARD_Y + 180), selected["name"], HORIZONTAL_ALIGNMENT_LEFT, CARD_W - 40, 30, Color.WHITE)

	# Play button
	var btn_color := Color(0.2, 0.7, 0.3) if not selected["locked"] else Color(0.4, 0.4, 0.4)
	draw_rect(Rect2(PLAY_BTN_X, PLAY_BTN_Y, PLAY_BTN_W, PLAY_BTN_H), btn_color)
	draw_string(font, Vector2(PLAY_BTN_X + 20, PLAY_BTN_Y + 28), "PLAY", HORIZONTAL_ALIGNMENT_CENTER, PLAY_BTN_W - 40, 28, Color.WHITE)
