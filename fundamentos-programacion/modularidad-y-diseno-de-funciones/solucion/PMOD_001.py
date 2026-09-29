
def calcular_descuento(cantidad_entradas, subtotal, porcentaje=0.1):
    if cantidad_entradas > 5:
        valor = int(subtotal * porcentaje)
    else:
        valor = 0
    return valor


def mostrar_cotizacion(cantidad_entradas, subtotal, descuento, total):
    titulo = "\nCotización de entradas"
    print(titulo)
    print("="* len(titulo))
    print(f"{'Cantidad total de entradas':<30}: {cantidad_entradas:>11}")
    print(f"{'Subtotal':<30}: ${subtotal:>10}")
    print(f"{'Descuento':<30}:-${descuento:>10}")
    print(f"{'Total':<30}: ${total:>10}")


def cotizar_compra():

    generales = int(input('Cantidad de entradas generales: '))
    estudiantes = int(input('Cantidad de entradas estudiante: '))

    if generales > 0 and estudiantes > 0:
        cantidad_total = generales + estudiantes
        subtotal = generales * 6000 + estudiantes * 4000
        descuento = calcular_descuento(cantidad_total, subtotal)
        total = subtotal - descuento
        mostrar_cotizacion(cantidad_total, subtotal, descuento, total)

    else:
        print('Error: Ambas cantidades deben ser mayores que 0.')


cotizar_compra()