import networkx as nx
import math
import matplotlib.pyplot as plt
import os

def nearest_neighbor_order(points):
    """
    Ordena uma lista de pontos usando a heurística do vizinho mais próximo.
    
    Parâmetros:
    - points: lista de tuplas (x, y)
    
    Retorna:
    - order: lista de pontos ordenados
    """
    pts = points.copy()
    order = []
    current = pts.pop(0)
    order.append(current)

    while pts:
        # Calcula distância euclidiana para os pontos restantes
        dists = [math.hypot(current[0] - p[0], current[1] - p[1]) for p in pts]
        idx = dists.index(min(dists))
        current = pts.pop(idx)
        order.append(current)

    return order

def find_closest_graph_node(G, point):
    """
    Encontra o nó do grafo mais próximo de um ponto (x, y).
    
    Parâmetros:
    - G: NetworkX graph com atributo 'pos' nos nós
    - point: tupla (x, y)
    
    Retorna:
    - best: nó mais próximo
    """
    best = None
    best_d = float('inf')
    for n, data in G.nodes(data=True):
        x, y = data['pos']
        d = math.hypot(point[0] - x, point[1] - y)
        if d < best_d:
            best = n
            best_d = d
    return best

def compute_routes_for_clusters(G, df, centers, output_dir='outputs'):
    """
    Calcula rotas para cada cluster usando heurística de vizinho mais próximo
    e A* no grafo, salvando gráficos das rotas.
    
    Parâmetros:
    - G: grafo NetworkX
    - df: DataFrame com colunas ['x','y','cluster']
    - centers: coordenadas dos centros dos clusters
    - output_dir: diretório para salvar imagens
    
    Retorna:
    - routes: dicionário com pontos ordenados e distância por cluster
    - metrics: métricas gerais de distância total e por cluster
    """
    os.makedirs(output_dir, exist_ok=True)
    routes = {}
    metrics = {'total_distance': 0, 'clusters': {}}

    for c in sorted(df['cluster'].unique()):
        cluster_points = df[df['cluster'] == c][['x', 'y']].values.tolist()
        if len(cluster_points) == 0:
            continue

        # Ordena os pontos do cluster
        ordered = nearest_neighbor_order(cluster_points)
        path_nodes = []
        dist_sum = 0

        # Constrói a rota usando A* entre cada ponto
        for i in range(len(ordered) - 1):
            a = find_closest_graph_node(G, ordered[i])
            b = find_closest_graph_node(G, ordered[i + 1])
            try:
                path = nx.astar_path(
                    G,
                    a,
                    b,
                    heuristic=lambda u, v: math.hypot(
                        G.nodes[u]['pos'][0] - G.nodes[v]['pos'][0],
                        G.nodes[u]['pos'][1] - G.nodes[v]['pos'][1]
                    ),
                    weight='weight'
                )

                # Calcula distância da rota
                d = sum(G.edges[u, v]['weight'] for u, v in zip(path[:-1], path[1:]))
                dist_sum += d
                path_nodes.extend(path)
            except nx.NetworkXNoPath:
                continue

        # Armazena rotas e métricas
        routes[c] = {'ordered_points': ordered, 'distance': dist_sum}
        metrics['total_distance'] += dist_sum
        metrics['clusters'][c] = {'n_points': len(ordered), 'distance': dist_sum}

        # Plot da rota
        xs = [p[0] for p in ordered]
        ys = [p[1] for p in ordered]
        plt.figure(figsize=(6, 6))
        plt.plot(xs, ys, marker='o')
        plt.title(f'Rota cluster {c} (dist ~ {dist_sum:.2f})')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig(os.path.join(output_dir, f'routes_cluster_{c}.png'))
        plt.close()

    return routes, metrics

