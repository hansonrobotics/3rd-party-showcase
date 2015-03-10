# CMT #

Consensus-based Matching and Tracking of Keypoints (CMT) is an award-winning object tracking algorithm, initially published at the Winter Conference on Applications of Computer Vision 2014, where it received the Best Paper Award.

[More info and videos here.](http://www.gnebehay.com/cmt/)

## Run ##

Download and run with a single command.

```bash
$ dockerX11run --privileged --rm gaboose/cmt
```

Or by building yourself.

```bash
$ docker build -t cmt .
$ dockerX11run --privileged --rm cmt
```

## Controls ##

Press **any key** and draw a bounding box around the object to track with your mouse.

Press **Q** to exit.

## Troubleshooting ##

### `command not found: dockerX11run` ###

To run X11 docker applications easier, it is recommended that you define the following alias in your `~/.bashrc`.
```bash
$ alias dockerX11run="docker run -v /tmp/.X11-unix/X0:/tmp/.X11-unix/X0 -e DISPLAY=:0 -e LIBGL_ALWAYS_INDIRECT=1"
```

### `cannot open display: :0` ###

Try disabling xserver access control.
```bash
$ xhost +
```
