#!/usr/bin/env bash
# Part 7: a small installation script, committed on the feature-script branch

echo "Starting installation..."

# Update the package lists (Debian/Ubuntu)
sudo apt-get update

# Install a package of my choice
sudo apt-get install -y tree

echo "Installation complete!"
