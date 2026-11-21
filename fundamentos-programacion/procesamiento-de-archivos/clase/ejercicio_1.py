from csv import reader


def leer_niveles(archivo, simbolo_decimal=','):

    fechas, niveles = [], []

    try:
        fid = open(archivo)
    except FileNotFoundError:
        print('Archivo no encontrado!')
        return fechas, niveles

    registros = reader(fid, delimiter=';')

    encabezado = True
    for registro in registros:
        if encabezado:
            encabezado = False
            continue

        fecha = registro[0]
        nivel = registro[1]

        if simbolo_decimal in nivel:
            nivel = convierte_a_decimal(nivel, simbolo_decimal)

        fechas.append(fecha)
        niveles.append(nivel)

    fid.close()

    return fechas, niveles


def convierte_a_decimal(campo, simbolo):

    idx = campo.index(simbolo)
    decimal = campo[:idx] + '.' + campo[idx+1:]

    return float(decimal)



if __name__ == '__main__':

    mi_archivo = "../registros/niveles_coma_decimal.csv"
    fechas, niveles = leer_niveles(mi_archivo)

    for i in range(len(fechas)):
        print(fechas[i], ':', niveles[i])