from load_data import group_metric_data_by_month
from interpolation import generate_interpolated_array
from matrix_to_gif import generate_gif
from matplotlib import cm
from safe_path import safe_path
import numpy as np

YEARS = range(1995, 2015)
MONTHS = range(1, 13)

METRICS = [
    'Chloride',
    'Chlorophyll-a',
    'Secchi Depth',
    'Total Phosphorus',
    'Alkalinity',
    'Temperature',
    'Total Nitrogen',
    'Dissolved Oxygen'
]


def station_map():
    """A map of all station IDs to their coordinates on the low-res
       Lake Champlain image """

    return {
        51: {
            'location': [1, 9],
        },
        50: {
            'location': [2, 7],
        },
        40: {
            'location': [10, 8],
        },
        34: {
            'location': [14, 6],
        },
        46: {
            'location': [4, 4],
        },
        36: {
            'location': [11, 2],
        },
        33: {
            'location': [14, 0],
        },
        25: {
            'location': [17, 4],
        },
        19: {
            'location': [21, 3],
        },
        21: {
            'location': [21, 5],
        },
        16: {
            'location': [23, 6],
        },
        9: {
            'location': [30, 3],
        },
        7: {
            'location': [34, 0],
        },
        4: {
            'location': [40, 0],
        },
        2: {
            'location': [48, 0],
        }
    }


def tween(data, frames):
    """Linearly 'tween' the data by the passed in number of frames
       to smooth out the eventual animation"""

    # steps is one more than frames b/c 1 extra frame means 2 steps from prev
    # to next value
    steps = frames + 1
    tweened_data = []
    for i, layer in enumerate(data):
        if i != len(data) - 1:  # if not last row
            for step in range(steps):
                if step % steps == 0:
                    tweened_data.append(layer)
                    continue
                else:
                    tweened_slice = []
                    for j, row in enumerate(layer):
                        tweened_slice.append([])
                        for k, value in enumerate(row):
                            next_value = data[i + 1][j][k]
                            tweened_value = value + step * (
                                (next_value - value) / float(steps))
                            tweened_slice[j].append(tweened_value)
                    tweened_data.append(tweened_slice)

        else:
            tweened_data.append(layer)

    return tweened_data


def generate_lake_array(metric, clip_to_lake, tween_frames, remove_null_months=True):
    """Generate an array of raw Lake Champlain metric data, for creation of 2D
       and 3D GIFs.
       `tween_frames` - number of frames to tween between data points"""

    lake_data = group_metric_data_by_month(metric)

    arrays = []
    for year in YEARS:
        for month in MONTHS:
            station_data = station_map()
            if lake_data[year][month]:  # if month contains_data
                for station in lake_data[year][month]:
                    data = lake_data[year][month][station]
                    monthly_value = sum(data) / len(data)
                    station_data[station]['value'] = monthly_value
            else:
                if remove_null_months:
                    continue
                else:
                    # show 0 for whole lake for month
                    # 4 = random station, whole lake will be extrapolated
                    station_data[4]['value'] = 0
            arrays.append(station_data)

    interpolated_array = [generate_interpolated_array(raw_data, clip_to_lake, 0)
        for raw_data in arrays]

    if tween_frames:
        interpolated_array = tween(interpolated_array, tween_frames)

    return interpolated_array


def normalize_values(array, max_value, min_value):
    """Normalize values to 0 -> 1 with 0 as data minimum and 1 as data max"""

    data = array
    for i, x in enumerate(data):
        for j, y in enumerate(x):
            value = data[i][j]
            data[i][j] = value / max_value

    return data


def map_value_to_color(a, color_map):
    vfunc = np.vectorize(color_map, otypes=[object])

    arrays = []
    for array in a:
        mapped_list = vfunc(array).tolist()
        arrays.append(mapped_list)

    return arrays


def add_empty_frames(data, empty_frames=10):
    """Adds the specified number of empty frames to the Lake Brite GIF"""

    for i in range(0, empty_frames):
        data.append([[[0] * 3] * 50] * 150)

    return data


def which_bin(reading, maximum, minimum, bins=15):
    """Given a reading and a number of bins, determine which bin a value
       belongs to"""

    diff = maximum - minimum
    bin_width = diff / (bins - 1)
    value = reading - minimum
    if bin_width:
        bin_index = value / bin_width
    else:
        bin_index = 0

    return int(bin_index)


def new_array():
    array = []
    for i in range(15):
        array.append([])
        for j in range(50):
            array[i].append(np.nan)
    return array


def increase_dimensions(data, max_value, min_value, bins=15, color_by_bin=True):
    """Turns a 2D array into a 3D array. The value in the 2D matrix determines
       is used to populate the third dimension. If the data ranges from 0-10
       and a value of the 2D matrix is 5, it will look like this in the third
       dimension: [5, 5, 5, 5, 5, 0, 0, 0, 0, 0]
       The input is expected to be 10x50, the output is 10xbinsx50"""

    frames = []
    for row in data:
        lake_brite_frame = new_array()
        for reading_index, reading in enumerate(row):
            if not np.isnan(reading):
                bin_number = which_bin(reading, max_value, min_value, bins)
                for i in range(1, bin_number + 1):
                    try:
                        if color_by_bin:
                            lake_brite_frame[i][reading_index] = (
                                reading / bin_number) * i
                        else:  # color purely by value
                            lake_brite_frame[i][reading_index] = reading
                    except IndexError:
                        print reading

        frames.append(lake_brite_frame)

    return frames


def stack_frames(frames):
    """Take 3D matrix and flatten it into a 2D matrix by taking each row in
       the 3rd dimension and concatenating them in a 2D matrix"""

    flat_frames = []
    for frame in frames:
        # reversing here changes vertical orientation of slices
        flat_frames += list(frame)

    return flat_frames


def get_max_of_data(data):
    max_value = 0
    for i in data:
        for j in i:
            for k in j:
                if k > max_value:
                    max_value = k
    return max_value


def get_min_of_data(data):
    min_value = 10000
    for i in data:
        for j in i:
            for k in j:
                if k < min_value:
                    min_value = k
    return min_value


def generate_lake_brite_gif(metric, palette='winter_r', duration=0.125,
        clip_to_lake=True, tween_frames=1, empty_frames=0):
    """Generate 3D Lake GIF for consumption by LakeBrite"""

    print "Generating 3D Lake GIFs of %s" % metric

    a = generate_lake_array(metric, clip_to_lake, tween_frames)
    max_value = get_max_of_data(a)
    min_value = get_min_of_data(a)

    print "Rotating matrix"
    rotated = []
    for index, frame in enumerate(a):
        rotated.append(zip(*frame))

    print "Increasing dimensions"
    slices = [increase_dimensions(frame, max_value, min_value) for
        frame in rotated]

    print "Stackining frames"
    frames = [stack_frames(frame) for frame in slices]

    print "Normalizing values"
    normalized = [normalize_values(frame, max_value, min_value)
        for frame in frames]

    # TODO: this should live outside of `generate_lake_brite_gif()`
    # it lives here because I use `palette` from the arguments
    # and can't figure out how to bind it to `color_map` otherwise
    def color_map(x, palette=palette):
        """To be consumed by np.vectorize to transform nan values to black
        and provide the color map"""

        if np.isnan(x):
            return [0, 0, 0]
        elif x < 0:
            return list(cm.get_cmap(palette)(0, bytes=True)[:3])
        else:
            return list(cm.get_cmap(palette)(x, bytes=True)[:3])

    print "Mapping values to colors"
    a = map_value_to_color(normalized, color_map)

    print "Adding empty frames"
    with_empties = add_empty_frames(a, empty_frames)

    print "Converting to numpy array"
    arrays = [np.fliplr(np.asarray(with_empties[i], 'uint8'))
        for i, f in enumerate(with_empties)]

    print "Generating GIFs"
    path_to_gif = safe_path('gif/lake-animation')
    generate_gif(arrays, path_to_gif, duration)

    return '%s.gif' % path_to_gif

if __name__ == '__main__':
    generate_lake_brite_gif('Temperature')
