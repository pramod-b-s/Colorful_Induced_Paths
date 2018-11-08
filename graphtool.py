from graph_tool.all import *

def deg_sampler():
    return 2

g = random_graph(6,deg_sampler,directed=False)

# g = graph_tool.generation.random_graph(6,directed=False)

graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(200, 200), output="graph.png")
