# CtrlN Architecture Overview

This document describes the high-level architecture of the CtrlN project, which consists of two separate codebases for different platforms.

## Project Structure

```
CtrlN/
├── godot/          Android game (Godot 4.6.1)
└── src/ctrln/      Python [desktop] game (Pygame)
```

## Codebase Relationship

### Godot Application (`godot/`)
- **Purpose**: Primary game client on desktop and Android
- **Technology**: Godot 4.6.1 (GDScript)
- **Platforms**: Windows, macOS, Linux, Android
- **Key Features**:
  - Playable game with UI and character selection
  - Android OAuth2 integration with deep link callback (`ctrln://auth`)
  - Local player profile storage
- **Build System**: Godot export presets + custom Gradle manifest injection for Android deep links
- **Build Script**: `build-release.sh` (requires `.env.build` credentials)

### Python Utilities (`src/ctrln/`)
- **Purpose**: Prototyping, testing, and desktop development
- **Technology**: Python 3.12+ with Pygame
- **Platforms**: Development/testing only
- **Key Features**:
  - Game mechanics prototyping
  - Character and achievement system
  - Profile serialization
  - UI layout testing
- **Status**: Optional; main game uses Godot

## Android Integration: Deep Link OAuth Flow

When users log in on Android:

1. **Game initiates login** → Opens browser to auth relay service Matrica endpoint
2. **Browser redirects to Matrica** → User grants permission
3. **Matrica redirects back** → auth relay service callback endpoint
4. **Backend stores profile** → Temporary storage (keyed by auth token)
5. **Backend redirects** → `ctrln://auth?status=done&state=...` (deep link)
6. **Android OS routes** → to CtrlN app (system-level, can't be hijacked)
7. **Game polls auth relay** → Retrieves and loads user profile

(See [CONFIG.md](CONFIG.md) for endpoint configuration details)

**Security**: This flow uses PKCE (Proof Key for Public Clients) because the game is a public client that cannot securely store backend secrets.

## Configuration & Deployment

- **Godot Build Credentials**: `godot/.env.build` (local-only, git-ignored)
- **Game Config**: `src/ctrln/config.py`
- **Backend Authentication Service**: Separate repository and deployment
  - See [CONFIG.md](CONFIG.md) for OAuth endpoint configuration

## Documentation

- **Android Workarounds**: `docs/android/` — Technical deep dives on Gradle manifest injection
- **OAuth Flow**: `docs/android/MATRICA_OAUTH_MOBILE_FLOW.md` — Complete security architecture
- **Design Docs**: `docs/design/` — Game design and feature planning
- **Build Process**: `godot/build-release.sh` — Release APK signing with keystore workaround

## Key Design Decisions

### Why Godot + Python Hybrid?

- **Godot**: Production game client (cross-platform, performant)
- **Python**: Development tools, testing infrastructure, and algorithm prototyping
- They coexist but are independent; Python not shipped in production

### Why External OAuth Backend?

- Matrica OAuth requires `client_secret` that cannot live in public game code
- Backend authentication service acts as a stateless relay between game and Matrica
- PKCE ensures security even though game is a public client
- One-time cached profile delivery prevents replay attacks

### Why Custom Gradle Manifest Injection?

Godot's manifest merge pipeline strips the deep link `<intent-filter>` during export.
Solution: Gradle post-merge hook that reinjects it at the right stage of the build pipeline.
See `docs/android/ANDROID_INTENT_FILTER_WORKAROUNDS.md` for full technical history.

## Building & Testing

### Build Release APK (signed)
```bash
cd godot
./build-release.sh  # Requires godot/.env.build with keystore credentials
```

### Run Game (Godot editor)
```bash
cd godot
godot  # Open in editor
```

### Run Tests (Python)
```bash
cd ..
python -m pytest tests/
```

## Security Checklist

- ✅ Keystore password: Local-only env vars, never in git
- ✅ OAuth tokens: Never stored in game; only ephemeral profile
- ✅ PKCE code_verifier: Browser-secure, embedded in HMAC-signed serverState
- ✅ Deep link scheme: (`ctrln://`) Android OS-enforced; can't be hijacked
- ✅ Redis auth profile: One-time retrieval, 10-minute TTL
- ✅ Git history: No credentials exposed (verified clean)

## Development Workflow

1. **Proto in Python** (`src/ctrln/`) — Test mechanics
2. **Port to GDScript** (`godot/scripts/`) — Implement in Godot
3. **Test on Device** — Run signed APK via `build-release.sh`
4. **Commit** — Git ignores keystore and build artifacts
