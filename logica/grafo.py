# Grafo implementado mediante un diccionario de adyacencias.
# Relaciona estudiantes, actividades y beneficios.


# Crea un grafo vacío.
def crear_grafo():
    return {
        "adyacencias": {}
    }


# Agrega un nodo al grafo si todavía no existe.
def agregar_nodo(grafo, nodo):
    if nodo not in grafo["adyacencias"]:
        grafo["adyacencias"][nodo] = []


# Crea una relación dirigida entre dos nodos.
def agregar_arista(grafo, nodo_origen, nodo_destino, relacion):
    agregar_nodo(grafo, nodo_origen)
    agregar_nodo(grafo, nodo_destino)

    conexion = {
        "destino": nodo_destino,
        "relacion": relacion
    }

    grafo["adyacencias"][nodo_origen].append(conexion)


# Devuelve todos los nodos registrados en el grafo.
def obtener_nodos(grafo):
    return list(grafo["adyacencias"].keys())


# Devuelve las conexiones de un nodo específico.
def obtener_conexiones(grafo, nodo):
    return grafo["adyacencias"].get(nodo, [])


# Devuelve el grafo completo para mostrarlo en la interfaz.
def obtener_grafo(grafo):
    return grafo["adyacencias"]