import glob
import csv


def load_all_csvs(directory='data'):
    """Takes a directory and loads all CSVs in the directory into memory
       as an array of objects. The objects from the 'data' dir look like:
       {
         'Symbol': '',
         'Stratum': 'E',
         'VisitDate': '7/8/93',
         'Depth': 'COM',
         'Lab': 'VT',
         'StationID': '16',
         'Station': 'Shelburne Bay',
         'Result': '11.5',
         'Time': '1640',
         'Test': 'Chloride',
         'FieldID': '9341134'
       }
    """

    all_data = []
    for filename in glob.glob('%s/*.csv' % directory):
        with open(filename, 'rU') as fin:
            f = csv.DictReader(fin)
            data = [l for l in f]
            all_data += data

    return all_data


def print_all_values_of_field(field, data=load_all_csvs()):
    """Print all possible values of a given field"""

    possible_values = []
    for measurement in data:
        if measurement[field] not in possible_values:
            possible_values.append(measurement[field])
            print measurement[field]


def get_metric(metric, data=load_all_csvs()):
    """Consumes an array of objects and a desired metric and returns all
       readings for the given metric organized by station"""

    metric_data = {metric: {}}
    for measurement in data:
        if measurement['Test'] == metric:
            station = measurement['Station']
            reading = {key: measurement[key]
                for key in ['Depth', 'VisitDate', 'Result']}

            if station not in metric_data[metric]:
                metric_data[metric][station] = [reading]
            else:
                metric_data[metric][station].append(reading)

    return metric_data

print_all_values_of_field('Station')
