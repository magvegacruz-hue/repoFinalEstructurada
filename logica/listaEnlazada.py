# Lista enlazada simple implementada con diccionarios y funciones.
# Se utiliza para almacenar las solicitudes pendientes en orden de llegada.


# Crea una lista enlazada vacía.
def crear_lista():
    return {
        "cabeza": None
    }


# Crea un nodo individual que guarda una solicitud y la referencia al siguiente nodo.
def crear_nodo(dato):
    return {
        "dato": dato,
        "siguiente": None
    }


# Agrega una solicitud al final de la lista enlazada.
def agregar(lista, dato):
    nuevo_nodo = crear_nodo(dato)

    # Si la lista está vacía, el nuevo nodo se convierte en la cabeza.
    if lista["cabeza"] is None:
        lista["cabeza"] = nuevo_nodo
        return

    # Recorre la lista hasta llegar al último nodo.
    actual = lista["cabeza"]

    while actual["siguiente"] is not None:
        actual = actual["siguiente"]

    # Conecta el último nodo con el nuevo nodo.
    actual["siguiente"] = nuevo_nodo


# Elimina una solicitud de la lista utilizando su ID.
def eliminar_por_id(lista, id_solicitud):
    actual = lista["cabeza"]
    anterior = None

    while actual is not None:
        # Si encuentra la solicitud, ajusta las conexiones para eliminarla.
        if actual["dato"]["id_solicitud"] == id_solicitud:
            if anterior is None:
                lista["cabeza"] = actual["siguiente"]
            else:
                anterior["siguiente"] = actual["siguiente"]

            return True

        anterior = actual
        actual = actual["siguiente"]

    return False


# Recorre la lista y devuelve todas las solicitudes almacenadas.
def obtener_todos(lista):
    elementos = []
    actual = lista["cabeza"]

    while actual is not None:
        elementos.append(actual["dato"])
        actual = actual["siguiente"]

    return elementos


# Indica si la lista no contiene solicitudes.
def esta_vacia(lista):
    return lista["cabeza"] is None