# Solana Wallet Login Setup Instructions

## Quick Start (3 Steps)

### Step 1: Install godot-solana-sdk GDExtension

```bash
# Download latest release
curl -L https://github.com/Virus-Axel/godot-solana-sdk/releases/download/v1.4.5/addons.zip -o /tmp/solana_sdk.zip

# Extract to Godot project
unzip /tmp/solana_sdk.zip -d ~/Projects/CtrlN/godot/
```

### Step 2: Enable Plugin in Godot

1. Open `godot/project.godot` in editor
2. Go to **Project → Project Settings → Plugins**
3. Find "SolanaSDK" and set to **Active** (Green checkmark)
4. Restart Godot editor
5. Verify: You should see debug message "✓ SolanaAuth: WalletAdapter loaded" in console

### Step 3: Register Autoload Singleton

In `godot/project.godot`, add under `[autoload]` section:

```ini
[autoload]
MatricaAuth="*res://scripts/autoload/matrica_auth.gd"
SolanaAuth="*res://scripts/autoload/solana_auth.gd"
```

**Done!** The login screen now has:
- "Login" button (Matrica OAuth)
- "Wallet" button (Solana wallet signing)
- "Play as Guest" button

---

## Testing on Device

1. **Install wallet app** on Android:
   - [Phantom](https://play.google.com/store/apps/details?id=com.phantom)
   - [Solflare](https://play.google.com/store/apps/details?id=com.solflare.mobile)

2. **Build and run APK**:
   ```bash
   cd godot
   ./build-release.sh
   adb install ctrln.apk
   ```

3. **Test login**:
   - Launch game
   - Click "Wallet" button
   - Approve wallet connection and signature in wallet app
   - Game should load your profile

---

## Troubleshooting

### "Solana SDK not installed" message
- Extract godot-solana-sdk to `godot/addons/SolanaSDK/`
- Enable in Project Settings → Plugins
- Restart Godot editor

### Wallet button doesn't appear
- Check Godot console for errors
- Verify `SolanaAuth="*res://scripts/autoload/solana_auth.gd"` in project.godot
- Ensure OS is Android in export preset

### "Could not open wallet" or no wallet app response
- Install Phantom or Solflare on device
- Verify wallet app works manually before testing login

### Signature verification fails on backend
- Verify backend is properly deployed (see [CelKeysIO repository](https://github.com/Celshade/CelKeysIO))
- Check backend logs for validation errors

---

## Files Changed

- `godot/scripts/login_screen.gd` — Added "Wallet" button and handler
- `godot/scripts/autoload/solana_auth.gd` — New wallet auth manager
- `godot/project.godot` — Need to add SolanaAuth autoload

## Next Steps

- Download and extract godot-solana-sdk
- Register SolanaAuth autoload in project.godot
- Build new APK
- Test on Android device with Phantom/Solflare installed
