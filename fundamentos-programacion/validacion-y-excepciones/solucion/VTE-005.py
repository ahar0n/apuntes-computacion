
def validar_panel(panel):
    """Valida las dimensiones y los valores del panel."""

    if type(panel) != list:
        return "El panel debe ser una lista."

    filas = len(panel)

    if filas < 2 or filas > 8:
        return "El panel debe tener entre 2 y 8 filas."

    if type(panel[0]) != list:
        return "Cada fila debe ser una lista."

    columnas = len(panel[0])

    if columnas < 2 or columnas > 8:
        return "El panel debe tener entre 2 y 8 columnas."

    for fila in panel:
        if type(fila) != list:
            return "Cada fila debe ser una lista."

        if len(fila) != columnas:
            return "Todas las filas deben tener igual longitud."

        for valor in fila:
            if type(valor) != int or (valor != 0 and valor != 1):
                return "Las luces deben tener valores 0 o 1."

    return ""


def contar_vecinas(panel, fila, columna):
    """Cuenta las luces encendidas alrededor de una posición."""

    filas = len(panel)
    columnas = len(panel[0])
    cantidad = 0

    desplazamientos = [
        [-1, 0],  # Arriba
        [1, 0],   # Abajo
        [0, -1],  # Izquierda
        [0, 1]    # Derecha
    ]

    for desplazamiento in desplazamientos:
        i = fila + desplazamiento[0]
        j = columna + desplazamiento[1]

        if 0 <= i < filas and 0 <= j < columnas:
            cantidad += panel[i][j]

    return cantidad


def construir_siguiente_estado(panel):
    """Construye un nuevo panel aplicando la regla."""

    siguiente = []

    for i in range(len(panel)):
        nueva_fila = []

        for j in range(len(panel[i])):
            vecinas = contar_vecinas(panel, i, j)

            if vecinas == 2:
                nueva_fila.append(1)
            else:
                nueva_fila.append(0)

        siguiente.append(nueva_fila)

    return siguiente


def siguiente_estado(panel):
    """Valída el panel y obtiene su siguiente estado."""

    mensaje = validar_panel(panel)

    if mensaje != "":
        return None, mensaje

    nuevo_panel = construir_siguiente_estado(panel)

    return nuevo_panel, ""


def mostrar_panel(panel):
    """Muestra las filas y columnas de un panel."""

    for fila in panel:
        for valor in fila:
            print(valor, end=" ")
        print()
