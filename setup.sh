#!/bin/bash
set -e

PLIST_NAME="com.takase.golf-notifier"
PLIST_SRC="$HOME/golf_notifier/$PLIST_NAME.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"

echo "=== Golf Notifier Setup ==="

# 1. Copy plist
echo "[1/3] Installing launchd job..."
cp "$PLIST_SRC" "$PLIST_DEST"
launchctl unload "$PLIST_DEST" 2>/dev/null || true
launchctl load "$PLIST_DEST"
echo "    launchd job loaded."

# 2. Set pmset wake at 8:45 PM daily (5 min before script fires)
echo "[2/3] Setting Mac wake schedule (requires sudo)..."
sudo pmset repeat wakeorpoweron MTWRFSU 20:45:00
echo "    Wake scheduled at 20:45 daily."

# 3. Trigger Calendar access (will prompt if not yet granted)
echo "[3/3] Verifying Calendar access..."
osascript -e 'tell application "Calendar" to return name of every calendar' > /dev/null
echo "    Calendar access OK."

echo ""
echo "=== Setup complete! ==="
echo "Run a test with:"
echo "  python3 ~/golf_notifier/check_golf_schedule.py --dry-run"
