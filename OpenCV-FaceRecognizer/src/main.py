#Copyright (c) 2013-2018 Hanson Robotics, Ltd.
import cv2
import os
import trollius as asyncio
from trollius import From, sleep, Return
import logging
import composition, crop, utils
import numpy as np

logging.basicConfig(level=logging.DEBUG)

class Context:
    def __init__(self, **kwargs):
        # Frame buffers
        self.webcam = None
        self.composed = None

        # Snapshot futures
        self.snaps = []

        # Configuration
        self.wname = kwargs['wname']
        self.faceCascade = kwargs['faceCascade']
        self.eyeCascade = kwargs['eyeCascade']

        # CPU performance can be tuned with minSize, maxSize and scaleFactor
        # Threshold for a positive result can be adjusted with minNeighbours
        self.face_cascade_params = {'scaleFactor': 1.2,
                                    'minNeighbors': 5,
                                    'minSize': (70, 70),
                                    'flags': cv2.cv.CV_HAAR_SCALE_IMAGE}
        self.eye_cascade_params = {'scaleFactor': 1.2,
                                   'minNeighbors': 3}


class Frame:
    """ Holds an image and detected features in it. """
    def __init__(self, bitmap, context):
        self.bitmap = bitmap
        self.context = context
        self._faces = None
        self._eyes = None

    @property
    def faces(self):
        self._detect()
        return self._faces

    @property
    def eyes(self):
        self._detect()
        return self._eyes

    @staticmethod
    def _addpos(box, pos):
        return (box[0]+pos[0], box[1]+pos[1], box[2], box[3])

    def _detect(self):
        if self._faces != None and self._eyes != None:
            return
        gray = cv2.cvtColor(self.bitmap, cv2.COLOR_BGR2GRAY)
        self._faces = context.faceCascade.detectMultiScale(gray, **self.context.face_cascade_params)
        self._eyes = [[self._addpos(box, (x, y)) for box in
            context.eyeCascade.detectMultiScale(gray[y:y+h, x:x+w],
                                                minSize=(h/10, w/10),
                                                maxSize=(h/3, w/3),
                                                **self.context.eye_cascade_params)]
            for x,y,w,h in self._faces]


@asyncio.coroutine
def webcam(context):
    video_capture = cv2.VideoCapture(0)
    try:
        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()
            # Send the frame to context
            context.webcam = Frame(frame, context)
            # Yield to other coroutines
            yield From(sleep(0))
    except:
        # Release webcam when the coroutine is cancelled
        # and on other exceptions
        video_capture.release()
        raise


@asyncio.coroutine
def compose(context):
    while True:
        if context.webcam == None:
            continue
        frameobj = context.webcam
        frame = frameobj.bitmap.copy()

        # Draw rectangles around the faces
        for (x, y, w, h) in frameobj.faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Draw rectangles around eyes
        for eyegroup in frameobj.eyes:
            for (x, y, w, h) in eyegroup:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        # Display snapshots
        if len(context.snaps) > 0:
            snaps = [future.result() if future.done() else
                     np.ones((70, 70, 3), np.uint8)*128
                     for future in context.snaps]
            stack = composition.stack(snaps, frame.shape[0])
            frame = composition.horizontally(frame, stack)

        context.composed = frame
        yield From(sleep(0))


@asyncio.coroutine
def display(context):
    # Create window
    cv2.namedWindow(context.wname)
    try:
        # Display the composed frames buffered in context
        while True:
            if context.composed != None:
                cv2.imshow(context.wname, context.composed)
                context.composed = None
            yield From(sleep(0))
    except:
        # Destroy window when the coroutine is cancelled
        # and on other exceptions
        cv2.destroyAllWindows()
        raise


@asyncio.coroutine
def keyboard(context):
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            context.snaps.append(asyncio.Task(captureface(context)))
        yield From(sleep(0))


@asyncio.coroutine
def captureface(context):
    while True:
        frameobj = context.webcam

        # Pick the face that has two eyes
        eyegroups = [eyes for eyes in frameobj.eyes if len(eyes) == 2]
        if len(eyegroups) == 0:
            yield From(sleep(0))
            continue

        # Crop
        eyes = eyegroups[0]
        leye = utils.getcenter(min(eyes, key=lambda e: e[0]))
        reye = utils.getcenter(max(eyes, key=lambda e: e[0]))
        cropped = crop.face(frameobj.bitmap, leye, reye)

        raise Return(cropped)


if __name__ == '__main__':

    # Build context
    CASCADES_DIR = '/usr/share/opencv/haarcascades'
    context = Context(wname = 'Video',
        faceCascade=cv2.CascadeClassifier(
            os.path.join(CASCADES_DIR,'haarcascade_frontalface_default.xml')),
        eyeCascade=cv2.CascadeClassifier(
            os.path.join(CASCADES_DIR,'haarcascade_eye.xml')))

    # Initialize pipeline
    tasks = [asyncio.Task(webcam(context)),
             asyncio.Task(compose(context)),
             asyncio.Task(display(context))]

    # This will suspend the main routine until q is pressed
    loop = asyncio.get_event_loop()
    loop.run_until_complete(keyboard(context))

    for t in tasks:
        t.cancel()

    # Give tasks a chance to shut down gracefully
    loop.run_until_complete(asyncio.wait(tasks))
