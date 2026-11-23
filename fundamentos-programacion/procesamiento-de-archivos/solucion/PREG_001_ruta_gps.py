from math import hypot
from csv import DictReader


def procesar_recorrido(archivo):

    try:
        fid = open(archivo)
    except FileNotFoundError:
        print('Archivo no encontrado!')
        return None, None

    recorrido = 0
    tramo_mas_largo = (None, None, 0)
    posiciones = DictReader(fid)
    primero = True
    for actual in posiciones:
        if primero:
            anterior = actual
            primero = False

        dn = float(actual['norte_m']) - float(anterior['norte_m'])
        de = float(actual['este_m']) - float(anterior['este_m'])

        dh = distancia(de, dn)
        recorrido += dh

        if dh > tramo_mas_largo[2]:
            tramo_mas_largo = anterior['id_punto'], actual['id_punto'], dh

        anterior = actual

    fid.close()

    return redondear(recorrido/1000, 3), tramo_mas_largo


def distancia(a, b):
    return hypot(a, b)


def redondear(numero, decimales):

    factor = 10 ** decimales
    entero = int(numero * factor + 0.5)

    return entero / factor


if __name__ == '__main__':

    archivo_recorrido = "../registros/ruta_gps.wpoint"
    total, mas_largo = procesar_recorrido(archivo_recorrido)

    print(total, mas_largo)