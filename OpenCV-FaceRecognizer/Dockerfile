FROM ubuntu

RUN apt-get update && apt-get install -y \
    python-opencv \
    opencv-data \
    python-pip

RUN pip install \
    trollius

COPY src /root
WORKDIR /root

CMD python main.py
