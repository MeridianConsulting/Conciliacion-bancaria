# Solución al problema de imágenes en el ejecutable y modo desarrollo

## Problema detectado

Después de implementar la solución para que las imágenes se mostraran correctamente en el ejecutable (.exe), surgió un nuevo problema: las imágenes dejaron de mostrarse al ejecutar el programa desde el código fuente (modo desarrollo).

## Causa raíz

El problema se debe a que la función `resource_path` estaba configurada para buscar los recursos solo en un directorio específico según el modo de ejecución, sin intentar rutas alternativas cuando el archivo no se encuentra.

## Solución implementada

Se han realizado los siguientes cambios para solucionar el problema:

1. **Mejora de la función `resource_path`**: Se ha modificado la función en `src/resource_path.py` para que intente múltiples rutas posibles en modo desarrollo:
   - Directorio actual
   - Directorio del script
   - Directorio raíz del proyecto

2. **Implementación de rutas alternativas**: Se ha añadido código en las funciones que cargan imágenes para intentar con rutas alternativas cuando la ruta obtenida con `resource_path` no existe.

3. **Mejora de la detección de rutas**: Se ha añadido código para imprimir mensajes de depuración que muestran qué ruta se está utilizando para cargar cada imagen.

4. **Herramientas de prueba**: Se han creado scripts de prueba adicionales para verificar la carga de imágenes tanto en modo desarrollo como en modo empaquetado.

## Cómo probar la solución

### Para modo desarrollo:
1. Ejecutar `test_dev.bat` para probar la carga de imágenes en modo desarrollo
2. Verificar que las imágenes se muestren correctamente en la aplicación de prueba y en la aplicación principal

### Para modo empaquetado:
1. Ejecutar `test_solution.bat` para probar la solución en modo empaquetado
2. Verificar que las imágenes se muestren correctamente en el ejecutable

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
            print(f"Modo frozen: Buscando {relative_path} en {base_path}")
            return os.path.join(base_path, relative_path)
        else:
            # Estamos ejecutando en modo desarrollo
            # Primero intentar con la ruta relativa al directorio actual
            current_dir_path = os.path.join(os.path.abspath("."), relative_path)
            if os.path.exists(current_dir_path):
                print(f"Modo desarrollo: Encontrado {relative_path} en directorio actual")
                return current_dir_path
            
            # Si no se encuentra, intentar con la ruta relativa al directorio del script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            script_dir_path = os.path.join(script_dir, relative_path)
            if os.path.exists(script_dir_path):
                print(f"Modo desarrollo: Encontrado {relative_path} en directorio del script")
                return script_dir_path
            
            # Si aún no se encuentra, intentar con la ruta relativa al directorio raíz del proyecto
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            project_root_path = os.path.join(project_root, relative_path)
            if os.path.exists(project_root_path):
                print(f"Modo desarrollo: Encontrado {relative_path} en directorio raíz del proyecto")
                return project_root_path
            
            # Si no se encuentra en ninguna parte, devolver la ruta relativa al directorio actual
            print(f"Modo desarrollo: No se encontró {relative_path}, devolviendo ruta relativa")
            return current_dir_path
            
    except Exception as e:
        print(f"Error al obtener ruta de recurso {relative_path}: {e}")
        # En caso de error, intentar con la ruta relativa directa
        return relative_path
```

### Implementación de rutas alternativas

```python
# Ejemplo de cómo cargar una imagen con ruta alternativa
# Intentar cargar el ícono usando resource_path
icon_path = resource_path(os.path.join('assets', 'logo.ico'))

# Si no se encuentra, intentar con la ruta absoluta (para modo desarrollo)
if not os.path.exists(icon_path):
    alt_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'logo.ico'))
    if os.path.exists(alt_path):
        icon_path = alt_path
        print(f"Usando ruta alternativa para el ícono: {icon_path}")

if os.path.exists(icon_path):
    self.iconbitmap(icon_path)
```

## Recomendaciones adicionales

1. **Depuración**: Si hay problemas con las imágenes en el futuro, usar los scripts de prueba para depurar la carga de recursos:
   - `test_dev_mode.py`: Para probar en modo desarrollo
   - `src/test_resources.py`: Para probar en modo empaquetado

2. **Estructura de archivos**: Mantener una estructura de archivos consistente con los recursos en la carpeta `assets/`.

3. **Uso de resource_path**: Siempre usar `resource_path()` para referenciar archivos externos, pero implementar una lógica de fallback para intentar con rutas alternativas si la ruta principal no existe.

4. **Mensajes de depuración**: Mantener los mensajes de depuración en la función `resource_path` para facilitar la identificación de problemas. 