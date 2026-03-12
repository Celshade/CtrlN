# CtrlN Configuration Guide

## Authentication Relay Service

Authentication endpoints are centralized in `AuthConfig` and configured via environment variables. This prevents hardcoding of service addresses and enables flexible deployment.

### Configuration Priority

1. **Environment variables** (takes precedence)
2. **Default values** (fallback, for development)

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `CTRLN_AUTH_RELAY_URL` | Base URL for auth relay service | `https://api.auth-relay.local` |
| `CTRLN_MATRICA_ENDPOINT` | Matrica OAuth start endpoint path | `/auth/start` |
| `CTRLN_WALLET_ENDPOINT` | Solana wallet verification endpoint path | `/wallet-authenticate` |

### Default Configuration

By default, CtrlN uses placeholder URLs (`auth-relay.local` domain) to prevent accidental hardcoding of service addresses in production. During development, you'll see:

```
⚠ AuthConfig: Using placeholder auth relay URL. Set CTRLN_AUTH_RELAY_URL environment variable for production.
```

### Setting Environment Variables

#### Local Development (Linux/macOS)

```bash
export CTRLN_AUTH_RELAY_URL="http://localhost:3000"
export CTRLN_MATRICA_ENDPOINT="/api/auth/start"
export CTRLN_WALLET_ENDPOINT="/api/v1/wallet-authenticate"

# Then run CtrlN
godot --editor
```

#### Production Deployment

Set environment variables in your deployment platform:

**Godot Export (Android .apk)**:
```gdscript
# In build script or export preset
OS.set_environment("CTRLN_AUTH_RELAY_URL", "https://api.production.example.com")
```

**Docker**:
```dockerfile
ENV CTRLN_AUTH_RELAY_URL=https://api.production.example.com
ENV CTRLN_WALLET_ENDPOINT=/api/v1/wallet-authenticate
```

**GitHub Actions**:
```yaml
- name: Build APK
  env:
    CTRLN_AUTH_RELAY_URL: ${{ secrets.AUTH_RELAY_URL }}
    CTRLN_WALLET_ENDPOINT: /api/v1/wallet-authenticate
  run: |
    # build commands
```

### URL Construction

`AuthConfig` builds complete URLs from base URL + endpoint path:

```gdscript
# Matrica start
https://api.auth-relay.local + /auth/start + ?state=TOKEN
→ https://api.auth-relay.local/auth/start?state=TOKEN

# Solana wallet verification
https://api.auth-relay.local + /wallet-authenticate
→ https://api.auth-relay.local/wallet-authenticate
```

### Accessing Configuration in Code

**✅ Correct - Use AuthConfig**:
```gdscript
var url = AuthConfig.get_wallet_authenticate_url()
var poll_url = AuthConfig.get_matrica_poll_url(state)
```

**❌ Incorrect - Hardcoding URLs**:
```gdscript
# Don't do this - makes URL management impossible
var url = "https://api.auth-relay.local/wallet-authenticate"
```

## Authentication Flow

### Matrica OAuth (Login Screen)

```
1. Game calls: AuthConfig.get_matrica_start_url(state)
2. Opens browser to auth relay service
3. User authenticates via Matrica
4. Relay service stores profile in temporary storage
5. Game polls: AuthConfig.get_matrica_poll_url(state)
6. Relay returns profile when ready
```

### Solana Wallet Login

```
1. Wallet generates challenge (nonce + timestamp)
2. User signs challenge in wallet app
3. Game calls: AuthConfig.get_wallet_authenticate_url()
4. Sends signature to relay service
5. Relay verifies and stores profile
6. Game polls for authenticated profile
```

## Troubleshooting

### "Using placeholder auth relay URL" warning

This is normal during development. Set `CTRLN_AUTH_RELAY_URL` environment variable to use a real service.

### Auth fails with "Connection refused"

- Verify `CTRLN_AUTH_RELAY_URL` is set correctly
- Check that auth relay service is running and accessible
- Enable network debugging in Godot

### URLs still hardcoded?

Search your codebase:
```bash
grep -r "celkeys.io" godot/scripts/
grep -r "auth-relay.local" godot/scripts/autoload/matrica_auth.gd
grep -r "auth-relay.local" godot/scripts/autoload/solana_auth.gd
```

If found outside `AuthConfig`, update to use `AuthConfig.get_*()` methods.

## See Also

- [SOLANA_WALLET_LOGIN.md](SOLANA_WALLET_LOGIN.md) - Solana integration architecture
- [ARCHITECTURE.md](ARCHITECTURE.md) - Overall system design
- [godot/scripts/autoload/auth_config.gd](../godot/scripts/autoload/auth_config.gd) - Implementation
