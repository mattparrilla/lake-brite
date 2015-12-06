from load_data import group_metric_data_by_month
from interpolation import generate_interpolated_array
from matrix_to_gif import generate_gif
from matplotlib import cm
from safe_path import safe_path
import numpy as np
from memory_profiler import profile

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


def generate_lake_array(metric, clip_to_lake, remove_null_months=True):
    """Generate an array of raw Lake Champlain metric data, for creation of 2D
       and 3D GIFs"""

    lake_data = group_metric_data_by_month(metric)

    arrays = []
    for year in YEARS:
        for month in MONTHS:
            station_data = station_map()
            if not lake_data[year][month]:  # if month contains no data
                if remove_null_months:
                    continue
                else:
                    # show 0 for whole lake for month
                    # 4 = random station, whole lake will be extrapolated
                    station_data[4]['value'] = 0
            else:
                for station in lake_data[year][month]:
                    data = lake_data[year][month][station]
                    monthly_value = sum(data) / len(data)
                    station_data[station]['value'] = monthly_value
            array = generate_interpolated_array(station_data, clip_to_lake)
            arrays.append(array.tolist())

    return arrays


# TODO: probably need min value as well, otherwise scaling from max to zero
def normalize_values(array, max_value):
    """Normalize values to 0 -> 1"""

    data = array
    for i, x in enumerate(data):
        for j, y in enumerate(x):
            value = data[i][j]
            if max_value:
                data[i][j] = value / max_value
            else:
                data[i][j] = value

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
        flat_frames += list(reversed(frame))

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


@profile
def generate_lake_brite_gif(metric, palette='jet', duration=0.125, clip_to_lake=True):
    """Generate 3D Lake GIF for consumption by LakeBrite"""

    print "Generating 3D Lake GIFs of %s" % metric

    a = generate_lake_array(metric, clip_to_lake)
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
    normalized = [normalize_values(frame, max_value) for frame in frames]

    # TODO: this should live outside of `generate_lake_brite_gif()`
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
    with_empties = add_empty_frames(a, 10)

    print "Converting to numpy array"
    arrays = [np.asarray(with_empties[i], 'uint8')
        for i, f in enumerate(with_empties)]

    print "Generating GIFs"
    path_to_gif = safe_path('gif/lake-animation')
    generate_gif(arrays, path_to_gif, duration)

    return '%s.gif' % path_to_gif

generate_lake_brite_gif('Temperature')
