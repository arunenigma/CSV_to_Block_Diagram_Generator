import csv


class ReadCSV(object):
    def __init__(self):
        self.knol = {}
        self.knol_ = {}  # dictionary of columns of csv
        self.data = []
        self.data_ = []
        self.dot = None
        self.knol_all = {}  # dict of dicts of knol

    @staticmethod
    def read_csv(directory, csv_name):
        path = directory + '/' + csv_name
        csv_f = open(path, 'rU')
        csv_obj = csv.reader(csv_f)
        return csv_name.split('.')[0], csv_obj

    def read_csv_contents(self, directory, csv_name):
        self.data = []
        self.data_ = []
        self.knol = {}
        self.knol_ = {}
        path = directory + '/' + csv_name
        csv_f = open(path, 'rU')
        f = csv.reader(csv_f)
        for i, row in enumerate(f):

            if i == 0:
                for j, heading in enumerate(row):
                    self.knol[str(j) + '_' + heading] = None
            else:
                self.data.append(row)

        cols = len(self.data[0])
        cnt = 0

        while not cnt > cols - 1:
            temp = []
            for row in self.data:
                temp.append(row[cnt])
            self.data_.append(temp)
            cnt += 1

        for k, v in self.knol.iteritems():
            for i, lst in enumerate(self.data_):
                if i == int(k[0]):
                    self.knol_[k[2:]] = lst
        self.knol_all[csv_name] = self.knol_