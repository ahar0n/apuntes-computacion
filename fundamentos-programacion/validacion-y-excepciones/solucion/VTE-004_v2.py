

def validar_lectura(lectura):

    try:
        valor = int(lectura)
    except ValueError:
        print("Las lecturas deben ser valores numéricos.")
        return False, None

    if not(0 <= valor <= 100):
        print("El valor de cada brillo debe estar entre 0 y 100.")
        return False, None

    return True, valor


def lecturas_a_lista(lecturas):

    # separar lecturas
    lectura = ''
    lista_de_lecturas_str = []
    for caracter in lecturas:
        if caracter == ',':
            lista_de_lecturas_str.append(lectura)
            lectura = ''
        else:
            lectura += caracter
    lista_de_lecturas_str.append(lectura)

    lista_de_lecturas_int = []
    for lectura_str in lista_de_lecturas_str:
        es_valida, lectura_int = validar_lectura(lectura_str)
        if not es_valida:
            return []
        lista_de_lecturas_int.append(lectura_int)

    return lista_de_lecturas_int


def detectar_destellos(lecturas):

    destellos = []
    i = 1
    while i < len(lecturas)-1:

        anterior, actual, posterior = lecturas[i-1], lecturas[i], lecturas[i+1]
        if anterior < actual > posterior:
            destellos.append((i, actual))
        i += 1
    return destellos


def main():

    while True:
        lecturas_str = input('Ingrese lecturas: ')
        lista_de_lecturas = lecturas_a_lista(lecturas_str)

        if 4 <= len(lista_de_lecturas) <= 12:
            destellos = detectar_destellos(lista_de_lecturas)
            print(destellos)
            break

        print("Debe ingresar entre 4 y 12 lecturas.")


main()