"""
Script de prueba para verificar la carga de recursos
Ejecutar con: python src/test_resources.py
"""

import os
import sys
import tkinter as tk
from PIL import Image, ImageTk
from resource_path import resource_path

def test_resource_loading():
    """Prueba la carga de recursos usando resource_path"""
    print("=== TEST DE CARGA DE RECURSOS ===")
    print(f"Modo de ejecución: {'Frozen (PyInstaller)' if getattr(sys, 'frozen', False) else 'Desarrollo'}")
    print(f"Directorio actual: {os.getcwd()}")
    
    # Probar carga de recursos
    assets_dir = 'assets'
    logo_files = [
        'logo.ico', 'logo.png', 'itau.png', 'BBVA.png', 
        'Bancolombia.png', 'BancoBogota.png', 'Occidente.png', 
        'AvVillas.png', 'Credicorp.png', 'Corfi.jpeg', 'Fidu.jpg'
    ]
    
    # Verificar cada archivo
    for logo_file in logo_files:
        try:
            # Obtener ruta del recurso
            resource_file = resource_path(os.path.join(assets_dir, logo_file))
            exists = os.path.exists(resource_file)
            
            print(f"Archivo: {logo_file}")
            print(f"  Ruta: {resource_file}")
            print(f"  Existe: {'SÍ' if exists else 'NO'}")
            
            if exists:
                # Intentar cargar con PIL
                try:
                    img = Image.open(resource_file)
                    print(f"  Dimensiones: {img.size}")
                    print(f"  Formato: {img.format}")
                    print(f"  Modo: {img.mode}")
                    print("  Carga con PIL: EXITOSA")
                except Exception as e:
                    print(f"  Error cargando con PIL: {e}")
            
            print("")
        except Exception as e:
            print(f"Error procesando {logo_file}: {e}")
    
    # Prueba visual con tkinter
    print("Iniciando prueba visual con tkinter...")
    try:
        root = tk.Tk()
        root.title("Test de Recursos")
        root.geometry("800x600")
        
        # Cargar y mostrar logo
        try:
            logo_path = resource_path(os.path.join(assets_dir, 'logo.png'))
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                img = img.resize((200, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                label = tk.Label(root, image=photo)
                label.image = photo  # Mantener referencia
                label.pack(pady=20)
                
                info_label = tk.Label(root, text=f"Logo cargado desde: {logo_path}")
                info_label.pack(pady=10)
                
                print("Logo cargado correctamente en tkinter")
            else:
                error_label = tk.Label(root, text=f"No se encontró el logo en: {logo_path}")
                error_label.pack(pady=20)
                print(f"No se encontró el logo en: {logo_path}")
        except Exception as e:
            error_label = tk.Label(root, text=f"Error cargando logo: {str(e)}")
            error_label.pack(pady=20)
            print(f"Error cargando logo: {e}")
        
        # Botón para cerrar
        close_button = tk.Button(root, text="Cerrar", command=root.destroy)
        close_button.pack(pady=20)
        
        root.mainloop()
    except Exception as e:
        print(f"Error en la prueba visual: {e}")

if __name__ == "__main__":
    test_resource_loading() 