## SolanaAuth — Solana wallet authentication manager (autoload singleton)
##
## TODO: Re-enable when SolanaSDK integration is ready
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
		wallet_error.emit("Solana SDK not installed - see docs/SOLANA_WALLET_LOGIN.md for installation")
		return
	
	print("➤ SolanaAuth: Starting wallet login...")
	# Request wallet connection
	wallet_adapter.connect_wallet()
	await get_tree().create_timer(0.5).timeout
	print("➤ SolanaAuth: Requesting wallet signature...")
	_request_wallet_signature()

func _request_wallet_signature() -> void:
	print("➤ SolanaAuth: Getting wallet address...")
	# Get user's public key first
	var user_wallet = wallet_adapter.get_public_key()
	if not user_wallet:
		wallet_error.emit("Could not retrieve wallet address")
		return
	
	print("✓ SolanaAuth: Got wallet: ", user_wallet)
	
	# Generate challenge and message (v2 format with wallet address)
	var challenge = _generate_nonce()
	var timestamp = int(Time.get_ticks_msec() / 1000)
	var message = "AUTH:v2:%s:%s:%d" % [user_wallet, challenge, int(timestamp / 10)]
	var message_bytes = message.to_utf8_buffer()
	
	print("➤ SolanaAuth: Waiting for wallet signature...")
	# Request signature from wallet
	var signature = await wallet_adapter.sign_message(message_bytes)
	print("✓ SolanaAuth: Signature response received: ", type_string(typeof(signature)))
	
	if signature == null:
		wallet_error.emit("Wallet signing was cancelled")
		return
	
	if signature is String:
		wallet_error.emit("Wallet signing failed: " + str(signature))
		return
	
	# Send to backend for verification
	_verify_wallet_signature(user_wallet, signature, challenge, timestamp)

func _verify_wallet_signature(wallet: String, signature: PackedByteArray, challenge: String, timestamp: int) -> void:
	var http = HTTPRequest.new()
	add_child(http)
	http.request_completed.connect(func(_result, _code, _headers, body):
		_on_wallet_verify_response(http, _code, body))
	
	var body = JSON.stringify({
		"wallet": wallet,
		"challenge": challenge + ":" + str(timestamp),
		"signature": Marshalls.raw_to_base64(signature)
	})
	
	print("➤ SolanaAuth: Sending signature to backend...")
	var headers = ["Content-Type: application/json"]
	http.request(
		AuthConfig.get_wallet_authenticate_url(),
		headers,
		HTTPClient.METHOD_POST,
		body
	)

func _on_wallet_verify_response(http: HTTPRequest, code: int, body: PackedByteArray) -> void:
	print("✓ SolanaAuth: Backend response code: ", code)
	var response = JSON.parse_string(body.get_string_from_utf8())
	http.queue_free()
	
	if response == null:
		wallet_error.emit("Backend returned invalid JSON: " + body.get_string_from_utf8())
		return
	
	print("✓ SolanaAuth: Backend response: ", response)
	
	if code != 200:
		var error = response.get("error", "HTTP %d" % code) if response is Dictionary else "HTTP %d" % code
		wallet_error.emit(error)
		return
	
	if response.has("authToken"):
		_game_state = response["authToken"]
		print("✓ SolanaAuth: Got authToken: ", _game_state)
		_start_profile_polling()
	else:
		var error = response.get("error", "No authToken in response") if response is Dictionary else "No authToken in response"
		wallet_error.emit(error)

func _start_profile_polling() -> void:
	if is_polling:
		return
	
	print("➤ SolanaAuth: Starting profile polling...")
	is_polling = true
	var max_polls = 200  # ~5 minutes with 1.5s interval
	var poll_count = 0
	
	while poll_count < max_polls:
		await get_tree().create_timer(1.5).timeout
		
		var http = HTTPRequest.new()
		add_child(http)
		
		var poll_url = AuthConfig.get_matrica_poll_url(_game_state)
		http.request(poll_url)
		
		var response = await http.request_completed
		http.queue_free()
		
		if response[0] == OK:
			var data_str = response[3].get_string_from_utf8()
			print("  Poll #%d: %s" % [poll_count + 1, data_str])
			
			# Check if response is still "pending"
			if data_str != "pending":
				var profile = JSON.parse_string(data_str)
				if profile and profile.has("id"):
					is_polling = false
					print("✓ SolanaAuth: Profile authenticated!")
					wallet_authenticated.emit(profile)
					return
		
		poll_count += 1
	
	is_polling = false
	print("✗ SolanaAuth: Polling timeout")
	wallet_error.emit("Wallet login timeout - please try again")

func _generate_nonce() -> String:
	# Generate base64-encoded random nonce
	var nonce_bytes = []
	for i in range(32):
		nonce_bytes.append(randi() % 256)
	return Marshalls.raw_to_base64(PackedByteArray(nonce_bytes))


