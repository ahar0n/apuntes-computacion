def leer_observaciones(archivo_de_observaciones):

    observaciones = []
    try:
        fid = open(archivo_de_observaciones)
    except FileNotFoundError:
        print("ERROR: Archivo no encontrado.")
        return observaciones

    while True:
        linea = fid.readline()

        if linea == "":
            break

        if linea[-1] == "\n":
            linea = linea[:-1]

        if linea == '-999':
            observaciones.append(None)
            continue

        observaciones.append(float(linea))

    fid.close()

    return observaciones


def leer_mensajes(archivo):

    mensajes = []

    try:
        fid = open(archivo, "r")
    except FileNotFoundError:
        print("ERROR: Archivo no encontrado.")
        return mensajes

    while True:

        linea = fid.readline()
        if linea == "":
            break

        if linea[-1] == '\n':
            linea = linea[:-1]

        mensajes.append(separar_texto(linea, ' ', eliminar_puntuacion=True))

    fid.close()

    return mensajes


def separar_texto(texto, delimitador, eliminar_puntuacion=True):
    """Separa texto (no vacío) en un delimitador

    :param eliminar_puntuacion:
    :param texto:
    :param delimitador:
    :return:
    """

    segmentos = []
    segmento = ''

    for caracter in texto:
        if caracter == delimitador:
            if segmento != '':
                segmentos.append(segmento)
            segmento = ''
            continue

        segmento = segmento + caracter
    segmentos.append(segmento) # utimo segmento

    if eliminar_puntuacion:
        puntuacion = "¡!¿?.,;:-()"
        segmentos_limpios = []
        for segmento in segmentos:
            segmento_sin_puntuacion = remueve_simbolos(segmento, puntuacion)
            segmentos_limpios.append(segmento_sin_puntuacion)

        segmentos = segmentos_limpios

    return segmentos


def remueve_simbolos(texto, simbolos):

    texto_limpio = ''
    for caracter in texto:
        if caracter in simbolos:
            continue
        texto_limpio += caracter

    return texto_limpio


def juntar_segmentos(segmentos, delimitador):

    secuencia = ''
    for segmento in segmentos:
        secuencia += segmento + delimitador

    if secuencia[-1] == delimitador:
        secuencia = secuencia[:-1]

    return secuencia



if __name__ == '__main__':

    lista_mensajes = leer_mensajes("../datos/mensajes.txt")
    for mensaje in lista_mensajes:
        print(mensaje)
        input()
