#!/bin/bash
# Get exact 1.21.10 server URL
VERSION_URL=$(curl -s https://piston-meta.mojang.com/mc/game/version_manifest_v2.json | grep -o '"url":"[^"]*1\.21\.10[^"]*"' | head -1 | cut -d'"' -f4)
SERVER_URL=$(curl -s "$VERSION_URL" | grep -o '"server":{"url":"[^"]*"' | cut -d'"' -f4)
echo "Downloading from: $SERVER_URL"
wget "$SERVER_URL" -O server.jar
