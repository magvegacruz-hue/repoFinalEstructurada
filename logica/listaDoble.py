# Lista doblemente enlazada implementada con diccionarios y funciones.
# Se utiliza para guardar el historial de solicitudes de cada estudiante.


# Crea una lista doblemente enlazada vacía.
def crear_lista_doble():
    return {
        "inicio": None,
        "fin": None
    }


# Crea un nodo con referencia al nodo anterior y al siguiente.
def crear_nodo_doble(dato):
    return {
        "dato": dato,
        "anterior": None,
        "siguiente": None
    }


# Agrega una solicitud al final del historial.
def agregar(lista, dato):
    nuevo_nodo = crear_nodo_doble(dato)

    # Si la lista está vacía, el nuevo nodo es inicio y fin.
    if lista["inicio"] is None:
        lista["inicio"] = nuevo_nodo
        lista["fin"] = nuevo_nodo
        return

    # Conecta el nuevo nodo con el último nodo existente.
    nuevo_nodo["anterior"] = lista["fin"]
    lista["fin"]["siguiente"] = nuevo_nodo
    lista["fin"] = nuevo_nodo


# Recorre la lista desde el inicio y devuelve todas las solicitudes.
def obtener_todos(lista):
    elementos = []
    actual = lista["inicio"]

    while actual is not None:
        elementos.append(actual["dato"])
        actual = actual["siguiente"]

    return elementos


# Devuelve la solicitud anterior a una solicitud específica.
def obtener_anterior(lista, id_solicitud):
    actual = lista["inicio"]

    while actual is not None:
        if actual["dato"]["id_solicitud"] == id_solicitud:
            if actual["anterior"] is not None:
                return actual["anterior"]["dato"]

            return None

        actual = actual["siguiente"]

    return None


# Devuelve la solicitud siguiente a una solicitud específica.
def obtener_siguiente(lista, id_solicitud):
    actual = lista["inicio"]

    while actual is not None:
        if actual["dato"]["id_solicitud"] == id_solicitud:
            if actual["siguiente"] is not None:
                return actual["siguiente"]["dato"]

            return None

        actual = actual["siguiente"]

    return None