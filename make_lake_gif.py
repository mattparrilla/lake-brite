from load_data import group_metric_data_by_month, get_max_value
from interpolation import generate_interpolated_array
from matrix_to_gif import generate_gif
from matplotlib import cm
import numpy as np

YEARS = range(1995, 2015)
MONTHS = range(5, 10)

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


def map_values_to_colors(x):
    """To be consumed by np.vectorize to transform nan values to black
       and provide the color map"""
    if np.isnan(x):
        return [0, 0, 0]
    elif x < 0:
        return list(cm.hot(0, bytes=True)[:3])
    else:
        return list(cm.hot(x, bytes=True)[:3])

max_value = 0
min_value = 10000


def generate_lake_array(metric):
    """Generate an array of raw Lake Champlain metric data, for creation of 2D
       and 3D GIFs"""

    lake_data = group_metric_data_by_month(metric)

    arrays = []
    for year in YEARS:
        for month in MONTHS:
            station_data = station_map()
            if not lake_data[year][month]:  # if month contains no data
                station_data[4]['value'] = 0  # show 0 for whole lake for month
            else:
                for station in lake_data[year][month]:
                    data = lake_data[year][month][station]
                    monthly_value = sum(data) / len(data)
                    station_data[station]['value'] = monthly_value
            array = generate_interpolated_array(station_data)
            arrays.append(array.tolist())

    return arrays


# TODO: probably need min value as well, otherwise scaling from max to zero
def normalize_values(array, max_value):
    """Normalize values to 0 -> 1"""

    data = array
    for i, x in enumerate(data):
        for j, y in enumerate(x):
            for k, z in enumerate(y):
                value = data[i][j][k]
                if max_value:
                    data[i][j][k] = value / max_value
                else:
                    data[i][j][k] = value

    return data


def map_value_to_color(a):
    vfunc = np.vectorize(map_values_to_colors, otypes=[object])

    arrays = []
    for array in a:
        mapped_list = vfunc(array).tolist()
        arrays.append(mapped_list)

    return arrays


def generate_lake_gif(metric):
    """Generate a GIF of Lake Champlain, displaying how a metric has changed
       over the course of the long term lake monitoring program"""

    max_value = get_max_value(metric)

    data = generate_lake_array(metric)
    normalized = normalize_values(data, max_value)
    a = map_value_to_color(normalized)
    arrays = [np.asarray(a[i], 'uint8') for i, f in enumerate(a)]
    generate_gif(arrays, '2D-lake/%s' % metric.replace(' ', '-').lower())


def generate_lake_gifs(metrics=METRICS):
    """Generate 2D Lake GIFs for defined metrics"""

    for metric in metrics:
        print "Starting to generate: %s" % metric
        generate_lake_gif(metric)


def which_bin(reading, maximum=max_value, minimum=min_value, bins=15):
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


def increase_dimensions(data, max_value, min_value):
    """Changes a list of 1-D array into a array of 2-D array. The input array is
       48 items long (representing the longest axis of LakeBrite). The 2D array
       will be 15 array of 48 items, the 15 array representing vertical slices
       of LakeBrite."""

    frames = []
    for row in data:
        lake_brite_frame = new_array()
        for reading_index, reading in enumerate(row):
            if not np.isnan(reading):
                bin_number = -which_bin(reading, max_value, min_value)
                for i in range(bin_number, 0):
                    try:
                        lake_brite_frame[i][reading_index] = reading
                    except IndexError:
                        reading

        frames.append(lake_brite_frame)

    return frames


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


# TODO: Each frame is only 1D, it needs to be 2D, colored appropriately
# and its height should reflect its metric value

# TODO: rotate arrays for lake brite
def generate_lake_brite_gifs(metric):
    """Generate 3D Lake GIFs for consumption by LakeBrite"""

    a = generate_lake_array(metric)
    max_value = get_max_of_data(a)
    min_value = get_min_of_data(a)

    rotated = []
    for index, frame in enumerate(a):
        rotated.append(zip(*frame))

    lake_brite_frames = [increase_dimensions(frame, max_value, min_value) for
        frame in rotated]

    normalized = [normalize_values(frame, max_value) for frame in lake_brite_frames]
    a = map_value_to_color(normalized)
    arrays = [np.asarray(a[i], 'uint8') for i, f in enumerate(a)]
    for index, array in enumerate(arrays):
        generate_gif(array, '3D-lake/%05d%s' % (
            index, metric.replace(' ', '-').lower()))

generate_lake_brite_gifs('Temperature')
# generate_lake_gif('Temperature')
