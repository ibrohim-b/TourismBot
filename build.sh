#!/usr/bin/env bash
# Render build script

set -o errexit

pip3 install --upgrade pip
pip3 install -r requirements.txt

# Create necessary directories
mkdir -p media/images media/audio media/videos media/documents logs

echo "Build completed successfully!"
