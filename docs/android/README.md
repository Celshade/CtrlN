# Android Documentation

Technical guides for building and deploying CtrlN to Android.

## Contents

### [ANDROID_INTENT_FILTER_WORKAROUNDS.md](../../BuildResources/ANDROID_INTENT_FILTER_WORKAROUNDS.md)
Complete chronicle of the deep link intent-filter issue and the final Gradle post-merge injection solution. Essential reading if:
- Deep links aren't working in your build
- You want to understand why the workaround is needed
- You're modifying the manifest injection logic

**Topics covered**:
- Why intent-filters get stripped by Gradle
- History of 5 attempted workarounds and why they failed
- Technical explanation of the final solution
- How to verify it's working

### [MATRICA_OAUTH_MOBILE_FLOW.md](../../BuildResources/MATRICA_OAUTH_MOBILE_FLOW.md)
Complete OAuth flow architecture with security rationale. Read this to understand:
- How login works on Android
- Why we use PKCE (Proof Key for Public Clients)
- Security model (why the game never sees tokens)
- Integration with CelKeysIO backend

**Topics covered**:
- 6-stage OAuth flow with ASCII diagram
- PKCE code_verifier and challenge explained
- HMAC state verification for replay attack prevention
- One-time Redis profile retrieval
- Deep link redirect on Android OS
- Deployment checklist for environment variables

### Build Process

See `../scripts/README.md` for build commands and troubleshooting.

See `../ARCHITECTURE.md` for high-level project structure and design decisions.

## Quick Links

- **Build Android APK**: `godot/build-release.sh`
- **Gradle Manifest Injection Task**: `godot/android/build/build.gradle` (lines 352-410)
- **Intent-Filter Source**: `godot/android/build/src/main/AndroidManifest.xml` (lines 43-48)

## Key Takeaways

1. **Deep links work via post-merge Gradle injection** — not in source manifest
2. **OAuth uses PKCE for public clients** — game never stores secrets
3. **Keystore credentials come from env vars** — never in version control
4. **Build script is required** — `godot export-release` alone won't work
