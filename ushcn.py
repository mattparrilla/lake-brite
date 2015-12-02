import csv
import numpy as np
from matrix_to_gif import generate_gif
from make_lake_gif import stack_frames


def csv_to_matrix(csv_filename='data/ushcn/btv_max_temp.csv'):
    """Transform USHCN daily data into an array of year arrays"""

    with open(csv_filename, 'rU') as csv_f:
        f = csv.reader(csv_f)
        values = [l for l in f][2:]  # First two lines are headers, not data

    years = range(1940, 2015)
    months = range(1, 13)
    day_ranges = ['a', 'b', 'c', 'd']

    # create data structure
    d = {}
    for year in years:
        d[year] = {}
        for month in months:
            d[year][month] = {}
            for day_range in day_ranges:
                d[year][month][day_range] = []

    # populate data object with readings
    for value in values:
        day = int(value[0])
        month = int(value[2])
        year = int(value[4])
        try:
            reading = int(value[5])
        except ValueError:
            # don't add item to list if invalid value
            continue

        if day <= 8:
            day_range = 'a'
        elif day <= 16:
            day_range = 'b'
        elif day <= 24:
            day_range = 'c'
        else:
            day_range = 'd'

        d[year][month][day_range].append(reading)

    # convert list of readings into average for day_range
    for year in d:
        for month in d[year]:
            for day_range in d[year][month]:
                value_list = d[year][month][day_range]
                if value_list:
                    value = sum(value_list) / len(value_list)
                else:
                    value = np.nan

                d[year][month][day_range] = value

    # create array of year arrays, looping again even though inefficient b/c easier to test
    array_of_years = []
    for year in years:
        current_year = []
        for month in months:
            for day_range in day_ranges:
                current_year.append(d[year][month][day_range])
        array_of_years.append(current_year)

    return array_of_years


def get_max_of_data(data):
    max_value = 0
    for year in data:
        for value in year:
            if value > max_value:
                max_value = value
    return max_value


def get_min_of_data(data):
    min_value = 100
    for year in data:
        for value in year:
            if isinstance(value, int) and value < min_value:
                min_value = value
    return min_value


def which_bin(reading, maximum, minimum, bins=15):
    """Given a reading and a number of bins, determine which bin a value
       belongs to"""

    diff = maximum - minimum
    bin_width = diff / (bins - 1)
    value = reading - minimum
    bin_index = value / bin_width

    return bin_index


def new_array():
    array = []
    for i in range(15):
        array.append([])
        for j in range(50):
            array[i].append(np.nan)
    return array


# TODO: consider rotating array here
def increase_dimensions(data, max_temp, min_temp):
    """Changes a list of 1-D array into a array of 2-D array. The input array is
       48 items long (representing the longest axis of LakeBrite). The 2D array
       will be 15 array of 48 items, the 15 array representing vertical slices
       of LakeBrite."""

    all_years = []
    for year in data:
        year_frame = new_array()
        for reading_index, reading in enumerate(year):
            if not np.isnan(reading):
                bin_number = -which_bin(reading, max_temp, min_temp)
                for i in range(bin_number, 0):
                    try:
                        year_frame[i][reading_index] = reading
                    except IndexError:
                        reading

        all_years.append(year_frame)

    return all_years


def assign_colors(data, max_temp, min_temp):
    """Convert temperature values to RGB colors"""

    for i, year in enumerate(data):
        for j, row in enumerate(year):
            for k, item in enumerate(row):
                data[i][j][k] = color_map(item, max_temp, min_temp)

    return data


def make_frames(data, slices=10):
    """Take an array of data of indeterminate length and group into groups of
       10"""

    all_frames = []
    for i in range(len(data) - slices):
        frame = data[i:i + 10]
        all_frames.append(frame)
    return all_frames


def assign_colors_2d(data, max_temp, min_temp):
    """Convert 2D array of temperature values to RGB colors"""

    for i, year in enumerate(data):
        for j, item in enumerate(year):
            data[i][j] = color_map(item, max_temp, min_temp)

    return data


def add_empty_slices(data, empty_slices=10):
    """Adds the specified number of empty slices to the Lake Brite GIF"""

    print len(data)
    # print data[0]
    print len(data[0])
    print len(data[0][0])
    for i in range(0, empty_slices):
        data.append([[(0,) * 3] * 50] * 15)

    # print data[-1]
    print len(data[-1])
    print len(data[-1][0])
    print len(data)

    return data


def color_map(value, max_temp, min_temp):
    """Take a reading and map it to a color"""

    if np.isnan(value):
        return (125, 100, 100)
    elif value > 32:
        return (255 - 2 * (max_temp - value), 0, max_temp - value)
    elif value <= 32:
        return (0, 0, 255 - 4 * (value - min_temp))
    else:
        return (0, 0, 0)


def make_three_d_gifs():
    """Turn temperature dataset into 3d GIFs for LakeBrite"""
    data = csv_to_matrix()
    max_temp = get_max_of_data(data)
    min_temp = get_min_of_data(data)

    three_d_data = increase_dimensions(data, max_temp, min_temp)
    colored_data = assign_colors(three_d_data, max_temp, min_temp)
    length = len(colored_data)
    arrays = []
    for index, frame in enumerate(colored_data):
        if index < length - 10:
            single_frame = colored_data[index:index + 10]
            frame = stack_frames(single_frame)
            arrays.append(np.asarray(frame))

    generate_gif(arrays, 'temperature/lake')


def make_temp_gif():
    """A single GIF of the entire temperature dataset"""
    data = csv_to_matrix()
    max_temp = get_max_of_data(data)
    min_temp = get_min_of_data(data)

    three_d_data = increase_dimensions(data, max_temp, min_temp)
    colored_data = assign_colors(three_d_data, max_temp, min_temp)
    arrays = [np.asarray(colored_data[i], 'uint8')
        for i, f in enumerate(colored_data)]
    generate_gif(arrays, 'temp')


def make_lake_brite_gif():
    """A single GIF, "10 slices" tall that contains the USHCN temperature
       visualization for consumption by Lake Brite"""

    print "Making USHCN GIF"
    data = csv_to_matrix()
    max_temp = get_max_of_data(data)
    min_temp = get_min_of_data(data)

    three_d_data = increase_dimensions(data, max_temp, min_temp)
    colored_data = assign_colors(three_d_data, max_temp, min_temp)
    add_empties = add_empty_slices(colored_data)
    frames = make_frames(add_empties)

    arrays = np.asarray(frames, 'uint8')

    generate_gif(arrays, 'ushcn/temperature')
