FROM ubuntu:trusty

RUN echo "source ~/.bashrc" >> ~/.bash_profile

# General dependencies
RUN apt-get update && apt-get install -y \
    wget \
    software-properties-common

# Register HARK apt repository
RUN wget -q -O - http://winnie.kuis.kyoto-u.ac.jp/HARK/harkrepos/public.gpg | apt-key add - && \
    echo "\
deb http://winnie.kuis.kyoto-u.ac.jp/HARK/harkrepos trusty non-free\n\
deb-src http://winnie.kuis.kyoto-u.ac.jp/HARK/harkrepos trusty non-free\
" > /etc/apt/sources.list.d/hark.list

# Hark-designer dependency
RUN add-apt-repository ppa:chris-lea/node.js && \
    apt-get update && \
    apt-get install -y nodejs

# Install HARK
RUN apt-get install -y \
    harkfd \
    hark-designer \
    julius-4.2.3-hark-plugin \
    harktool4

# Install the Python wrapper for HARK
RUN apt-get install -y \
    hark-python

# Install ALSA for microphone access
RUN apt-get install -y alsa-utils && \
# Change group of /dev/snd/* on login, because the devices don't exist until
# the container is run in '--privileged' mode.
    echo "find /dev/snd/ -mindepth 1 -exec chgrp audio {} \;" >> ~/.bashrc

# Add a non-root sudo user. It's required to run hark_designer.
RUN useradd user -mG sudo,audio && \
# Password is "user"
    echo user:user | chpasswd && \
# Add user to the 'audio' group to give access to a microphone through ALSA.
    usermod -aG audio user
