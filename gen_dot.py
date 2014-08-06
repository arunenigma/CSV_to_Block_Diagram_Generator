#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygraphviz as pgv


class GenerateDot(object):
    def __init__(self, dot_out_dir, block_out_dir):
        self.dot = None
        self.block_out_dir = block_out_dir
        self.dot_out_dir = dot_out_dir

    def generate_dot(self, choice, block_map, knol):
        choice = choice.split(' ')
        for n in choice:
            block = block_map[int(n)]
            block_label = block.replace('.csv', '')
            self.dot = pgv.AGraph(comment=block_label, directed=True, compound=True, rank='same',
                                  splines='ortho', multiedges=True,
                                  strict=False, overlap=False, rankdir='LR', ranksep='.5', ratio='1', page="11,11",
                                  size="20.0, 20.0", margin="1.0")
            signals = [signal.strip() for signal in knol[block]['Signal Name']]
            direction = [direct for direct in knol[block]['Direction']]
            self.add_nodes_edges(block_label, signals, direction)
            self.write_dot(block_label)

    def add_nodes_edges(self, block_label, signals, direction):
        empty_left = block_label + '_left'
        empty_right = block_label + '_right'
        self.dot.add_node(empty_left, label=empty_left, style='invis', shape='box', fontsize='10', width='10',
                          height='70', color='peachpuff')
        label = """<<TABLE BGCOLOR="lavenderblush"> \
            <TR><TD><FONT POINT-SIZE="100">%s</FONT></TD></TR> \
            </TABLE>>"""
        label_values = [block_label]
        label = label % tuple(label_values)
        self.dot.add_node(block_label, label=label, style='filled', shape='box', fontsize='10', width='10',
                          height='70', color='peachpuff')
        self.dot.add_node(empty_right, label=empty_right, style='invis', shape='box', fontsize='10', width='10',
                          height='70', color='peachpuff')
        for i, signal in enumerate(signals):
            if direction[i] == 'in':
                self.dot.add_edge(empty_left, block_label, style='filled', xlabel=signal, arrowhead='normal',
                                  fontsize='40',
                                  penwidth='1',
                                  arrowsize=2, weight=2.)
            else:
                self.dot.add_edge(block_label, empty_right, style='filled', xlabel=signal, arrowhead='normal',
                                  fontsize='40',
                                  penwidth='1',
                                  arrowsize=2, weight=2.)

    def write_dot(self, block_label):
        dot_out_file = self.dot_out_dir + '/' + block_label + '.dot'
        f = open(dot_out_file, 'wb')
        f.write(self.dot.string())
        f.close()

        g = pgv.AGraph(file=dot_out_file)
        g.layout(prog='dot')
        block_out = self.block_out_dir + '/' + block_label + '.pdf'
        g.draw(block_out)
        g.close()