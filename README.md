# Sistema de Conciliación Bancaria

## Descripción
Este proyecto implementa un sistema automatizado para la conciliación de extractos bancarios con registros contables. El sistema permite procesar diferentes formatos de archivos Excel, normalizar los datos y realizar la conciliación automática.

## Estructura del Proyecto

```
bank_reconciliation_project/
├── src/ # Código fuente
│ ├── frontend/ # Interfaz de usuario
│ │ ├── init.py
│ │ └── interface.py # Interfaz gráfica
│ ├── backend/ # Lógica de negocio
│ │ ├── init.py
│ │ └── reconciliation.py # Lógica de conciliación
│ └── main.py # Punto de entrada
│
├── data/ # Datos del sistema
│ ├── input/ # Datos de entrada
│ │ ├── bank/ # Extractos bancarios
│ │ └── accounting/ # Registros contables
│ └── output/ # Resultados y reportes
│
└── requirements.txt # Dependencias del proyecto
```

## Módulos Principales

### 1. Frontend (`src/frontend/`)
- Interfaz gráfica de usuario
- Gestión de interacciones del usuario
- Visualización de datos y resultados

### 2. Backend (`src/backend/`)
- Procesamiento de datos
- Lógica de conciliación
- Generación de reportes

## Requisitos del Sistema

- Python 3.x
- Dependencias listadas en `requirements.txt`
- Acceso a archivos de extractos bancarios y registros contables

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   venv\Scripts\activate     # En Windows
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Colocar los archivos de entrada en las carpetas correspondientes:
   - Extractos bancarios en `data/input/bank/`
   - Registros contables en `data/input/accounting/`

2. Ejecutar el programa:
   ```bash
   python src/main.py
   ```

3. Los resultados se generarán en:
   - `data/output/` - Reportes y resultados de la conciliación

## Flujo de Trabajo

1. Cargar Archivos
   - Seleccionar el extracto bancario
   - Seleccionar el registro contable

2. Procesar Datos
   - Los archivos se procesan automáticamente
   - Se normalizan los datos para la conciliación

3. Generar Resultados
   - Se realiza la conciliación automática
   - Se genera un reporte detallado
   - Se guardan los resultados en la carpeta de salida

## Contribución

1. Crear una rama para la nueva característica
2. Implementar los cambios
3. Enviar un pull request

## Licencia

Este proyecto está bajo la licencia MIT. 