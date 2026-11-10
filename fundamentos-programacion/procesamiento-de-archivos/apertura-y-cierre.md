# Apertura y cierre de archivos

## Rutas, modos de apertura y codificación

La función `open()` abre un archivo y devuelve un **objeto archivo**, 
mediante el cual se puede leer o escribir su contenido. Sus argumentos 
básicos son la ruta y el modo de apertura, para archivos de texto también 
puede indicarse el tipo de codificación.

:::{code-block} python
:linenos:
archivo = open("data/lorem_ipsum.txt", "r", encoding="utf-8")
# Procesar el contenido aquí.
archivo.close()
:::

La **ruta** indica la ubicación del archivo. 
Puede ser absoluta o relativa al directorio de trabajo 
desde el que se ejecuta el programa.

Los modos básicos son:

|  Modo  | Propósito       | Si el archivo existe          | Si no existe               |
|:------:|:----------------|:------------------------------|:---------------------------|
| `"r"`  | Leer            | Conserva su contenido         | Genera `FileNotFoundError` |
| `"w"`  | Escribir        | Vacía su contenido al abrirlo | Crea el archivo            |
| `"a"`  | Añadir al final | Conserva su contenido         | Crea el archivo            |

Estos modos trabajan con texto por defecto. El modo predeterminado 
de `open()` es `"r"`, equivalente a `"rt"` (`read text`). 
La letra `"b"` permite trabajar en modo binario, por ejemplo, `"rb"`, en ese caso no se especifica `encoding`.

**Nota:** `"w"` y `"a"` pueden crear el archivo, pero no los 
directorios no existentes. Para ejecutar los ejemplos, la carpeta `data` 
debe existir. El archivo `lorem_ipsum.txt` debe contener texto guardado 
con codificación UTF-8.

Estos argumentos y comportamientos se describen en la documentación de `open()` [@pythonOpen].

## Cierre explícito

El método `close()` cierra el archivo, vacía sus búferes de escritura y libera los recursos asociados:

:::{code-block} python
:linenos:
# 1. Abrir
archivo = open("data/lorem_ipsum.txt", "r", encoding="utf-8")
# 2. Procesar
contenido = archivo.read()
# 3. Cerrar
archivo.close()
print(contenido)
:::

Después del cierre, el objeto archivo no admite nuevas lecturas ni escrituras. 
Sin embargo, los datos ya leídos siguen disponibles. En el ejemplo, 
`contenido` conserva la cadena de texto.

**Nota:** si una excepción interrumpe el procesamiento antes de `close()`, 
el flujo no llega al cierre. Garantizar el cierre ante errores requiere 
un mecanismo adicional.

## Manejo de errores de apertura

Si se intenta abrir para lectura un archivo inexistente, Python lanza 
una excepción `FileNotFoundError`. Se puede capturar para informar 
lo ocurrido:

:::{code-block} python
:linenos:

try:
    # 1. Abrir
    archivo = open("data/lorem_ipsum.txt", "r", encoding="utf-8")

    # 2. Procesar
    contenido = archivo.read()

    # 3. Cerrar
    archivo.close()
    print(contenido)

except FileNotFoundError:
    print("Archivo no encontrado.")
:::

Este ejemplo trata únicamente el archivo inexistente durante la apertura. 
También pueden ocurrir otros errores, como falta de permisos o una 
codificación incompatible durante la lectura.
