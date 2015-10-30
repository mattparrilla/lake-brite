from load_data import group_metric_data_by_month, get_max_value
from interpolation import generate_interpolated_array
from matrix_to_gif import generate_gif
from matplotlib import cm
import numpy as np

metrics = [
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
        return list(cm.winter(0, bytes=True)[:3])
    else:
        return list(cm.winter(x, bytes=True)[:3])


def generate_lake_array(metric):
    """Generate an array of Lake Champlain metric data, for creation of 2D
       and 3D GIFs"""

    lake_data = group_metric_data_by_month(metric)

    vfunc = np.vectorize(map_values_to_colors, otypes=[object])
    max_value = get_max_value(metric)

    arrays = []
    for year in range(1995, 2015):
        for month in range(1, 13):
            station_data = station_map()
            if not lake_data[year][month]:  # if month contains no data
                station_data[4]['value'] = 0  # show 0 for whole lake for month
            else:
                for station in lake_data[year][month]:
                    data = lake_data[year][month][station]
                    monthly_value = sum(data) / len(data)
                    station_data[station]['value'] = monthly_value / max_value
            array = generate_interpolated_array(station_data)
            mapped_list = vfunc(array).tolist()  # BAD: array -> list -> array
            arrays.append(mapped_list)

    return arrays


def generate_lake_gif(metric):
    """Generate a GIF of Lake Champlain, displaying how a metric has changed
       over the course of the long term lake monitoring program"""

    a = generate_lake_array(metric)
    arrays = [np.asarray(a[i], 'uint8') for i, f in enumerate(a)]
    generate_gif(arrays, '2D-lake/%s' % metric.replace(' ', '-').lower())


def generate_lake_gifs(metrics=metrics):
    """Generate 2D Lake GIFs for defined metrics"""

    for metric in metrics:
        print "Starting to generate: %s" % metric
        generate_lake_gif(metric)


# TODO: Each frame is only 1D, it needs to be 2D, colored appropriately
# and its height should reflect its metric value

# TODO: rotate arrays for lake brite
def generate_lake_brite_gifs(metric):
    """Generate 3D Lake GIFs for consumption by LakeBrite"""

    a = generate_lake_array(metric)

    for index, frame in enumerate(a):
        arrays = [np.asarray(frame[i], 'uint8')
            for i, f in enumerate(frame)]

        generate_gif(arrays, '3D-lake/%03d_%s' % (index,
            metric.replace(' ', '-').lower()))

generate_lake_brite_gifs('Temperature')
