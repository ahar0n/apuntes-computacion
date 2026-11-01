def validar_imagen(imagen):
    if not 1 <= len(imagen) <= 6:
        return "La imagen debe tener entre 1 y 6 filas."

    columnas = len(imagen[0])

    if not 1 <= columnas <= 6:
        return "La imagen debe tener entre 1 y 6 columnas."

    for fila in imagen:
        if len(fila) != columnas:
            return "Todas las filas deben tener la misma cantidad de píxeles."

        for pixel in fila:
            if len(pixel) != 3:
                return "Cada píxel debe tener exactamente tres componentes."

            for componente in pixel:
                if not 0 <= componente <= 255:
                    return "Todas las componentes deben estar entre 0 y 255."

    return ""


def transformar_imagen(imagen, operacion):
    # Recibe una imagen y una operación previamente validadas.
    resultado = []

    for fila in imagen:
        nueva_fila = []

        if operacion == "ESPEJO":
            for c in range(len(fila) - 1, -1, -1):
                nueva_fila.append(fila[c])
        else:
            for rojo, verde, azul in fila:
                nueva_fila.append(
                    (255 - rojo, 255 - verde, 255 - azul)
                )

        resultado.append(nueva_fila)

    return resultado


def mostrar_imagen(imagen):
    for fila in imagen:
        print(fila)


def ejecutar_editor(imagen):
    mensaje = validar_imagen(imagen)

    if mensaje != "":
        print(mensaje)
        return

    while True:
        operacion = input("Operación (ESPEJO o NEGATIVO): ")

        if operacion in ("ESPEJO", "NEGATIVO"):
            break

        print("Operación desconocida.")

    resultado = transformar_imagen(imagen, operacion)

    print("Imagen original:")
    mostrar_imagen(imagen)

    print("Imagen transformada:")
    mostrar_imagen(resultado)


imagen = [
    [(255, 255, 255), (255, 0, 0),     (255, 255, 255), (255, 0, 0),     (255, 255, 255)],
    [(255, 0, 0),     (255, 0, 0),     (255, 0, 0),     (255, 0, 0),     (255, 0, 0)],
    [(255, 0, 0),     (255, 0, 0),     (255, 0, 0),     (255, 0, 0),     (255, 0, 0)],
    [(255, 255, 255), (255, 0, 0),     (255, 0, 0),     (255, 0, 0),     (255, 255, 255)],
    [(255, 255, 255), (255, 255, 255), (255, 0, 0),     (255, 255, 255), (255, 255, 255)],
]

ejecutar_editor(imagen)