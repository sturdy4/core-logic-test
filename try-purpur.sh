#!/bin/bash
echo "Trying Purpur 1.21.10..."
wget https://api.purpurmc.org/v2/purpur/1.21.10/latest/download -O server.jar
if [ $? -ne 0 ]; then
    echo "Purpur 1.21.10 not available, using 1.21.4 for now"
    wget https://api.purpurmc.org/v2/purpur/1.21.4/latest/download -O server.jar
fi
