"""
Script para probar la carga de imágenes en modo desarrollo
Ejecutar con: python test_dev_mode.py
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

# Agregar la carpeta src al path para poder importar los módulos
sys.path.insert(0, os.path.abspath("src"))

from src.resource_path import resource_path

def test_resource_loading():
    """Prueba la carga de recursos usando resource_path"""
    print("=== TEST DE CARGA DE RECURSOS EN MODO DESARROLLO ===")
    print(f"Directorio actual: {os.getcwd()}")
    
    # Probar carga de recursos
    assets_dir = 'assets'
    logo_files = [
        'logo.ico', 'logo.png', 'itau.png', 'BBVA.png', 
        'Bancolombia.png', 'BancoBogota.png', 'Occidente.png', 
        'AvVillas.png', 'Credicorp.png', 'Corfi.jpeg', 'Fidu.jpg'
    ]
    
    print("\n=== Probando resource_path ===")
    # Verificar cada archivo
    for logo_file in logo_files:
        try:
            # Obtener ruta del recurso
            resource_file = resource_path(os.path.join(assets_dir, logo_file))
            exists = os.path.exists(resource_file)
            
            print(f"Archivo: {logo_file}")
            print(f"  Ruta: {resource_file}")
            print(f"  Existe: {'SÍ' if exists else 'NO'}")
            print("")
        except Exception as e:
            print(f"Error procesando {logo_file}: {e}")
    
    print("\n=== Probando rutas absolutas ===")
    # Probar rutas absolutas
    for logo_file in logo_files:
        try:
            # Ruta absoluta directa
            abs_path = os.path.abspath(os.path.join('assets', logo_file))
            exists = os.path.exists(abs_path)
            
            print(f"Archivo: {logo_file}")
            print(f"  Ruta absoluta: {abs_path}")
            print(f"  Existe: {'SÍ' if exists else 'NO'}")
            
            # Ruta desde directorio del script
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', logo_file))
            script_exists = os.path.exists(script_path)
            print(f"  Ruta desde script: {script_path}")
            print(f"  Existe: {'SÍ' if script_exists else 'NO'}")
            print("")
        except Exception as e:
            print(f"Error procesando {logo_file}: {e}")
    
    # Prueba visual con tkinter
    print("\n=== Iniciando prueba visual con tkinter ===")
    try:
        from PIL import Image, ImageTk
        
        root = tk.Tk()
        root.title("Test de Carga de Imágenes - Modo Desarrollo")
        root.geometry("800x600")
        
        # Frame principal con scroll
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Canvas con scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        ttk.Label(
            scrollable_frame, 
            text="Prueba de Carga de Imágenes en Modo Desarrollo",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(0, 20))
        
        # Probar cada imagen
        for logo_file in logo_files:
            try:
                # Frame para cada imagen
                img_frame = ttk.Frame(scrollable_frame)
                img_frame.pack(fill="x", pady=10)
                
                # Etiqueta con el nombre del archivo
                ttk.Label(
                    img_frame, 
                    text=f"Archivo: {logo_file}",
                    font=("Segoe UI", 12, "bold")
                ).pack(anchor="w")
                
                # Intentar cargar con resource_path
                resource_file = resource_path(os.path.join(assets_dir, logo_file))
                if os.path.exists(resource_file) and not logo_file.endswith('.ico'):
                    img = Image.open(resource_file)
                    # Redimensionar manteniendo proporción
                    width, height = img.size
                    max_size = 150
                    if width > height:
                        new_width = max_size
                        new_height = int(height * (max_size / width))
                    else:
                        new_height = max_size
                        new_width = int(width * (max_size / height))
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    
                    # Mostrar imagen
                    img_label = tk.Label(img_frame, image=photo)
                    img_label.image = photo  # Mantener referencia
                    img_label.pack(pady=5)
                    
                    # Mostrar ruta
                    ttk.Label(
                        img_frame, 
                        text=f"Cargada desde: {resource_file}",
                        font=("Segoe UI", 9)
                    ).pack(anchor="w")
                else:
                    ttk.Label(
                        img_frame, 
                        text=f"No se pudo cargar la imagen desde: {resource_file}",
                        foreground="red"
                    ).pack(anchor="w")
            except Exception as e:
                ttk.Label(
                    img_frame, 
                    text=f"Error: {str(e)}",
                    foreground="red"
                ).pack(anchor="w")
        
        # Botón para cerrar
        ttk.Button(
            scrollable_frame,
            text="Cerrar",
            command=root.destroy
        ).pack(pady=20)
        
        # Configurar el scroll con la rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        root.bind_all("<MouseWheel>", _on_mousewheel)
        
        root.mainloop()
    except Exception as e:
        print(f"Error en la prueba visual: {e}")

if __name__ == "__main__":
    test_resource_loading() 