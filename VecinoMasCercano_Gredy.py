import networkx as nx
import numpy as np
import folium
from geopy.distance import geodesic

# Coordenadas de ejemplo (clientes)
locations = {
    "Centro": (19.4326, -99.1332),
    "Cliente 1": (19.4512, -99.1312),
    "Cliente 2": (19.4294, -99.1501),
    "Cliente 3": (19.4101, -99.1325)
}

# Crear grafo de distancias
G = nx.Graph()
for loc1, coord1 in locations.items():
    for loc2, coord2 in locations.items():
        if loc1 != loc2:
            dist = geodesic(coord1, coord2).km
            G.add_edge(loc1, loc2, weight=dist)

# Algoritmo de Vecino Más Cercano (Greedy)
def nearest_neighbor(G, start):
    path = [start]
    unvisited = set(G.nodes) - {start}
    while unvisited:
        last = path[-1]
        next_node = min(unvisited, key=lambda node: G[last][node]["weight"])
        path.append(next_node)
        unvisited.remove(next_node)
    path.append(start)  # Volver al inicio
    return path

# Calcular la ruta óptima
route = nearest_neighbor(G, "Centro")
print("Ruta:", " → ".join(route))

# Visualizar en mapa
m = folium.Map(location=locations["Centro"], zoom_start=14)
for loc, coord in locations.items():
    folium.Marker(coord, popup=loc).add_to(m)

# Dibujar ruta
coords = [locations[loc] for loc in route]
folium.PolyLine(coords, color="blue", weight=2.5, opacity=0.8).add_to(m)
m.save("ruta_optima.html")
