# Lectura de archivos de texto

Una vez abierto un archivo en modo `"r"`, se puede leer su contenido mediante
el objeto archivo. Las lecturas sucesivas avanzan desde la posición actual,
no vuelven automáticamente al inicio.

## Lectura con `read()`

En modo texto, `read(n)` devuelve una cadena con **hasta `n` caracteres**. 
Si se omite el argumento, `read()` lee todo el contenido, por lo que debe 
considerarse la memoria disponible. Cuando se alcanza el final, 
devuelve la cadena vacía `""`.

El siguiente ejemplo, la función cuenta los caracteres leídos de un archivo, 
incluidos los espacios y saltos de línea:

:::{code-block} python
:linenos:
def contar_caracteres(nombre_archivo):
    # 1. Abrir
    archivo = open(nombre_archivo, "r", encoding="utf-8")

    # 2. Procesar: leer un carácter por vez.
    cantidad = 0
    while archivo.read(1) != "":
        cantidad += 1

    # 3. Cerrar
    archivo.close()
    return cantidad


cantidad = contar_caracteres("data/lorem_ipsum.txt")
print(f"Se leyeron {cantidad} caracteres.")
:::

Además de la codificación, la lectura en modo texto puede normalizar
los saltos de línea. La lectura carácter por carácter se utiliza 
aquí para ilustrar el avance hasta el final. Para volúmenes mayores 
de texto se recomienda leer líneas o bloques.

**Nota:** Recordar que, una excepción que no se captura dentro 
de una función se propaga hacia la llamada. En tanto, es posible 
mantener la función `contar_caracteres()` centrada en su tarea y 
tratar `FileNotFoundError` mediante un bloque `try-except` alrededor 
de su llamada.


## Lectura por líneas con `readline()`

El método `readline()` devuelve la siguiente línea y conserva el salto 
de línea `\n` cuando está presente. La última línea puede no terminar 
con este carácter.

- Una línea vacía del archivo se lee como `"\n"`.
- El fin del archivo se indica con `""`.
- Si se proporciona un límite, `readline(n)` lee como máximo `n` caracteres de la línea en modo texto.

El siguiente ejemplo muestra cada línea junto con su número:

:::{code-block} python
:linenos:

def imprimir_lineas(nombre_archivo):
    
    # 1. Abrir
    archivo = open(nombre_archivo, "r", encoding="utf-8")
    numero = 1

    # 2. Procesar
    while True:
        linea = archivo.readline()
        if linea == "":
            break

        if linea[-1] == "\n":
            linea = linea[:-1]

        print(f"{numero:>2} {linea}")
        numero += 1

    # 3. Cerrar
    archivo.close()


imprimir_lineas("data/lorem_ipsum.txt")
:::

- Una **secuencia de escape** permite representar ciertos caracteres dentro de una cadena. Por ejemplo, `\n` representa un salto de línea. Aunque se escribe mediante dos símbolos, corresponde a un solo carácter en la cadena [@pythonEscapeSequences].
- El formato `:>2` alinea el número a la derecha en un campo de al menos 
dos posiciones.


## Iteración directa por líneas

Un objeto archivo también puede iterarse con el ciclo `for`. 
Esta alternativa procesa una línea a la vez y termina automáticamente 
al llegar al final, conservando el mismo flujo de apertura, 
procesamiento y cierre:

:::{code-block} python
:linenos:

# 1. Abrir
archivo = open("data/lorem_ipsum.txt", "r", encoding="utf-8")

# 2. Procesar
numero = 1
for linea in archivo:
    if linea[-1] == "\n":
        linea = linea[:-1]

    print(f"{numero:>2} {linea}")
    numero += 1

# 3. Cerrar
archivo.close()
:::



