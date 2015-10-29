from load_data import get_date_sorted_metric, get_max_value
from interpolation import generate_interpolated_array
from matrix_to_gif import generate_gif
from matplotlib import cm
import numpy as np

# A map of all station IDs to their coordinates on the low-res Lake Champlain
# image
station_data = {
    51: {
        'value': 0,
        'location': [1, 9],
    },
    50: {
        'value': 0,
        'location': [2, 7],
    },
    40: {
        'value': 0,
        'location': [10, 8],
    },
    34: {
        'value': 0,
        'location': [14, 6],
    },
    46: {
        'value': 0,
        'location': [4, 4],
    },
    36: {
        'value': 0,
        'location': [11, 2],
    },
    33: {
        'value': 0,
        'location': [14, 0],
    },
    25: {
        'value': 0,
        'location': [17, 4],
    },
    19: {
        'value': 0,
        'location': [21, 3],
    },
    21: {
        'value': 0,
        'location': [21, 5],
    },
    16: {
        'value': 0,
        'location': [23, 6],
    },
    9: {
        'value': 0,
        'location': [30, 3],
    },
    7: {
        'value': 0,
        'location': [34, 0],
    },
    4: {
        'value': 0,
        'location': [40, 0],
    },
    2: {
        'value': 0,
        'location': [48, 0],
    }
}


def map_values_to_colors(x):
    """To be consumed by np.vectorize to transform nan values to black
       and provide the color map"""
    if np.isnan(x):
        return [0, 0, 0]
    elif x < 0:
        return list(cm.jet(0, bytes=True)[:3])
    else:
        return list(cm.jet(x, bytes=True)[:3])


def generate_lake_gif(metric):
    """Generate a GIF of Lake Champlain, displaying how a metric has changed
       over the course of the long term lake monitoring program"""

    lake_data = get_date_sorted_metric(metric)

    vfunc = np.vectorize(map_values_to_colors, otypes=[object])
    max_value = get_max_value(lake_data)

    arrays = []
    for data in lake_data:
        station_data[data['StationID']]['value'] = data['Result'] / max_value
        array = generate_interpolated_array(station_data)
        mapped_list = vfunc(array).tolist()  # BAD: array -> list -> array
        arrays.append(np.asarray(mapped_list, 'uint8'))

    return generate_gif(arrays, metric.replace(' ', '-').lower())

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

for metric in metrics:
    print "Starting to generate: %s" % metric
    generate_lake_gif(metric)
