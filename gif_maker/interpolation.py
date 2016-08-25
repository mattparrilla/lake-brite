import numpy as np
import scipy.interpolate as inter
from lake_clip import clip_data_to_lake
import matplotlib.pyplot as plt


def show_station_data(station_data):
    """Takes an array of station data objects and generates an image of the
       array
       Doesn't return anything, just called for side effect"""

    stations = np.empty((50, 10))
    stations[:] = np.NAN
    for station in station_data:
        data = station_data[station]
        if 'value' in data:
            stations[data['location'][0],
                data['location'][1]] = data['value']

    plt.matshow(stations, cmap=plt.cm.winter)
    plt.show()


def interpolate_stations(station_data, interpolation_method, print_img=False):
    """Given lake station data, interpolates values based on 2D array
       and the interpolation method.
       Returns the 2D array"""

    vals = []
    points = []
    for station in station_data:
        if 'value' in station_data[station]:
            vals.append(station_data[station]['value'])
            points.append(station_data[station]['location'])
    values = np.asarray(vals)
    grid_x, grid_y = np.mgrid[0:49:50j, 0:9:10j]
    grid_z = inter.griddata(points, values, (grid_x, grid_y),
        method=interpolation_method)

    if print_img:
        plt.matshow(grid_z, cmap=plt.cm.winter)
        plt.show()

    return grid_z


def remove_non_edges(neighbor_data, print_img=False):
    """Replaces all data in array with nan except for edge nodes
       Returns 2D array of same size."""

    new_array = np.empty((50, 10))
    new_array[:] = np.NAN
    new_array[0] = neighbor_data[0]                # first row
    new_array[-1] = neighbor_data[-1]              # last row
    new_array[:, 0] = neighbor_data[:, 0]          # first column
    new_array[:, -1] = neighbor_data[:, -1]        # last column

    if print_img:
        plt.matshow(new_array, cmap=plt.cm.winter)
        plt.show()

    return new_array


def interpolate_nans(station_array, print_img=False):
    """Takes a 2D array of station data and edge values (calculated from
       nearest neighbor) for interpolation.
       Returns an interpolated 2D array"""

    interpolated_array = np.copy(station_array)
    nans = np.isnan(interpolated_array)
    notnans = np.logical_not(nans)
    grid_x, grid_y = np.mgrid[0:49:50j, 0:9:10j]

    interpolated_array[nans] = inter.griddata((grid_x[notnans], grid_y[notnans]),
        interpolated_array[notnans], (grid_x[nans], grid_y[nans]), method='cubic')

    if print_img:
        plt.matshow(interpolated_array, cmap=plt.cm.winter)
        # plt.colorbar()
        plt.show()

    return interpolated_array


def combine_arrays(base_array, secondary_array, print_img=False):
    """Takes a base array and pastes the secondary array on top of it, only
       where the base array doesn't have values.
       Returns combined 2D array"""

    for i in range(len(base_array)):
        for j in range(len(base_array[0])):
            if np.isnan(base_array[i][j]) and not np.isnan(secondary_array[i][j]):
                base_array[i][j] = secondary_array[i][j]

    if print_img:
        plt.matshow(base_array, cmap=plt.cm.winter)
        plt.show()

    return base_array


def generate_interpolated_array(data, clip_to_lake, tween_frames, print_img=True):
    """Takes station data and a 50x10 matrix and returns nicely interpolated
    results in the shape of Lake Champlain"""

    if print_img:
        show_station_data(data)

    nearest_neighbor = interpolate_stations(data, 'nearest', print_img)
    just_edges = remove_non_edges(nearest_neighbor, print_img)
    cubic_interpolated_stations = interpolate_stations(data, 'cubic', print_img)
    stations_and_edges = combine_arrays(cubic_interpolated_stations,
        just_edges, print_img)
    interpolated = interpolate_nans(stations_and_edges, print_img)

    if clip_to_lake:
        lake_data = clip_data_to_lake(interpolated)

        if print_img:
            plt.matshow(lake_data, cmap=plt.cm.winter)
            # plt.colorbar()
            plt.show()

        return lake_data

    else:
        return interpolated
