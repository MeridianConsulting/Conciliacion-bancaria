import os
import sys

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