def interpretar_lecturas(texto):
    campos = texto.split(",")

    if not 4 <= len(campos) <= 12:
        return None, "Debe ingresar entre 4 y 12 lecturas."

    lecturas = []

    for i in range(len(campos)):
        try:
            brillo = int(campos[i])
        except ValueError:
            return None, f"La lectura del índice {i} debe ser un entero no vacío."

        if not 0 <= brillo <= 100:
            return None, f"La lectura del índice {i} debe estar entre 0 y 100."

        lecturas.append(brillo)

    return lecturas, ""


def detectar_destellos(lecturas):
    destellos = []

    for i in range(1, len(lecturas) - 1):
        if lecturas[i] > lecturas[i - 1] and lecturas[i] > lecturas[i + 1]:
            destellos.append((i, lecturas[i]))

    return destellos


while True:
    texto = input("Lecturas de brillo separadas por comas: ")
    lecturas, mensaje = interpretar_lecturas(texto)

    if mensaje != "":
        print(mensaje)
        continue

    print("Destellos:", detectar_destellos(lecturas))
    break