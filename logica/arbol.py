# Árbol binario de búsqueda implementado con diccionarios y funciones.
# Se utiliza para organizar y buscar actividades por su nombre.


# Crea un árbol vacío.
def crear_arbol():
    return {
        "raiz": None
    }


# Crea un nodo del árbol con una clave de búsqueda y la actividad asociada.
def crear_nodo_arbol(clave, actividad):
    return {
        "clave": clave.lower(),
        "actividad": actividad,
        "izquierda": None,
        "derecha": None
    }


# Inserta una actividad en el árbol utilizando su nombre como clave.
def insertar(arbol, actividad):
    arbol["raiz"] = insertar_nodo(
        arbol["raiz"],
        actividad["nombre"],
        actividad
    )


# Inserta un nodo de forma recursiva respetando el orden alfabético.
def insertar_nodo(nodo, clave, actividad):
    # Si llega a una posición vacía, crea el nuevo nodo.
    if nodo is None:
        return crear_nodo_arbol(clave, actividad)

    # Si el nombre es menor, se inserta en la rama izquierda.
    if clave.lower() < nodo["clave"]:
        nodo["izquierda"] = insertar_nodo(
            nodo["izquierda"],
            clave,
            actividad
        )
    else:
        # Si es mayor o igual, se inserta en la rama derecha.
        nodo["derecha"] = insertar_nodo(
            nodo["derecha"],
            clave,
            actividad
        )

    return nodo


# Busca una actividad por su nombre exacto.
def buscar(arbol, nombre):
    return buscar_nodo(arbol["raiz"], nombre.lower())


# Busca de forma recursiva comparando la clave con el nombre solicitado.
def buscar_nodo(nodo, nombre):
    if nodo is None:
        return None

    if nombre == nodo["clave"]:
        return nodo["actividad"]

    if nombre < nodo["clave"]:
        return buscar_nodo(nodo["izquierda"], nombre)

    return buscar_nodo(nodo["derecha"], nombre)


# Recorre el árbol en orden y devuelve las actividades ordenadas alfabéticamente.
def recorrer_inorden(arbol):
    actividades = []
    recorrer_nodo(arbol["raiz"], actividades)
    return actividades


# Recorrido inorden: izquierda, nodo actual y derecha.
def recorrer_nodo(nodo, actividades):
    if nodo is not None:
        recorrer_nodo(nodo["izquierda"], actividades)
        actividades.append(nodo["actividad"])
        recorrer_nodo(nodo["derecha"], actividades)