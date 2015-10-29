import glob
import csv
import arrow


def load_all_csvs(directory='data/long-term-lake-monitoring'):
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


def print_all_metrics(data=load_all_csvs()):
    """Print all possible values of a given field"""

    possible_values = []
    for measurement in data:
        metric = measurement['Test']
        if metric not in possible_values:
            possible_values.append(metric)
            print metric


def print_all_metrics_and_year(data=load_all_csvs()):
    """Print a dict of all metrics with the counts of reading by year"""

    possible_values = []
    readings_by_year = {}
    for measurement in data:
        metric = measurement['Test']
        year = arrow.get(measurement['VisitDate'], 'M/D/YY').year
        if metric not in possible_values:
            possible_values.append(metric)
            readings_by_year[metric] = {
                year: 1
            }
        else:
            if year in readings_by_year[metric]:
                readings_by_year[metric][year] += 1
            else:
                readings_by_year[metric][year] = 1
    print readings_by_year


def get_metric(metric, max_depth=3, data=load_all_csvs()):
    """Reads all lake monitoring data, picking out results by metric.
       Returns an array of measurement objects"""

    metric_data = []
    for measurement in data:
        if measurement['Test'] == metric:
            try:
                if measurement['Test'] == 'Secchi Depth' or (
                        measurement['Depth'] == 'COM' or
                        int(float(measurement['Depth'])) < max_depth):
                    reading = {
                        'Depth': measurement['Depth'],
                        'VisitDate': arrow.get(measurement['VisitDate'],
                            'M/D/YY').date(),
                        'Result': float(measurement['Result']),
                        'StationID': int(measurement['StationID']),
                    }
                    metric_data.append(reading)
            except ValueError:
                pass

    return metric_data


def get_date_sorted_metric(metric):
    """Return all measurements of a given metric sorted by date"""

    all_measurements = get_metric(metric)
    date_sorted = sorted(all_measurements, key=lambda r: r['VisitDate'])

    return date_sorted


def get_max_value(metric):
    """Get maximum value of dataset"""

    data = get_metric(metric)
    max_value = 0.
    for i in data:
        if float(i['Result']) > max_value:
            max_value = float(i['Result'])

    return max_value


def group_metric_data_by_month(metric):
    """Takes dataset by metric, groups measurements by year, then month,
       then station.
        {
            1992: {
                5: {
                    33: [10.5, 8.7],
                    34: [9.1],
                    36: [8.7],
                    7: [6.7, 9.2],
                }, ...
       """

    all_measurements = get_metric(metric)

    results = {}
    for reading in all_measurements:
        year = reading['VisitDate'].year
        month = reading['VisitDate'].month
        station = reading['StationID']
        value = reading['Result']

        if year not in results:
            results[year] = {}
            for i in range(13)[1:]:
                results[year][i] = {}

            results[year][month] = {
                station: [value]
            }
        elif month not in results[year]:
            results[year][month] = {
                station: [value]
            }
        elif station not in results[year][month]:
            results[year][month][station] = [value]
        else:
            results[year][month][station].append(value)

    return results
