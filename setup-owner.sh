#!/bin/bash
echo "Setting up Owner permissions for Binwalk..."

# Create owner group
lp creategroup owner

# Add Binwalk to owner group
lp user Binwalk parent set owner

# Set permissions
PERMS=(
  "essentials.fly"
  "essentials.give"
  "essentials.time"
  "essentials.time.set"
  "essentials.clear"
  "essentials.gamemode"
  "essentials.gamemode.creative"
  "essentials.gamemode.survival"
  "essentials.teleport"
  "essentials.teleport.here"
  "essentials.teleport.all"
  "essentials.weather"
  "essentials.heal"
  "essentials.feed"
  "essentials.god"
  "minecraft.command.tp"
  "minecraft.command.gamemode"
  "minecraft.command.give"
  "minecraft.command.kill"
  "minecraft.command.time"
)

for perm in "${PERMS[@]}"; do
  lp group owner permission set "$perm"
done

# Set tab prefix
lp group owner meta addprefix 100 "&4[Owner] &f"

echo "Done! Owner permissions set for Binwalk"
echo "Commands available: /fly, /give, /time, /gamemode, /tp, etc."
