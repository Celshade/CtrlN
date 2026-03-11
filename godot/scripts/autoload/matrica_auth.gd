extends Node
## Matrica OAuth2 relay login flow.
##
## Flow:
##   1. call start_login()
##   2. GET celkeys.io/api/auth/start?state=<token>  → authUrl
##   3. OS.shell_open(authUrl) — user logs in via browser
##   4. celkeys.io/api/auth/callback stores the profile in KV
##   5. Poll celkeys.io/api/auth/poll?state=<token> every 1.5 s
##   6. emits login_succeeded(profile) or login_failed(reason)
##
## The game never handles secrets or tokens — only the profile dict.

signal login_succeeded(profile: Dictionary)
signal login_failed(reason: String)
signal browser_open_failed(url: String)

const RELAY_BASE_URL  := "https://www.celkeys.io"
const POLL_INTERVAL   := 1.5   # seconds between poll attempts
const POLL_TIMEOUT    := 300.0 # 5 minutes before giving up

# Dev bypass: set to a JSON string of a profile dict to skip the browser flow.
# Example: '{"username":"devuser","avatar_url":""}'
const DEV_PROFILE_JSON := ""

var _http_request: HTTPRequest = null
var _state_token      := ""
var _http_stage       := ""   # "start" | "poll"
var _poll_timer       := 0.0
var _poll_elapsed     := 0.0
var _request_in_flight := false
var _active           := false


func _ready() -> void:
	_http_request = HTTPRequest.new()
	add_child(_http_request)
	_http_request.request_completed.connect(_on_http_completed)


# ── Public ────────────────────────────────────────────────────────

func start_login() -> void:
	if DEV_PROFILE_JSON != "":
		var json := JSON.new()
		if json.parse(DEV_PROFILE_JSON) == OK:
			login_succeeded.emit(json.data)
		else:
			login_succeeded.emit({"username": "devuser"})
		return

	_state_token       = _random_string(32)
	_http_stage        = "start"
	_poll_timer        = 0.0
	_poll_elapsed      = 0.0
	_request_in_flight = true
	_active            = true
	set_process(true)

	var url := RELAY_BASE_URL + "/api/auth/start?state=" + _state_token.uri_encode()
	_http_request.request(url)


# ── Poll loop ─────────────────────────────────────────────────────

func _process(delta: float) -> void:
	if not _active or _http_stage != "poll":
		return

	_poll_elapsed += delta

	if _poll_elapsed >= POLL_TIMEOUT:
		_fail("Login timed out — please try again")
		return

	if _request_in_flight:
		return

	_poll_timer -= delta
	if _poll_timer > 0.0:
		return

	_poll_timer        = POLL_INTERVAL
	_request_in_flight = true
	var url := RELAY_BASE_URL + "/api/auth/poll?state=" + _state_token.uri_encode()
	_http_request.request(url)


# ── HTTP callback ─────────────────────────────────────────────────

func _notification(what: int) -> void:
	# When the app comes back from background (e.g. returning from browser after OAuth),
	# any in-flight poll may have been silently dropped by the OS. Clear the flag so
	# _process can send a fresh poll immediately.
	if what == NOTIFICATION_APPLICATION_FOCUS_IN and _active and _http_stage == "poll":
		_request_in_flight = false
		_poll_timer = 0.0


func _on_http_completed(result: int, response_code: int, _headers: PackedStringArray, body: PackedByteArray) -> void:
	_request_in_flight = false

	if result != HTTPRequest.RESULT_SUCCESS:
		# During the poll stage a transient connection error (e.g. the OS dropped the
		# socket while the app was backgrounded) is not fatal — just retry.
		if _http_stage == "poll":
			_poll_timer = POLL_INTERVAL
			return
		_fail("Network error (code %d)" % result)
		return
	if response_code < 200 or response_code >= 300:
		_fail("Server error %d" % response_code)
		return

	var json := JSON.new()
	if json.parse(body.get_string_from_utf8()) != OK:
		_fail("Invalid JSON from relay server")
		return
	var data: Dictionary = json.data

	if _http_stage == "start":
		var auth_url: String = data.get("authUrl", "")
		if auth_url == "":
			_fail(data.get("error", "No authUrl returned by relay"))
			return
		if OS.shell_open(auth_url) != OK:
			browser_open_failed.emit(auth_url)
		_http_stage = "poll"
		_poll_timer = 0.0   # poll immediately on first tick

	elif _http_stage == "poll":
		var status: String = data.get("status", "")
		if status == "done":
			_active = false
			set_process(false)
			login_succeeded.emit(data.get("profile", {}))
		elif status != "pending":
			_fail("Unexpected poll response: %s" % status)
		# "pending" → do nothing, _process will retry after POLL_INTERVAL


# ── Helpers ───────────────────────────────────────────────────────

func _fail(reason: String) -> void:
	_active = false
	set_process(false)
	login_failed.emit(reason)


func _random_string(length: int) -> String:
	const CHARS := "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
	var rng := RandomNumberGenerator.new()
	rng.randomize()
	var out := ""
	for i in range(length):
		out += CHARS[rng.randi() % CHARS.length()]
	return out
