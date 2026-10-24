#!/bin/bash

APP_NAME="MyOverlay"
INSTALL_PATH="/Applications/$APP_NAME.app"
PLIST_NAME="com.fkcodetantra.myoverlay.plist"
LAUNCH_AGENT_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME"
APP_DATA_DIR="$HOME/Library/Application Support/$APP_NAME"
PREFS_FILE="$HOME/Library/Preferences/com.fkcodetantra.myoverlay.plist"

echo "=== Uninstalling $APP_NAME ==="

# 1. Quit running application process
pkill -f "$APP_NAME" 2>/dev/null || true

# 2. Unload and remove LaunchAgent
if [ -f "$LAUNCH_AGENT_PATH" ]; then
    echo "Removing auto-start configuration..."
    launchctl unload "$LAUNCH_AGENT_PATH" 2>/dev/null || true
    rm -f "$LAUNCH_AGENT_PATH"
fi

# 3. Remove App from /Applications
if [ -d "$INSTALL_PATH" ]; then
    echo "Removing application bundle..."
    rm -rf "$INSTALL_PATH"
fi

# 4. Optional: Clean stored API keys and app data
if [[ "$*" == *"--clean-app-data"* ]]; then
    echo "Cleaning user preferences and stored API keys..."
    rm -rf "$APP_DATA_DIR"
    rm -f "$PREFS_FILE"
fi

echo "=== Uninstallation Complete! ==="