# Solana Wallet Login: Architecture & Implementation

## Overview

CtrlN now supports **two authentication methods**:

1. **Matrica OAuth** (existing) — Social login via Matrica (Discord, etc.)
2. **Solana Wallet Signing** (new) — Direct wallet signing via Mobile Wallet Adapter (Android only)

Both methods ultimately authenticate the user and store their profile in the same system. Users can choose their preferred method on the login screen.

This implementation uses the [godot-solana-sdk](https://github.com/Virus-Axel/godot-solana-sdk) GDExtension, a mature, production-ready plugin that provides native Solana support in Godot with built-in Mobile Wallet Adapter integration.

---

## Architecture

### Authentication Flow with Solana Wallet

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       GODOT GAME (Android)                              │
│                                                                           │
│  User selects "Login with Solana Wallet"                                │
│           ↓                                                              │
│  1. Game requests wallet authorization                                  │
│     via SolanaWalletPlugin.authorize()                                  │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│              ANDROID RUNTIME (Solana Wallet Plugin)                      │
│                                                                           │
│  2. Establish local WebSocket with wallet app                           │
│     (via MobileWalletAdapterClient)                                     │
│                                                                           │
│  3. MWA protocol: authorize RPC call                                    │
│     - Same device: Solflare, Phantom, etc.                              │
│     - User approves in wallet UI                                        │
│     - Plugin receives: auth_token, user_pubkey                          │
│                                                                           │
│  4. Sign message with user's private key:                               │
│     - Generate cryptographic challenge                                  │
│     - MWA protocol: signMessages RPC call                               │
│     - Wallet returns: signature_bytes                                   │
│                                                                           │
│  5. Return to game: (pubkey, signature, challenge)                      │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                    GODOT GAME (Android)                                 │
│                                                                           │
│  6. Credential object ready, game calls backend API                    │
│     AuthConfig endpoint                                                │
│     Body: {wallet, challenge, signature}                               │
│                                                                           │
│  7. Game receives: gameState token for polling                          │
│                                                                           │
│  8. Start polling loop:                                                 │
│     AuthConfig.get_matrica_poll_url(authToken)                          │
│     Loop runs every 1.5 seconds until success or timeout                │
│                                                                           │
│  9. Polling returns: user profile dict (name, avatar, etc.)            │
│     Profile stored in game's player data                                │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────────────────────────────────┐
│              AUTH RELAY SERVICE BACKEND (Node.js)                        │
│                                                                           │
│  Wallet verification:
│  - Verify signature against wallet public key                         │
│  - Verify challenge TTL (prevent replay attacks)                      │
│  - Create or fetch user profile from database                         │
│  - Generate auth token                                                │
│  - Store: profile temporarily keyed by auth token                     │
│  - Return: auth token to game for polling                             │
│                                                                       │
│  Polling endpoint (same as Matrica flow):                              │
│  - Returns cached profile (one-time retrieval)                        │
│  - Same as Matrica flow                                                 │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Security Properties

**Why Wallet Signing?**
- User proves they own the wallet without revealing private key
- No intermediary OAuth provider needed
- On-device signing (Phantom, Solflare handle key management)
- Nonce + timestamp prevent replay attacks
- One-time profile retrieval from secure storage (same as Matrica)

**Nonce Verification:**
- Challenge is generated and validated server-side
- Short TTL prevents replay attacks
- Server validates challenge freshness before processing

**Signature Verification:**
- Signature is verified against user's public key
- Invalid or expired signatures are rejected
- No private key ever leaves user's wallet

---

## Implementation Details

### 1. Godot GDScript (Character Select Screen)

**File**: `godot/scenes/character_select.gd` (add wallet button)

Uses **godot-solana-sdk** WalletAdapter node for MWA integration:

```gdscript
# In _ready():
wallet_adapter = WalletAdapter.new()
wallet_adapter.connected.connect(_on_wallet_connected)

# When user clicks wallet login:
func _on_wallet_login_pressed():
	wallet_adapter.connect_wallet()  # Opens wallet app (MWA protocol)
	
	# Generate challenge and request signature
	var signature = await wallet_adapter.sign_message(...)
	var pubkey = wallet_adapter.get_public_key()
	
	# Send to backend for verification
	_verify_wallet_signature(pubkey, signature)
```

### 2. Android Plugin Setup (godot-solana-sdk)

**Installation**: 
1. Download [godot-solana-sdk release](https://github.com/Virus-Axel/godot-solana-sdk/releases)
2. Extract to `godot/addons/SolanaSDK` (or `res://bin/`)
3. Enable in Project → Project Settings → Plugins → SolanaSDK

**No custom Kotlin code needed** — the SDK handles:
- Mobile Wallet Adapter protocol (MWA 2.0)
- Signature verification
- Local WebSocket communication with wallet apps
- Android permission handling

**Supported Wallets** (automatically detected):
- Phantom
- Solflare
- Seed Vault Wallet

**Backend**: Signature verification is handled by a separate backend authentication service. Endpoints are configured via environment variables at deployment time.

### 4. Build Configuration

**No custom Gradle configuration needed** — godot-solana-sdk is a GDExtension that handles everything automatically.

**Required Godot Settings** (`project.godot`):

```ini
[gdextension_list]
# If SolanaSDK is in res://bin/:
enabled_extension = "res://bin/godot-solana-sdk.gdextension"

# Or if in res://addons/:
enabled_extension = "res://addons/SolanaSDK/godot-solana-sdk.gdextension"
```

**Android Manifest** (auto-handled by godot-solana-sdk, but verify):

```xml
<!-- Allow queries for wallet apps -->
<queries>
	<intent>
		<action android:name="android.intent.action.VIEW" />
		<data android:scheme="solana-wallet" />
	</intent>
</queries>
```

**Export Preset** (`android` section, `project.godot`):

```ini
[android]
# Minimum Android version for MWA support
android/api_level = 24

# Required permissions
permissions = [
	# Network access (already typical for HTTP requests)
	"android.permission.INTERNET"
]
```

---

## Integration Checklist

### Frontend (Godot)
- [ ] Download [godot-solana-sdk](https://github.com/Virus-Axel/godot-solana-sdk/releases) and extract to `res://addons/SolanaSDK`
- [ ] Enable plugin in Project Settings → Plugins
- [ ] Add wallet login button to character select screen (`godot/scripts/character_select_wallet.gd`)
- [ ] Implement `_on_wallet_login_pressed()` with WalletAdapter connection
- [ ] Implement signature verification HTTP request
- [ ] Implement polling loop with timeout handling
- [ ] Add error states and recovery UI
- [ ] Test on Android device (requires Phantom/Solflare installed)

### Backend
- Implemented in separate backend authentication service repository
- See backend service documentation for wallet verification endpoint setup

### Mobile Testing
- [ ] Install Phantom or Solflare wallet on Android device
- [ ] Compile CtrlN release APK
- [ ] Run and test wallet login button
- [ ] Verify wallet app opens and prompts for signature approval
- [ ] Verify signature verification on backend
- [ ] Verify profile loads and game starts

### Security & Testing
- [ ] Test signature verification with multiple wallets (Phantom, Solflare)
- [ ] Verify challenge validity enforcement
- [ ] Test on both devnet and mainnet
- [ ] Load test polling endpoint
- [ ] Verify one-time retrieval works correctly
- [ ] Audit for general security issues

---

## Quick Start: Testing

### 1. Setup godot-solana-sdk
```bash
# Download release from:
# https://github.com/Virus-Axel/godot-solana-sdk/releases

# Extract to Godot project:
cd godot
mkdir -p addons/SolanaSDK
unzip ~/Downloads/godot-solana-sdk-4.x.zip -d addons/SolanaSDK/

# Open project.godot and enable plugin in Project Settings
```

### 2. Integrate Wallet Login (GDScript)
```bash
# Copy character_select_wallet.gd to godot/scenes/
cp character_select_wallet.gd godot/scenes/
```

### 3. Install Wallet App on Device
```bash
# Install one of the supported wallets:
# - Phantom: https://play.google.com/store/apps/details?id=com.phantom
# - Solflare: https://play.google.com/store/apps/details?id=com.solflare.mobile
```

### 4. Build and Test
```bash
# Build release APK
cd godot
./build-release.sh

# Install on device
adb install ctrln.apk

# Run game and test wallet login
```

## 5. Test Backend Endpoint (Local)

For development testing, configure the auth relay service locally:

```bash
# Set environment variable for local testing
export CTRLN_AUTH_RELAY_URL="http://localhost:3000"

# Then run CtrlN - AuthConfig will use this URL
godot --editor
```

---

## Troubleshooting

### "Solana SDK not available" / Plugin not loaded
- Ensure godot-solana-sdk is extracted to `res://addons/SolanaSDK/` or `res://bin/`
- Verify plugin is enabled: Project Settings → Plugins → SolanaSDK (should show "Active")
- Restart Godot editor and re-export APK if changes made to plugin path

### "Connecting to wallet..." hangs indefinitely
- Ensure Phantom or Solflare wallet is installed on device
- Check wallet app can be started manually
- Verify platform is Android (MWA only, iOS not supported)
- Check device network connectivity

### "Invalid signature" from backend
- Verify signature was generated by the wallet
- Ensure request was sent to correct endpoint
- Contact backend administrator if issue persists

### Profile not retrieved after poll
- Verify auth service is running and accessible
- Check auth token from verify response matches polling request
- Verify profile retrieval works correctly

### "Invalid challenge format" from backend
- Ensure challenge was generated by the wallet
- Check that challenge matches what was signed
- Verify backend received complete signature data

### Wallet app doesn't prompt for signature approval
- Compare message being signed with backend expectation
- Verify user has balance to pay network fee (if applicable)
- Check wallet is not in app-switching mode
- Try signing a simple test message first

---

## Future Enhancements

1. **NFT-Gated Access**: Verify user owns specific Metaplex NFT for cosmetics/characters
2. **Token Airdrops**: Gift in-game tokens to users who link wallets
3. **On-Chain Achievements**: Record championships on Solana for soulbound tokens
4. **Profile Linking**: Allow users to link both Matrica + Solana wallet for cross-chain profile
5. **iOS Support**: Implement web-based wallet flow for iOS (when MWA expands)
