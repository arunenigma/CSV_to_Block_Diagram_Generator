import pygraphviz as pgv


def draw_layout():
    graph = pgv.AGraph(directed=True, compound=True, rank='same',
                       splines='ortho', multiedges=True,
                       strict=True, overlap=False, rankdir='LR', ranksep='2')

    graph.add_node('A')

    label = '<<TABLE BGCOLOR="bisque"><TR><TD COLSPAN="3">elephant</TD> <TD ROWSPAN="2" BGCOLOR="chartreuse" VALIGN="bottom" ALIGN="right">two</TD> </TR><TR><TD COLSPAN="2" ROWSPAN="2"><TABLE BGCOLOR="grey"><TR> <TD>corn</TD> </TR> <TR> <TD BGCOLOR="yellow">c</TD> </TR> <TR> <TD>f</TD> </TR> </TABLE> </TD><TD BGCOLOR="white">penguin</TD> </TR><TR> <TD COLSPAN="2" BORDER="4" ALIGN="right" PORT="there">4</TD> </TR></TABLE>>'
    graph.get_node('A').attr.update({'shape': 'plaintext', 'label': label})
    graph.add_edge('B', 'C')

    f = open('demo.dot', 'wb')
    f.write(graph.string())
    f.close()
    g = pgv.AGraph(file='demo.dot')
    g.layout(prog='dot')
    g.draw('demo.pdf')
    g.close()


draw_layout()