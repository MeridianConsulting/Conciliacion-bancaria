# Solución al problema de imágenes en el ejecutable

## Problema detectado

Las imágenes no se están empaquetando correctamente dentro del ejecutable (.exe) generado con PyInstaller. Cuando se ejecuta el programa desde el código fuente (usando `python src/main.py`), las imágenes se muestran correctamente, pero cuando se ejecuta el archivo .exe empaquetado, las imágenes no aparecen.

## Causa raíz

El problema se debe a la forma en que se están referenciando las rutas de los archivos de imágenes en el código. Cuando el programa se ejecuta desde el código fuente, las rutas relativas funcionan correctamente, pero cuando se ejecuta como un ejecutable empaquetado por PyInstaller, las rutas son diferentes ya que los archivos se extraen a un directorio temporal (`sys._MEIPASS`).

## Solución implementada

Se han realizado los siguientes cambios para solucionar el problema:

1. **Mejora de la función `resource_path`**: Se ha modificado la función en `src/resource_path.py` para manejar mejor la detección del modo de ejecución (desarrollo vs. empaquetado) y proporcionar rutas absolutas correctas en ambos casos.

2. **Uso consistente de `resource_path`**: Se ha actualizado el código en los siguientes archivos para usar la función `resource_path` al cargar imágenes y recursos:
   - `src/frontend/bank_selector.py`: Para cargar los logos de los bancos
   - `src/frontend/interface.py`: Para cargar el ícono de la aplicación

3. **Mejor manejo del directorio de trabajo**: Se ha mejorado la función `main()` en `src/main.py` para establecer correctamente el directorio de trabajo cuando se ejecuta como .exe.

4. **Mejoras en el script de empaquetado**: Se ha actualizado `build_exe.py` para incluir más información de depuración y asegurar que todos los recursos se incluyan correctamente.

5. **Herramientas de prueba**: Se han creado scripts de prueba (`test_resources.py`, `test_build.py` y `test_solution.bat`) para verificar la carga de recursos tanto en modo desarrollo como en modo empaquetado.

## Cómo probar la solución

1. Ejecutar `test_solution.bat` para probar la solución en ambos modos (desarrollo y empaquetado)
2. Verificar que las imágenes se muestren correctamente en ambos casos
3. Empaquetar la aplicación completa con `python build_exe.py`
4. Ejecutar el archivo `dist/ConciliacionBancaria.exe` y verificar que las imágenes se muestren correctamente

## Detalles técnicos

### Función resource_path mejorada

```python
def resource_path(relative_path):
    """
    Función para obtener la ruta absoluta a los recursos, tanto en modo
    desarrollo como cuando la aplicación está empaquetada con PyInstaller
    
    Args:
        relative_path (str): Ruta relativa al recurso
        
    Returns:
        str: Ruta absoluta al recurso
    """
    try:
        # PyInstaller crea un directorio temporal _MEIPASS en caso de empaquetamiento
        if getattr(sys, 'frozen', False):
            # Estamos ejecutando en un bundle (PyInstaller)
            base_path = sys._MEIPASS
        else:
            # Estamos ejecutando en modo desarrollo
            base_path = os.path.abspath(".")
            
        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Error al obtener ruta de recurso {relative_path}: {e}")
        # En caso de error, intentar con la ruta relativa directa
        return relative_path
```

### Uso de resource_path para cargar imágenes

```python
# Ejemplo de cómo cargar una imagen
image_path = resource_path(os.path.join('assets', 'logo.png'))
if os.path.exists(image_path):
    img = Image.open(image_path)
    # Procesar la imagen...
```

## Recomendaciones adicionales

1. **Depuración**: Si hay problemas con las imágenes en el futuro, usar `test_resources.py` para depurar la carga de recursos.
2. **Estructura de archivos**: Mantener una estructura de archivos consistente con los recursos en la carpeta `assets/`.
3. **Uso de resource_path**: Siempre usar `resource_path()` para referenciar archivos externos que deben ser empaquetados con PyInstaller. 