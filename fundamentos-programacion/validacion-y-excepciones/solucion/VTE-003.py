def validar_datos(secuencia, motivo):
    if not 6 <= len(secuencia) <= 60:
        return "La secuencia debe tener entre 6 y 60 caracteres."

    if len(motivo) != 3:
        return "El motivo debe tener exactamente tres caracteres."

    for letra in secuencia:
        if letra not in "ACGT":
            return "La secuencia solo admite las letras A, C, G y T."

    for letra in motivo:
        if letra not in "ACGT":
            return "El motivo solo admite las letras A, C, G y T."

    return ""


def buscar_motivo(secuencia, motivo):
    posiciones = []

    for i in range(len(secuencia) - len(motivo) + 1):
        if secuencia[i:i + len(motivo)] == motivo:
            posiciones.append(i)

    return posiciones


def validacion_de_secuencias():

    while True:
        secuencia = input("Ingrese secuencia de ADN: ")
        motivo = input("Ingrese motivo: ")

        estado_de_validacion = validar_datos(secuencia, motivo)

        if estado_de_validacion != "":
            print(estado_de_validacion)
            continue

        posiciones = buscar_motivo(secuencia, motivo)
        print("Índices de las coincidencias:", posiciones)
        break