import pygraphviz as pgv
from os import walk
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
        #print main_prop
        # strict=False -- allows duplicate edges but disables the ability to create invisible edges
        self.dot = pgv.AGraph(comment=main_block, directed=True, compound=True, rankdir='LR', rank='same',
                              splines='ortho', multiedges=True,
                              strict=False, overlap=False)

        self.dot.add_node('empty_1', label='empty_1', style='invis', shape='box', fontsize='10',
                          width='1', height='1')
        self.dot.add_node('fifo_ctrl', label='fifo_ctrl', shape='box', fontsize='10',
                          width='2', height='2')
        self.dot.add_node('empty_mid', label='empty_2', style='invis', shape='box', fontsize='10',
                          width='1', height='1')
        self.dot.add_node('fifo', label='fifo', shape='box', fontsize='10',
                          width='2', height='2')
        self.dot.add_node('empty_2', label='empty_2', style='invis', shape='box', fontsize='10',
                          width='1', height='1')

        self.dot.edge_attr['style'] = 'invis'
        self.dot.add_edge('empty_1', 'fifo_ctrl')
        self.dot.add_edge('fifo_ctrl', 'empty_mid')
        self.dot.add_edge('empty_mid', 'fifo')
        self.dot.add_edge('fifo', 'empty_2')
        direction = main_prop['Direction']
        self.dot.subgraph(nbunch=['empty_1', 'fifo_ctrl', 'empty_mid', 'fifo', 'empty_2'], name='cluster_1',
                          label='UART',
                          rank='same')

        self.dot.edge_attr['style'] = 'filled'
        for i, item in enumerate(main_prop['Physical Name']):
            if direction[i] == 'in':
                self.dot.add_node(str(i), style='invis')
                self.dot.add_edge(str(i), 'empty_1', taillabel=item, lhead='cluster_1', arrowhead='normal',
                                  fontsize='8',
                                  penwidth='1', arrowsize=.5, weight=2., constraint='true')
            else:
                self.dot.add_node(str(i), style='invis')
                self.dot.add_edge('empty_2', str(i), headlabel=item, ltail='cluster_1', arrowhead='normal',
                                  fontsize='8', penwidth='1', arrowsize=.5, weight=2., constraint='true')
        self.construct_subgraphs()

    def construct_subgraphs(self):
        """
        construct subgraph blocks with their signals
        """
        #self.dot.add_subgraph(['fifo', 'fifo_ctrl'], name='s1', rank='same')
        #self.dot.graph_attr['rank'] = 'same'

        fifo_ctrl_info = self.knol_all['fifo_ctrl.csv']
        # draw in/out edges of fifo_ctrl block using fifo_ctrl_info
        direction = fifo_ctrl_info['Direction']
        for i, item in enumerate(fifo_ctrl_info['Physical Name']):
            if direction[i] == 'in':
                if not fifo_ctrl_info['Source'][i] == 'fifo':
                    self.dot.add_edge('empty_1', 'fifo_ctrl', taillabel=item, arrowhead='normal', fontsize='8',
                                      penwidth='1',
                                      arrowsize=.5, weight=2., style='filled')
                else:
                    self.dot.add_edge('fifo', 'fifo_ctrl', taillabel=item, arrowhead='normal', fontsize='8',
                                      penwidth='1',
                                      arrowsize=.5, weight=2., style='filled')

            else:
                self.dot.add_edge('fifo_ctrl', 'empty_mid', headlabel=item, arrowhead='normal', fontsize='8',
                                  penwidth='1',
                                  arrowsize=.5, weight=2., constraint='true')

        # draw in/out edges of fifo block using fifo_info
        fifo_info = self.knol_all['fifo.csv']
        #print fifo_info
        direction = fifo_info['Direction']
        for i, item in enumerate(fifo_info['Physical Name']):
            if direction[i] == 'in':
                if not fifo_info['Source'][i] == 'fifo_ctrl':
                    self.dot.add_edge('empty_mid', 'fifo', taillabel=item, arrowhead='normal', fontsize='8',
                                      penwidth='1',
                                      arrowsize=.5, weight=2., style='filled')
                else:
                    self.dot.add_edge('fifo_ctrl', 'fifo', taillabel=item, arrowhead='normal', fontsize='8',
                                      penwidth='1',
                                      arrowsize=.5, weight=2., style='filled')

            else:
                self.dot.add_edge('fifo', 'empty_2', headlabel=item, arrowhead='normal', fontsize='8',
                                  penwidth='1',
                                  arrowsize=.5, weight=2., constraint='true')

    def write_dot(self):
        """
            write dot and draw block diagram

        """
        f = open('block.dot', 'wb')
        f.write(self.dot.string())
        f.close()
        g = pgv.AGraph(file='block.dot')
        g.layout(prog='dot')
        g.draw('block.pdf')
        g.close()

if __name__ == '__main__':
    c = CSVtoBlock()
    c.read_csv_dir()
    c.hierarchy()
    c.write_dot()