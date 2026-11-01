def leer_clave_y_digito():
    digito = int(input("Dígito original (0 a 9): "))
    clave = int(input("Clave (0 a 9): "))
    return digito, clave


def codificar(digito, clave):
    return (digito + clave) % 10


def decodificar(cifrado, clave):
    return (cifrado - clave) % 10


while True:
    try:
        digito, clave = leer_clave_y_digito()
    except ValueError:
        print("El dígito y la clave deben ser números enteros.")
        continue

    if not (0 <= digito <= 9 and 0 <= clave <= 9):
        print("El dígito y la clave deben estar entre 0 y 9.")
        continue

    cifrado = codificar(digito, clave)
    recuperado = decodificar(cifrado, clave)

    print("Valor codificado:", cifrado)
    print("Dígito recuperado:", recuperado)
    break