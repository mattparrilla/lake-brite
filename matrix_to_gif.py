from PIL import Image
from numpy import asarray
from libs.images2gif import writeGif
import colorsys


def hsl_to_rgb(h, s, l):
    """Convert H, L, S color space to R, G, B"""
    normalized_color = colorsys.hls_to_rgb(h / 360.0, l / 100.0, s / 100.0)
    return tuple([int(i * 255) for i in normalized_color])


def generate_sample_matrix(n, x=50, y=15, z=10):
    """Build a 3D matrix of given dimensions"""
    matrix = []
    for i in range(0, z):
        matrix.append([])
        for j in range(0, y):
            matrix[i].append([])
            for k in range(0, x):
                if n > k and n > j * 3 and n > i * 5:
                    matrix[i][j].append(hsl_to_rgb(100 + n * 3, 100, 30 + k))
                else:
                    matrix[i][j].append((0, 0, 0))

    return matrix


def generate_pil_images(matrix):
    """Generate an array of PIL images from a matrix"""
    return [Image.fromarray(asarray(matrix[i], 'uint8'))
        for i, f in enumerate(matrix)]


def generate_gif(images, name, directory='gif', duration=.5):
    """Creates a gif from a list of PIL images"""

    gif_name = "%s/%s.gif" % (directory, name)
    writeGif(gif_name, images, duration)
    return gif_name


def normal_gif_to_lake_brite(normal_gif, directory='gif/regular-image'):
    """Take a normal, animated GIF and allow it to display on lake brite"""

    def iter_frames(gif):
        """Frame generator"""
        im = Image.open(gif)
        try:
            i = 0
            while 1:
                im.seek(i)
                imframe = im.copy()
                if i == 0:
                    palette = imframe.getpalette()
                else:
                    imframe.putpalette(palette)
                yield imframe
                i += 1
        except EOFError:
            pass

    frames = []
    for i, frame in enumerate(iter_frames(normal_gif)):
        result = Image.new('RGB', (50, 150))
        for i in range(0, 10):
            img = frame.copy()
            img.thumbnail((400, 400), Image.ANTIALIAS)
            x = 0
            y = i * 15
            w, h = img.size
            print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
            result.paste(img, (x, y, x + w, y + h))
        frames.append(result)
    generate_gif(frames, 'regular-image/test')


# matrix = generate_sample_matrix(1)
# # images = generate_pil_images(matrix)
# arrays = [asarray(matrix[i], 'uint8') for i, f in enumerate(matrix)]
# # print arrays
# gif = generate_gif(arrays, 'array4')
# gif = generate_gif(images, 'test2')

# for step in range(1, 51):
#     matrix = generate_sample_matrix(step)
#     arrays = [asarray(matrix[i], 'uint8') for i, f in enumerate(matrix)]
#     gif = generate_gif(arrays, '%03d_pulse' % step)

normal_gif_to_lake_brite('brook-trout.gif')
