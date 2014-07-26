import pygraphviz as pgv


def draw_layout():
    graph = pgv.AGraph(directed=True, compound=True, rank='same',
                       splines='ortho', multiedges=True,
                       strict=True, overlap=False, rankdir='LR', ranksep='2')

    graph.add_node('A')
    graph.add_edge('B', 'C')
    #graph.subgraph(['B', 'C'], name='cluster_1')
    s = graph.subgraph(['B', 'C'], name='cluster_1')

    # adding a node into a subgraph
    s.add_node('X')
    s.add_edge('T', 'U')
    s.add_node('aa', style='invis')

    xx = s.subgraph(['T', 'U', 'aa'], name='cluster_11', label='arun')
    s.add_edge('R', 'P')

    s.add_node('bb', style='invis')
    yy = s.subgraph(['R', 'P', 'bb'], name='cluster_12', label='hari')


    """
    s.add_edge('T', 'R', ltail='cluster_11',

               lhead='cluster_12', name='arun', xlabel='arun'
    )
    s.add_edge('aa', 'R', ltail='cluster_11',

               lhead='cluster_12', name='hari', xlabel='hari'
    )


    s.add_edge('aa', 'bb', ltail='cluster_11',

               lhead='cluster_12', name='hai', xlabel='baba'
    )
    """

    # add edges between arun and hari
    s.add_edge('X', 'T')



    f = open('demo.dot', 'wb')
    f.write(graph.string())
    f.close()
    g = pgv.AGraph(file='demo.dot')
    g.layout(prog='dot')
    g.draw('demo.pdf')
    g.close()




draw_layout()