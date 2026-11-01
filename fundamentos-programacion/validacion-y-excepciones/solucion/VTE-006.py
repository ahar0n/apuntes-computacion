def agregar_reaccion(mensajes, usuarios, identificador, usuario):
    autor, texto, reacciones = mensajes[identificador]

    if usuario not in usuarios:
        return None, "El usuario no está registrado."

    if usuario == autor:
        return None, "No puede dar «Me gusta» a su propio mensaje."

    if usuario in reacciones:
        return None, "El usuario ya dio «Me gusta» a este mensaje."

    nuevas_reacciones = reacciones + [usuario]
    mensajes[identificador] = (autor, texto, nuevas_reacciones)

    return len(nuevas_reacciones), ""


def gestionar_reacciones(mensajes, usuarios):
    while True:
        entrada = input("Identificador del mensaje o FIN: ")

        if entrada == "FIN":
            return

        try:
            identificador = int(entrada)
        except ValueError:
            print("El identificador debe ser un número entero.")
            continue

        usuario = input("Nombre de usuario: ")

        try:
            cantidad, mensaje = agregar_reaccion(
                mensajes, usuarios, identificador, usuario
            )
        except KeyError:
            print("El mensaje no existe.")
            continue

        if mensaje != "":
            print(mensaje)
            continue

        print("Cantidad de reacciones del mensaje:", cantidad)


mensajes = {
    101: (
        "la_mon",
        "Vecino, no estoy gritando: estoy ensayando el coro.",
        [],
    ),
    205: (
        "nino_maravilla",
        "Cabros, era pichanga, no final del mundo. ¡Devuelvan la pelota, po!",
        ["la_mon"],
    ),
}
usuarios = ("la_mon", "nino_maravilla", "yei_lo")

gestionar_reacciones(mensajes, usuarios)

print("Mensajes al finalizar:")
for identificador, datos in mensajes.items():
    print(identificador, datos)