

def alternar_signos(secuencia):

    secuencia_alternada = []
    i = 0
    while i < len(secuencia):
        print(i)

        valor = secuencia[i]
        if not(i % 2 == 0):
            valor = -secuencia[i]

        secuencia_alternada += [valor]

        i += 1

    return secuencia_alternada


def intercambiar(datos, i, j):

    aux = datos[i]
    datos[i] = datos[j]
    datos[j] = aux


def promedio_ventana(secuencia, inicio, k):

    i = inicio
    suma = 0
    while i < (inicio + k):
        suma += secuencia[i]
        i += 1

    return suma / k


def promedios_moviles(secuencia, k):

    i = 0
    promedios = []
    while i <= (len(secuencia) - k):

        j = 0
        suma = 0
        while j < k:
            suma += secuencia[i+j]
            j += 1

        promedios += [suma / k]

        i += 1

    return tuple(promedios)


print(promedios_moviles((4, 8), 1))





