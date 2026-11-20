# Implementación del método de ordenamiento por inserción.
# Ordena solicitudes o actividades según el campo seleccionado.


# La función "clave" permite indicar qué campo se utilizará para ordenar.
# Ejemplo: clave=lambda solicitud: solicitud["fecha_solicitud"]
def ordenar_por_insercion(lista, clave=lambda elemento: elemento):
    # Se trabaja sobre una copia para no modificar la lista original.
    lista_ordenada = lista.copy()

    # Comienza desde el segundo elemento porque el primero ya está "ordenado".
    for indice in range(1, len(lista_ordenada)):
        elemento_actual = lista_ordenada[indice]
        valor_actual = clave(elemento_actual)
        posicion = indice - 1

        # Desplaza los elementos mayores hacia la derecha.
        while posicion >= 0 and clave(lista_ordenada[posicion]) > valor_actual:
            lista_ordenada[posicion + 1] = lista_ordenada[posicion]
            posicion -= 1

        # Inserta el elemento actual en su posición correcta.
        lista_ordenada[posicion + 1] = elemento_actual

    return lista_ordenada