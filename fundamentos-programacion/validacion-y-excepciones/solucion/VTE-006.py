def validar_reaccion(mensajes, usuarios, identificador, usuario):
    """Comprueba si un usuario puede reaccionar a un mensaje.

    Args:
        mensajes (dict): Diccionario de mensajes.
        usuarios (list): Usuarios registrados.
        identificador (int): Identificador del mensaje.
        usuario (str): Usuario que desea reaccionar.

    Returns:
        str: Cadena vacía si la reacción es válida o mensaje de error.
    """

    if identificador not in mensajes:
        return "El mensaje no existe."

    if usuario not in usuarios:
        return "El usuario no está registrado."

    autor, texto, reacciones = mensajes[identificador]

    if usuario == autor:
        return "No puede dar «Me gusta» a su propio mensaje."

    if usuario in reacciones:
        return "El usuario ya dio «Me gusta» a este mensaje."

    return ""


def agregar_reaccion(mensajes, usuarios, identificador, usuario):
    """Agrega una reacción válida a un mensaje.

    Args:
        mensajes (dict): Diccionario de mensajes.
        usuarios (list): Usuarios registrados.
        identificador (int): Identificador del mensaje.
        usuario (str): Usuario que desea reaccionar.

    Returns:
        tuple: Cantidad de reacciones y mensaje de error.
            Si la operación falla, la cantidad es None.
    """
    mensaje = validar_reaccion(
        mensajes, usuarios, identificador, usuario
    )

    if mensaje != "":
        return None, mensaje

    autor, texto, reacciones = mensajes[identificador]

    nuevas_reacciones = reacciones + [usuario]
    mensajes[identificador] = (autor, texto, nuevas_reacciones)

    return len(nuevas_reacciones), ""


def gestionar_reacciones(mensajes, usuarios):
    """Gestiona las solicitudes de reacción hasta ingresar FIN.

    Args:
        mensajes (dict): Diccionario de mensajes.
        usuarios (list): Usuarios registrados.

    Returns:
        None: No retorna ningún valor.
    """
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

        cantidad, mensaje = agregar_reaccion(
            mensajes, usuarios, identificador, usuario
        )

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