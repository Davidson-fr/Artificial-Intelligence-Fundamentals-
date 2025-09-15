import os
import argparse
import pandas as pd
import numpy as np
from clustering import cluster_deliveries
from graph_builder import build_grid_graph
from routing import compute_routes_for_clusters

OUTPUT_DIR = 'outputs'
DATA_PATH = 'data/sample_deliveries.csv'

def generate_sample_csv(path=DATA_PATH, n=30, seed=42):
    """
    Gera um CSV de amostra com coordenadas aleatórias para entregas.
    """
    np.random.seed(seed)
    xs = np.random.uniform(0, 100, size=n)
    ys = np.random.uniform(0, 100, size=n)
    df = pd.DataFrame({'id': range(n), 'x': xs, 'y': ys})
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f'Sample saved to {path}')

def main(k=3, generate_sample=False):
    """
    Função principal que executa o fluxo:
    - Gera amostra de entregas (opcional)
    - Lê CSV de entregas
    - Constrói o grafo
    - Agrupa entregas por cluster
    - Calcula rotas para cada cluster
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Gera CSV caso não exista ou se solicitado
    if generate_sample or not os.path.exists(DATA_PATH):
        generate_sample_csv()

    df = pd.read_csv(DATA_PATH)

    # Construindo o grafo de grade
    G = build_grid_graph(width=100, height=100, step=5)

    # Clusterização das entregas
    labels, centers = cluster_deliveries(df[['x', 'y']].values, k)
    df['cluster'] = labels

    # Calculando rotas
    routes, metrics = compute_routes_for_clusters(G, df, centers, OUTPUT_DIR)

    print('Metrics summary:')
    print(metrics)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--k', type=int, default=3, help='Número de clusters')
    parser.add_argument('--generate_sample', action='store_true', help='Gerar CSV de amostra')
    args = parser.parse_args()

    main(k=args.k, generate_sample=args.generate_sample)
