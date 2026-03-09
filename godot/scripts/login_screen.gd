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
const COL1_X     := 80.0   # Left column
const COL2_X     := 295.0  # Right column (just a few pixels to the right)
const BTN_START_Y := 165.0

var _buttons: Array[Dictionary] = []
var _hovered := -1
var _waiting_for_login := false


func _ready() -> void:
	# Set Control size to fill viewport
	custom_minimum_size = Vector2(WINDOW_WIDTH, WINDOW_HEIGHT)
	size = Vector2(WINDOW_WIDTH, WINDOW_HEIGHT)
	
	var labels := ["Login with Matrica", "Login with Solana", "Play as Guest", "Website", "Store"]
	for i in range(labels.size()):
		# First 3 buttons in left column (vertical), last 2 in right column
		var col := COL1_X if i < 3 else COL2_X
		var row := i if i < 3 else (i - 3)
		_buttons.append({
			"label": labels[i],
			"rect": Rect2(col, BTN_START_Y + row * (BTN_H + BTN_GAP), BTN_W, BTN_H),
		})
	
	# Matrica OAuth callbacks
	MatricaAuth.login_succeeded.connect(_on_matrica_success)
	MatricaAuth.login_failed.connect(_on_matrica_failed)
	MatricaAuth.browser_open_failed.connect(_on_browser_open_failed)
	
	# Solana wallet callbacks (if SDK available)
	if ClassDB.class_exists("WalletAdapter"):
		SolanaAuth.wallet_authenticated.connect(_on_wallet_success)
		SolanaAuth.wallet_error.connect(_on_wallet_error)
	
	set_process_input(true)
	queue_redraw()  # Ensure login screen renders immediately


func _input(event: InputEvent) -> void:
	if _waiting_for_login:
		return
	if event is InputEventMouseMotion:
		var pos: Vector2 = event.position
		_hovered = -1
		for i in range(_buttons.size()):
			if i >= 3:  # Only first 3 buttons are interactive (4 and 5 are disabled)
				continue
			if _buttons[i]["rect"].has_point(pos):
				_hovered = i
				break
		queue_redraw()

	elif event is InputEventMouseButton:
		if event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
			for i in range(_buttons.size()):
				if i >= 3:  # Skip disabled buttons
					continue
				if _buttons[i]["rect"].has_point(event.position):
					_on_button_pressed(i)
					return


func _on_button_pressed(idx: int) -> void:
	match idx:
		0:  # Matrica Login
			_waiting_for_login = true
			queue_redraw()
			MatricaAuth.start_login()
		1:  # Solana Wallet Login
			_waiting_for_login = true
			queue_redraw()
			if ClassDB.class_exists("WalletAdapter"):
				SolanaAuth.start_wallet_login()
			else:
				_on_wallet_error("Solana SDK not installed")
		2:  # Play as Guest
			guest_pressed.emit()
		3:  # Website (disabled)
			website_pressed.emit()
		4:  # Store (disabled)
			store_pressed.emit()


func _on_matrica_success(profile: Dictionary) -> void:
	_waiting_for_login = false
	login_succeeded.emit(profile)


func _on_matrica_failed(reason: String) -> void:
	_waiting_for_login = false
	login_failed.emit(reason)


func _on_wallet_success(profile: Dictionary) -> void:
	_waiting_for_login = false
	login_succeeded.emit(profile)


func _on_wallet_error(reason: String) -> void:
	_waiting_for_login = false
	login_failed.emit(reason)
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
	var title_width := font.get_string_size(title, HORIZONTAL_ALIGNMENT_LEFT, -1, 56).x
	var title_x := (WINDOW_WIDTH - title_width) / 2.0
	draw_string(font, Vector2(title_x, 60), title,
		HORIZONTAL_ALIGNMENT_LEFT, -1, 56, Color.WHITE)

	# Subtitle / status
	var subtitle := _status_message if _status_message != "" \
		else ("Waiting for browser login…" if _waiting_for_login \
		else "Sign in to save your progress")
	var subtitle_color := Color(1, 0.4, 0.4) if _status_message != "" \
		else Color(1, 1, 0.6) if _waiting_for_login \
		else Color(0.85, 0.85, 0.85)
	var subtitle_width := font.get_string_size(subtitle, HORIZONTAL_ALIGNMENT_LEFT, -1, 20).x
	var subtitle_x := (WINDOW_WIDTH - subtitle_width) / 2.0
	draw_string(font, Vector2(subtitle_x, 120), subtitle,
		HORIZONTAL_ALIGNMENT_LEFT, -1, 20, subtitle_color)

	# Manual URL fallback (browser open failed)
	if _manual_url != "":
		draw_string(font, Vector2(20, 300), "Browser didn't open. URL copied to clipboard — paste in browser:",
			HORIZONTAL_ALIGNMENT_LEFT, -1, 14, Color(1, 0.9, 0.5))
		draw_string(font, Vector2(20, 325), _manual_url,
			HORIZONTAL_ALIGNMENT_LEFT, WINDOW_WIDTH - 40, 12, Color(0.7, 0.9, 1.0))
		return

	# Buttons (hidden while waiting)
	if _waiting_for_login:
		return
	for i in range(_buttons.size()):
		var btn: Dictionary = _buttons[i]
		var rect: Rect2 = btn["rect"]
		var is_hovered := i == _hovered

		var is_disabled := i >= 3  # Only buttons 0, 1, 2 are interactive
		var bg_color := Color(0.25, 0.55, 0.9) if i == 0 \
			else Color(0.2, 0.75, 0.35) if i == 1 \
			else Color(0.85, 0.55, 0.1) if i == 2 \
			else Color(0.25, 0.25, 0.28)  # Disabled buttons (3+) are grey
		if not is_disabled and is_hovered:
			bg_color = bg_color.lightened(0.18)

		draw_rect(rect, bg_color)
		draw_rect(rect, Color.WHITE if (is_hovered and not is_disabled) else Color(1, 1, 1, 0.3), false, 1.5)

		var text: String = btn["label"]
		var label_color := Color(0.5, 0.5, 0.5) if is_disabled else Color.WHITE
		var tw := font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, 20).x
		var tx := rect.position.x + (rect.size.x - tw) / 2.0
		var ty := rect.position.y + rect.size.y * 0.65
		draw_string(font, Vector2(tx, ty), text,
			HORIZONTAL_ALIGNMENT_LEFT, -1, 20, label_color)
