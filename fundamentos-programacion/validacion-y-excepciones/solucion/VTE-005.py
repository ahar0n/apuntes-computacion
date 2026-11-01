def validar_panel(panel):
    if not 2 <= len(panel) <= 8:
        return "El panel debe tener entre 2 y 8 filas."

    columnas = len(panel[0])

    if not 2 <= columnas <= 8:
        return "El panel debe tener entre 2 y 8 columnas."

    for fila in panel:
        if len(fila) != columnas:
            return "Todas las filas deben tener la misma cantidad de elementos."

        for luz in fila:
            if luz not in (0, 1):
                return "Cada elemento debe valer 0 o 1."

    return ""


def contar_vecinas(panel, fila, columna):
    encendidas = 0

    if fila > 0:
        encendidas += panel[fila - 1][columna]

    if fila < len(panel) - 1:
        encendidas += panel[fila + 1][columna]

    if columna > 0:
        encendidas += panel[fila][columna - 1]

    if columna < len(panel[0]) - 1:
        encendidas += panel[fila][columna + 1]

    return encendidas


def actualizar_panel(panel):
    mensaje = validar_panel(panel)

    if mensaje != "":
        return None, mensaje

    nuevo = []

    for fila in range(len(panel)):
        nueva_fila = []

        for columna in range(len(panel[0])):
            vecinas = contar_vecinas(panel, fila, columna)

            if vecinas == 2:
                nueva_fila.append(1)
            else:
                nueva_fila.append(0)

        nuevo.append(nueva_fila)

    return nuevo, ""


def mostrar_panel(panel):
    for fila in panel:
        print(fila)


paneles = [
    [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
    [[1, 1], [1, 1]],
    [[1, 1], [0, 0]],
    [[0, 0], [0, 0]],
    [[0, 1], [1]],
    [[0, 2], [1, 0]],
    [],
]

for numero, panel in enumerate(paneles, start=1):
    print(f"\nCaso {numero}")

    nuevo, mensaje = actualizar_panel(panel)

    if mensaje != "":
        print("Panel rechazado:", mensaje)
        continue

    print("Panel original:")
    mostrar_panel(panel)

    print("Siguiente estado:")
    mostrar_panel(nuevo)

panel = [[1, 1], [0, 0]]
esperado = [[0, 0], [0, 0]]

nuevo, mensaje = actualizar_panel(panel)

if mensaje == "":
    print("Actualización correcta:", nuevo == esperado)
    print("Original conservado:", panel == [[1, 1], [0, 0]])

    # Cambiar el resultado no debe modificar el original ni otra fila.
    nuevo[0][0] = 1

    print("Original independiente:", panel == [[1, 1], [0, 0]])
    print("Filas independientes:", nuevo[1] == [0, 0])