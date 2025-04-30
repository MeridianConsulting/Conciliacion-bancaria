from frontend.interface import ConciliacionBancaria
from backend.reconciliation import Reconciliation
from backend.reconciliation_report import ReconciliationReport
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import threading
from pathlib import Path

class ArchivoProtector(FileSystemEventHandler):
    def __init__(self, directorios):
        self.directorios = directorios
        
    def on_deleted(self, event):
        # Comprobar si es un archivo Excel
        if event.src_path.endswith('.xlsx'):
            print(f"Se detectó intento de eliminación: {event.src_path}")
            # Buscar en directorio de backup si existe una copia
            nombre_archivo = os.path.basename(event.src_path)
            for dir_base in self.directorios:
                backup_dir = dir_base.parent / 'backup'
                if backup_dir.exists():
                    for subdir in backup_dir.glob('*'):
                        if subdir.is_dir():
                            backup_path = subdir / nombre_archivo
                            if backup_path.exists():
                                # Restaurar archivo desde backup
                                import shutil
                                dest_dir = Path(os.path.dirname(event.src_path))
                                dest_dir.mkdir(parents=True, exist_ok=True)
                                shutil.copy2(backup_path, event.src_path)
                                print(f"Archivo restaurado desde backup: {nombre_archivo}")
                                # Proteger archivo restaurado
                                if os.name == 'nt':
                                    import win32api, win32con
                                    win32api.SetFileAttributes(event.src_path, win32con.FILE_ATTRIBUTE_READONLY)
                                else:
                                    os.chmod(event.src_path, 0o444)
                                break

def iniciar_proteccion(app):
    # Directorios a monitorear
    directorios = [
        app.input_bank_path,
        app.input_accounting_path,
        app.report_path
    ]
    
    # Iniciar observadores
    event_handler = ArchivoProtector(directorios)
    observer = Observer()
    
    for directorio in directorios:
        if directorio.exists():
            observer.schedule(event_handler, str(directorio), recursive=False)
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    """Inicia la aplicación de conciliación bancaria"""
    try:
        app = ConciliacionBancaria()
        
        # Iniciar protección de archivos después de que la aplicación esté lista
        app.after(1000, lambda: threading.Thread(target=iniciar_proteccion, args=(app,), daemon=True).start())
        
        app.mainloop()
    except Exception as e:
        print(f"Error: {str(e)}")
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {str(e)}")

if __name__ == "__main__":
    main()
