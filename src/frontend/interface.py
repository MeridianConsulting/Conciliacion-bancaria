import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os

class ConciliacionBancaria(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración básica de la ventana
        self.title("Sistema de Conciliación Bancaria")
        
        # Obtener dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calcular dimensiones iniciales (90% del tamaño de la pantalla)
        initial_width = int(screen_width * 0.9)
        initial_height = int(screen_height * 0.9)
        
        # Establecer tamaño mínimo más grande para evitar scroll
        self.minsize(1024, 768)
        
        # Centrar la ventana
        x = (screen_width - initial_width) // 2
        y = (screen_height - initial_height) // 2
        self.geometry(f"{initial_width}x{initial_height}+{x}+{y}")
        
        # Definir las paletas de colores
        self.theme = {
            'bg_primary': '#1e1e2e',      # Fondo principal más oscuro y elegante
            'bg_secondary': '#2a2a3e',    # Fondo secundario para tarjetas
            'bg_tertiary': '#313244',     # Fondo terciario para elementos internos
            'button_bg': '#3584e4',       # Azul más vibrante para botones
            'button_hover': '#1a5fb4',    # Azul más oscuro para hover
            'text_primary': '#ffffff',    # Texto principal blanco
            'text_secondary': '#9999a8',  # Texto secundario gris más suave
            'border': '#363649',          # Color de bordes más sutil
            'listbox_bg': '#2a2a3e',      # Fondo para listbox
            'listbox_fg': '#ffffff',      # Texto para listbox
            'card_shadow': '0 2px 4px rgba(0, 0, 0, 0.2)'  # Sombra sutil para tarjetas
        }
        
        # Configurar el estilo de la aplicación
        self.configure(bg=self.theme['bg_primary'])
        
        # Crear contenedor principal
        self.container = ttk.Frame(self, style='Main.TFrame')
        self.container.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        
        # Configurar grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Configurar estilos
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Variables para almacenar los archivos
        self.extractos_seleccionados = []
        self.registros_seleccionados = []
        
        # Crear widgets
        self.create_widgets()
        
        # Vincular evento de redimensionamiento
        self.bind('<Configure>', self.on_window_resize)
    
    def configure_styles(self):
        """Configura los estilos personalizados para los widgets"""
        # Estilo para el frame principal
        self.style.configure('Main.TFrame',
                           background=self.theme['bg_primary'])
        
        # Estilo para las tarjetas
        self.style.configure('Card.TFrame',
                           background=self.theme['bg_secondary'],
                           relief='flat')
        
        # Estilo para el título principal
        self.style.configure('Title.TLabel',
                           background=self.theme['bg_primary'],
                           foreground=self.theme['text_primary'],
                           font=('Segoe UI', 28, 'bold'),
                           padding=(0, 10, 0, 20))
        
        # Estilo para los títulos de las tarjetas
        self.style.configure('CardTitle.TLabel',
                           background=self.theme['bg_secondary'],
                           foreground=self.theme['text_primary'],
                           font=('Segoe UI', 16, 'bold'),
                           padding=(0, 5))
        
        # Estilo para botones principales
        self.style.configure('Primary.TButton',
                           background=self.theme['button_bg'],
                           foreground=self.theme['text_primary'],
                           font=('Segoe UI', 11),
                           padding=(15, 8),
                           relief='flat',
                           borderwidth=0)
        
        self.style.map('Primary.TButton',
                      background=[('active', self.theme['button_hover'])])
        
        # Estilo para botones secundarios
        self.style.configure('Secondary.TButton',
                           background=self.theme['bg_tertiary'],
                           foreground=self.theme['text_secondary'],
                           font=('Segoe UI', 10),
                           padding=(12, 6))
        
        # Estilo para el contenedor de la lista
        self.style.configure('ListContainer.TFrame',
                           background=self.theme['bg_secondary'],
                           relief='flat')

    def create_widgets(self):
        # Configurar pesos de las filas del contenedor principal
        self.container.grid_rowconfigure(1, weight=1)  # Extractos
        self.container.grid_rowconfigure(2, weight=1)  # Registros
        self.container.grid_rowconfigure(3, weight=0)  # Botones de acción

        # Título principal
        title_frame = ttk.Frame(self.container, style='Main.TFrame')
        title_frame.grid(row=0, column=0, sticky='ew', pady=(0, 20))
        title_frame.grid_columnconfigure(0, weight=1)
        
        title = ttk.Label(title_frame,
                         text="Sistema de Conciliación Bancaria",
                         style='Title.TLabel',
                         anchor='center')
        title.grid(row=0, column=0)
        
        # Frame para extractos bancarios
        extractos_frame = self.create_card_frame("⚡ Paso 1: Cargar Extractos Bancarios", 1)
        
        # Botón cargar extractos
        load_extractos_btn = ttk.Button(
            extractos_frame,
            text="🏠 Cargar Extractos Bancarios",
            command=self.cargar_extractos,
            style='Primary.TButton'
        )
        load_extractos_btn.grid(row=1, column=0, pady=15)
        
        # Lista de extractos
        self.extractos_listbox = tk.Listbox(
            extractos_frame,
            bg=self.theme['listbox_bg'],
            fg=self.theme['listbox_fg'],
            selectmode=tk.EXTENDED,
            height=6,  # Aumentar altura de la lista
            font=('Segoe UI', 10),
            relief='flat',
            borderwidth=0
        )
        self.extractos_listbox.grid(row=2, column=0, sticky='ew', padx=20, pady=15)
        
        # Botón eliminar extractos
        delete_extractos_btn = ttk.Button(
            extractos_frame,
            text="Eliminar Extractos Seleccionados",
            command=self.eliminar_extractos,
            style='Secondary.TButton'
        )
        delete_extractos_btn.grid(row=3, column=0, pady=10)
        
        # Frame para registros contables
        registros_frame = self.create_card_frame("🎲 Paso 2: Cargar Registros Contables", 2)
        
        # Botón cargar registros
        load_registros_btn = ttk.Button(
            registros_frame,
            text="🎲 Cargar Registros Contables",
            command=self.cargar_registros,
            style='Primary.TButton'
        )
        load_registros_btn.grid(row=1, column=0, pady=15)
        
        # Lista de registros
        self.registros_listbox = tk.Listbox(
            registros_frame,
            bg=self.theme['listbox_bg'],
            fg=self.theme['listbox_fg'],
            selectmode=tk.EXTENDED,
            height=6,  # Aumentar altura de la lista
            font=('Segoe UI', 10),
            relief='flat',
            borderwidth=0
        )
        self.registros_listbox.grid(row=2, column=0, sticky='ew', padx=20, pady=15)
        
        # Botón eliminar registros
        delete_registros_btn = ttk.Button(
            registros_frame,
            text="Eliminar Registros Seleccionados",
            command=self.eliminar_registros,
            style='Secondary.TButton'
        )
        delete_registros_btn.grid(row=3, column=0, pady=10)
        
        # Frame para botones de acción
        actions_frame = ttk.Frame(self.container, style='Card.TFrame')
        actions_frame.grid(row=3, column=0, sticky='ew', pady=(20, 0))
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)
        
        # Botones de acción
        conciliacion_btn = ttk.Button(
            actions_frame,
            text="Iniciar Conciliación",
            command=self.iniciar_conciliacion,
            style='Primary.TButton'
        )
        conciliacion_btn.grid(row=0, column=0, padx=5, pady=15)
        
        reportes_btn = ttk.Button(
            actions_frame,
            text="Ver Reportes",
            command=self.ver_reportes,
            style='Primary.TButton'
        )
        reportes_btn.grid(row=0, column=1, padx=5, pady=15)

    def create_card_frame(self, title, row):
        """Crea un frame tipo tarjeta con título"""
        frame = ttk.Frame(self.container, style='Card.TFrame')
        frame.grid(row=row, column=0, sticky='nsew', pady=10)
        frame.grid_columnconfigure(0, weight=1)
        
        # Título de la tarjeta
        title_label = ttk.Label(
            frame,
            text=title,
            style='CardTitle.TLabel'
        )
        title_label.grid(row=0, column=0, sticky='w', padx=20, pady=10)
        
        return frame

    def on_window_resize(self, event=None):
        """Maneja el evento de redimensionamiento de la ventana"""
        if event and event.widget == self:
            # Calcular padding basado en el tamaño de la ventana
            width = self.winfo_width()
            
            # Ajustar el tamaño de la fuente del título según el ancho de la ventana
            title_size = min(28, max(20, int(width * 0.025)))
            self.style.configure('Title.TLabel', font=('Segoe UI', title_size, 'bold'))

    def cargar_extractos(self):
        filenames = filedialog.askopenfilenames(
            title="Seleccionar Extractos Bancarios",
            filetypes=[
                ("Archivos Excel", "*.xlsx"),
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*")
            ]
        )
        if filenames:
            self.extractos_listbox.delete(0, tk.END)
            for filename in filenames:
                if filename not in self.extractos_seleccionados:
                    self.extractos_seleccionados.append(filename)
                    self.extractos_listbox.insert(tk.END, os.path.basename(filename))
            messagebox.showinfo("Información", f"Se han cargado {len(filenames)} extractos bancarios")

    def cargar_registros(self):
        filenames = filedialog.askopenfilenames(
            title="Seleccionar Registros Contables",
            filetypes=[
                ("Archivos Excel", "*.xlsx"),
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*")
            ]
        )
        if filenames:
            self.registros_listbox.delete(0, tk.END)
            for filename in filenames:
                if filename not in self.registros_seleccionados:
                    self.registros_seleccionados.append(filename)
                    self.registros_listbox.insert(tk.END, os.path.basename(filename))
            messagebox.showinfo("Información", f"Se han cargado {len(filenames)} registros contables")

    def eliminar_extractos(self):
        selected_indices = self.extractos_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("Información", "Por favor, seleccione extractos para eliminar")
            return
            
        for index in sorted(selected_indices, reverse=True):
            self.extractos_listbox.delete(index)
            self.extractos_seleccionados.pop(index)
            
        messagebox.showinfo("Información", f"Se han eliminado {len(selected_indices)} extractos")

    def eliminar_registros(self):
        selected_indices = self.registros_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("Información", "Por favor, seleccione registros para eliminar")
            return
            
        for index in sorted(selected_indices, reverse=True):
            self.registros_listbox.delete(index)
            self.registros_seleccionados.pop(index)
            
        messagebox.showinfo("Información", f"Se han eliminado {len(selected_indices)} registros")

    def iniciar_conciliacion(self):
        if not self.extractos_seleccionados or not self.registros_seleccionados:
            messagebox.showwarning(
                "Advertencia",
                "Debe cargar al menos un extracto bancario y un registro contable para iniciar la conciliación"
            )
            return
            
        messagebox.showinfo(
            "Información",
            f"Iniciando conciliación con {len(self.extractos_seleccionados)} extractos y {len(self.registros_seleccionados)} registros"
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
