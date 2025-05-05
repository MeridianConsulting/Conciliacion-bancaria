import tkinter as tk
from tkinter import ttk
import os

class BankSelector(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configuración básica de la ventana
        self.title("Seleccionar Banco")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Configurar el tema oscuro para la ventana
        self.configure(bg='#1e1e2e')
        
        # Centrar la ventana
        self.center_window()
        
        # Variable para almacenar el banco seleccionado
        self.selected_bank = tk.StringVar()
        
        # Lista de bancos disponibles
        self.available_banks = [
            "Itaú",
            "BBVA",
            "Bancolombia",
            "Banco de Bogotá",
            "Banco de Occidente",
            "AV Villas",
            "Credicorp",
            "Corficolombiana",
            "Fiduciaria"
        ]
        
        # Crear contenido
        self.create_content()
        
        # Variable para rastrear si se ha seleccionado un banco
        self.bank_selected = False
        
        # Vincular evento de cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        # Obtener dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calcular posición
        x = (screen_width - 400) // 2
        y = (screen_height - 300) // 2
        
        # Posicionar ventana
        self.geometry(f"400x300+{x}+{y}")
    
    def create_content(self):
        # Frame principal
        main_frame = tk.Frame(self, bg='#1e1e2e')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title = tk.Label(
            main_frame,
            text="Seleccionar Banco",
            bg='#1e1e2e',
            fg='white',
            font=('Segoe UI', 16, 'bold')
        )
        title.pack(pady=(0, 20))
        
        # Instrucciones
        info = tk.Label(
            main_frame,
            text="Elija el banco para la conciliación:",
            bg='#1e1e2e',
            fg='white',
            font=('Segoe UI', 11)
        )
        info.pack(pady=(0, 20))
        
        # Selector de banco
        self.bank_combo = ttk.Combobox(
            main_frame,
            textvariable=self.selected_bank,
            values=self.available_banks,
            state='readonly',
            font=('Segoe UI', 11),
            width=25
        )
        self.bank_combo.current(0)  # Seleccionar Itaú por defecto
        self.bank_combo.pack(pady=10)
        
        # Botón continuar
        continue_button = tk.Button(
            main_frame,
            text="Continuar",
            bg='#3584e4',
            fg='white',
            font=('Segoe UI', 11),
            bd=0,
            padx=15,
            pady=8,
            command=self.on_continue
        )
        continue_button.pack(pady=20)
    
    def on_continue(self):
        self.bank_selected = True
        self.destroy()
    
    def on_closing(self):
        if not self.bank_selected:
            self.master.destroy()
        else:
            self.destroy() 