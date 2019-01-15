#!/bin/bash
#Copyright (c) 2013-2018 Hanson Robotics, Ltd.

# Exit if any of the commands fail
set -e

BUILD_DIR=build

# Start License Server
$BUILD_DIR/bin/run_pgd.sh start || true

# Create pipe for application's stderr
test -p $BUILD_DIR/stderr || mkfifo $BUILD_DIR/stderr

# Split screen to two: one for stdout, one for stderr, and run the app.
tmux new-session -s VeriLookGreet -d
tmux send-keys 'export LD_LIBRARY_PATH=' $BUILD_DIR '/lib' C-j
tmux send-keys 'source ' $BUILD_DIR '/ENV/bin/activate' C-j
tmux send-keys 'python3 main.py 2>' $BUILD_DIR '/stderr' C-j
tmux split-window -h
tmux send-keys 'while true; do cat ' $BUILD_DIR '/stderr; done' C-j
tmux attach -t VeriLookGreet.0
