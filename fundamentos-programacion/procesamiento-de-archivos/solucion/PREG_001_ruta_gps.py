from math import hypot
from csv import DictReader


def procesar_recorrido(archivo):

    try:
        fid = open(archivo)
    except FileNotFoundError:
        print('ERROR: Archivo no encontrado!')
        return None, None

    recorrido = 0
    tramo_mas_largo = ("", "", 0)

    posiciones = DictReader(fid)

    primera = True
    for actual in posiciones:

        if primera:
            primera = False

        else:

            dh = distancia(
                float(anterior['este_m']), float(anterior['norte_m']),
                float(actual['norte_m']), float(actual['norte_m'])
            )
            recorrido += dh

            if dh > tramo_mas_largo[2]:
                tramo_mas_largo = anterior['id_punto'], actual['id_punto'], dh

        anterior = actual

    fid.close()

    return redondear(recorrido/1000, 3), tramo_mas_largo


def distancia(e1, n1, e2, n2):
    return hypot(e2-e1, n2-n1)


def redondear(numero, decimales):

    factor = 10 ** decimales
    entero = int(numero * factor + 0.5)

    return entero / factor


if __name__ == '__main__':

    archivo_recorrido = "../registros/ruta_gps.wpoint"
    total, mas_largo = procesar_recorrido(archivo_recorrido)

    print(f"{total:.3f}", mas_largo)