from PIL import Image
import numpy as np


def find_current_boundary():
    """Finds all non-white pixels in the low-res image of lake champlain
    for use in an image clipper"""
    im = Image.open('champlain-low-res.png')

    lake_coords = []
    arr = np.array(im)
    for x, row in enumerate(arr):
        for z, item in enumerate(row):
            if not np.array_equal(item, np.array([255, 255, 255, 255])):
                lake_coords.append([x, z])

    return lake_coords


def clip_data_to_lake(image):
    """Clips a numpy array to the boundary of lake champlain, returning array
    with NaN when the coordinates are outside of the lake"""
    lake_boundary = find_current_boundary()
    arr = np.array(image)

    for x, row in enumerate(arr):
        for z, item in enumerate(row):
            if [x, z] not in lake_boundary:
                arr[x][z] = np.nan

    return arr
