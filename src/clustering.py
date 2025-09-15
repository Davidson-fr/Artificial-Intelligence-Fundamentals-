from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os

def cluster_deliveries(X, k=3):
    """
    Agrupa entregas usando KMeans e salva o gráfico dos clusters.
    
    Parâmetros:
    - X: array-like, coordenadas das entregas (n_samples, 2)
    - k: int, número de clusters
    
    Retorna:
    - labels: array de rótulos de cluster para cada ponto
    - centers: coordenadas dos centros dos clusters
    """
    # Inicializa o KMeans
    kmeans = KMeans(n_clusters=k, random_state=0)
    labels = kmeans.fit_predict(X)
    centers = kmeans.cluster_centers_

    # Garante que o diretório de saída exista
    os.makedirs('outputs', exist_ok=True)

    # Plotando os clusters
    plt.figure(figsize=(6, 6))
    plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', alpha=0.6, edgecolor='k')
    plt.scatter(centers[:, 0], centers[:, 1], marker='x', s=100, c='red', label='Centros')
    plt.title('Clusters de entregas')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.savefig('outputs/clusters.png')
    plt.close()

    return labels, centers
