from frontend.interface import ConciliacionBancaria
from frontend.bank_selector import BankSelector
from backend.reconciliation import Reconciliation
from backend.reconciliation_report import ReconciliationReport
import os
import time
from pathlib import Path
import tkinter as tk

def proteger_archivos(directorio):
    """Protege archivos Excel contra eliminación accidental"""
    try:
        if directorio.exists():
            for archivo in directorio.glob("*.xlsx"):
                try:
                    # Cambiar atributos del archivo para protegerlo
                    if os.name == 'nt':  # Windows
                        import win32api, win32con
                        win32api.SetFileAttributes(str(archivo), win32con.FILE_ATTRIBUTE_READONLY)
                    else:
                        os.chmod(archivo, 0o444)
                    print(f"Archivo protegido: {archivo}")
                except Exception as e:
                    print(f"No se pudo proteger {archivo}: {e}")
    except Exception as e:
        print(f"Error al procesar directorio {directorio}: {e}")

def main():
    """Inicia la aplicación de conciliación bancaria"""
    try:
        # Crear una ventana temporal como parent para el selector
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana root
        
        # Mostrar selector de banco
        bank_selector = BankSelector(root)
        root.wait_window(bank_selector)  # Esperar hasta que se cierre la ventana
        
        # Verificar si se seleccionó un banco
        if not hasattr(bank_selector, 'bank_selected') or not bank_selector.bank_selected:
            print("Selección de banco cancelada")
            root.destroy()
            return
        
        # Obtener el banco seleccionado
        selected_bank = bank_selector.selected_bank.get()
        print(f"Banco seleccionado: {selected_bank}")
        
        # Destruir ventana temporal
        root.destroy()
        
        # Si el banco seleccionado es Itaú, continuar con la interfaz actual
        if selected_bank == "Itaú":
            app = ConciliacionBancaria()
            
            # Función para proteger archivos una vez que la aplicación esté iniciada
            def proteger_archivos_al_inicio():
                try:
                    project_root = Path(__file__).parent.parent
                    directorios = [
                        project_root / 'data' / 'input' / 'bank',
                        project_root / 'data' / 'input' / 'accounting',
                        project_root / 'data' / 'output',
                        project_root / 'data' / 'reports'
                    ]
                    
                    for directorio in directorios:
                        proteger_archivos(directorio)
                        
                    print("Protección de archivos completada")
                except Exception as e:
                    print(f"Error en protección de archivos: {e}")
            
            # Llamar a la protección después de que la interfaz esté completamente cargada
            app.after(3000, proteger_archivos_al_inicio)
            
            app.mainloop()
        else:
            # Para otros bancos, mostrar mensaje de "próximamente"
            root = tk.Tk()
            root.withdraw()
            
            import tkinter.messagebox as messagebox
            messagebox.showinfo(
                "Funcionalidad en Desarrollo",
                f"La conciliación para el banco {selected_bank} estará disponible próximamente.\n\n"
                "Actualmente solo está implementada la conciliación para Itaú."
            )
            
            # Volver a iniciar la aplicación para permitir seleccionar otro banco
            main()
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {str(e)}")

if __name__ == "__main__":
    main()
