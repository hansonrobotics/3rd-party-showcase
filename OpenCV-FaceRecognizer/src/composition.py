import numpy as np
import utils

def stack(imgs, height):
    # Sort images into groups
    groups = list(utils.split(imgs, utils.capacitor(height, lambda img: img.shape[0])))
    # Join images into columns
    columns = [vertically(*group) for group in groups]
    # Join columns into a stack
    return horizontally(*columns)

def horizontally(*imgs):
    """ Join images horizontally """
    heights = [img.shape[0] for img in imgs]
    widths = [img.shape[1] for img in imgs]
    vis = np.zeros((max(heights), sum(widths), 3), np.uint8)
    x, y = (0, 0)
    for img in imgs:
        h, w = img.shape[:2]
        vis[y:y+h, x:x+w] = img
        x += w
    return vis

def vertically(*imgs):
    """ Join images vertically """
    heights = [img.shape[0] for img in imgs]
    widths = [img.shape[1] for img in imgs]
    vis = np.zeros((sum(heights), max(widths), 3), np.uint8)
    x, y = (0, 0)
    for img in imgs:
        h, w = img.shape[:2]
        vis[y:y+h, x:x+w] = img
        y += h
    return vis
