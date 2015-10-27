from load_data import get_date_sorted_metric, get_max_value
from interpolation import generate_interpolated_array
from matrix_to_gif import generate_gif
from matplotlib import cm
import numpy as np

sample_data = get_date_sorted_metric('Temperature')

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
    if np.isnan(x):
        return [0, 0, 0]
    elif x < 0:
        return list(cm.winter(0, bytes=True)[:3])
    else:
        return list(cm.winter(x, bytes=True)[:3])

vfunc = np.vectorize(map_values_to_colors, otypes=[object])

max_value = get_max_value(sample_data[:100])
arrays = []
for data in sample_data[:100]:
    station_data[data['StationID']]['value'] = data['Result'] / max_value
    array = generate_interpolated_array(station_data)
    mapped_array = vfunc(array).tolist()
    arrays.append(np.asarray(mapped_array, 'uint8'))

generate_gif(arrays, 'lake-temp')
