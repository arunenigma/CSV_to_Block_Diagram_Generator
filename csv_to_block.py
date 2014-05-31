from graphviz import Digraph
import pygraphviz as pgv
from os import walk
import simplejson
import json
import csv


class CSVtoBlock(object):
    def __init__(self):
        """
        converts given data in csv format into a block diagram
        """
        self.knol = {}
        self.knol_ = {}
        self.data = []
        self.data_ = []

    def read_csv(self, directory, csv_file):
        path = directory + '/' + csv_file
        csv_f = open(path, 'rU')
        f = csv.reader(csv_f)
        for i, row in enumerate(f):
            row = row[0].split('\t')
            if i == 0:
                for j, heading in enumerate(row):
                    self.knol[str(j)+'_'+heading] = None
            else:
                self.data.append(row)

        l = len(self.data)
        cnt = 0
        while not cnt > l - 1:
            temp = []
            for row in self.data:
                temp.append(row[cnt])
            self.data_.append(temp)
            cnt += 1

        for k, v in self.knol.iteritems():
            for i, lst in enumerate(self.data_):
                if i == int(k[0]):
                    self.knol_[k[2:]] = lst
        print self.knol_

    def read_csv_dir(self):
        # read the csv files from dir "csv"
        for(directory, _, csv_files) in walk('./csv'):
            for csv_file in csv_files:
                self.read_csv(directory, csv_file)

    def construct_digraph(self):
        pass

    def find_correlation(self):
        pass

    

    @staticmethod
    def boo():
        dot = Digraph(comment='foo')
        dot.node('A', 'Apple')
        dot.node('B', 'Ball')
        dot.edges(['AB'])
        f = open('foo.dot', 'wb')
        f.write(dot.source)
        f.close()
        g = pgv.AGraph(file='sample.dot')
        g.layout(prog='dot')
        g.draw('foo.pdf')
        g.close()

if __name__ == '__main__':
    c = CSVtoBlock()
    c.boo()
    c.read_csv_dir()