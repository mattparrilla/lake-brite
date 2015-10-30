import csv
import numpy as np


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


def increase_dimensions(data=csv_to_matrix()[1:2]):
    """Changes a list of 1-D array into a array of 2-D array. The input array is
       48 items long (representing the longest axis of LakeBrite). The 2D array
       will be 15 array of 48 items, the 15 array representing vertical slices
       of LakeBrite."""

    max_temp = get_max_of_data(data)
    min_temp = get_min_of_data(data)

    all_years = []
    for year in data:
        year_frame = new_array()
        for reading_index, reading in enumerate(year):
            bin_number = -which_bin(reading, max_temp, min_temp)
            for i in range(bin_number, 0):
                year_frame[i][reading_index] = reading

        all_years.append(year_frame)

    return all_years

print increase_dimensions()
