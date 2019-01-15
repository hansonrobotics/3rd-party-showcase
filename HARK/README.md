# HARK #

...in development... (only includes the HARK installation atm)

### Description ###

[HARK](http://hark.jp) provides sound source localization, separation, acoustic feature extraction, and automatic speech recognition. Utilizes microphone arrays, e.g. 8 microphones arranged in a circle.

Sound localization and separation can be used to find the conversation partner's direction and even listen to several people at once.

## Build ##

```bash
$ docker build -t hark .
```

## Run ##

```bash
$ dockerX11run --privileged --rm hark
```
#####Copyright (c) 2013-2018 Hanson Robotics, Ltd.
