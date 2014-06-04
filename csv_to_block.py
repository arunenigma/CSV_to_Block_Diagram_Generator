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
        self.knol_ = {}  # dictionary of columns of csv
        self.data = []
        self.data_ = []
        self.dot = None
        self.knol_all = {}  # dict of dicts of knol

    def read_csv(self, directory, csv_file):
        self.data = []
        self.data_ = []
        self.knol = {}
        self.knol_ = {}
        path = directory + '/' + csv_file
        csv_f = open(path, 'rU')
        f = csv.reader(csv_f)
        for i, row in enumerate(f):
            row = row[0].split('\t')
            if i == 0:
                for j, heading in enumerate(row):
                    self.knol[str(j) + '_' + heading] = None
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
        self.knol_all[csv_file] = self.knol_

    def read_csv_dir(self):
        # read the csv files from dir "csv"
        for (directory, _, csv_files) in walk('./csv'):
            for csv_file in csv_files:
                self.read_csv(directory, csv_file)

    def hierarchy(self):
        """
        driver method for constructing csv hierarchy
        if csv contains source as "system" => it is a MAIN block
        """
        main_block = ''
        for csv_name, properties in self.knol_all.iteritems():
            for prop, items in properties.iteritems():
                if prop == 'Source' and items[0] == 'system':
                    main_block = csv_name
                    break
        main_prop = self.knol_all[main_block]
        self.construct_digraph(main_block, main_prop)

    def construct_digraph(self, main_block, main_prop):
        """
        MAIN block
        """
        print main_prop
        self.dot = Digraph(comment=main_block)
        self.dot.node('main', main_block.split('.')[0].upper(), shape='box', fontsize='8', fixedsize='true', width='2', height='3')
        direction = main_prop['Direction']
        for i, item in enumerate(main_prop['Physical Name']):
            if direction[i] == 'in':
                self.dot.node(str(i), 'secret', style='invis')
                self.dot.edge(str(i), 'main', xlabel=item, fontsize='7', constraint='true', arrowsize='0.5',
                              arrowhead='empty')
            else:
                self.dot.node(str(i), 'secret', style='invis')
                self.dot.edge('main', str(i), xlabel=item, fontsize='7', constraint='true', arrowsize='0.5',
                              arrowhead='empty')

    @staticmethod
    def construct_subgraphs():
        """
        stub
        """
        pass

    @staticmethod
    def pack_subgraphs():
        """
        stub
        """
        pass

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
        """
        mock method
        """
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

    def tests(self):
        pass


if __name__ == '__main__':
    c = CSVtoBlock()
    c.boo()
    c.read_csv_dir()
    c.hierarchy()
    c.write_dot()