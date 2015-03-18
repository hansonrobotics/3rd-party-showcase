import cv2
import sys
import trollius as asyncio
from trollius import From, sleep
import logging

logging.basicConfig(level=logging.DEBUG)

class Context:
    def __init__(self, **kwargs):
        # Frame buffers
        self.webcam = None
        self.composed = None

        # Snapshots
        self.snaps = []

        # Configuration
        self.wname = kwargs['wname']
        self.faceCascade = kwargs['faceCascade']

        # CPU performance can be tuned with minSize and scaleFactor
        self.cascade_params = {'scaleFactor': 1.2,
                               'minNeighbors': 5,
                               'minSize': (100, 100),
                               'flags': cv2.cv.CV_HAAR_SCALE_IMAGE}


@asyncio.coroutine
def webcam(context):
    video_capture = cv2.VideoCapture(0)
    try:
        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()
            # Send the frame to context
            context.webcam = frame
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
        frame = context.webcam

        # Detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = context.faceCascade.detectMultiScale(gray, **context.cascade_params)

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

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
    while not cv2.waitKey(1) & 0xFF == ord('q'):
        yield From(sleep(0))


if __name__ == '__main__':

    # Build context
    cascPath = sys.argv[1]
    context = Context(wname = 'Video',
                      faceCascade=cv2.CascadeClassifier(cascPath))

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
