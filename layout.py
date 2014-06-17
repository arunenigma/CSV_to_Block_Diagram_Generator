import pygraphviz as pgv


class BlockDiagramLayout(object):
    def __init__(self, levels, knol):
        self.levels = levels
        self.knol = knol
        self.dot = None
        self.empty_left = ''
        self.empty_right = ''

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
        print main_prop
        # strict=False -- allows duplicate edges but disables the ability to create invisible edges
        main_block = main_block.split('.')[0]
        self.dot = pgv.AGraph(comment=main_block, directed=True, compound=True, rankdir='LR', rank='same',
                              splines='ortho', multiedges=True,
                              strict=False, overlap=False)
        print self.levels
        second_level_nodes = []
        for node, level in self.levels.iteritems():
            if level == 2:
                second_level_nodes.append(node)

        n_second_level = len(second_level_nodes)

        # create empty nodes depending on the number of nodes in the level
        # TODO
        # for now this process is manual
        # for a more generic representation, this needs to be automated

        bunch = []
        for n in range(n_second_level):
            if n == 0:
                self.empty_left = '2' + str(n) + 'left'
                self.empty_right = '2' + str(n) + 'right'
                self.dot.add_node(self.empty_left, label=self.empty_left, style='invis', shape='box', fontsize='10',
                                  width='1', height='1')
                self.dot.add_node(second_level_nodes[n], label=second_level_nodes[n], shape='box', fontsize='10',
                                  width='2', height='2')
                self.dot.add_node(self.empty_right, label=self.empty_right, style='invis', shape='box', fontsize='10',
                                  width='1', height='1')

                self.dot.edge_attr['style'] = 'invis'
                self.dot.add_edge(self.empty_left, second_level_nodes[n])
                self.dot.add_edge(second_level_nodes[n], self.empty_right)
                bunch.append(self.empty_left)
                bunch.append(second_level_nodes[n])
                bunch.append(self.empty_right)
            else:

                self.dot.add_node(second_level_nodes[n], label=second_level_nodes[n], shape='box', fontsize='10',
                                  width='2', height='2')
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

        # subgraphs
        self.dot.subgraph(nbunch=bunch, name='cluster_1',
                          label=main_block,
                          rank='same')

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

        #self.construct_subgraphs_level_3()
        self.construct_subgraphs_level_2()
        self.construct_subgraphs_level_1()

    def construct_subgraphs_level_3(self):
        """
        construct subgraph blocks with their signals
        """
        #self.dot.add_subgraph(['fifo', 'fifo_ctrl'], name='s1', rank='same')
        #self.dot.graph_attr['rank'] = 'same'

        fifo_ctrl_info = self.knol['a23_core.csv']
        # draw in/out edges of fifo_ctrl block using fifo_ctrl_info
        direction = fifo_ctrl_info['Direction']
        for i, item in enumerate(fifo_ctrl_info['Signal Name']):
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
        fifo_info = self.knol['a23_execute.csv']
        #print fifo_info
        direction = fifo_info['Direction']
        for i, item in enumerate(fifo_info['Signal Name']):
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

    def construct_subgraphs_level_2(self):
        pass

    def construct_subgraphs_level_1(self):
        pass

    def write_dot(self):
        f = open('block_new.dot', 'wb')
        f.write(self.dot.string())
        f.close()
        g = pgv.AGraph(file='block_new.dot')
        g.layout(prog='dot')
        g.draw('block_new.pdf')
        g.close()