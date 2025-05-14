"""
Script para empaquetar una versión de prueba del programa
Ejecutar con: python test_build.py
"""

import os
import subprocess
import sys
import shutil

def create_test_executable():
    """
    Crea un archivo ejecutable (.exe) de prueba usando PyInstaller
    """
    print("Iniciando el proceso de empaquetado de prueba...")
    
    # Verificar que estamos en el directorio raíz del proyecto
    if not os.path.exists("src") or not os.path.exists("assets"):
        print("Error: Ejecute este script desde el directorio raíz del proyecto")
        return False
    
    # Instalar PyInstaller si no está instalado
    try:
        import PyInstaller
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller>=6.0.0"])
    
    # Crear el directorio dist si no existe
    if not os.path.exists("dist"):
        os.makedirs("dist")
    
    # Ejecutar PyInstaller usando el módulo directamente con Python
    python_exe = sys.executable
    
    print(f"Usando Python desde: {python_exe}")
    
    # Empaquetar el script de prueba de recursos
    pyinstaller_cmd = [
        python_exe, 
        "-m", 
        "PyInstaller",
        "--name=TestResources",
        "--onefile",  # Crear un solo archivo ejecutable
        "--windowed",  # Aplicación GUI (no mostrar consola)
        "--icon=assets/logo.ico",  # Icono para el ejecutable
        "--add-data=assets;assets",  # Incluir carpeta de assets
        "--noconfirm",  # No preguntar para sobrescribir
        "--clean",  # Limpiar archivos temporales
        "--log-level=DEBUG",  # Nivel de log detallado
        "src/test_resources.py"  # Archivo de prueba
    ]
    
    print("Ejecutando PyInstaller para test_resources.py...")
    print(f"Comando: {' '.join(pyinstaller_cmd)}")
    
    try:
        # Ejecutar PyInstaller
        subprocess.check_call(pyinstaller_cmd)
        
        print("\n¡Empaquetado de prueba completado con éxito!")
        print(f"El ejecutable se encuentra en: {os.path.abspath('dist/TestResources.exe')}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error durante el empaquetado: {e}")
        return False

if __name__ == "__main__":
    create_test_executable() 