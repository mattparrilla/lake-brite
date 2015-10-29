from load_data import group_metric_data_by_month, get_max_value
from interpolation import generate_interpolated_array
from matrix_to_gif import generate_gif
from matplotlib import cm
import numpy as np


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
        return list(cm.jet(0, bytes=True)[:3])
    else:
        return list(cm.jet(x, bytes=True)[:3])


def generate_lake_gif(metric):
    """Generate a GIF of Lake Champlain, displaying how a metric has changed
       over the course of the long term lake monitoring program"""

    lake_data = group_metric_data_by_month(metric)

    vfunc = np.vectorize(map_values_to_colors, otypes=[object])
    max_value = get_max_value(metric)

    arrays = []
    for year in lake_data:
        for month in lake_data[year]:
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
