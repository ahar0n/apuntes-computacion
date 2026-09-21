def es_observacion_valida(valor):
    """Indica si valor pertenece al intervalo cerrado [0, 100]."""
    return 0 <= valor <= 100


def calcular_promedio(observaciones_validas):
    """Devuelve el promedio de una lista no vacía de observaciones válidas."""
    suma = 0
    cantidad = 0

    for valor in observaciones_validas:
        suma += valor
        cantidad += 1

    return suma / cantidad


def leer_observacion(posicion):
    """Lee y devuelve la observación situada en posicion."""
    return int(input(f"Observación {posicion}: "))


def mostrar_resumen(validas, rechazadas, promedio):
    """Muestra las cantidades y el promedio, cuando está definido."""
    print("Observaciones válidas:", validas)
    print("Observaciones rechazadas:", rechazadas)

    if promedio is None:
        print("Promedio no calculado: sin observaciones válidas")
    else:
        print("Promedio:", promedio)


def procesar_observaciones(cantidad):
    """Lee, clasifica y resume una cantidad positiva de observaciones."""
    observaciones_validas = []
    rechazadas = 0

    for posicion in range(1, cantidad + 1):
        valor = leer_observacion(posicion)

        if es_observacion_valida(valor):
            observaciones_validas.append(valor)
        else:
            rechazadas += 1

    validas = len(observaciones_validas)

    if validas > 0:
        promedio = calcular_promedio(observaciones_validas)
    else:
        promedio = None

    mostrar_resumen(validas, rechazadas, promedio)


cantidad = int(input("Cantidad de observaciones: "))
procesar_observaciones(cantidad)