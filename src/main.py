from frontend.interface import ConciliacionBancaria
from frontend.bank_selector import BankSelector
import os
import tkinter as tk
from tkinter import messagebox
import sys
import traceback
from resource_path import resource_path

def launch_main_app():
    """Inicia la aplicación principal de conciliación para Itaú"""
    try:
        app = ConciliacionBancaria()
        app.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación principal: {str(e)}")
        traceback.print_exc()

def show_unavailable_message(bank_name):
    """Muestra un mensaje de función no disponible para el banco seleccionado"""
    messagebox.showinfo(
        "Funcionalidad en Desarrollo",
        f"La conciliación para {bank_name} estará disponible próximamente.\n\n"
        "Actualmente solo está implementada la conciliación para Itaú."
    )

def main():
    """Función principal de la aplicación"""
    try:
        # Establecer directorio de trabajo para asegurar que se encuentren los recursos
        # cuando se ejecuta como .exe
        if getattr(sys, 'frozen', False):
            # Si estamos ejecutando como .exe (PyInstaller)
            application_path = os.path.dirname(sys.executable)
            os.chdir(application_path)
        
        # Crear y mostrar el selector de bancos
        selector = BankSelector()
        selector.mainloop()
        
        # Si el selector fue cerrado sin seleccionar un banco, salir
        if not hasattr(selector, 'bank_selected') or not selector.bank_selected:
            print("Selección de banco cancelada")
            return
        
        # Obtener el banco seleccionado
        bank_name = selector.selected_bank.get()
        print(f"Banco seleccionado: {bank_name}")
        
        # Asegurarse de que el selector se cierre por completo
        selector.destroy()
        
        # Lanzar la aplicación correspondiente según el banco seleccionado
        if bank_name == "Itaú":
            # Para Itaú, lanzar la aplicación principal directamente
            launch_main_app()
        else:
            # Para otros bancos, mostrar mensaje de "próximamente"
            show_unavailable_message(bank_name)
            
            # Volver a mostrar el selector
            main()
    except Exception as e:
        print(f"Error en la aplicación: {str(e)}")
        traceback.print_exc()
        try:
            messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
        except:
            pass

if __name__ == "__main__":
    main()
