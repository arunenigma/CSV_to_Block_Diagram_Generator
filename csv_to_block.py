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
        self.dot = None

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
        self.construct_digraph(csv_file)

    def read_csv_dir(self):
        # read the csv files from dir "csv"
        for(directory, _, csv_files) in walk('./csv'):
            for csv_file in csv_files:
                self.read_csv(directory, csv_file)

    def construct_digraph(self, f_name):
        """
        MAIN block
        """
        main_block = f_name.split('.')[0].upper()
        self.dot = Digraph(comment=main_block)
        self.dot.node('main', main_block, shape='box', fontsize='8', fixedsize='true', width='2', height='3')

    def find_correlation(self):
        direction = self.data_[1]
        for i, item in enumerate(self.data_[0]):
            if direction[i] == 'in':
                self.dot.node(str(i), 'secret', style='invis')
                self.dot.edge(str(i), 'main', xlabel=item, fontsize='7', constraint='true', arrowsize='0.5', arrowhead='empty')
            else:
                self.dot.node(str(i), 'secret', style='invis')
                self.dot.edge('main', str(i), xlabel=item, fontsize='7', constraint='true', arrowsize='0.5', arrowhead='empty')

    def write_dot(self):
        """

        """
        f = open('block.dot', 'wb')
        f.write(self.dot.source)
        f.close()
        g = pgv.AGraph(file='block.dot', rankdir='LR', splines='ortho')
        g.layout(prog='dot')
        g.draw('block.pdf')
        g.close()

    @staticmethod
    def boo():
        dot = Digraph(comment='foo')
        dot.node('A', 'Apple')
        dot.node('B', 'Ball')
        dot.edges(['AB'])
        f = open('foo.dot', 'wb')
        f.write(dot.source)
        f.close()
        g = pgv.AGraph(file='comp.dot')
        g.layout(prog='dot')
        g.draw('foo.pdf')
        g.close()

if __name__ == '__main__':
    c = CSVtoBlock()
    c.boo()
    c.read_csv_dir()
    c.find_correlation()
    c.write_dot()