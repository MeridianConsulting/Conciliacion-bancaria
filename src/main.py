from frontend.interface import ConciliacionBancaria
from backend.reconciliation import Reconciliation
from backend.reconciliation_report import ReconciliationReport
import os
import time
from pathlib import Path

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
    except Exception as e:
        print(f"Error: {str(e)}")
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {str(e)}")

if __name__ == "__main__":
    main()
