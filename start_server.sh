#!/bin/bash

# Define the cleanup function
cleanup() {
    # Kill the tmux session entirely
    tmux kill-session -t mc 2>/dev/null
    # Clear the terminal so it looks fresh
    clear
    exit
}

# Trap Ctrl+C (SIGINT) to run the cleanup function
trap cleanup SIGINT

# Start the tmux session in the background
tmux new-session -d -s mc '~/playit'
tmux split-window -v -t mc 'cd ~/mc-server-1.21.10/ && java -Xmx4G -Xms4G -jar server.jar nogui'

# Attach to the session. 
# Once you hit Ctrl+C, the trap above will trigger.
tmux attach-session -t mc
