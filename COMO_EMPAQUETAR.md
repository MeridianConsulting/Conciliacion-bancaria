# Guía para Empaquetar la Aplicación

Este documento explica cómo crear un archivo ejecutable (.exe) de la aplicación de Conciliación Bancaria para distribuirlo sin necesidad de instalar Python ni sus dependencias.

## Requisitos previos

- Python 3.9 o superior
- Todas las dependencias listadas en requirements.txt

## Métodos para empaquetar

Existen tres formas de empaquetar la aplicación:

### 1. Usando el archivo batch (Recomendado para Windows)

1. Simplemente haga doble clic en el archivo `empaquetar.bat`
2. El script instalará las dependencias necesarias y creará el ejecutable
3. El archivo .exe resultante se encontrará en la carpeta `dist/`

### 2. Usando PyInstaller directamente con el archivo spec

1. Instale las dependencias: `pip install -r requirements.txt`
2. Ejecute: `pyinstaller --clean ConciliacionBancaria.spec`
3. El archivo .exe resultante se encontrará en la carpeta `dist/`

### 3. Usando el script Python de empaquetado

1. Instale las dependencias: `pip install -r requirements.txt`
2. Ejecute: `python build_exe.py`
3. El archivo .exe resultante se encontrará en la carpeta `dist/`

## Contenido del archivo ejecutable

El archivo .exe resultante incluirá:
- Todos los módulos Python necesarios
- Todas las dependencias externas
- Archivos de recursos (imágenes, iconos, etc.) de la carpeta `assets/`
- Archivos de datos necesarios de la carpeta `data/` (si existen)

## Distribución

Para distribuir la aplicación:
1. Copie el archivo `ConciliacionBancaria.exe` de la carpeta `dist/`
2. Opcionalmente, puede crear un instalador con NSIS, Inno Setup u otra herramienta similar

## Solución de problemas

Si encuentra problemas durante la ejecución del .exe:

1. **Error de recursos no encontrados**: Asegúrese de que todas las imágenes y archivos de datos estén en las carpetas correctas
2. **Dependencias faltantes**: Verifique que todas las dependencias estén listadas en requirements.txt
3. **Errores de PyInstaller**: Consulte la documentación oficial de PyInstaller para problemas específicos

## Notas adicionales

- El archivo .exe puede ser grande (50-100 MB) debido a que contiene Python y todas las dependencias
- La primera ejecución puede ser más lenta mientras Windows verifica el archivo 