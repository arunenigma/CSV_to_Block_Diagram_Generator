import pygraphviz as pgv
from random import randint


class BlockDiagramLayout(object):
    def __init__(self, levels, knol, hier):
        self.levels = levels
        self.knol = knol
        self.dot = None
        self.empty_left = None
        self.empty_right = None
        self.hier = hier
        self.subgraphs_level_2 = []
        self.subgraphs_level_2_obj = {}
        self.subgraphs_level_2_obj_proj = {}
        self.main_block = None
        self.top_level = None

    def draw_layout(self):
        """
        construct_digraph for main block --> system
        MAIN block
        """
        self.main_block = ''
        for csv_name, properties in self.knol.iteritems():
            for prop, items in properties.iteritems():
                if prop == 'Source' and items[0] == 'system':
                    self.main_block = csv_name
                    break

        self.main_block = self.main_block.split('.')[0]
        self.dot = pgv.AGraph(comment=self.main_block, directed=True, compound=True,
                              splines='ortho', multiedges=True,
                              strict=False, overlap=False, rankdir='LR', ranksep='2', size="325, 125!", nodesep='0.5')

        # testing html table as node label
        self.dot.add_node('foo', shape='box', label='<>')
        second_level_nodes = []
        for node, level in self.levels.iteritems():
            if level == 2:
                second_level_nodes.append(node)

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
        empty_node = 'empty_node' + self.main_block
        self.dot.add_node(empty_node, label=self.empty_left, style='invis')
        bunch.append(empty_node)
        # subgraph
        self.top_level = self.dot.subgraph(nbunch=bunch, name='cluster_' + self.main_block,
                                           label=self.main_block)

        # ____________________________________________________________________________________________________________

        print third_level_hier
        for parent_children in third_level_hier:
            bunch = []
            bunch_proj = []
            if parent_children[1] is None:
                empty_node = parent_children[0] + '_empty'
                empty_node_proj = parent_children[0] + '_empty_proj'

                self.top_level.add_node(empty_node, label=empty_node, style='invis', shape='box', fontsize='10')
                bunch.append(empty_node)
                self.top_level.add_node(empty_node_proj, label=empty_node_proj, style='invis', shape='box',
                                        fontsize='10')
                bunch.append(empty_node)
                bunch_proj.append(empty_node_proj)
                s_graph_proj = self.top_level.subgraph(bunch_proj, name='cluster_proj_' + parent_children[0], color='invis')
                s_graph = self.top_level.subgraph(bunch, name='cluster_' + parent_children[0], label=parent_children[0])
                self.subgraphs_level_2.append('cluster_' + parent_children[0])
                self.subgraphs_level_2_obj[parent_children[0]] = s_graph
                self.subgraphs_level_2_obj_proj[parent_children[0]] = s_graph_proj

            if parent_children[1]:  # if the node has children
                empty_node_proj = parent_children[0] + '_empty_proj'
                for n, node in enumerate(parent_children[1]):
                    self.empty_left = '3' + str(n) + 'left'
                    self.empty_right = '3' + str(n) + 'right'
                    self.top_level.add_node(self.empty_left, label=self.empty_left, style='invis', shape='box',
                                            fontsize='10', width='2', height='5')
                    self.top_level.add_node(parent_children[1][n], label=parent_children[1][n], shape='box',
                                            fontsize='10',
                                            width='2', height='5')
                    self.top_level.add_node(self.empty_right, label=self.empty_right, style='invis', shape='box',
                                            fontsize='10', width='2', height='5')

                    self.dot.edge_attr['style'] = 'invis'
                    self.top_level.add_edge(self.empty_left, parent_children[1][n])
                    self.top_level.add_edge(parent_children[1][n], self.empty_right)
                    bunch.append(self.empty_left)
                    bunch.append(parent_children[1][n])
                    bunch.append(self.empty_right)
                bunch_proj.append(empty_node_proj)
                s_graph_proj = self.top_level.subgraph(bunch_proj, name='cluster_proj_' + parent_children[0],
                                                       color='invis')
                # subgraph
                s_graph = self.top_level.subgraph(bunch, name='cluster_' + parent_children[0], label=parent_children[0])
                self.subgraphs_level_2.append('cluster_' + parent_children[0])
                self.subgraphs_level_2_obj[parent_children[0]] = s_graph
                self.subgraphs_level_2_obj_proj[parent_children[0]] = s_graph_proj

                self.draw_signals_third_level(parent_children[0], bunch, parent_children[1])

    def draw_signals_third_level(self, parent, bunch, nodes):
        """
            signals are btw nodes
        """
        for i, node in enumerate(nodes):
            node_info = self.knol[node + '.csv']
            # draw in/out edges
            direction = node_info['Direction']
            for j, item in enumerate(node_info['Signal Name']):
                if direction[j] == 'in':
                    if node_info['Source'][j]:
                        if not node_info['Source'][j] == parent:
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
                        else:
                            for idx, b_node in enumerate(bunch):
                                if b_node == node:
                                    self.dot.add_edge(bunch[idx - 1], node, headlabel=item, arrowhead='normal',
                                                      fontsize='8',
                                                      penwidth='1',
                                                      arrowsize=.5, weight=2., style='filled')
                                    # adding invisible edges to space them out evenly
                                    self.dot.add_edge(bunch[idx - 1], node, taillabel=item + str(100 + j),
                                                      arrowhead='normal',
                                                      fontsize='8',
                                                      penwidth='1',
                                                      arrowsize=.5, weight=2., style='invis')
                                    self.dot.add_edge(bunch[idx - 1], node, taillabel=item + str(200 + j),
                                                      arrowhead='normal',
                                                      fontsize='8',
                                                      penwidth='1',
                                                      arrowsize=.5, weight=2., style='invis')
                                    self.dot.add_edge(bunch[idx - 1], node, taillabel=item + str(300 + j),
                                                      arrowhead='normal',
                                                      fontsize='8',
                                                      penwidth='1',
                                                      arrowsize=.5, weight=2., style='invis')
                else:
                    for idx, b_node in enumerate(bunch):
                        if b_node == node:
                            self.dot.add_edge(node, bunch[idx + 1], headlabel=item, arrowhead='normal',
                                              fontsize='8',
                                              penwidth='1',
                                              arrowsize=.5, weight=2., style='filled')
                            # adding invisible edges to space them out evenly
                            self.dot.add_edge(node, bunch[idx + 1], taillabel=item + str(100 + j),
                                              arrowhead='normal',
                                              fontsize='8',
                                              penwidth='1',
                                              arrowsize=.5, weight=2., style='invis')
                            self.dot.add_edge(node, bunch[idx + 1], taillabel=item + str(200 + j),
                                              arrowhead='normal',
                                              fontsize='8',
                                              penwidth='1',
                                              arrowsize=.5, weight=2., style='invis')
                            self.dot.add_edge(node, bunch[idx + 1], taillabel=item + str(300 + j),
                                              arrowhead='normal',
                                              fontsize='8',
                                              penwidth='1',
                                              arrowsize=.5, weight=2., style='invis')

    def subgraph_lr(self):
        """
        this method tries to align subgraphs in LR fashion
        """
        print self.subgraphs_level_2_obj.keys()
        print
        print
        print self.subgraphs_level_2_obj_proj.keys()

        pivot_nodes = []
        for i, sub_g in enumerate(self.subgraphs_level_2):
            node = sub_g.split('_')[1] + '_' + sub_g.split('_')[2]
            sub_graph_curr_proj = self.subgraphs_level_2_obj_proj[node]
            sub_graph_curr = self.subgraphs_level_2_obj[node]
            sub_graph_curr_proj.add_node(node + '_pivot_proj', style='invis')
            sub_graph_curr.add_node(node + '_pivot', style='invis')
            pivot_nodes.append(node + '_pivot_proj')
            pivot_nodes.append(node + '_pivot')

        # draw invisible edges btw the pivots of subgraphs and hope to see them aligned
        for i in xrange(len(pivot_nodes) - 1):
            current_item, next_item = pivot_nodes[i], pivot_nodes[i + 1]
            print current_item, next_item
            if '_proj' in current_item and not '_proj' in next_item:
                current_item_cluster = 'cluster_proj_' + current_item.replace('_pivot_proj', '')
                next_item_cluster = 'cluster_' + next_item.replace('_pivot', '')
                self.dot.add_edge(current_item, next_item, ltail=current_item_cluster,
                                  lhead=next_item_cluster, style='invis')

            if not '_proj' in current_item and 'proj' in next_item:
                current_item_cluster = 'cluster_' + current_item.replace('_pivot', '')
                next_item_cluster = 'cluster_proj_' + next_item.replace('_pivot_proj', '')
                self.dot.add_edge(current_item, next_item, ltail=current_item_cluster,
                                  lhead=next_item_cluster, style='invis')

    def draw_signals_second_level(self):
        """
        signals are btw subgraphs so following a different approach
        works only if number of signals are less (<20)
        gets messy for large number of signals
        """
        for i, sub_g in enumerate(self.subgraphs_level_2):

            node = sub_g.split('_')[1] + '_' + sub_g.split('_')[2]
            sub_graph_curr = self.subgraphs_level_2_obj[node]
            node_info = self.knol[node + '.csv']
            # draw in/out edges
            direction = node_info['Direction']
            for j, item in enumerate(node_info['Signal Name']):
                print 'Item->', item
                if direction[j] == 'in' and j < 10:  # current version only works for < 20 signals
                    if node_info['Source'][j]:
                        if not node_info['Source'][j] == self.main_block:
                            sub_graph_other = self.subgraphs_level_2_obj[node_info['Source'][j]]
                            sub_graph_curr.add_node(item + '_curr', style='invis', shape='point')
                            sub_graph_other.add_node(item + '_other', style='invis', shape='point')
                            self.dot.add_edge(item + '_curr', item + '_other',
                                              lhead='cluster_' + node_info['Source'][j],
                                              ltail=sub_g, headlabel=item, arrowhead='normal',
                                              fontsize='8',
                                              penwidth='1',
                                              arrowsize=.5, weight=2., style='filled', constraint=True)
                        else:
                            """
                            sub_graph_curr.add_node(item + '_orig', style='invis', shape='point')
                            self.subgraphs_level_2_obj_proj[node].add_node(item + '_proj', style='invis',
                                                                           shape='point')
                            sub_g_proj = sub_g.replace('cluster', 'cluster_proj')
                            self.dot.add_edge(item + '_proj', item + '_orig', ltail=sub_g_proj, lhead=sub_g, headlabel=item, arrowhead='normal',
                                              fontsize='8',
                                              penwidth='1',
                                              arrowsize=.5, weight=2., style='filled', constraint=False)
                            """
                else:
                    pass

    def write_dot(self):
        f = open('block_new.dot', 'wb')
        f.write(self.dot.string())
        f.close()
        g = pgv.AGraph(file='block_new.dot')
        g.layout(prog='dot')
        g.draw('block_new.pdf')
        g.close()