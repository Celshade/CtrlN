#!/bin/bash
# Build signed release APK for CtrlN Android app
# 
# Godot 4.6.1 has a bug where absolute keystore paths in export_presets.cfg
# are not found during export. Workaround: pass keystore via env vars.
#
# FEATURES:
#   - Prompts for auth relay URL interactively (or reads from CTRLN_AUTH_RELAY_URL env var)
#   - Embeds auth config in APK so it works without environment variables at runtime
#   - Validates keystore credentials (loads from .env.build if present)
#   - Supports CI/CD by accepting all inputs via environment variables

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

# Validate that auth relay URL is set (no hardcoded URLs in production builds)
if [ -z "$CTRLN_AUTH_RELAY_URL" ]; then
    echo
    echo "────────────────────────────────────────────────────────────"
    echo "CtrlN Release Build — Authentication Configuration"
    echo "────────────────────────────────────────────────────────────"
    echo
    read -p "Enter authentication relay URL: " CTRLN_AUTH_RELAY_URL
    
    if [ -z "$CTRLN_AUTH_RELAY_URL" ]; then
        echo "Error: Auth relay URL cannot be empty"
        exit 1
    fi
    echo
fi

echo "✓ Auth relay URL: $CTRLN_AUTH_RELAY_URL"

# Verify keystore file exists
if [ ! -f "$GODOT_ANDROID_KEYSTORE_RELEASE_PATH" ]; then
    echo "Error: Keystore not found at $GODOT_ANDROID_KEYSTORE_RELEASE_PATH"
    exit 1
fi

echo "Building signed release APK..."
cd "$SCRIPT_DIR"

# Write auth config to a temporary file that will be packaged in the APK
CONFIG_FILE="$SCRIPT_DIR/auth_config.txt"
echo "$CTRLN_AUTH_RELAY_URL" > "$CONFIG_FILE"

# Build with Godot
CTRLN_AUTH_RELAY_URL="$CTRLN_AUTH_RELAY_URL" \
GODOT_ANDROID_KEYSTORE_RELEASE_PATH="$GODOT_ANDROID_KEYSTORE_RELEASE_PATH" \
GODOT_ANDROID_KEYSTORE_RELEASE_USER="$GODOT_ANDROID_KEYSTORE_RELEASE_USER" \
GODOT_ANDROID_KEYSTORE_RELEASE_PASSWORD="$GODOT_ANDROID_KEYSTORE_RELEASE_PASSWORD" \
godot --headless --export-release "Android" "$OUTPUT_APK"

# Clean up config file
rm -f "$CONFIG_FILE"

echo "✓ Release APK built: $OUTPUT_APK"
