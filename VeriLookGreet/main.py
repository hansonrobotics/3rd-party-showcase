#Copyright (c) 2013-2018 Hanson Robotics, Ltd.
import sys, os, shutil
import pexpect
from time import sleep

BIN_DIR = 'build/bin'
DATA_DIR = 'data'

class VisionException(Exception):
    pass

def captureface(filename):
    # Capture face data from camera
    child = pexpect.spawnu('{0} {1}.jpg {1}.template'.format(
        os.path.join(BIN_DIR, 'EnrollFaceFromCamera'),
        filename
    ))
    child.logfile = sys.stderr
    i = child.expect(["template saved successfully",
                      "template extraction failed!biometric status: (\w+)"], timeout=None)

    # Raise exception on failure
    if i > 0:
        # This status may be either BadExposure or BadSharpness
        status = child.match.groups()[0]
        raise VisionException(status)


def identify(probename, directory):
    try:
        gallery = [f for f in os.listdir(directory) if os.path.splitext(f)[1] == '.template']
        gallery_relative = [os.path.join(directory, file) for file in gallery]
        if len(gallery) == 0:
            raise FileNotFoundError
    except FileNotFoundError:
        # In case of an unexistant or empty template directory.
        return []

    # Spawn VeriLook's 'Identify'.
    child = pexpect.spawnu('{0} {1}.template {2}'.format(
        os.path.join(BIN_DIR, 'Identify'),
        probename,
        ' '.join(gallery_relative)
    ))
    child.logfile = sys.stderr

    # Parse output
    results = []
    while True:
        i = child.expect(["matched with ID 'GallerySubject_([0-9]+)' with score '([0-9]+)'", pexpect.EOF])
        if i == 0:
            results.append(child.match.groups())
        else:
            break
    results = [{'id': int(j), 'score': score, 'file': gallery[int(j)-1]} for j, score in results]
    return results

def enroll(filename, directory, name):
    os.makedirs(directory, exist_ok=True)
    shutil.copyfile(filename + '.template', os.path.join(directory, name + '.template'))
    shutil.copyfile(filename + '.jpg', os.path.join(directory, name + '.jpg'))

TEMPORARY_FILE = os.path.join(DATA_DIR, 'last')
TEMPLATE_DIR = os.path.join(DATA_DIR, 'templates')

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    while True:
        # Try and capture face from webcam.
        try:
            captureface(TEMPORARY_FILE)
        except VisionException as e:
            print("Can't see. {0}.".format(e))
            continue

        # Try and match among the existing saved faces.
        results = identify(TEMPORARY_FILE, TEMPLATE_DIR)
        print('Identified {0}'.format(results), file=sys.stderr)

        # Print the results or ask for a name.
        if len(results) == 0:
            print("I don't know you. What's your name?", end=' ')
            name = input()
            enroll(TEMPORARY_FILE, TEMPLATE_DIR, name)
        elif len(results) == 1:
            name = os.path.splitext(results[0]['file'])[0]
            print('Hi {0}!'.format(name))
        else:
            names = [os.path.splitext(match['file'])[0] for match in
                     sorted(results, key=lambda x: x['score'], reverse=True)]
            print('Hi {0}! You look like {1}.'.format(names[0], ', '.join(names[1:])))
