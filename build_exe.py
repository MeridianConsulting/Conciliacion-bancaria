import os
import subprocess
import sys
import shutil

def create_executable():
    """
    Crea un archivo ejecutable (.exe) del programa usando PyInstaller
    """
    print("Iniciando el proceso de empaquetado...")
    
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
    
    # Obtener lista de archivos de assets
    assets_files = []
    for file in os.listdir("assets"):
        assets_files.append(os.path.join("assets", file))

    # Ejecutar PyInstaller usando el módulo directamente con Python
    python_exe = sys.executable
    
    print(f"Usando Python desde: {python_exe}")
    
    pyinstaller_cmd = [
        python_exe, 
        "-m", 
        "PyInstaller",
        "--name=ConciliacionBancaria",
        "--onefile",  # Crear un solo archivo ejecutable
        "--windowed",  # Aplicación GUI (no mostrar consola)
        "--icon=assets/logo.ico",  # Icono para el ejecutable
        "--add-data=assets;assets",  # Incluir carpeta de assets
        "--noconfirm",  # No preguntar para sobrescribir
        "--clean",  # Limpiar archivos temporales
        "src/main.py"  # Archivo principal
    ]
    
    print("Ejecutando PyInstaller...")
    print(f"Comando: {' '.join(pyinstaller_cmd)}")
    
    try:
        # Ejecutar PyInstaller
        subprocess.check_call(pyinstaller_cmd)
        
        print("\n¡Empaquetado completado con éxito!")
        print(f"El ejecutable se encuentra en: {os.path.abspath('dist/ConciliacionBancaria.exe')}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error durante el empaquetado: {e}")
        return False

if __name__ == "__main__":
    create_executable() 