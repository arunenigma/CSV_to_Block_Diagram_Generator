import csv


class ReadCSV(object):
    def __init__(self):
        pass

    @staticmethod
    def read_csv(directory, csv_name):
        path = directory + '/' + csv_name
        csv_f = open(path, 'rU')
        csv_obj = csv.reader(csv_f)
        return csv_name.split('.')[0], csv_obj