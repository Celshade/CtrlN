## AuthConfig — Centralized authentication relay configuration (autoload singleton)
##
## Abstracts backend authentication service URLs to prevent hardcoding.
## Single source of truth for all auth endpoints.

extends Node

# Authentication relay service configuration
const AUTH_RELAY_BASE_URL := "https://api.auth-relay.local"
const MATRICA_ENDPOINT := "/auth/start"
const MATRICA_POLL_ENDPOINT := "/auth/poll"
const WALLET_ENDPOINT := "/wallet-authenticate"

func get_matrica_start_url(state: String) -> String:
	return "%s%s?state=%s" % [AUTH_RELAY_BASE_URL, MATRICA_ENDPOINT, state]

func get_matrica_poll_url(state: String) -> String:
	return "%s%s?state=%s" % [AUTH_RELAY_BASE_URL, MATRICA_POLL_ENDPOINT, state]

func get_wallet_authenticate_url() -> String:
	return "%s%s" % [AUTH_RELAY_BASE_URL, WALLET_ENDPOINT]
