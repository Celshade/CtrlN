## AuthConfig — Centralized authentication relay configuration (autoload singleton)
##
## Abstracts backend authentication service URLs to prevent hardcoding.
## Single source of truth for all auth endpoints.
##
## Configuration priority:
## 1. Environment variables (CTRLN_AUTH_RELAY_URL, etc.)
## 2. Default values below
##
## Use OS.get_environment() for local testing:
##   export CTRLN_AUTH_RELAY_URL="http://localhost:3000"

extends Node

# Environment variable names
const ENV_AUTH_RELAY_URL := "CTRLN_AUTH_RELAY_URL"
const ENV_MATRICA_ENDPOINT := "CTRLN_MATRICA_ENDPOINT"
const ENV_WALLET_ENDPOINT := "CTRLN_WALLET_ENDPOINT"

# Default endpoints (placeholder domain prevents accidental hardcoding)
const DEFAULT_AUTH_RELAY_BASE_URL := "https://api.auth-relay.local"
const DEFAULT_MATRICA_ENDPOINT := "/api/auth/start"
const DEFAULT_MATRICA_POLL_ENDPOINT := "/api/auth/poll"
const DEFAULT_WALLET_ENDPOINT := "/api/auth/wallet/verify"

# Cached configuration values
var _auth_relay_url: String
var _matrica_endpoint: String
var _matrica_poll_endpoint: String
var _wallet_endpoint: String

func _ready() -> void:
	_load_configuration()

func _load_configuration() -> void:
	# Load from environment or use defaults
	_auth_relay_url = OS.get_environment(ENV_AUTH_RELAY_URL) if OS.get_environment(ENV_AUTH_RELAY_URL) else DEFAULT_AUTH_RELAY_BASE_URL
	
	# If using placeholder, try to load from packaged config file (set at APK build time)
	if _auth_relay_url.contains("auth-relay.local"):
		# Try to load from res://auth_config.txt (project root)
		var config_path = "res://auth_config.txt"
		if FileAccess.file_exists(config_path):
			var config = FileAccess.get_file_as_string(config_path)
			if config:
				_auth_relay_url = config.strip_edges()
				print("✓ AuthConfig: Loaded from %s" % config_path)
	
	_matrica_endpoint = OS.get_environment(ENV_MATRICA_ENDPOINT) if OS.get_environment(ENV_MATRICA_ENDPOINT) else DEFAULT_MATRICA_ENDPOINT
	_matrica_poll_endpoint = DEFAULT_MATRICA_POLL_ENDPOINT
	_wallet_endpoint = OS.get_environment(ENV_WALLET_ENDPOINT) if OS.get_environment(ENV_WALLET_ENDPOINT) else DEFAULT_WALLET_ENDPOINT
	
	# Warn if using development/placeholder endpoints
	if _auth_relay_url.contains("auth-relay.local"):
		print("⚠ AuthConfig: Using placeholder auth relay URL. Set CTRLN_AUTH_RELAY_URL environment variable for production.")
	
	print("✓ AuthConfig: Loaded configuration")
	print("  - Auth Relay: %s" % _auth_relay_url)
	print("  - Matrica: %s%s" % [_auth_relay_url, _matrica_endpoint])
	print("  - Wallet: %s%s" % [_auth_relay_url, _wallet_endpoint])

func get_matrica_start_url(state: String) -> String:
	return "%s%s?state=%s" % [_auth_relay_url, _matrica_endpoint, state]

func get_matrica_poll_url(state: String) -> String:
	return "%s%s?state=%s" % [_auth_relay_url, _matrica_poll_endpoint, state]

func get_wallet_authenticate_url() -> String:
	return "%s%s" % [_auth_relay_url, _wallet_endpoint]
