import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import ctypes
from backend.reconciliation import Reconciliation
from backend.reconciliation_report import ReconciliationReport
from pathlib import Path
import shutil
import datetime
import tkinter.font as tkfont
import threading
from resource_path import resource_path

# --- Constantes de Diseño --- #
COLOR_BG_MAIN = "#F4F7FA"
COLOR_BG_CARD = "#FFFFFF"
COLOR_TEXT_DARK = "#2A2F35"
COLOR_TEXT_SUBTLE = "#6C757D"
COLOR_PRIMARY_ACCENT = "#1E325A"  # Azul cabecera
COLOR_SUCCESS = "#38B000"        # Verde primario
COLOR_SUCCESS_HOVER = "#40C800"   # Verde hover (+12% aprox)
COLOR_SECONDARY_ACCENT = "#4FB0C6" # Turquesa suave
COLOR_SECONDARY_HOVER = "#5EC5DC"  # Turquesa hover (+12% aprox)
COLOR_ALERT = "#E63946"           # Rojo alerta
COLOR_ALERT_HOVER = "#FF4050"     # Rojo hover (+12% aprox)
COLOR_BORDER = "#D0D5DD"           # Gris neutro para bordes
COLOR_WHITE = "#FFFFFF"

class InstruccionesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configuración básica de la ventana
        self.title("Instrucciones de Uso")
        self.geometry("800x600")
        
        # Establecer el mismo ícono que la ventana principal
        try:
            # Intentar cargar el ícono usando resource_path
            icon_path = resource_path(os.path.join('assets', 'logo.ico'))
            
            # Si no se encuentra, intentar con la ruta absoluta (para modo desarrollo)
            if not os.path.exists(icon_path):
                alt_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'logo.ico'))
                if os.path.exists(alt_path):
                    icon_path = alt_path
                    print(f"Usando ruta alternativa para el ícono: {icon_path}")
            
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error cargando el ícono en instrucciones: {e}")
        
        # Hacer la ventana modal (bloquea la interacción con la ventana principal)
        self.transient(parent)
        self.grab_set()
        
        # Configurar el tema claro para la ventana (coincidiendo con bank_selector)
        self.configure(bg='#F8F9FA')  # Usando el color light_bg de bank_selector
        
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
        
        # Configurar estilos para el tema claro
        style.configure('Instructions.TFrame',
                       background='#F8F9FA')  # light_bg
        
        style.configure('Instructions.TLabel',
                       background='#F8F9FA',  # light_bg
                       foreground='#212529',  # dark_text
                       font=('Segoe UI', 11),
                       wraplength=750,
                       padding=5)
        
        style.configure('InstructionsTitle.TLabel',
                       background='#F8F9FA',  # light_bg
                       foreground='#0A2F5C',  # primary (azul oscuro)
                       font=('Segoe UI', 16, 'bold'),
                       padding=(0, 10))
        
        # Configurar estilo para el botón Entendido
        style.configure('Instructions.TButton',
                       background='#0066B3',  # Azul secundario (secondary de bank_selector) 
                       foreground='#FFFFFF',  # Texto blanco
                       padding=(20, 10))
        
        style.map('Instructions.TButton',
                 background=[('active', '#0A2F5C')])  # Hover en azul más oscuro (primary)
        
        # Frame principal con tema claro
        self.main_frame = ttk.Frame(self, style='Instructions.TFrame')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Canvas con scrollbar (tema claro)
        self.canvas = tk.Canvas(
            self.main_frame,
            bg='#F8F9FA',
            highlightthickness=0,
            bd=0
        )
        
        # Scrollbar con tema claro
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
            bg='#F8F9FA'  # Asegurar que el canvas tenga fondo claro
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

        # --- Configuración Inicial --- #
        self.title("Sistema de Conciliación Bancaria - Meridian Consulting")
        self.configure(bg=COLOR_BG_MAIN)
        self.load_fonts() # Cargar fuentes primero
        self.setup_icon()
        self.configure_window_size() # Ajustar tamaño y mínimo
        self.bind("<Configure>", self.on_window_resize)

        # --- Rutas y Backend --- #
        self.setup_paths()
        self.proteger_archivos_excel() # Intentar proteger (con manejo de errores interno)
        self.reconciliation = Reconciliation()
        self.report_generator = ReconciliationReport()

        # --- Estado UI --- #
        self.extractos_bancarios = []
        self.registros_contables = []
        self.is_loading_extractos = False
        self.is_loading_registros = False
        self.is_processing = False

        # --- Estilos TTK --- #
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        # --- Crear Widgets --- #
        self.create_widgets()

        # --- Mostrar Instrucciones (Opcional) --- #
        # self.after(500, self.show_instructions)

    def load_fonts(self):
        """Carga fuentes preferidas o usa alternativas del sistema."""
        families = tkfont.families()
        primary_font = "Segoe UI" # Default
        if 'Inter' in families:
            primary_font = 'Inter'
        elif 'Roboto' in families:
            primary_font = 'Roboto'
        elif 'Segoe UI' in families:
            primary_font = 'Segoe UI' # Ya es el default, pero explícito
        elif 'Helvetica' in families:
            primary_font = 'Helvetica'
        elif 'Arial' in families:
            primary_font = 'Arial'
        else:
            primary_font = tkfont.nametofont("TkDefaultFont").actual()["family"]

        self.FONT_TITLE = (primary_font, 24, 'bold')
        self.FONT_SUBTITLE = (primary_font, 16, 'bold')
        self.FONT_BODY = (primary_font, 11)
        self.FONT_BODY_BOLD = (primary_font, 11, 'bold')
        self.FONT_BUTTON = (primary_font, 11, 'bold')
        self.FONT_CAPTION = (primary_font, 9)

    def setup_icon(self):
        """Configura el ícono de la ventana y la barra de tareas."""
        try:
            # Intentar cargar el ícono usando resource_path
            icon_path = resource_path(os.path.join('assets', 'logo.ico'))
            
            # Si no se encuentra, intentar con la ruta absoluta (para modo desarrollo)
            if not os.path.exists(icon_path):
                alt_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'logo.ico'))
                if os.path.exists(alt_path):
                    icon_path = alt_path
                    print(f"Usando ruta alternativa para el ícono: {icon_path}")
            
            if os.path.exists(icon_path):
                self.iconbitmap(default=icon_path)
                if os.name == 'nt':
                    app_id = "Meridian.ConciliacionBancaria.1"
                    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except Exception as e:
            print(f"Advertencia: No se pudo configurar el ícono: {e}")

    def setup_paths(self):
        """Configura las rutas del proyecto y crea directorios necesarios."""
        self.project_root = Path(__file__).parent.parent.parent
        self.input_bank_path = self.project_root / 'data' / 'input' / 'bank'
        self.input_accounting_path = self.project_root / 'data' / 'input' / 'accounting'
        self.output_path = self.project_root / 'data' / 'output'
        self.report_path = self.project_root / 'data' / 'reports'

        for path in [self.input_bank_path, self.input_accounting_path, self.output_path, self.report_path]:
            path.mkdir(parents=True, exist_ok=True)

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

        # Calcular dimensiones de la ventana
        # Ancho basado en el listbox (80 caracteres) más márgenes
        window_width = 900  # Ancho óptimo para los listbox de 80 caracteres
        window_height = min(800, screen_height - 100)  # Altura máxima de 800px o screen_height - 100

        # Calcular posición para centrar la ventana
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2

        # Configurar geometría de la ventana
        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        
        # Establecer tamaños mínimos
        self.minsize(900, 700)  # Tamaño mínimo ajustado al contenido

    def configure_styles(self):
        """Configura los estilos TTK para los widgets"""
        # Estilo base para Frames
        self.style.configure('TFrame', background=COLOR_BG_MAIN)

        # Frame principal que contiene todo
        self.style.configure('MainContainer.TFrame', background=COLOR_BG_MAIN)

        # Frame tipo "Card" para cada paso
        self.style.configure('Card.TFrame', 
                           background=COLOR_BG_CARD, 
                           relief='solid', 
                           borderwidth=1, 
                           bordercolor=COLOR_BORDER)

        # Estilo para el título principal de la aplicación
        self.style.configure('Title.TLabel', 
                           background=COLOR_BG_MAIN, 
                           foreground=COLOR_TEXT_DARK, 
                           font=self.FONT_TITLE, 
                           anchor='center')

        # Estilo para los subtítulos de cada paso ("Paso 1:", etc.)
        self.style.configure('Subtitle.TLabel', 
                           background=COLOR_BG_CARD, 
                           foreground=COLOR_PRIMARY_ACCENT, 
                           font=self.FONT_SUBTITLE)
        
        # Estilo para texto cuerpo normal
        self.style.configure('Body.TLabel', 
                           background=COLOR_BG_CARD, 
                           foreground=COLOR_TEXT_DARK, 
                           font=self.FONT_BODY)

        # --- Estilos de Botones --- #
        button_padding = (20, 10) # Padding horizontal y vertical para botones

        # Botón Primario (Cargar)
        self.style.configure('Success.TButton', 
                           background=COLOR_SUCCESS,
                           foreground=COLOR_WHITE, 
                           font=self.FONT_BUTTON, 
                           padding=button_padding, 
                           relief='flat', 
                           borderwidth=0)
        self.style.map('Success.TButton', 
                       background=[('active', COLOR_SUCCESS_HOVER), ('disabled', '#B0B0B0')])

        # Botón Secundario (Ver Reportes)
        self.style.configure('Secondary.TButton', 
                           background=COLOR_SECONDARY_ACCENT, 
                           foreground=COLOR_WHITE, 
                           font=self.FONT_BUTTON, 
                           padding=button_padding, 
                           relief='flat', 
                           borderwidth=0)
        self.style.map('Secondary.TButton', 
                       background=[('active', COLOR_SECONDARY_HOVER), ('disabled', '#B0B0B0')])

        # Botón de Alerta (Eliminar)
        self.style.configure('Alert.TButton', 
                           background=COLOR_ALERT, 
                           foreground=COLOR_WHITE, 
                           font=self.FONT_BUTTON, 
                           padding=button_padding, 
                           relief='flat', 
                           borderwidth=0)
        self.style.map('Alert.TButton', 
                       background=[('active', COLOR_ALERT_HOVER), ('disabled', '#B0B0B0')])

        # --- Estilos Treeview --- #
        self.style.configure('Treeview', 
                           background=COLOR_WHITE, 
                           foreground=COLOR_TEXT_DARK, 
                           fieldbackground=COLOR_WHITE, 
                           rowheight=25, 
                           font=self.FONT_BODY, 
                           relief='solid', 
                           borderwidth=1, 
                           bordercolor=COLOR_BORDER)
        self.style.map('Treeview', background=[('selected', COLOR_PRIMARY_ACCENT)]) # Color de selección
        
        self.style.configure("Treeview.Heading", 
                           background=COLOR_BG_MAIN, 
                           foreground=COLOR_PRIMARY_ACCENT, 
                           font=self.FONT_BODY_BOLD, 
                           relief="flat")
        self.style.map("Treeview.Heading", background=[('active', COLOR_BORDER)])

    def create_widgets(self):
        """Crea y organiza los widgets principales de la interfaz."""
        # Contenedor principal con padding
        main_frame = ttk.Frame(self, padding=(30, 20), style='MainContainer.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Configurar filas y columnas para expandir
        main_frame.grid_rowconfigure(1, weight=1) # Fila para Paso 1
        main_frame.grid_rowconfigure(2, weight=1) # Fila para Paso 2
        main_frame.grid_columnconfigure(0, weight=1)

        # --- Título --- #
        title_label = ttk.Label(main_frame, 
                                text="Sistema de Conciliación Bancaria", 
                                style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 30), sticky='ew')

        # --- Paso 1: Extractos Bancarios --- #
        self.extractos_frame = self.create_step_ui(
            main_frame, 
            title="Paso 1: Cargar Extractos Bancarios",
            load_command=self.cargar_extractos_con_spinner,
            delete_command=self.confirmar_eliminar_extractos,
            treeview_attr="extractos_treeview",
            load_btn_attr="load_extractos_btn"
        )
        self.extractos_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 20))

        # --- Paso 2: Registros Contables --- #
        self.registros_frame = self.create_step_ui(
            main_frame, 
            title="Paso 2: Cargar Registros Contables",
            load_command=self.cargar_registros_con_spinner,
            delete_command=self.confirmar_eliminar_registros,
            treeview_attr="registros_treeview",
            load_btn_attr="load_registros_btn"
        )
        self.registros_frame.grid(row=2, column=0, sticky='nsew', pady=(0, 30))

        # --- Línea Divisoria --- #
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=3, column=0, sticky='ew', pady=(0, 20))

        # --- Botones de Acción Finales --- #
        actions_frame = ttk.Frame(main_frame, style='MainContainer.TFrame')
        actions_frame.grid(row=4, column=0, sticky='ew')
        actions_frame.grid_columnconfigure(0, weight=1) # Espaciador
        actions_frame.grid_columnconfigure(1, weight=0) # Botón Reportes
        actions_frame.grid_columnconfigure(2, weight=0) # Botón Conciliar

        self.reportes_btn = ttk.Button(
            actions_frame,
            text="Ver Reportes",
            command=self.ver_reportes,
            style='Secondary.TButton'
        )
        self.reportes_btn.grid(row=0, column=1, sticky='e', padx=(0, 15))

        self.conciliacion_btn = ttk.Button(
            actions_frame,
            text="Iniciar Conciliación",
            command=self.iniciar_conciliacion,
            style='Success.TButton' # Usar estilo Success para verde
        )
        self.conciliacion_btn.grid(row=0, column=2, sticky='e')

    def create_step_ui(self, parent, title, load_command, delete_command, treeview_attr, load_btn_attr):
        """Crea la UI para una sección de carga de archivos (Paso 1 o Paso 2)."""
        # Frame contenedor tipo Card
        card_frame = ttk.Frame(parent, padding=20, style='Card.TFrame')
        card_frame.grid_columnconfigure(0, weight=1)
        card_frame.grid_rowconfigure(1, weight=1) # Hacer que TreeView se expanda

        # Subtítulo del paso
        subtitle_label = ttk.Label(card_frame, text=title, style='Subtitle.TLabel')
        subtitle_label.grid(row=0, column=0, sticky='w', pady=(0, 15))

        # --- TreeView para mostrar archivos --- #
        tree_frame = ttk.Frame(card_frame, style='TFrame', padding=0) # Frame sin padding interno extra
        tree_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 15))
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        columns = ('nombre', 'tamaño')
        treeview = ttk.Treeview(tree_frame, columns=columns, show='headings', height=5, style='Treeview')

        treeview.heading('nombre', text='Nombre del Archivo', anchor='w')
        treeview.heading('tamaño', text='Tamaño', anchor='e')
        treeview.column('nombre', stretch=tk.YES, anchor='w')
        treeview.column('tamaño', width=120, stretch=tk.NO, anchor='e')

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=treeview.yview)
        treeview.configure(yscrollcommand=scrollbar.set)

        treeview.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Guardar referencia al TreeView
        setattr(self, treeview_attr, treeview)

        # --- Botones de Carga y Eliminación --- #
        button_frame = ttk.Frame(card_frame, style='Card.TFrame') # Fondo blanco de la card
        button_frame.grid(row=2, column=0, sticky='e')

        load_btn = ttk.Button(
            button_frame,
            text="Cargar Archivos",
            command=load_command,
            style='Success.TButton' # Usar estilo Success para verde
        )
        load_btn.pack(side=tk.LEFT, padx=(0, 15))
        # Guardar referencia al botón de carga
        setattr(self, load_btn_attr, load_btn)

        delete_btn = ttk.Button(
            button_frame,
            text="Eliminar Seleccionados",
            command=delete_command,
            style='Alert.TButton'
        )
        delete_btn.pack(side=tk.LEFT)

        return card_frame

    def on_window_resize(self, event):
        """Maneja el evento de redimensionamiento de la ventana"""
        if event.widget == self:
            # Actualizar el layout si es necesario
            self.update_idletasks()

    def cargar_extractos_con_spinner(self):
        """Carga extractos bancarios mostrando un spinner durante el proceso"""
        if getattr(self, 'is_loading_extractos', False):
            return

        self.is_loading_extractos = True
        original_text = self.load_extractos_btn.cget('text')
        self.load_extractos_btn.config(text="Cargando...", state="disabled", style='Success.TButton') # Mantener estilo
        self.update_idletasks()

        def process():
            try:
                archivos = filedialog.askopenfilenames(
                    title="Seleccionar Extractos Bancarios",
                    filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*"))
                )
                if archivos:
                    self.extractos_bancarios.extend(archivos)
                    for archivo in archivos:
                        nombre_archivo = os.path.basename(archivo)
                        tamaño = self.get_file_size(archivo)
                        self.extractos_treeview.insert('', 'end', values=(nombre_archivo, tamaño))
                    self.after(0, lambda: messagebox.showinfo("Éxito", f"Se cargaron {len(archivos)} extractos bancarios."))
            except Exception as e:
                print(f"Error cargando extractos: {e}")
                self.after(0, lambda: messagebox.showerror("Error", f"Error al cargar extractos: {e}"))
            finally:
                self.is_loading_extractos = False
                # Usar after para asegurar que se ejecute en el hilo principal
                self.after(0, lambda: self.load_extractos_btn.config(text=original_text, state="normal"))

        threading.Thread(target=process, daemon=True).start()

    def cargar_registros_con_spinner(self):
        """Carga registros contables mostrando un spinner durante el proceso"""
        if getattr(self, 'is_loading_registros', False):
            return

        self.is_loading_registros = True
        original_text = self.load_registros_btn.cget('text')
        self.load_registros_btn.config(text="Cargando...", state="disabled", style='Success.TButton') # Mantener estilo
        self.update_idletasks()

        def process():
            try:
                archivos = filedialog.askopenfilenames(
                    title="Seleccionar Registros Contables",
                    filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*"))
                )
                if archivos:
                    self.registros_contables.extend(archivos)
                    for archivo in archivos:
                        nombre_archivo = os.path.basename(archivo)
                        tamaño = self.get_file_size(archivo)
                        self.registros_treeview.insert('', 'end', values=(nombre_archivo, tamaño))
                    self.after(0, lambda: messagebox.showinfo("Éxito", f"Se cargaron {len(archivos)} registros contables."))
            except Exception as e:
                print(f"Error cargando registros: {e}")
                self.after(0, lambda: messagebox.showerror("Error", f"Error al cargar registros: {e}"))
            finally:
                self.is_loading_registros = False
                self.after(0, lambda: self.load_registros_btn.config(text=original_text, state="normal"))

        threading.Thread(target=process, daemon=True).start()

    def confirmar_eliminar_extractos(self):
        """Muestra diálogo de confirmación y elimina extractos seleccionados."""
        seleccionados = self.extractos_treeview.selection()
        if not seleccionados:
            messagebox.showinfo("Información", "No hay extractos seleccionados para eliminar.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar {len(seleccionados)} extracto(s) seleccionado(s)?",
            icon='warning'
        )

        if confirmar:
            items_a_eliminar = list(seleccionados) # Copiar selección
            indices_a_eliminar = sorted([self.extractos_treeview.index(item) for item in items_a_eliminar], reverse=True)
            
            for index in indices_a_eliminar:
                if index < len(self.extractos_bancarios):
                     del self.extractos_bancarios[index]
            
            for item_id in items_a_eliminar:
                 self.extractos_treeview.delete(item_id)

            messagebox.showinfo("Éxito", f"Se eliminaron {len(seleccionados)} extracto(s).")

    def confirmar_eliminar_registros(self):
        """Muestra diálogo de confirmación y elimina registros seleccionados."""
        seleccionados = self.registros_treeview.selection()
        if not seleccionados:
            messagebox.showinfo("Información", "No hay registros seleccionados para eliminar.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar {len(seleccionados)} registro(s) seleccionado(s)?",
            icon='warning'
        )

        if confirmar:
            items_a_eliminar = list(seleccionados) # Copiar selección
            indices_a_eliminar = sorted([self.registros_treeview.index(item) for item in items_a_eliminar], reverse=True)

            for index in indices_a_eliminar:
                 if index < len(self.registros_contables):
                     del self.registros_contables[index]
            
            for item_id in items_a_eliminar:
                self.registros_treeview.delete(item_id)

            messagebox.showinfo("Éxito", f"Se eliminaron {len(seleccionados)} registro(s).")

    def get_file_size(self, file_path):
        """Devuelve el tamaño del archivo en formato legible (KB, MB)."""
        try:
            size_bytes = os.path.getsize(file_path)
            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1024**2:
                return f"{size_bytes / 1024:.1f} KB"
            else:
                return f"{size_bytes / (1024**2):.1f} MB"
        except FileNotFoundError:
            return "N/A"
        except Exception as e:
            print(f"Error obteniendo tamaño de {file_path}: {e}")
            return "Error"

    def iniciar_conciliacion(self):
        # Verificar que se hayan cargado archivos
        if not self.extractos_treeview.size() or not self.registros_treeview.size():
            messagebox.showwarning(
                "Archivos Faltantes",
                "Debe cargar al menos un extracto bancario y un registro contable"
            )
            return
            
        # Mostrar un indicador de procesamiento
        self.config(cursor="wait")
        self.update()
        
        try:
            # Usar directamente las rutas de archivos originales almacenadas en:
            # self.extractos_bancarios - para archivos de banco
            # self.registros_contables - para archivos de contabilidad
            
            # Paso 1: Procesar archivos contables con rutas originales
            print("=== Procesando archivos contables ===")
            contabilidad_ok = self.reconciliation.extract_excel_to_json(self.registros_contables)
            
            # Paso 2: Procesar extractos bancarios con rutas originales
            print("=== Procesando extractos bancarios ===")
            banco_ok = self.reconciliation.extract_bank_excel_to_json(self.extractos_bancarios)
            
            # Paso 3: Generar reportes
            if contabilidad_ok and banco_ok:
                print("=== Generando reportes de conciliación ===")
                result = self.report_generator.process()
                
                if result:
                    # Mostrar mensaje de éxito con detalles
                    mensaje = f"""
Conciliación completada con éxito

Archivos generados:"""
                    
                    # Verificar si se generó el reporte Excel
                    if result['excel_report']:
                        mensaje += f"\n- Excel: {os.path.basename(result['excel_report'])}"
                    else:
                        mensaje += "\n- Excel: No se pudo generar debido a un error"
                    
                    # Verificar si se generó el reporte PDF
                    if result['pdf_report']:
                        mensaje += f"\n- PDF: {os.path.basename(result['pdf_report'])}"
                    else:
                        mensaje += "\n- PDF: No se pudo generar debido a un error"
                    
                    mensaje += f"""

Resumen:
- Transacciones conciliadas: {len(result['comparison_result']['conciliadas'])}
- Solo en contabilidad: {len(result['comparison_result']['no_conciliadas_contabilidad'])}
- Solo en banco: {len(result['comparison_result']['no_conciliadas_banco'])}
"""
                    messagebox.showinfo("Conciliación Completada", mensaje)
                else:
                    messagebox.showwarning(
                        "Advertencia", 
                        "Se procesaron los archivos pero no se pudieron generar los reportes."
                    )
            else:
                messagebox.showwarning(
                    "Procesamiento Incompleto", 
                    "No se pudieron procesar todos los archivos. Revise el formato y estructura."
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error durante la conciliación: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            # Restaurar el cursor
            self.config(cursor="")

    def ver_reportes(self):
        try:
            # Buscar los reportes más recientes
            excel_files = list(self.report_path.glob("conciliacion_*.xlsx"))
            pdf_files = list(self.report_path.glob("conciliacion_*.pdf"))
            
            if not excel_files and not pdf_files:
                messagebox.showinfo("Información", "No se encontraron reportes generados.")
                return
                
            # Ordenar por fecha de creación (más recientes primero)
            if excel_files:
                excel_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                # Abrir el archivo Excel más reciente
                os.startfile(str(excel_files[0]))
                
            if pdf_files:
                pdf_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                # Abrir el archivo PDF más reciente
                os.startfile(str(pdf_files[0]))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir los reportes: {str(e)}")

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

    def create_shortcut(self, icon_path, app_id):
        """Crea un acceso directo para ayudar a Windows a asociar el ícono con la aplicación"""
        import win32com.client
        import sys
        
        # Ruta para el acceso directo
        shortcut_path = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Conciliación Bancaria.lnk")
        
        # Verificar si el acceso directo ya existe
        if not os.path.exists(shortcut_path):
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = sys.executable
            shortcut.Arguments = os.path.abspath(sys.argv[0])
            shortcut.WorkingDirectory = os.path.dirname(os.path.abspath(sys.argv[0]))
            shortcut.IconLocation = icon_path
            shortcut.save()

    def proteger_archivos_excel(self):
        """Protege los archivos Excel contra eliminación accidental"""
        try:
            # Directorios donde están los archivos
            directorios = [
                self.input_bank_path,
                self.input_accounting_path,
                self.report_path
            ]
            
            # Proteger todos los archivos Excel en estos directorios
            for directorio in directorios:
                if directorio.exists():
                    for archivo in directorio.glob("*.xlsx"):
                        try:
                            # Cambiar atributos del archivo para protegerlo
                            if os.name == 'nt':  # Windows
                                # Establecer atributo de solo lectura
                                import win32api, win32con
                                win32api.SetFileAttributes(str(archivo), win32con.FILE_ATTRIBUTE_READONLY)
                            else:
                                # Para sistemas Unix/Linux
                                os.chmod(archivo, 0o444)  # Solo lectura para todos
                            print(f"Archivo protegido: {archivo}")
                        except Exception as e:
                            print(f"No se pudo proteger el archivo {archivo}: {e}")
        except Exception as e:
            print(f"Error al proteger archivos: {e}")

def main():
    try:
        app = ConciliacionBancaria()
        app.mainloop()
    except Exception as e:
        print(f"Error: {str(e)}")
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {str(e)}")

if __name__ == "__main__":
    main()
