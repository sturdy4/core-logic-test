#!/bin/bash
# Clear RAM cache for a fresh start
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches

# Launch with GraalVM and G1GC optimization
# Using 1200M to leave room for GNOME and PolyMC
gamemoderun java -Xmx1200M -Xms512M \
  -XX:+UseG1GC \
  -XX:+UnlockExperimentalVMOptions \
  -XX:+ParallelRefProcEnabled \
  -XX:MaxGCPauseMillis=200 \
  -XX:+DisableExplicitGC \
  -XX:+AlwaysPreTouch \
  -jar server.jar nogui
