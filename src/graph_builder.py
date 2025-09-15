import networkx as nx
import math

def build_grid_graph(width=100, height=100, step=5):
     
    G = nx.Graph()

    xs = list(range(0, width + 1, step))
    ys = list(range(0, height + 1, step))

    # Adiciona nós com atributo 'pos'
    for x in xs:
        for y in ys:
            G.add_node((x, y), pos=(x, y))

    # Adiciona arestas horizontais e verticais com peso igual à distância euclidiana
    for x in xs:
        for y in ys:
            if (x + step, y) in G:
                dist = math.hypot(step, 0)
                G.add_edge((x, y), (x + step, y), weight=dist)
            if (x, y + step) in G:
                dist = math.hypot(0, step)
                G.add_edge((x, y), (x, y + step), weight=dist)

    return G
