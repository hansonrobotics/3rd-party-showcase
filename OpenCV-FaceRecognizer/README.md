# OpenCV Face Recognizer #

...in development...

Following these guides:
- [Face Detection using Haar Cascades](http://docs.opencv.org/trunk/doc/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html)
- [FaceRecognizer - Face Recognition with OpenCV](http://docs.opencv.org/trunk/modules/contrib/doc/facerec/)

## Build ##

```bash
$ docker build -t opencv-fr .
```

## Run ##

```bash
$ dockerX11run --privileged --rm opencv-fr
```


## Controls ##

- **S** - take a snapshot of the visible face.
- **Q** - exit.
#####Copyright (c) 2013-2018 Hanson Robotics, Ltd.
