"""
Módulo: Solución Ejercicio VTE-011
===================================

Solución modular del ejercicio VTE-011

Documentación mínima, y en algunos casos usando estilos Google y
reStructuredText (reST).

Ref.: https://realpython.com/how-to-write-docstrings-in-python/

:Authors:
    - Cuevas, A.
:Version: 0.1
:Copyright: ...
"""

def duplicar_registro(registro):
    """Genera una copia independiente del registro de expedientes."""

    copia = {}
    for matricula, expediente in registro.items():
        nueva_ficha = expediente.copy()
        nueva_ficha["notas"] = expediente["notas"].copy()
        copia[matricula] = nueva_ficha

    return copia


def validar_entrada(registro, matricula, nota):
    """Valída los datos de una solicitud de modificación de expediente.

    Comprueba que matrícula exista en registro y nota se encuentre dentro
    del intervalo cerrado [1.0, 7.0].

    :param registro: Diccionario de expedientes académicos.
    :type registro: dict
    :param matricula: Matrícula del expediente que se modificará.
    :type matricula: str
    :param nota: Calificación que se desea incorporar al expediente.
    :type nota: float

    :return: True si la matrícula existe y la nota está dentro del
             intervalo permitido, False en caso contrario.
    :rtype: bool
    """

    if matricula not in registro:
        return False

    try:
        nota = float(nota)

    except ValueError:
        return False

    except TypeError:
        return False

    if not (1.0 <= nota <= 7.0):
        return False

    return True


def insertar_nota(registro, solicitud):
    """Incorpora una nota al expediente si la solicitud es válida.

    Extrae matrícula y nota de solicitud, verifica ambas datos mediante
    validar_entrada(). Si son válidos, inserta la nota el expediente.

    Args:
        registro (dict): Diccionario de expedientes que será actualizado.
        solicitud (dict): Solicitud que contiene las claves "matricula" (str)
                        y "nota" (float).

    Returns:
        bool: True si la nota fue incorporada correctamente.
        False si la solicitud no superó la validación.

    Note:
        Modifica registro (parámetro) cuando la solicitud es válida.
    """

    try:
        matricula = solicitud["matricula"]
        nota = solicitud["nota"]

    except KeyError:
        return False

    except TypeError:
        return False

    es_valida = validar_entrada(registro, matricula, nota)

    if es_valida:
        registro[matricula]["notas"].append(float(nota))

    return es_valida


def contar_aprobadas(notas):
    """Cuenta las notas mayores o igual que 4.0 de una lista."""

    cantidad = 0

    for nota in notas:
        if nota >= 4.0:
            cantidad = cantidad + 1

    return cantidad


def generar_informe(registro):
    """Genera un informe resumido de los expedientes académicos."""

    informe = {}

    for matricula, expediente in registro.items():
        informe[matricula] = {
            "nombre": expediente["nombre"],
            "cantidad": len(expediente["notas"]),
            "aprobadas": contar_aprobadas(expediente["notas"]),
        }

    return informe


def actualizar_registro(original, solicitudes):
    """Procesa solicitudes de actualización y genera informe."""

    registro = duplicar_registro(original)
    resumen = {"aceptadas": 0, "rechazadas": 0}

    for solicitud in solicitudes:
        if insertar_nota(registro, solicitud):
            resumen["aceptadas"] += 1
        else:
            resumen["rechazadas"] += 1

    return {
        "registro": registro,
        "solicitudes": resumen,
        "informe": generar_informe(registro),
    }
