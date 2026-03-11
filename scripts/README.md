# Scripts Directory

This directory contains utility scripts for building and deploying CtrlN.

## Available Scripts

### Android Build

**Location**: `../godot/build-release.sh`

Builds a signed release APK for Android.

**Prerequisites**:
- Godot 4.6.1+ installed and in PATH
- Android SDK configured in Godot
- Keystore file and credentials set up

**Usage**:
```bash
cd godot
./build-release.sh
```

**Configuration**: 
- Requires `godot/.env.build` with keystore credentials (git-ignored)
- See `config/.env.example` for template
- See `docs/ARCHITECTURE.md` for build architecture overview

## Build Troubleshooting

If you encounter build errors:

1. **"Error: Keystore credentials not set"**
   - Create `godot/.env.build` with credentials
   - Copy `config/.env.example` as a template

2. **"Keystore not found at..."**
   - Ensure `ctrln-release.keystore` is in `godot/` directory
   - Update path in `godot/.env.build` if necessary

3. **APK installs but OAuth deep link doesn't work**
   - See `docs/android/ANDROID_INTENT_FILTER_WORKAROUNDS.md`
   - Verify Gradle manifest injection task is running
   - Check `godot/android/build/build.gradle` lines 352-410

## Documentation

- **Full Architecture**: `docs/ARCHITECTURE.md`
- **Android Build Deep Dive**: `docs/android/ANDROID_INTENT_FILTER_WORKAROUNDS.md`
- **OAuth Flow & Security**: `docs/android/MATRICA_OAUTH_MOBILE_FLOW.md`
