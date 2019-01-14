#!/bin/bash
#Copyright (c) 2013-2018 Hanson Robotics, Ltd.
# Would've done a docker image instead, but for some reason the demo can't
# find the webcam from a docker container, even with /dev/video0 mounted.

# Exit if any of the commands fail
set -e

DIRNAME=Neurotec_Biometric_5_1_Algorithm_Demo_Linux_x86_64

# Download demo if it's not already there
if test ! -d $DIRNAME; then
  wget -O tmp.zip http://download.neurotechnology.com/$DIRNAME\_2015-03-02.zip
  unzip tmp.zip
  rm tmp.zip
fi

# Run
./$DIRNAME/FacesAlgorithmDemo
