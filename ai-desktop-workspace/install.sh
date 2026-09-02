#!/usr/bin/env bash
# Author: Hexwyrm
set -e

echo "=== AI Desktop Workspace Installer ==="

BIN_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/applications"

mkdir -p "$BIN_DIR"
mkdir -p "$APP_DIR"

# 1. Copy application executable
echo "[1/3] Installing executable to $BIN_DIR/ai-desktop..."
cp -f ai-desktop.py "$BIN_DIR/ai-desktop"
chmod +x "$BIN_DIR/ai-desktop"

# 2. Copy desktop entry and inject full binary path into Exec line
echo "[2/3] Installing desktop entry to $APP_DIR/ai-desktop.desktop..."
cp -f ai-desktop.desktop "$APP_DIR/ai-desktop.desktop"
sed -i "s|^Exec=.*|Exec=$BIN_DIR/ai-desktop|" "$APP_DIR/ai-desktop.desktop"

# 3. Refresh Desktop Application Database
echo "[3/3] Updating desktop application database..."
if command -v update-desktop-database > /dev/null 2>&1; then
    update-desktop-database "$APP_DIR"
fi

echo "================================================="
echo "Installation completed successfully!"
echo "You can launch the app from your application menu (under Internet) or by running:"
echo "  $BIN_DIR/ai-desktop"
