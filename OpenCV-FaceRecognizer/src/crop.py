#Copyright (c) 2013-2018 Hanson Robotics, Ltd.
import math
import cv2

def face(image, eye_left, eye_right, eye_offset=(0.25, 0.25), dest_sz=(70, 70)):
    # get the direction
    eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
    # calc rotation angle in radians
    rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))
    # calculate scale
    eye_dist = _distance(eye_left, eye_right)
    new_eye_dist = (1-eye_offset[0]*2)*dest_sz[0]
    scale = new_eye_dist/eye_dist
    # rotate original
    image = cv2.warpAffine(
        image,
        cv2.getRotationMatrix2D(eye_left, -math.degrees(rotation), 1.0),
        image.shape[:2]
    )
    # crop the rotated image
    x,y,w,h = (int(eye_left[0]-eye_offset[0]*dest_sz[0]/scale),
               int(eye_left[1]-eye_offset[1]*dest_sz[1]/scale),
               int(dest_sz[0]/scale),
               int(dest_sz[1]/scale))
    image = image[y:y+h, x:x+w]
    # resize it
    image = cv2.resize(image, dest_sz)
    return image

def _distance(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.sqrt(dx*dx+dy*dy)
