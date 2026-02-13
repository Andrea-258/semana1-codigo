import networkx as nx
import random
import math
import matplotlib.pyplot as plt
from collections import deque


# 1. CREAMOS UN GRAFO DIRIGIDO CON PESOS EN 3D
def crear_grafo_3d(n_nodos=15, distancia_max=5.0, prob_arista=0.6):

    G = nx.DiGraph()

    # Creamos nodos con posición 3D
    for i in range(n_nodos):
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        z = random.uniform(0, 10)
        G.add_node(i, pos=(x, y, z))

    pos = nx.get_node_attributes(G, 'pos')

    # Definimos aristas en función de la distancia euclídea 3D
    for i in range(n_nodos):
        for j in range(n_nodos):
            if i != j:
                d = math.sqrt((pos[i][0] - pos[j][0]) ** 2 + (pos[i][1] - pos[j][1]) ** 2 + (pos[i][2] - pos[j][2]) ** 2)
                if d <= distancia_max and random.random() < prob_arista:
                    G.add_edge(i, j, weight=d)

    return G


# 2. DEFINIMOS BFS (camino óptimo en número de saltos)
def bfs(G, inicio, fin):
    cola = deque([inicio])
    visitados = {inicio}
    padre = {inicio: None}

    while cola:
        actual = cola.popleft()

        if actual == fin:
            break

        for vecino in G.successors(actual):
            if vecino not in visitados:
                visitados.add(vecino)
                padre[vecino] = actual
                cola.append(vecino)

    if fin not in padre:
        return None

    camino = []
    nodo = fin
    while nodo is not None:
        camino.append(nodo)
        nodo = padre[nodo]

    return camino[::-1]


# 3. DEFINIMOS DFS ITERATIVO
def dfs_iterative(G, start):
    visited = set()
    stack = [start]
    recorrido = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            recorrido.append(node)

            vecinos = list(G.successors(node))
            stack.extend(reversed(vecinos))

    return recorrido


# 4. VISUALIZACIÓN 3D
def dibujar_grafo_3d(G, camino_bfs=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    pos = nx.get_node_attributes(G, 'pos')

    # Dibujar nodos
    for nodo, (x, y, z) in pos.items():
        ax.scatter(x, y, z)
        ax.text(x, y, z, str(nodo), size=8)

    # Dibujar aristas
    for u, v in G.edges():
        x = [pos[u][0], pos[v][0]]
        y = [pos[u][1], pos[v][1]]
        z = [pos[u][2], pos[v][2]]
        ax.plot(x, y, z, alpha=0.5)

    # Dibujar camino BFS
    if camino_bfs:
        for i in range(len(camino_bfs) - 1):
            u = camino_bfs[i]
            v = camino_bfs[i + 1]
            x = [pos[u][0], pos[v][0]]
            y = [pos[u][1], pos[v][1]]
            z = [pos[u][2], pos[v][2]]
            ax.plot(x, y, z, linewidth=3)

    ax.set_title("Grafo dirigido 3D")
    plt.show()


# 5. PROGRAMA PRINCIPAL
if __name__ == "__main__":
    G = crear_grafo_3d()

    inicio = 0
    fin = 10

    recorrido_dfs = dfs_iterative(G, inicio)
    print("DFS:", recorrido_dfs)

    camino_bfs = bfs(G, inicio, fin)
    print("BFS:", camino_bfs)

    dibujar_grafo_3d(G, camino_bfs)
