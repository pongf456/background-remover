# Background Remover CLI

`background_remover` es una potente herramienta de línea de comandos (CLI) diseñada para eliminar el fondo de tus imágenes de forma rápida y eficiente. Ya sea que necesites preparar imágenes para e-commerce, diseño gráfico o simplemente quieras aislar un sujeto, esta CLI te proporciona las funcionalidades necesarias.

## Características Principales

- **Eliminación de Fondo**: Procesa imágenes para separar el primer plano del fondo.
- **Múltiples Operadores**: Elige entre diferentes algoritmos o métodos para el procesamiento de la imagen.
- **Entrada Flexible**: Carga imágenes desde un archivo binario o una ruta de archivo.
- **Salida Personalizable**: Guarda la imagen procesada en un archivo o imprímela directamente en la salida estándar.

## Uso

La aplicación se ejecuta a través de la línea de comandos y acepta varios argumentos para controlar el proceso de eliminación de fondo.

## Argumentos

- `--data <BINARIO>`:
  El binario de la imagen que se va a procesar. Útil para pasar datos de imagen directamente desde otra fuente (por ejemplo, a través de un pipe).

- `--operator <OPERADOR>`:
  **Requerido**. El operador que va a procesar la imagen. Actualmente, soporta:
  - `1`: (Descripción del operador 1, ej. "Método basado en umbral simple")
  - `2`: (Descripción del operador 2, ej. "Método avanzado con IA")

- `--path <RUTA>`:
  La ubicación de la imagen en tu sistema de archivos. Si se proporciona `data`, este argumento es opcional.

- `--out <NOMBRE_SALIDA>`:
  El nombre del archivo de salida (sin extensión) para la imagen procesada. Por defecto es `processed`. Si se especifica `-`, la imagen procesada se imprimirá en la salida estándar (stdout).
