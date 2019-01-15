#!/bin/bash
#Copyright (c) 2013-2018 Hanson Robotics, Ltd.

# Exit if any of the commands fail
set -e

BUILD_DIR=build

# Build docker image and copy binaries from it
IMAGE_NAME=verilookgreet-extract
docker build -t $IMAGE_NAME .
docker run --name $IMAGE_NAME $IMAGE_NAME
docker cp $IMAGE_NAME:/root/bin $BUILD_DIR
docker cp $IMAGE_NAME:/root/lib $BUILD_DIR
docker rm $IMAGE_NAME

# Set up a python virtual environment
virtualenv $BUILD_DIR/ENV -p $(which python3)
source $BUILD_DIR/ENV/bin/activate
pip install pexpect

echo VeriLookGreet successfully built
