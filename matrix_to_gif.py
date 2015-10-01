from PIL import Image
from numpy import asarray
from libs.images2gif import writeGif

SAVE_TO_DIR = 'gif'


def generate_sample_matrix(x=50, y=15, z=10):
    """Build a 3D matrix of given dimensions"""
    matrix = []
    for i in range(0, 10):
        matrix.append([])
        for j in range(0, 15):
            matrix[i].append([])
            for k in range(0, 50):
                if i == j:
                    matrix[i][j].append((k * 5, 0, 0))
                else:
                    matrix[i][j].append((0, 0, 0))

    return matrix


def generate_pil_images(matrix):
    """Generate an array of PIL images from a matrix"""
    return [Image.fromarray(asarray(matrix[i], 'uint8'))
        for i, f in enumerate(matrix)]


def generate_gif(images, name, directory=SAVE_TO_DIR, duration=0.125):
    """Creates a gif from a list of PIL images"""

    gif_name = "%s/%s.gif" % (directory, name)
    writeGif(gif_name, images, duration)
    return gif_name

matrix = generate_sample_matrix()
images = generate_pil_images(matrix)
arrays = [asarray(matrix[i], 'uint8') for i, f in enumerate(matrix)]
gif = generate_gif(arrays, 'array2')
gif = generate_gif(images, 'test2')


# next step: get RGB out of matrix (unless passing image, apply color map)
