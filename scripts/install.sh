#!/bin/bash
set -e

REPO="Shresth2103/fk-codetantra"
APP_NAME="MyOverlay"
INSTALL_DIR="/Applications"
PLIST_NAME="com.fkcodetantra.myoverlay.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

echo "=== Installing $APP_NAME for macOS ==="

# 1. Fetch latest release archive download URL from GitHub API
RELEASE_URL=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | grep "browser_download_url.*zip" | cut -d '"' -f 4)

if [ -z "$RELEASE_URL" ]; then
    echo "Error: Could not find a ZIP release asset for $REPO."
    exit 1
fi

# 2. Download and Extract
TEMP_DIR=$(mktemp -d)
echo "Downloading latest release..."
curl -fsSL -o "$TEMP_DIR/app.zip" "$RELEASE_URL"

echo "Extracting..."
unzip -q "$TEMP_DIR/app.zip" -d "$TEMP_DIR"

# 3. Move .app bundle to /Applications
APP_PATH=$(find "$TEMP_DIR" -maxdepth 2 -name "*.app" | head -n 1)

if [ -z "$APP_PATH" ]; then
    echo "Error: No .app bundle found in release ZIP."
    rm -rf "$TEMP_DIR"
    exit 1
fi

TARGET_PATH="$INSTALL_DIR/$(basename "$APP_PATH")"

if [ -d "$TARGET_PATH" ]; then
    echo "Removing previous installation..."
    rm -rf "$TARGET_PATH"
fi

echo "Installing to $INSTALL_DIR..."
mv "$APP_PATH" "$INSTALL_DIR/"
rm -rf "$TEMP_DIR"

# 4. Configure Auto-Start on Login (macOS LaunchAgent)
mkdir -p "$LAUNCH_AGENTS_DIR"
cat <<EOF > "$LAUNCH_AGENTS_DIR/$PLIST_NAME"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.fkcodetantra.myoverlay</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/open</string>
        <string>-a</string>
        <string>$TARGET_PATH</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF

launchctl load "$LAUNCH_AGENTS_DIR/$PLIST_NAME" 2>/dev/null || true

# 5. Launch application immediately
echo "Starting $APP_NAME..."
open -a "$TARGET_PATH"

echo "=== Installation Complete! ==="