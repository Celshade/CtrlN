#!/bin/bash
# Build signed release APK for CtrlN Android app
# 
# Godot 4.6.1 has a bug where absolute keystore paths in export_presets.cfg
# are not found during export. Workaround: pass keystore via env vars.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$SCRIPT_DIR/.env.build"
OUTPUT_APK="$ROOT_DIR/ctrln.apk"

# Source .env.build for credentials if it exists
if [ -f "$ENV_FILE" ]; then
    source "$ENV_FILE"
fi

# Validate that credentials are set
if [ -z "$GODOT_ANDROID_KEYSTORE_RELEASE_PATH" ] || [ -z "$GODOT_ANDROID_KEYSTORE_RELEASE_PASSWORD" ] || [ -z "$GODOT_ANDROID_KEYSTORE_RELEASE_USER" ]; then
    echo "Error: Keystore credentials not set"
    echo "Create $SCRIPT_DIR/.env.build with:"
    echo "  export GODOT_ANDROID_KEYSTORE_RELEASE_PATH=\"./ctrln-release.keystore\""
    echo "  export GODOT_ANDROID_KEYSTORE_RELEASE_USER=\"ctrln\""
    echo "  export GODOT_ANDROID_KEYSTORE_RELEASE_PASSWORD=\"<password>\""
    exit 1
fi

# Verify keystore file exists
if [ ! -f "$GODOT_ANDROID_KEYSTORE_RELEASE_PATH" ]; then
    echo "Error: Keystore not found at $GODOT_ANDROID_KEYSTORE_RELEASE_PATH"
    exit 1
fi

echo "Building signed release APK..."
cd "$SCRIPT_DIR"

GODOT_ANDROID_KEYSTORE_RELEASE_PATH="$GODOT_ANDROID_KEYSTORE_RELEASE_PATH" \
GODOT_ANDROID_KEYSTORE_RELEASE_USER="$GODOT_ANDROID_KEYSTORE_RELEASE_USER" \
GODOT_ANDROID_KEYSTORE_RELEASE_PASSWORD="$GODOT_ANDROID_KEYSTORE_RELEASE_PASSWORD" \
godot --headless --export-release "Android" "$OUTPUT_APK"

echo "✓ Release APK built: $OUTPUT_APK"
