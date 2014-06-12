import pygraphviz as pgv
import csv
import sys


class Hierarchy(object):
    def __init__(self):
        self.hierarchy = {}
        self.levels = {}
        self.graph = None
        self.graph_ = {}

    def collect_first_row(self, csv_name, csv_obj):
        """
        This method extracts the first row (after heading) of every csv file in the user inputted directory
        """
        try:
            for i, row in enumerate(csv_obj):
                if i == 1:
                    self.hierarchy[csv_name] = row[4]
                    break
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (csv_name, csv_obj.line_num, e))

        return self.hierarchy

    def construct_graph(self):
        """
            hierarchy is constructed as a graph using the edges returned by collect_first_row method
        """
        self.graph = pgv.AGraph(directed=True)
        for block, src in self.hierarchy.iteritems():
            self.graph.add_node(src)
            self.graph.add_node(block)
            self.graph.add_edge(src, block)

    def bfs_edges(self):
        for node in self.graph.nodes():
            print node, self.graph.successors(node)
            self.graph_[str(node)] = set([str(successor) for successor in self.graph.successors(node)])

        top = 'system'
        print '_______)'
        print self.graph_
        visited, queue = set(), [top]  # system is default top level
        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                queue.extend(self.graph_[vertex] - visited)
        return visited