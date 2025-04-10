import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

class ConciliacionBancaria(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración básica de la ventana
        self.title("Conciliación Bancaria")
        self.geometry("1200x800")
        
        # Crear el contenedor principal
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear los elementos de la interfaz
        self.create_widgets()

    def create_widgets(self):
        # Título
        title_label = ttk.Label(
            self.main_frame, 
            text="Sistema de Conciliación Bancaria",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Frame para cargar archivos
        file_frame = ttk.LabelFrame(self.main_frame, text="Cargar Archivos", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Botón para cargar extracto bancario
        ttk.Button(
            file_frame,
            text="Cargar Extracto Bancario",
            command=self.cargar_extracto
        ).grid(row=0, column=0, padx=5, pady=5)

        # Botón para cargar registro contable
        ttk.Button(
            file_frame,
            text="Cargar Registro Contable",
            command=self.cargar_registro
        ).grid(row=0, column=1, padx=5, pady=5)

        # Frame para acciones
        action_frame = ttk.LabelFrame(self.main_frame, text="Acciones", padding="10")
        action_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Botón para iniciar conciliación
        ttk.Button(
            action_frame,
            text="Iniciar Conciliación",
            command=self.iniciar_conciliacion
        ).grid(row=0, column=0, padx=5, pady=5)

        # Botón para ver reportes
        ttk.Button(
            action_frame,
            text="Ver Reportes",
            command=self.ver_reportes
        ).grid(row=0, column=1, padx=5, pady=5)

    def cargar_extracto(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar Extracto Bancario",
            filetypes=[
                ("Archivos Excel", "*.xlsx"),
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*")
            ]
        )
        if filename:
            messagebox.showinfo("Información", f"Archivo seleccionado: {filename}")

    def cargar_registro(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar Registro Contable",
            filetypes=[
                ("Archivos Excel", "*.xlsx"),
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*")
            ]
        )
        if filename:
            messagebox.showinfo("Información", f"Archivo seleccionado: {filename}")

    def iniciar_conciliacion(self):
        messagebox.showinfo(
            "Información",
            "Función de conciliación en desarrollo"
        )

    def ver_reportes(self):
        messagebox.showinfo(
            "Información",
            "Función de reportes en desarrollo"
        )

def main():
    try:
        app = ConciliacionBancaria()
        app.mainloop()
    except Exception as e:
        print(f"Error: {str(e)}")
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {str(e)}")

if __name__ == "__main__":
    main()
