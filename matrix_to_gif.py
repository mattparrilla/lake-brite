from PIL import Image
from numpy import asarray
from libs.images2gif import writeGif
import colorsys

SAVE_TO_DIR = 'gif'


def hsl_to_rgb(h, s, l):
    """Convert H, L, S color space to R, G, B"""
    normalized_color = colorsys.hls_to_rgb(h / 360.0, l / 100.0, s / 100.0)
    return tuple([int(i * 255) for i in normalized_color])


def generate_sample_matrix(n, x=50, y=15, z=10):
    """Build a 3D matrix of given dimensions"""
    matrix = []
    for i in range(0, 10):
        matrix.append([])
        for j in range(0, 15):
            matrix[i].append([])
            for k in range(0, 50):
                matrix[i][j].append(hsl_to_rgb((i * j) * n, 100, 30 + k))

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

# matrix = generate_sample_matrix()
# images = generate_pil_images(matrix)
# arrays = [asarray(matrix[i], 'uint8') for i, f in enumerate(matrix)]
# gif = generate_gif(arrays, 'array2')
# gif = generate_gif(images, 'test2')

for step in range(1, 11):
    matrix = generate_sample_matrix(step)
    arrays = [asarray(matrix[i], 'uint8') for i, f in enumerate(matrix)]
    gif = generate_gif(arrays, 'array-%d' % step)
