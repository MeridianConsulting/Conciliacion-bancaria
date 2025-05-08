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
        base_path = sys._MEIPASS
    except Exception:
        # En modo desarrollo, usamos el directorio del script como base
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path) 