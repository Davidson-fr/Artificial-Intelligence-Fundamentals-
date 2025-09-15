# Delivery Routing Project - Artificial Intelligence Fundamentals

## Descrição

Este projeto é uma aplicação prática de **Inteligência Artificial e Algoritmos de Roteamento**.  
Ele gera rotas otimizadas para entregas usando **clusterização de pontos e grafos**, simulando cenários de logística.

O sistema realiza os seguintes passos:

1. **Geração de dados de entregas**: cria um CSV de amostra com coordenadas aleatórias.  
2. **Clusterização de entregas**: agrupa os pontos em clusters usando **KMeans**.  
3. **Construção do grafo de rotas**: gera uma **grade 2D** representando a área de entregas, com pesos baseados em distância euclidiana.  
4. **Cálculo de rotas por cluster**: utiliza a heurística do **vizinho mais próximo** combinada com **A\*** para encontrar rotas eficientes.  
5. **Visualização**: gera gráficos mostrando os clusters e as rotas, salvos na pasta `outputs/`.  

---

## Tecnologias

- Python 3.13  
- Bibliotecas:
  - `numpy`  
  - `pandas`  
  - `matplotlib`  
  - `scikit-learn`  
  - `networkx`  

---

## Estrutura do projeto


src/

├── main.py # Script principal

├── clustering.py # Clusterização de entregas

├── graph_builder.py # Construção do grafo de grade

└── routing.py # Cálculo de rotas e métricas

outputs/ # Gráficos gerados automaticamente

data/ # CSV de entregas gerado automaticamente


---

## Como executar

1. Clone o repositório:  
```bash
git clone <URL_DO_REPOSITORIO>

cd Artificial-Intelligence-Fundamentals



Instale as dependências:

pip install numpy pandas matplotlib scikit-learn networkx

Execute o script principal:

python src/main.py --generate_sample



Resultados:

Métricas de distância total e por cluster são exibidas no console.

Gráficos dos clusters e rotas são salvos na pasta outputs/.

Observações

O número de clusters pode ser ajustado com --k <numero>.

Se o CSV de entregas já existir, ele será usado; caso contrário, será gerado automaticamente.





