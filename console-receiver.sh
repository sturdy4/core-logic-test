#!/bin/bash
# Run this alongside your server to receive web commands
SERVER_DIR="$HOME/mc-server-1.21.10"
PIPE="$SERVER_DIR/console.pipe"

echo "Starting command receiver..."
echo "Pipe file: $PIPE"

# Create pipe if it doesn't exist
rm -f "$PIPE"
mkfifo "$PIPE"

while true; do
    if read line < "$PIPE"; then
        echo "[WEB] Command received: $line"
        # You can process commands here
        # For now, just log them
        echo "$(date): $line" >> "$SERVER_DIR/web-commands.log"
    fi
    sleep 1
done
