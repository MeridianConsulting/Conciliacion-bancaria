import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import ctypes

class InstruccionesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configuración básica de la ventana
        self.title("Instrucciones de Uso")
        self.geometry("800x600")
        
        # Hacer la ventana modal (bloquea la interacción con la ventana principal)
        self.transient(parent)
        self.grab_set()
        
        # Configurar el tema oscuro para la ventana
        self.configure(bg='#1e1e2e')
        
        # Centrar la ventana
        self.center_window()
        
        # Variable para rastrear si la ventana está activa
        self.is_active = True
        
        # Crear contenido
        self.create_content()
        
        # Vincular evento de cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self):
        # Obtener dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calcular posición
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        
        # Posicionar ventana
        self.geometry(f"800x600+{x}+{y}")
        
    def create_content(self):
        # Estilo para el contenido
        style = ttk.Style()
        
        # Configurar estilos para el tema oscuro
        style.configure('Instructions.TFrame',
                       background='#1e1e2e')
        
        style.configure('Instructions.TLabel',
                       background='#1e1e2e',
                       foreground='#ffffff',
                       font=('Segoe UI', 11),
                       wraplength=750,
                       padding=5)
        
        style.configure('InstructionsTitle.TLabel',
                       background='#1e1e2e',
                       foreground='#ffffff',
                       font=('Segoe UI', 16, 'bold'),
                       padding=(0, 10))
        
        # Configurar estilo para el botón Entendido
        style.configure('Instructions.TButton',
                       background='#e01b24',  # Mismo rojo que los botones de eliminar
                       foreground='#ffffff',
                       padding=(20, 10))
        
        style.map('Instructions.TButton',
                 background=[('active', '#a51d2d')])  # Mismo hover que los botones de eliminar
        
        # Frame principal con tema oscuro
        self.main_frame = ttk.Frame(self, style='Instructions.TFrame')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Canvas con scrollbar (tema oscuro)
        self.canvas = tk.Canvas(
            self.main_frame,
            bg='#1e1e2e',
            highlightthickness=0,
            bd=0
        )
        
        # Scrollbar con tema oscuro
        self.scrollbar = ttk.Scrollbar(
            self.main_frame,
            orient="vertical",
            command=self.canvas.yview
        )
        
        # Frame de contenido
        self.content_frame = ttk.Frame(
            self.canvas,
            style='Instructions.TFrame'
        )
        
        # Configurar scroll
        self.canvas.configure(
            yscrollcommand=self.scrollbar.set,
            bg='#1e1e2e'  # Asegurar que el canvas tenga fondo oscuro
        )
        
        # Pack scrollbar y canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Crear ventana en el canvas
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.content_frame,
            anchor="nw",
            width=self.canvas.winfo_width()
        )
        
        # Título principal
        ttk.Label(
            self.content_frame,
            text="Guía de Uso del Sistema de Conciliación Bancaria",
            style='InstructionsTitle.TLabel'
        ).pack(pady=(0, 20))
        
        # Sección 1: Cargar Extractos Bancarios
        ttk.Label(
            self.content_frame,
            text="1. Carga de Extractos Bancarios (Paso 1)",
            style='InstructionsTitle.TLabel'
        ).pack(anchor='w')
        
        ttk.Label(
            self.content_frame,
            text="• El botón 'Cargar Extractos Bancarios' se encuentra en la parte superior de la primera sección.\n"
                 "• Al hacer clic, se abrirá un explorador de archivos para seleccionar uno o varios extractos bancarios.\n"
                 "• Los archivos seleccionados aparecerán en la lista debajo del botón.\n"
                 "• Para eliminar extractos, seleccione uno o varios de la lista y use el botón 'Eliminar Extractos Seleccionados'.",
            style='Instructions.TLabel'
        ).pack(anchor='w', pady=(0, 20))
        
        # Sección 2: Cargar Registros Contables
        ttk.Label(
            self.content_frame,
            text="2. Carga de Registros Contables (Paso 2)",
            style='InstructionsTitle.TLabel'
        ).pack(anchor='w')
        
        ttk.Label(
            self.content_frame,
            text="• El botón 'Cargar Registros Contables' está ubicado en la segunda sección.\n"
                 "• Funciona de manera similar al botón de extractos bancarios.\n"
                 "• Permite seleccionar múltiples archivos de registros contables.\n"
                 "• Use el botón 'Eliminar Registros Seleccionados' para quitar registros de la lista.",
            style='Instructions.TLabel'
        ).pack(anchor='w', pady=(0, 20))
        
        # Sección 3: Acciones Principales
        ttk.Label(
            self.content_frame,
            text="3. Acciones Principales",
            style='InstructionsTitle.TLabel'
        ).pack(anchor='w')
        
        ttk.Label(
            self.content_frame,
            text="• Los botones principales se encuentran en la parte inferior de la ventana:\n"
                 "  - 'Iniciar Conciliación': Comienza el proceso de conciliación con los archivos seleccionados.\n"
                 "  - 'Ver Reportes': Muestra los reportes generados de las conciliaciones realizadas.",
            style='Instructions.TLabel'
        ).pack(anchor='w', pady=(0, 20))
        
        # Sección 4: Recomendaciones
        ttk.Label(
            self.content_frame,
            text="4. Recomendaciones Importantes",
            style='InstructionsTitle.TLabel'
        ).pack(anchor='w')
        
        ttk.Label(
            self.content_frame,
            text="• Asegúrese de cargar al menos un extracto bancario y un registro contable antes de iniciar la conciliación.\n"
                 "• Los archivos deben estar en formato Excel (.xlsx) o CSV.\n"
                 "• Puede seleccionar múltiples archivos manteniendo presionada la tecla Ctrl.\n"
                 "• Verifique que los archivos seleccionados sean correctos antes de iniciar la conciliación.",
            style='Instructions.TLabel'
        ).pack(anchor='w', pady=(0, 20))
        
        # Botón de cerrar con estilo rojo
        ttk.Button(
            self.content_frame,
            text="Entendido",
            command=self.on_closing,
            style='Instructions.TButton'
        ).pack(pady=20)
        
        # Configurar eventos
        self.content_frame.bind('<Configure>', self.on_frame_configure)
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        # Configurar el scroll con la rueda del mouse
        self.bind_mousewheel()
        
    def bind_mousewheel(self):
        """Vincula el evento de la rueda del mouse al canvas"""
        def _on_mousewheel(event):
            if self.is_active:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Vincular el evento a todos los frames
        self.bind_all("<MouseWheel>", _on_mousewheel)
        
    def unbind_mousewheel(self):
        """Desvincula el evento de la rueda del mouse"""
        self.unbind_all("<MouseWheel>")
        
    def on_frame_configure(self, event=None):
        """Actualiza el scroll region cuando el frame cambia de tamaño"""
        if self.is_active:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_canvas_configure(self, event):
        """Ajusta el ancho del frame contenedor cuando el canvas cambia de tamaño"""
        if self.is_active:
            self.canvas.itemconfig(self.canvas_window, width=event.width)
            
    def on_closing(self):
        """Maneja el cierre de la ventana"""
        self.is_active = False
        self.unbind_mousewheel()
        self.destroy()

class ConciliacionBancaria(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Conciliación Bancaria")
        
        # Agregar estas líneas para la configuración de la ventana
        self.configure_window_size()
        self.bind("<Configure>", self.on_window_resize)
        
        # Definir las paletas de colores
        self.theme = {
            'bg_primary': '#1e1e2e',
            'bg_secondary': '#2a2a3e',
            'bg_tertiary': '#313244',
            'button_bg': '#3584e4',
            'button_hover': '#1a5fb4',
            'text_primary': '#ffffff',
            'text_secondary': '#9999a8',
            'border': '#363649',
            'listbox_bg': '#2a2a3e',
            'listbox_fg': '#ffffff',
            'card_shadow': '0 2px 4px rgba(0, 0, 0, 0.2)',
            'delete_button_bg': '#e01b24',        # Nuevo color rojo para el botón eliminar
            'delete_button_hover': '#a51d2d'      # Nuevo color rojo más oscuro para el hover
        }
        
        # Configurar el estilo de la aplicación
        self.configure(bg=self.theme['bg_primary'])
        
        # Crear contenedor principal con márgenes optimizados
        self.container = ttk.Frame(self, style='Main.TFrame')
        self.container.grid(row=0, column=0, sticky="nsew", padx=15, pady=12)
        
        # Configurar grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Configurar pesos de las filas del contenedor
        self.container.grid_rowconfigure(0, weight=0)  # Título
        self.container.grid_rowconfigure(1, weight=3)  # Extractos
        self.container.grid_rowconfigure(2, weight=3)  # Registros
        self.container.grid_rowconfigure(3, weight=1)  # Botones
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
        
        # Mostrar instrucciones al inicio
        self.after(500, self.show_instructions)
    
    def configure_window_size(self):
        """Configura el tamaño inicial de la ventana basado en la resolución de la pantalla"""
        try:
            # Para Windows
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
        except:
            # Fallback para otros sistemas
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

        # Calcular dimensiones de la ventana (ahora 100px menos que la pantalla)
        window_width = screen_width - 150
        window_height = screen_height - 150  # Aumentamos el margen para la barra de tareas

        # Calcular posición para centrar la ventana
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2

        # Configurar geometría de la ventana
        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        
        # Establecer tamaños mínimos
        self.minsize(800, 600)

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
        
        # Agregar estilo para botones de eliminar
        self.style.configure('Delete.TButton',
                           background=self.theme['delete_button_bg'],
                           foreground=self.theme['text_primary'],
                           font=('Segoe UI', 10),
                           padding=(12, 6))
        
        self.style.map('Delete.TButton',
                      background=[('active', self.theme['delete_button_hover'])])

    def create_widgets(self):
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
            style='Delete.TButton'
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
            style='Delete.TButton'
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

    def on_window_resize(self, event):
        """Maneja el evento de redimensionamiento de la ventana"""
        if event.widget == self:
            # Actualizar el layout si es necesario
            self.update_idletasks()

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

    def show_instructions(self):
        """Muestra la ventana de instrucciones"""
        InstruccionesWindow(self)

    def create_file_entry(self, parent, label_text, y_position):
        label = tk.Label(parent, text=label_text)
        label.place(x=10, y=y_position)
        
        entry = tk.Entry(parent, width=35)  # Reducido de 50 a 40
        entry.place(x=150, y=y_position)
        
        button = tk.Button(parent, text="Examinar", command=lambda: self.browse_file(entry))
        button.place(x=500, y=y_position-2)
        
        return entry

def main():
    try:
        app = ConciliacionBancaria()
        app.mainloop()
    except Exception as e:
        print(f"Error: {str(e)}")
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {str(e)}")

if __name__ == "__main__":
    main()
