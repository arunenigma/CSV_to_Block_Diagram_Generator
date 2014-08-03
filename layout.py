#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygraphviz as pgv


class BlockDiagramLayout(object):
    def __init__(self, levels, knol, hier):
        self.levels = levels
        self.knol = knol
        self.dot = None
        self.empty_left = ''
        self.empty_right = ''
        self.hier = hier

    def draw_layout(self):
        """
        construct_digraph for main block --> system
        MAIN block
        """
        main_block = ''
        for csv_name, properties in self.knol.iteritems():
            for prop, items in properties.iteritems():
                if prop == 'Source' and items[0] == 'system':
                    main_block = csv_name
                    break

        # main_block -> a23_core -> Level 1
        main_prop = self.knol[main_block]
        #print main_prop
        # strict=False -- allows duplicate edges but disables the ability to create invisible edges
        main_block = main_block.split('.')[0]
        self.dot = pgv.AGraph(comment=main_block, directed=True, compound=True, rank='same',
                              splines='ortho', multiedges=True,
                              strict=False, overlap=False, rankdir='LR', ranksep='.5', ratio='1', page="11,11",
                              size="20.0, 20.0", margin="1.0")
        self.dot.graph_attr['bb'] = "-100, -100, 600, 600"
        second_level_nodes = []
        for node, level in self.levels.iteritems():
            if level == 2:
                second_level_nodes.append(node)
        n_second_level = len(second_level_nodes)

        third_level_nodes = []
        for node, level in self.levels.iteritems():
            if level == 3:
                third_level_nodes.append(node)

        third_level_hier = []
        for parent, children in self.hier.iteritems():
            for node in second_level_nodes:
                if parent == node:
                    if children:
                        third_level_hier.append([parent, children])
                    else:
                        third_level_hier.append([parent, None])

        # subgraphing level 2 nodes into main block
        bunch = []

        # restrict number of nodes in a row to 3 for etiquette purpose
        #row_nodes = 0

        # order of nodes -> fetch, decode and execute
        order = {'fetch': 0, 'decode': 1, 'execute': 2}
        sorted_second_level_nodes = [None, None, None, 'a23_coprocessor']
        for node in second_level_nodes:
            for key, value in order.iteritems():
                if key in node:
                    sorted_second_level_nodes[order[key]] = node
        second_level_nodes = sorted_second_level_nodes

        # Dummy Node for creating extra space at the top
        self.empty_left = '2_top_' + 'left'
        self.empty_right = '2_top_' + 'right'
        self.dot.add_node(self.empty_left, label=self.empty_left, style='invis', shape='point', fontsize='10')
        self.dot.add_node('dummy_top', label='dummy_top', shape='point', fontsize='10', style='invis')
        self.dot.add_node(self.empty_right, label=self.empty_right, style='invis', shape='point', fontsize='10')

        # self.dot.edge_attr['style'] = 'invis'  # already in effect
        self.dot.add_edge(self.empty_left, 'dummy_top')
        self.dot.add_edge('dummy_top', self.empty_right)
        bunch.append(self.empty_left)
        bunch.append('dummy_top')
        bunch.append(self.empty_right)

        for n in range(n_second_level):
            if n == 0:  # fetch node
                self.empty_left = '2' + str(n) + 'left'
                self.empty_right = '2' + str(n) + 'right'
                self.dot.add_node(self.empty_left, label=self.empty_left, style='invis', shape='box', fontsize='10',
                                  width='3', height='10')
                self.dot.add_node(second_level_nodes[n], label=second_level_nodes[n], shape='box', fontsize='60',
                                  width='10', height='70', style='filled', color='peachpuff')
                label = """<<TABLE BGCOLOR="white" WIDTH="200"> \
                    <TR><TD COLSPAN="1" ROWSPAN="1"><TABLE BGCOLOR="lightcyan"> \
                    <TR><TD BGCOLOR="white">%s</TD></TR> \
                    </TABLE></TD></TR></TABLE>>"""
                label_values = [second_level_nodes[n]]
                label = label % tuple(label_values)
                self.dot.get_node(second_level_nodes[n]).attr.update({'shape': 'plaintext', 'label': label})
                self.dot.add_node(self.empty_right, label=self.empty_right, style='invis', shape='box', fontsize='10',
                                  width='3', height='10')
                self.dot.edge_attr['style'] = 'invis'
                self.dot.add_edge(self.empty_left, second_level_nodes[n])
                self.dot.add_edge(second_level_nodes[n], self.empty_right)
                bunch.append(self.empty_left)
                bunch.append(second_level_nodes[n])
                bunch.append(self.empty_right)
            elif n == 1:  # decode node
                self.dot.add_node(second_level_nodes[n], label=second_level_nodes[n], shape='box', fontsize='60',
                                  width='10', height='50', style='filled', color='peachpuff')
                label = """<<TABLE BGCOLOR="white" WIDTH="200"> \
                    <TR><TD COLSPAN="1" ROWSPAN="1"><TABLE BGCOLOR="lightcyan"> \
                    <TR><TD BGCOLOR="white">%s</TD></TR> \
                    </TABLE></TD></TR></TABLE>>"""
                label_values = [second_level_nodes[n]]
                label = label % tuple(label_values)
                self.dot.get_node(second_level_nodes[n]).attr.update({'shape': 'plaintext', 'label': label})
                self.dot.edge_attr['style'] = 'invis'
                self.dot.add_edge(self.empty_right, second_level_nodes[n])
                self.empty_right = '2' + str(n) + 'right'
                self.dot.add_node(self.empty_right, label=self.empty_right, style='invis', shape='box', fontsize='10',
                                  width='3', height='10')
                self.dot.add_edge(second_level_nodes[n], self.empty_right)
                bunch.append(second_level_nodes[n])
                bunch.append(self.empty_right)

            elif n == 2:  # execute node
                self.dot.add_node(second_level_nodes[n], label=second_level_nodes[n], shape='box', fontsize='60',
                                  width='10', height='70', style='filled', color='peachpuff')
                label = """<<TABLE BGCOLOR="white" WIDTH="200"> \
                        <TR><TD COLSPAN="1" ROWSPAN="1"><TABLE BGCOLOR="lightcyan"> \
                        <TR><TD BGCOLOR="white">%s</TD></TR> \
                        <TR><TD>%s</TD></TR> \
                        <TR><TD>%s</TD></TR> \
                        <TR><TD>%s</TD></TR> \
                        <TR><TD>%s</TD></TR> \
                        </TABLE></TD></TR></TABLE>>"""
                label_values = [second_level_nodes[n]]
                for node in third_level_nodes:
                    label_values.append(node)
                label = label % tuple(label_values)

                self.dot.get_node(second_level_nodes[n]).attr.update({'shape': 'plaintext', 'label': label})
                self.dot.add_edge(self.empty_right, second_level_nodes[n])
                empty_right_top = '2' + str(n) + 'right_top'
                empty_right_down = '2' + str(n) + 'right_down'
                empty_last = '2' + str(n) + 'empty_last'
                self.dot.add_node(empty_right_top, label=empty_right_top, style='invis', shape='box', fontsize='10',
                                  width='1', height='20')
                self.dot.add_node(empty_right_down, label=empty_right_down, style='invis', shape='box', fontsize='10',
                                  width='1', height='20')
                self.dot.add_node(empty_last, label=empty_last, style='invis', shape='box', fontsize='10',
                                  width='1', height='20')
                self.dot.add_edge(second_level_nodes[n], empty_right_top, style='invis')
                self.dot.add_edge(second_level_nodes[n], empty_right_down, style='invis')
                self.dot.add_edge(empty_right_down, empty_last, style='invis')
                bunch.append(second_level_nodes[n])
                bunch.append(empty_right_top)
                bunch.append(empty_right_down)
                bunch.append(empty_last)

        # Dummy Node for creating extra space at the mid
        self.empty_left = '2_mid' + 'left'
        self.empty_right = '2_mid' + 'right'
        self.dot.add_node(self.empty_left, label=self.empty_left, style='invis', shape='point', fontsize='10')
        self.dot.add_node('dummy_mid', label='dummy_mid', shape='point', fontsize='10', style='invis')
        self.dot.add_node(self.empty_right, label=self.empty_right, style='invis', shape='point', fontsize='10')

        # self.dot.edge_attr['style'] = 'invis'  # already in effect
        self.dot.add_edge(self.empty_left, 'dummy_mid')
        self.dot.add_edge('dummy_mid', self.empty_right)
        bunch.append(self.empty_left)
        bunch.append('dummy_mid')
        bunch.append(self.empty_right)

        # TODO Logic implementation of customizing layout
        # there isn't a lot of freedom when it comes to laying out nodes with Graphviz

        n = 3  # last node (coprocessor)
        self.empty_left = '2' + str(n) + 'left'
        self.empty_right = '2' + str(n) + 'right'
        self.dot.add_node(self.empty_left, label=self.empty_left, style='invis', shape='point', fontsize='10')
        self.dot.add_node(second_level_nodes[n], label=second_level_nodes[n], shape='box', fontsize='60',
                          width='7', height='22', style='filled', color='skyblue')
        label = """<<TABLE BGCOLOR="white" WIDTH="200"> \
            <TR><TD COLSPAN="1" ROWSPAN="1"><TABLE BGCOLOR="lightcyan"> \
            <TR><TD BGCOLOR="white">%s</TD></TR> \
            </TABLE></TD></TR></TABLE>>"""
        label_values = [second_level_nodes[n]]
        label = label % tuple(label_values)
        self.dot.get_node(second_level_nodes[n]).attr.update({'shape': 'plaintext', 'label': label})
        #self.dot.get_node(second_level_nodes[n]).attr.update({'pin': True})  # doesn't work for some reason
        self.dot.add_node(self.empty_right, label=self.empty_right, style='invis', shape='point', fontsize='10')

        # self.dot.edge_attr['style'] = 'invis'  # already in effect
        self.dot.add_edge(self.empty_left, second_level_nodes[n])
        self.dot.add_edge(second_level_nodes[n], self.empty_right)
        bunch.append(self.empty_left)
        bunch.append(second_level_nodes[n])
        bunch.append(self.empty_right)

        # super hack
        # node placement heavily relies on the number of edges between the nodes
        # hack is to add max dummy nodes between 'dummy_mid', 'a23_coprocessor' so that coprocessor remains at bottom
        for i in range(100):
            self.dot.add_edge('dummy_mid', 'a23_coprocessor', xlabel=str(i) + '_hack', style='invis')

        # Dummy Node for creating extra space at the bottom
        self.empty_left = '2_bottom' + 'left'
        self.empty_right = '2_bottom' + 'right'
        self.dot.add_node(self.empty_left, label=self.empty_left, style='invis', shape='point', fontsize='10')
        self.dot.add_node('dummy_bottom', label='dummy_bottom', shape='point', fontsize='10', style='invis')
        self.dot.add_node(self.empty_right, label=self.empty_right, style='invis', shape='point', fontsize='10',
                          width='3', height='3')

        # self.dot.edge_attr['style'] = 'invis'  # already in effect
        self.dot.add_edge(self.empty_left, 'dummy_bottom')
        self.dot.add_edge('dummy_bottom', self.empty_right)
        bunch.append(self.empty_left)
        bunch.append('dummy_bottom')
        bunch.append(self.empty_right)
        direction = main_prop['Direction']

        # subgraph
        self.dot.subgraph(nbunch=bunch, name='cluster_1',
                          label=main_block)

        self.dot.edge_attr['style'] = 'filled'
        # drawing signals in and out of source
        print bunch
        for i, item in enumerate(main_prop['Signal Name']):
            if direction[i] == 'out':
                # TODO need automation here | find math logic later
                self.dot.add_node(str(i), style='invis')

                self.dot.add_edge(bunch[11], str(i), headlabel=item, ltail='cluster_1',
                                  taillabel=item.replace('i_', 'o_') + '(src)', arrowhead='normal',
                                  fontsize='20', penwidth='1', arrowsize=2, weight=2.)
            else:
                self.dot.add_node(str(i), style='invis')
                self.dot.add_edge(str(i), bunch[3], taillabel=item, lhead='cluster_1', arrowhead='normal',
                                  fontsize='20',
                                  penwidth='1', arrowsize=2, weight=2.)

        self.construct_subgraphs_level_2(second_level_nodes, bunch, main_block)

    def construct_subgraphs_level_2(self, nodes, bunch, main_block):
        """
            construct subgraph blocks with their signals
        """
        for i, node in enumerate(nodes):
            print bunch
            if not i == 3:  # not co-processor node (second row node)
                node_info = self.knol[node + '.csv']
                # draw in/out edges
                direction = node_info['Direction']
                for j, item in enumerate(node_info['Signal Name']):
                    if direction[j] == 'in':  # incoming signals to nodes
                        if node_info['Source'][j] == main_block:
                            if i == 0:
                                self.dot.add_edge(bunch[3], node, taillabel=item, arrowhead='normal', fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='filled')
                                # adding invisible edges to space them out evenly
                                self.dot.add_edge(bunch[3], node, taillabel=item + str(j), arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')
                                self.dot.add_edge(bunch[3], node, taillabel=item + str(100 + j), arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')
                                self.dot.add_edge(bunch[3], node, taillabel=item + str(200 + j), arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')
                                self.dot.add_edge(bunch[3], node, taillabel=item + str(300 + j), arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')
                            elif i == 1:
                                self.dot.add_edge(bunch[5], node, taillabel=item, arrowhead='normal', fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='filled')
                                # adding invisible edges to space them out evenly
                                self.dot.add_edge(bunch[5], node, taillabel=item + str(j), arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')
                                self.dot.add_edge(bunch[5], node, taillabel=item + str(100 + j), arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')
                                self.dot.add_edge(bunch[5], node, taillabel=item + str(200 + j), arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')
                                self.dot.add_edge(bunch[5], node, taillabel=item + str(300 + j), arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')
                            elif i == 2:
                                self.dot.add_edge(bunch[7], node, taillabel=item, arrowhead='normal', fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='filled')
                                # adding invisible edges to space them out evenly
                                self.dot.add_edge(bunch[7], node, taillabel=item + str(j), arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')
                                self.dot.add_edge(bunch[7], node, taillabel=item + str(100 + j), arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')
                                self.dot.add_edge(bunch[7], node, taillabel=item + str(200 + j), arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')
                        else:  # incoming signals from neighbor nodes

                            if node_info['Source'][j]:
                                self.dot.add_edge(node_info['Source'][j], node, headlabel=item,
                                                  taillabel=item.replace('i_', 'o_'), arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='filled')

                                # adding invisible edges to space them out evenly
                                self.dot.add_edge(node_info['Source'][j], node, taillabel=item + str(j),
                                                  arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')

                                self.dot.add_edge(node_info['Source'][j], node, taillabel=item + str(100 + j),
                                                  arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')
                                self.dot.add_edge(node_info['Source'][j], node, taillabel=item + str(200 + j),
                                                  arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')

                    else:  # outgoing signals from nodes to source

                        if node_info['Source'][j]:
                            self.dot.add_edge(node, node_info['Source'][j], headlabel=item,
                                              taillabel=item.replace('i_', 'o_'), arrowhead='normal',
                                              fontsize='20',
                                              penwidth='1',
                                              arrowsize=2, weight=2., style='filled')

                            # adding invisible edges to space them out evenly
                            self.dot.add_edge(node, node_info['Source'][j], taillabel=item + str(j),
                                              arrowhead='normal',
                                              fontsize='20',
                                              penwidth='1',
                                              arrowsize=2, weight=2., style='invis')

                            self.dot.add_edge(node, node_info['Source'][j], taillabel=item + str(100 + j),
                                              arrowhead='normal',
                                              fontsize='20',
                                              penwidth='1',
                                              arrowsize=2, weight=2., style='invis')
                            self.dot.add_edge(node, node_info['Source'][j], taillabel=item + str(200 + j),
                                              arrowhead='normal',
                                              fontsize='20',
                                              penwidth='1',
                                              arrowsize=2, weight=2., style='invis')

            else:  # co-processor node
                node_info = self.knol[node + '.csv']
                # draw in/out edges
                direction = node_info['Direction']
                for j, item in enumerate(node_info['Signal Name']):
                    if direction[j] == 'in':
                        if node_info['Source'][j] == main_block:
                            self.dot.add_edge(node, bunch[-i], taillabel=item, arrowhead='normal', fontsize='20',
                                              penwidth='1',
                                              arrowsize=2, weight=2., style='filled')
                            # adding invisible edges to space them out evenly
                            self.dot.add_edge(node, bunch[-i], taillabel=item + str(j), arrowhead='normal',
                                              fontsize='20',
                                              penwidth='1',
                                              arrowsize=2, weight=2., style='invis')
                            self.dot.add_edge(node, bunch[-i], taillabel=item + str(100 + j), arrowhead='normal',
                                              fontsize='20',
                                              penwidth='1',
                                              arrowsize=2, weight=2., style='invis')
                            self.dot.add_edge(node, bunch[-i], taillabel=item + str(200 + j), arrowhead='normal',
                                              fontsize='20',
                                              penwidth='1',
                                              arrowsize=2, weight=2., style='invis')

                        else:  # incoming signals to coprocessor form neighbor nodes
                            if node_info['Source'][j]:
                                print node_info['Source'][j], node
                                self.dot.add_edge(node_info['Source'][j], node, headlabel=item, arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='filled')

                                # adding invisible edges to space them out evenly
                                self.dot.add_edge(node_info['Source'][j], node, taillabel=item + str(j),
                                                  arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')

                                self.dot.add_edge(node_info['Source'][j], node, taillabel=item + str(100 + j),
                                                  arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')
                                self.dot.add_edge(node_info['Source'][j], node, taillabel=item + str(200 + j),
                                                  arrowhead='normal',
                                                  fontsize='20',
                                                  penwidth='1',
                                                  arrowsize=2, weight=2., style='invis')

                    else:  # out signals from coprocessor
                        if node_info['Source'][j]:
                            self.dot.add_edge(node, node_info['Source'][j], headlabel=item,
                                              taillabel=item.replace('i_', 'o_'), arrowhead='normal',
                                              fontsize='20',
                                              penwidth='1',
                                              arrowsize=2, weight=2., style='filled')

                            # adding invisible edges to space them out evenly
                            self.dot.add_edge(node, node_info['Source'][j], taillabel=item + str(j),
                                              arrowhead='normal',
                                              fontsize='20',
                                              penwidth='1',
                                              arrowsize=2, weight=2., style='invis')

                            self.dot.add_edge(node, node_info['Source'][j], taillabel=item + str(100 + j),
                                              arrowhead='normal',
                                              fontsize='20',
                                              penwidth='1',
                                              arrowsize=2, weight=2., style='invis')
                            self.dot.add_edge(node, node_info['Source'][j], taillabel=item + str(200 + j),
                                              arrowhead='normal',
                                              fontsize='20',
                                              penwidth='1',
                                              arrowsize=2, weight=2., style='invis')

    def write_dot(self):
        f = open('block_diag.dot', 'wb')
        f.write(self.dot.string())
        f.close()
        g = pgv.AGraph(file='block_diag.dot')
        g.layout(prog='dot')
        g.draw('block_diag.pdf')
        g.close()