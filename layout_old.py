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
                              strict=False, overlap=False, rankdir='LR', ranksep='1 equally', margin=5)
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




        # subgraphing level 2 nodes
        bunch = []
        bunch_2 = []

        for n in range(n_second_level):
            if n == 0:  # first node
                self.empty_left = '2' + str(n) + 'left'
                self.empty_right = '2' + str(n) + 'right'
                self.dot.add_node(self.empty_left, label=self.empty_left, style='invis', shape='box', fontsize='10',
                                  width='1', height='1')
                self.dot.add_node(second_level_nodes[n], label=second_level_nodes[n], shape='box', fontsize='10',
                                  width='2', height='10')
                self.dot.add_node(self.empty_right, label=self.empty_right, style='invis', shape='box', fontsize='10',
                                  width='1', height='1')

                self.dot.edge_attr['style'] = 'invis'
                self.dot.add_edge(self.empty_left, second_level_nodes[n])
                self.dot.add_edge(second_level_nodes[n], self.empty_right)
                bunch.append(self.empty_left)
                bunch.append(second_level_nodes[n])
                bunch.append(self.empty_right)
            elif second_level_nodes[n] == 'a23_coprocessor':
                self.dot.add_node(second_level_nodes[n], label=second_level_nodes[n], shape='box', fontsize='10',
                                  width='2', height='5')
                bunch_2.append(second_level_nodes[n])
            else:

                self.dot.add_node(second_level_nodes[n], label=second_level_nodes[n], shape='box', fontsize='10',
                                  width='2', height='10')
                self.dot.edge_attr['style'] = 'invis'
                self.dot.add_edge(self.empty_right, second_level_nodes[n])
                self.empty_right = '2' + str(n) + 'right'
                self.dot.add_node(self.empty_right, label=self.empty_right, style='invis', shape='box', fontsize='10',
                                  width='1', height='1')

                self.dot.edge_attr['style'] = 'invis'
                self.dot.add_edge(second_level_nodes[n], self.empty_right)
                bunch.append(second_level_nodes[n])
                bunch.append(self.empty_right)

        direction = main_prop['Direction']

        # subgraph
        top_level = self.dot.subgraph(nbunch=bunch, name='cluster_1',
                                      label=main_block)

        self.dot.subgraph(nbunch=bunch_2, name='cluster_2', label=main_block, color='invis')

        self.dot.edge_attr['style'] = 'filled'
        for i, item in enumerate(main_prop['Signal Name']):
            if direction[i] == 'out':
                self.dot.add_node(str(i), style='invis')
                self.dot.add_edge(bunch[-1], str(i), headlabel=item, ltail='cluster_1', arrowhead='normal',
                                  fontsize='8', penwidth='1', arrowsize=.5, weight=2., constraint='true')
            else:
                self.dot.add_node(str(i), style='invis')
                self.dot.add_edge(str(i), bunch[0], taillabel=item, lhead='cluster_1', arrowhead='normal',
                                  fontsize='8',
                                  penwidth='1', arrowsize=.5, weight=2., constraint='true')

        self.construct_subgraphs_level_2(second_level_nodes, bunch, main_block)


        # ____________________________________________________________________________________________________________

        # subgraphing level 3 nodes inside level 2 nodes
        # some level 2 nodes do not have children

        bunch_3 = []
        # current example has only one 2nd level node having children (3rd level)
        print third_level_hier
        for parent_children in third_level_hier:
            bunch = []
            print parent_children
            if parent_children[1]:  # if the node has children
                for n, node in enumerate(parent_children[1]):
                    self.empty_left = '3' + str(n) + 'left'
                    self.empty_right = '3' + str(n) + 'right'
                    top_level.add_node(self.empty_left, label=self.empty_left, style='invis', shape='box',
                                       fontsize='10')
                    top_level.add_node(parent_children[1][n], label=parent_children[1][n], shape='box', fontsize='10',
                                       width='2', height='2')
                    top_level.add_node(self.empty_right, label=self.empty_right, style='invis', shape='box',
                                       fontsize='10')

                    self.dot.edge_attr['style'] = 'invis'
                    top_level.add_edge(self.empty_left, parent_children[1][n])
                    top_level.add_edge(parent_children[1][n], self.empty_right)
                    bunch.append(self.empty_left)
                    bunch.append(parent_children[1][n])
                    bunch.append(self.empty_right)

                direction = main_prop['Direction']
                print bunch
                # subgraph
                top_level.subgraph(bunch, name='cluster_' + parent_children[0], label=parent_children[0])

                """
                self.dot.edge_attr['style'] = 'filled'
                for i, item in enumerate(main_prop['Signal Name']):
                    if direction[i] == 'in':
                        self.dot.add_node(str(i), style='invis')
                        self.dot.add_edge(str(i), bunch[0], taillabel=item, lhead='cluster_1', arrowhead='normal',
                                          fontsize='8',
                                          penwidth='1', arrowsize=.5, weight=2., constraint='true')
                    else:
                        self.dot.add_node(str(i), style='invis')
                        self.dot.add_edge(bunch[-1], str(i), headlabel=item, ltail='cluster_1', arrowhead='normal',
                                          fontsize='8', penwidth='1', arrowsize=.5, weight=2., constraint='true')
                """

                self.construct_subgraphs_level_3(parent_children[1][1], bunch, main_block)

            else:
                print 'foo'
                empty_node = parent_children[0] + '_empty'
                top_level.add_node(empty_node, label=empty_node, style='invis', shape='box', fontsize='10', width='2',
                                   height='10')
                bunch.append(empty_node)
                top_level.subgraph(bunch, name='cluster_' + parent_children[0], label=parent_children[0])


    def construct_subgraphs_level_2(self, nodes, bunch, main_block):
        """
            construct subgraph blocks with their signals
        """
        for i, node in enumerate(nodes):
            node_info = self.knol[node + '.csv']
            # draw in/out edges
            direction = node_info['Direction']
            for j, item in enumerate(node_info['Signal Name']):
                if direction[j] == 'in':
                    if node_info['Source'][j] == main_block:
                        self.dot.add_edge(bunch[2 * i], node, taillabel=item, arrowhead='normal', fontsize='8',
                                          penwidth='1',
                                          arrowsize=.5, weight=2., style='filled')
                        # adding invisible edges to space them out evenly
                        self.dot.add_edge(bunch[2 * i], node, taillabel=item + str(j), arrowhead='normal',
                                          fontsize='8',
                                          penwidth='1',
                                          arrowsize=.5, weight=2., style='invis')
                    else:
                        if node_info['Source'][j]:
                            self.dot.add_edge(node_info['Source'][j], node, headlabel=item, arrowhead='normal',
                                              fontsize='8',
                                              penwidth='1',
                                              arrowsize=.5, weight=2., style='filled')

                            # adding invisible edges to space them out evenly
                            self.dot.add_edge(node_info['Source'][j], node, taillabel=item + str(100 + j),
                                              arrowhead='normal',
                                              fontsize='8',
                                              penwidth='1',
                                              arrowsize=.5, weight=2., style='invis')
                            self.dot.add_edge(node_info['Source'][j], node, taillabel=item + str(200 + j),
                                              arrowhead='normal',
                                              fontsize='8',
                                              penwidth='1',
                                              arrowsize=.5, weight=2., style='invis')
                            self.dot.add_edge(node_info['Source'][j], node, taillabel=item + str(300 + j),
                                              arrowhead='normal',
                                              fontsize='8',
                                              penwidth='1',
                                              arrowsize=.5, weight=2., style='invis')

                    """
                else:
                    self.dot.add_edge(node, nodes[i+1], taillabel=item, arrowhead='normal', fontsize='8',
                                      penwidth='1',
                                      arrowsize=.5, weight=2., style='filled')
                """
                """
            else:
                self.dot.add_edge(node, bunch[(2*i)+1], headlabel=item, arrowhead='normal', fontsize='8',
                                  penwidth='1',
                                  arrowsize=.5, weight=2., constraint='true')
            """

    def construct_subgraphs_level_3(self, nodes, bunch, main_block):
        pass

    def write_dot(self):
        f = open('block_new.dot', 'wb')
        f.write(self.dot.string())
        f.close()
        g = pgv.AGraph(file='block_new.dot')
        g.layout(prog='dot')
        g.draw('block_new.pdf')
        g.close()