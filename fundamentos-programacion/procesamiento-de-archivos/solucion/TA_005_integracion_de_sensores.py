from lectura import leer_observaciones

def absoluto(x):
    if x < 0:
        return -x
    return x


def promedio(serie):
    suma = 0
    for i in serie:
        suma += i

    return suma / len(serie)


def integrar_datos(a, b, tolerancia):

    integrados = []

    i = 0
    while i < 24:

        lectura_a = a[i]
        lectura_b = b[i]

        valor = -999

        if lectura_a is not None:
            valor = lectura_a

        if lectura_b is not None:
            valor = lectura_b

        # Ambos None
        if (lectura_a is not None) and (lectura_b is not None):
            print(lectura_a, lectura_b)
            diferencia = absoluto(lectura_a - lectura_b)
            if diferencia < tolerancia:
                valor = promedio([lectura_a, lectura_b])
            else:
                valor = -999

        integrados.append(valor)
        i += 1

    return integrados


if __name__ == '__main__':
    sensor_a = leer_observaciones("../datos/sensor_a.txt")
    sensor_b = leer_observaciones("../datos/sensor_b.txt")

    integrados = integrar_datos(sensor_a, sensor_b, 1)

    print(integrados)

