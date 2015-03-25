import sys, os, shutil
import pexpect
from time import sleep

def captureface(filename):
    # Capture face data from camera
    while True:
        child = pexpect.spawnu('./EnrollFaceFromCamera {0}.jpg {0}.template'.format(filename))
        child.logfile = sys.stderr

        # Try again if the app failed because of BadExposure or BadSharpness
        if child.expect(["template saved successfully",
                         "template extraction failed!biometric status: \w+"] , timeout=None) == 0:
            break


def identify(probename, directory):
    gallery = [f for f in os.listdir(directory) if os.path.splitext(f)[1] == '.template']
    gallery_relative = [os.path.join(directory, file) for file in gallery]
    if len(gallery) == 0:
        return []

    # Spawn VeriLook's 'Identify'.
    child = pexpect.spawnu('./Identify {0}.template {1}'.format(
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
    shutil.copyfile(filename + '.template', os.path.join(directory, name + '.template'))
    shutil.copyfile(filename + '.jpg', os.path.join(directory, name + '.jpg'))

TEMPORARY_FILE = 'last'
TEMPLATE_DIR = 'templates'

if __name__ == '__main__':
    while True:
        captureface(TEMPORARY_FILE)
        results = identify(TEMPORARY_FILE, TEMPLATE_DIR)
        print(results, file=sys.stderr)

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
