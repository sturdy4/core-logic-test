#!/bin/bash
# Usage: ./silent-demote.sh PLAYERNAME
PLAYER="$1"

if [ -z "$PLAYER" ]; then
    echo "Usage: ./silent-demote.sh <player>"
    echo "Example: ./silent-demote.sh Notch"
    exit 1
fi

echo "Demoting $PLAYER silently..."

# Commands to run in server console (copy these):
echo "Copy and paste these in server console:"
echo ""
echo "# Remove from creative and set to survival"
echo "minecraft:gamemode survival $PLAYER"
echo ""
echo "# If using LuckPerms to remove perms"
echo "lp user $PLAYER permission unset essentials.gamemode.creative"
echo "lp user $PLAYER permission unset essentials.gamemode"
