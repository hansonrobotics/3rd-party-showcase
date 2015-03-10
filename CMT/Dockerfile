FROM ubuntu

# General dependencies
RUN apt-get update && apt-get install -y \
    git

# CMT dependencies
RUN apt-get install -y \
    python-opencv \
    python-numpy \
    python-scipy \
    python-ipdb

WORKDIR /root

# Install CMT
RUN git clone https://github.com/gnebehay/CMT.git

CMD CMT/run.py --with-rotation
