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

class InstruccionesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configuración básica de la ventana
        self.title("Instrucciones de Uso")
        self.geometry("800x600")
        
        # Establecer el mismo ícono que la ventana principal
        try:
            icon_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'logo.ico'))
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error cargando el ícono en instrucciones: {e}")
        
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
        
        # Configuración inicial
        self.title("Sistema de Conciliación Bancaria")
        
        # Configurar íconos para Windows (tanto ventana como barra de tareas)
        try:
            # Ruta absoluta al ícono
            icon_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'logo.ico'))
            
            if os.path.exists(icon_path):
                # Establecer ícono para la ventana
                self.iconbitmap(default=icon_path)
                
                # Configuración específica para la barra de tareas de Windows
                if os.name == 'nt':
                    # Establecer ID único para la aplicación
                    app_id = "ConciliacionBancaria.Application.1.0"
                    # Intentar configurar AppID para la barra de tareas
                    try:
                        from ctypes import windll
                        windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
                        # Crear acceso directo para mejorar asociación de íconos
                        self.create_shortcut(icon_path, app_id)
                    except Exception as e:
                        print(f"No se pudo configurar AppID: {e}")
        except Exception as e:
            print(f"Error al configurar ícono: {e}")
        
        # Proteger archivos al iniciar
        self.proteger_archivos_excel()
        
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
        self.container.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        
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
        self.extractos_bancarios = []
        self.registros_contables = []
        
        # Ruta de entrada y salida
        self.project_root = Path(__file__).parent.parent.parent
        self.input_bank_path = self.project_root / 'data' / 'input' / 'bank'
        self.input_accounting_path = self.project_root / 'data' / 'input' / 'accounting'
        self.output_path = self.project_root / 'data' / 'output'
        self.report_path = self.project_root / 'data' / 'reports'
        
        # Crear directorios necesarios
        self.input_bank_path.mkdir(parents=True, exist_ok=True)
        self.input_accounting_path.mkdir(parents=True, exist_ok=True)
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.report_path.mkdir(parents=True, exist_ok=True)
        
        # Crear widgets
        self.create_widgets()
        
        # Mostrar instrucciones al inicio
        self.after(500, self.show_instructions)
        
        # Inicializar los controladores del backend
        self.reconciliation = Reconciliation()
        self.report_generator = ReconciliationReport()
    
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
        
        # Frame para registros contables (ahora es Paso 1)
        extractos_frame = self.create_card_frame("⚡ Paso 1: Cargar Registros Contables", 1)
        extractos_frame.grid_columnconfigure(0, weight=1)  # Centrar contenido
        
        # Contenedor para la lista de extractos
        list_container_extractos = ttk.Frame(extractos_frame, style='Card.TFrame')
        list_container_extractos.grid(row=1, column=0, sticky='ew', padx=30, pady=15)
        
        # Lista de extractos con ancho ajustado
        self.extractos_listbox = tk.Listbox(
            list_container_extractos,
            bg=self.theme['listbox_bg'],
            fg=self.theme['listbox_fg'],
            selectmode=tk.EXTENDED,
            height=6,
            width=80,  # Ancho aumentado a 80 caracteres
            font=('Segoe UI', 10),
            relief='flat',
            borderwidth=0
        )
        self.extractos_listbox.pack(fill='both', expand=True)
        
        # Frame para los botones de extractos
        extractos_buttons_frame = ttk.Frame(extractos_frame, style='Card.TFrame')
        extractos_buttons_frame.grid(row=2, column=0, sticky='e', padx=20, pady=(0, 10))
        
        # Botón cargar extractos
        load_extractos_btn = ttk.Button(
            extractos_buttons_frame,
            text="🏠 Cargar Registros Contables",
            command=self.cargar_extractos,
            style='Primary.TButton'
        )
        load_extractos_btn.pack(side='left', padx=5)
        
        # Botón eliminar extractos
        delete_extractos_btn = ttk.Button(
            extractos_buttons_frame,
            text="Eliminar Seleccionados",
            command=self.eliminar_extractos,
            style='Delete.TButton'
        )
        delete_extractos_btn.pack(side='left', padx=5)
        
        # Frame para extractos bancarios (ahora es Paso 2)
        registros_frame = self.create_card_frame("🎲 Paso 2: Cargar Extractos Bancarios", 2)
        registros_frame.grid_columnconfigure(0, weight=1)  # Centrar contenido
        
        # Contenedor para la lista de registros
        list_container_registros = ttk.Frame(registros_frame, style='Card.TFrame')
        list_container_registros.grid(row=1, column=0, sticky='ew', padx=30, pady=15)
        
        # Lista de registros con ancho ajustado
        self.registros_listbox = tk.Listbox(
            list_container_registros,
            bg=self.theme['listbox_bg'],
            fg=self.theme['listbox_fg'],
            selectmode=tk.EXTENDED,
            height=6,
            width=80,  # Ancho aumentado a 80 caracteres
            font=('Segoe UI', 10),
            relief='flat',
            borderwidth=0
        )
        self.registros_listbox.pack(fill='both', expand=True)
        
        # Frame para los botones de registros
        registros_buttons_frame = ttk.Frame(registros_frame, style='Card.TFrame')
        registros_buttons_frame.grid(row=2, column=0, columnspan=2, sticky='e', padx=20, pady=(0, 10))
        
        # Botón cargar registros
        load_registros_btn = ttk.Button(
            registros_buttons_frame,
            text="🎲 Cargar Extractos Bancarios",
            command=self.cargar_registros,
            style='Primary.TButton'
        )
        load_registros_btn.pack(side='left', padx=5)
        
        # Botón eliminar registros
        delete_registros_btn = ttk.Button(
            registros_buttons_frame,
            text="Eliminar Seleccionados",
            command=self.eliminar_registros,
            style='Delete.TButton'
        )
        delete_registros_btn.pack(side='left', padx=5)
        
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
        # Solicitar al usuario seleccionar archivos
        archivos = filedialog.askopenfilenames(
            title="Seleccionar Registros Contables",
            filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*"))
        )
        
        if archivos:
            # Guardar lista de archivos seleccionados
            self.registros_contables.extend(archivos)
            
            # Mostrar archivos en la lista sin copiarlos
            for archivo in archivos:
                nombre_archivo = os.path.basename(archivo)
                self.extractos_listbox.insert(tk.END, nombre_archivo)
                print(f"Archivo referenciado: {archivo}")
            
            # NO copiar archivos físicamente al directorio de entrada

    def cargar_registros(self):
        # Solicitar al usuario seleccionar archivos
        archivos = filedialog.askopenfilenames(
            title="Seleccionar Extractos Bancarios",
            filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*"))
        )
        
        if archivos:
            # Guardar lista de archivos seleccionados
            self.extractos_bancarios.extend(archivos)
            
            # Mostrar archivos en la lista sin copiarlos
            for archivo in archivos:
                nombre_archivo = os.path.basename(archivo)
                self.registros_listbox.insert(tk.END, nombre_archivo)
                print(f"Archivo referenciado: {archivo}")
            
            # NO copiar archivos físicamente al directorio de entrada

    def eliminar_extractos(self):
        seleccionados = self.extractos_listbox.curselection()
        if seleccionados:
            # Eliminar desde el final para no afectar los índices
            for i in sorted(seleccionados, reverse=True):
                archivo = self.extractos_listbox.get(i)
                self.extractos_listbox.delete(i)
                
                # Eliminar de la lista interna
                if i < len(self.extractos_bancarios):
                    self.extractos_bancarios.pop(i)

    def eliminar_registros(self):
        seleccionados = self.registros_listbox.curselection()
        if seleccionados:
            # Eliminar desde el final para no afectar los índices
            for i in sorted(seleccionados, reverse=True):
                archivo = self.registros_listbox.get(i)
                self.registros_listbox.delete(i)
                
                # Eliminar de la lista interna
                if i < len(self.registros_contables):
                    self.registros_contables.pop(i)

    def iniciar_conciliacion(self):
        # Verificar que se hayan cargado archivos
        if not self.extractos_listbox.size() or not self.registros_listbox.size():
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

Archivos generados:
- Excel: {os.path.basename(result['excel_report'])}
- PDF: {os.path.basename(result['pdf_report'])}

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
