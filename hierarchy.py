from operator import itemgetter
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
            self.graph_[str(node)] = set([str(successor) for successor in self.graph.successors(node)])

        n_graph = {}
        for node, neighbors in self.graph_.iteritems():
            n_graph[node] = len(neighbors)

        for node, neighbors in self.graph_.iteritems():
            if neighbors:
                n_neighbors = []
                for neighbor in neighbors:
                    n_neighbors.append((neighbor, n_graph[neighbor]))
                self.graph_[node] = n_neighbors
            else:
                self.graph_[node] = []

        # sort the neighbors based on their neighbor count
        sorted_graph = {}
        for node, neighbors in self.graph_.iteritems():
            neighbors.sort(key=itemgetter(1))
            neighbors = [neighbor[0] for neighbor in neighbors]
            sorted_graph[node] = neighbors
        #print sorted_graph

        # Breadth first traversal/Level wise traversal
        top = 'system'
        level = 0
        visited, queue = [], [top]  # system is default top level
        while queue:
            vertex = queue.pop(0)
            self.levels[vertex] = level
            if sorted_graph[vertex] and vertex not in visited:
                visited.append(vertex)
                for node in sorted_graph[vertex]:
                    if node not in visited:
                        queue.append(node)
                level += 1