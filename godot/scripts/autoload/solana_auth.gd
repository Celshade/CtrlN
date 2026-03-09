## SolanaAuth — Solana wallet authentication manager (autoload singleton)
##
## Integrates godot-solana-sdk WalletAdapter for Solana Mobile Wallet Adapter (MWA)
## authentication on Android. Gracefully handles case where SDK not installed.

extends Node

signal wallet_authenticated(profile: Dictionary)
signal wallet_error(reason: String)

var wallet_adapter: Node = null
var is_polling = false
var _game_state = ""
var _sdk_available = false

func _ready() -> void:
	# Defer initialization to avoid early parse errors
	call_deferred("_initialize_wallet_adapter")

func _initialize_wallet_adapter() -> void:
	if not ClassDB.class_exists("WalletAdapter"):
		print("⚠ SolanaAuth: godot-solana-sdk not installed")
		return
	
	_sdk_available = true
	wallet_adapter = WalletAdapter.new()
	print("✓ SolanaAuth: WalletAdapter loaded")

func start_wallet_login() -> void:
	if not _sdk_available or not wallet_adapter:
		wallet_error.emit("Solana SDK not installed - see SOLANA_SETUP.md for installation")
		return
	
	# Request wallet connection
	wallet_adapter.connect_wallet()
	await get_tree().create_timer(0.5).timeout
	_request_wallet_signature()

func _request_wallet_signature() -> void:
	# Generate nonce and message
	var nonce = _generate_nonce()
	var timestamp = int(Time.get_ticks_msec() / 1000)
	var message = "CtrlN Login\nNonce: %s\nTimestamp: %d" % [nonce, timestamp]
	var message_bytes = message.to_utf8_buffer()
	
	# Request signature from wallet
	var signature = await wallet_adapter.sign_message(message_bytes)
	if signature == null or signature is String:
		wallet_error.emit("Wallet signing failed: " + str(signature))
		return
	
	# Get user's public key
	var user_pubkey = wallet_adapter.get_public_key()
	if not user_pubkey:
		wallet_error.emit("Could not retrieve wallet address")
		return
	
	# Send to backend for verification
	_verify_wallet_signature(user_pubkey, signature, nonce, timestamp)

func _verify_wallet_signature(pubkey: String, signature: PackedByteArray, nonce: String, timestamp: int) -> void:
	var http = HTTPRequest.new()
	add_child(http)
	http.request_completed.connect(func(_result, _code, _headers, body):
		_on_wallet_verify_response(http, body))
	
	var body = JSON.stringify({
		"pubkey": pubkey,
		"nonce": nonce + ":" + str(timestamp),
		"signature": Marshalls.raw_to_base64(signature),
		"auth_token": ""
	})
	
	var headers = ["Content-Type: application/json"]
	http.request(
		"https://celkeys.io/api/auth/wallet/verify",
		headers,
		HTTPClient.METHOD_POST,
		body
	)

func _on_wallet_verify_response(http: HTTPRequest, body: PackedByteArray) -> void:
	var response = JSON.parse_string(body.get_string_from_utf8())
	http.queue_free()
	
	if response and response.has("gameState"):
		_game_state = response["gameState"]
		_start_profile_polling()
	else:
		var error = response.get("error", "Wallet verification failed") if response else "Empty response"
		wallet_error.emit(error)

func _start_profile_polling() -> void:
	if is_polling:
		return
	
	is_polling = true
	var max_polls = 200  # ~5 minutes with 1.5s interval
	var poll_count = 0
	
	while poll_count < max_polls:
		await get_tree().create_timer(1.5).timeout
		
		var http = HTTPRequest.new()
		add_child(http)
		
		var poll_url = "https://celkeys.io/api/auth/poll?state=" + _game_state
		http.request(poll_url)
		
		var response = await http.request_completed
		http.queue_free()
		
		if response[0] == OK:
			var data_str = response[3].get_string_from_utf8()
			
			# Check if response is still "pending"
			if data_str != "pending":
				var profile = JSON.parse_string(data_str)
				if profile and profile.has("id"):
					is_polling = false
					wallet_authenticated.emit(profile)
					return
		
		poll_count += 1
	
	is_polling = false
	wallet_error.emit("Wallet login timeout - please try again")

func _generate_nonce() -> String:
	# Generate base64-encoded random nonce
	var nonce_bytes = []
	for i in range(32):
		nonce_bytes.append(randi() % 256)
	return Marshalls.raw_to_base64(PackedByteArray(nonce_bytes))


