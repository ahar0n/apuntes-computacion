datos = [5, 10, 15, 20, 25, 30]
texto = "Programacion"

# secuencia invertida, iterando sobre elementos
datos_invertido = []
for elemento in datos:
    datos_invertido = [elemento] + datos_invertido
datos_invertido

# secuencia invertida, iterando sobre indices (negativos)
texto_invertido = ''
i = 1
while i <= len(texto):
    texto_invertido += texto[-i]
    i += 1
texto_invertido