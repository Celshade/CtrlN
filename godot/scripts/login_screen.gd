extends Control
## Login / landing screen shown before character select.
##
## Emits signals for guest and (on success) login_succeeded with profile dict.

signal login_succeeded(profile: Dictionary)
signal login_failed(reason: String)
signal guest_pressed
signal store_pressed
signal website_pressed

const WINDOW_WIDTH  := 890
const WINDOW_HEIGHT := 400

# Button geometry
const BTN_W      := 200.0
const BTN_H      := 52.0
const BTN_GAP    := 16.0
const BTN_START_Y := 190.0

var _buttons: Array[Dictionary] = []
var _hovered := -1
var _waiting_for_login := false


func _ready() -> void:
	var labels := ["Login", "Play as Guest", "Store", "Website"]
	var total_w := labels.size() * BTN_W + (labels.size() - 1) * BTN_GAP
	var start_x := (WINDOW_WIDTH - total_w) / 2.0
	for i in range(labels.size()):
		_buttons.append({
			"label": labels[i],
			"rect": Rect2(start_x + i * (BTN_W + BTN_GAP), BTN_START_Y, BTN_W, BTN_H),
		})
	MatricaAuth.login_succeeded.connect(_on_matrica_success)
	MatricaAuth.login_failed.connect(_on_matrica_failed)
	MatricaAuth.browser_open_failed.connect(_on_browser_open_failed)
	set_process_input(true)


func _input(event: InputEvent) -> void:
	if _waiting_for_login:
		return
	if event is InputEventMouseMotion:
		var pos: Vector2 = event.position
		_hovered = -1
		for i in range(_buttons.size()):
			if i >= 2:
				continue
			if _buttons[i]["rect"].has_point(pos):
				_hovered = i
				break
		queue_redraw()

	elif event is InputEventMouseButton:
		if event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
			for i in range(_buttons.size()):
				if _buttons[i]["rect"].has_point(event.position):
					_on_button_pressed(i)
					return


func _on_button_pressed(idx: int) -> void:
	match idx:
		0:
			_waiting_for_login = true
			queue_redraw()
			MatricaAuth.start_login()
		1: guest_pressed.emit()
		# 2: store — disabled
		# 3: website — disabled


func _on_matrica_success(profile: Dictionary) -> void:
	_waiting_for_login = false
	login_succeeded.emit(profile)


func _on_matrica_failed(reason: String) -> void:
	_waiting_for_login = false
	_status_message = "Login failed: " + reason
	_manual_url = ""
	queue_redraw()


func _on_browser_open_failed(url: String) -> void:
	_manual_url = url
	_status_message = ""
	DisplayServer.clipboard_set(url)
	queue_redraw()


var _status_message := ""
var _manual_url := ""


func _draw() -> void:
	var font := ThemeDB.fallback_font

	# Title
	var title := "CKEY: Ctrl+N"
	draw_string(font, Vector2(WINDOW_WIDTH / 2.0 - 140, 100), title,
		HORIZONTAL_ALIGNMENT_CENTER, -1, 72, Color.WHITE)

	# Subtitle / status
	var subtitle := _status_message if _status_message != "" \
		else ("Waiting for browser login…" if _waiting_for_login \
		else "Sign in to save your progress")
	var subtitle_color := Color(1, 0.4, 0.4) if _status_message != "" \
		else Color(1, 1, 0.6) if _waiting_for_login \
		else Color(0.85, 0.85, 0.85)
	draw_string(font, Vector2(WINDOW_WIDTH / 2.0 - 140, 150), subtitle,
		HORIZONTAL_ALIGNMENT_CENTER, -1, 26, subtitle_color)

	# Manual URL fallback (browser open failed)
	if _manual_url != "":
		draw_string(font, Vector2(20, 200), "Browser didn't open. URL copied to clipboard — paste in browser:",
			HORIZONTAL_ALIGNMENT_LEFT, -1, 18, Color(1, 0.9, 0.5))
		draw_string(font, Vector2(20, 225), _manual_url,
			HORIZONTAL_ALIGNMENT_LEFT, WINDOW_WIDTH - 40, 14, Color(0.7, 0.9, 1.0))
		return

	# Buttons (hidden while waiting)
	if _waiting_for_login:
		return
	for i in range(_buttons.size()):
		var btn: Dictionary = _buttons[i]
		var rect: Rect2 = btn["rect"]
		var is_hovered := i == _hovered

		var is_disabled := i >= 2
		var bg_color := Color(0.25, 0.55, 0.9) if i == 0 \
			else Color(0.2, 0.75, 0.35) if i == 1 \
			else Color(0.35, 0.35, 0.45)
		if is_disabled:
			bg_color = Color(0.25, 0.25, 0.28)
		elif is_hovered:
			bg_color = bg_color.lightened(0.18)

		draw_rect(rect, bg_color)
		draw_rect(rect, Color.WHITE if (is_hovered and not is_disabled) else Color(1, 1, 1, 0.3), false, 1.5)

		var text: String = btn["label"]
		var label_color := Color(0.5, 0.5, 0.5) if is_disabled else Color.WHITE
		var tw := font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, 24).x
		var tx := rect.position.x + (rect.size.x - tw) / 2.0
		var ty := rect.position.y + rect.size.y * 0.67
		draw_string(font, Vector2(tx, ty), text,
			HORIZONTAL_ALIGNMENT_LEFT, -1, 24, label_color)
