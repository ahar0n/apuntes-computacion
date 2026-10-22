s = 120
texto = input("Velocidad de descarga (MB/s): ")
t = None

try:
    v = float(texto)
    t = s / v
except ValueError:
    print("La velocidad debe ingresarse como un número.")
except ZeroDivisionError:
    print("No se puede estimar el tiempo con una velocidad igual a cero.")

if t is not None:
    if t > 0:
        print(f"Tiempo estimado: {t:.1f} segundos.")
    else:
        print("La velocidad no puede ser negativa.")