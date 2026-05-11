#!/bin/bash
set -e

INSTALL_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_LABEL="golf-notifier"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_LABEL.plist"

echo "=== Golf Notifier Setup ==="
echo "Install directory: $INSTALL_DIR"

# 1. Check config
if [ ! -f "$INSTALL_DIR/config.json" ]; then
    echo ""
    echo "[!] config.json not found."
    echo "    Copy the example and fill in your details:"
    echo "      cp config.example.json config.json"
    echo "      open config.json"
    exit 1
fi

# 2. Generate plist from template
echo "[1/3] Generating launchd plist..."
sed "s|INSTALL_DIR|$INSTALL_DIR|g" "$INSTALL_DIR/golf-notifier.plist.template" > "$PLIST_DEST"
launchctl unload "$PLIST_DEST" 2>/dev/null || true
launchctl load "$PLIST_DEST"
echo "    launchd job loaded: $PLIST_LABEL"

# 3. Set pmset wake at 8:45 PM daily (5 min before script fires)
echo "[2/3] Setting Mac wake schedule (requires sudo)..."
sudo pmset repeat wakeorpoweron MTWRFSU 20:45:00
echo "    Wake scheduled at 20:45 daily."

# 4. Trigger Calendar access
echo "[3/3] Verifying Calendar access..."
osascript -e 'tell application "Calendar" to return name of every calendar' > /dev/null
echo "    Calendar access OK."

echo ""
echo "=== Setup complete! ==="
echo "Run a test with:"
echo "  python3 \"$INSTALL_DIR/check_golf_schedule.py\" --dry-run"
