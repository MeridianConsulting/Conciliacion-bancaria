# Sistema de Conciliación Bancaria

## Descripción
Este proyecto implementa un sistema automatizado para la conciliación de extractos bancarios con registros contables. El sistema permite procesar diferentes formatos de archivos (Excel, PDF), normalizar los datos y realizar la conciliación automática.

## Estructura del Proyecto

```
bank_reconciliation_project/
├── docs/                           # Documentación del proyecto
│   ├── requirements.md             # Especificación de requisitos
│   ├── design.md                   # Documentación de arquitectura
│   └── roadmap.md                  # Planificación del proyecto
│
├── data/                           # Datos del sistema
│   ├── raw/                        # Datos originales
│   │   ├── banks/                  # Extractos bancarios
│   │   └── accounting/             # Registros contables
│   └── processed/                  # Datos normalizados
│
├── logs/                           # Archivos de registro
│
├── src/                            # Código fuente
│   ├── config/                     # Configuración
│   │   ├── __init__.py
│   │   └── config.py               # Parámetros globales
│   │
│   ├── extraction/                 # Extracción de datos
│   │   ├── __init__.py
│   │   ├── excel_extractor.py      # Procesamiento de Excel
│   │   └── pdf_extractor.py        # Procesamiento de PDF
│   │
│   ├── normalization/              # Normalización de datos
│   │   ├── __init__.py
│   │   └── data_normalizer.py      # Transformación de datos
│   │
│   ├── validation/                 # Validación y conciliación
│   │   ├── __init__.py
│   │   └── reconciliation.py       # Lógica de conciliación
│   │
│   ├── reporting/                  # Generación de reportes
│   │   ├── __init__.py
│   │   └── report_generator.py     # Creación de reportes
│   │
│   ├── utils/                      # Utilidades
│   │   ├── __init__.py
│   │   └── logger.py               # Sistema de logs
│   │
│   └── main.py                     # Punto de entrada
│
└── tests/                          # Pruebas unitarias
    ├── __init__.py
    ├── test_extraction.py
    ├── test_normalization.py
    ├── test_validation.py
    └── test_reporting.py
```

## Módulos Principales

### 1. Extracción de Datos (`src/extraction/`)
- Procesa archivos Excel y PDF
- Extrae información de extractos bancarios y registros contables
- Implementa OCR para archivos PDF

### 2. Normalización (`src/normalization/`)
- Transforma datos a formato estándar
- Normaliza fechas, montos y textos
- Unifica formatos de diferentes fuentes

### 3. Validación (`src/validation/`)
- Compara transacciones entre sistemas
- Identifica discrepancias
- Genera alertas de diferencias

### 4. Reportes (`src/reporting/`)
- Genera reportes detallados
- Exporta resultados en diferentes formatos
- Crea dashboards de conciliación

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
   - Extractos bancarios en `data/raw/banks/`
   - Registros contables en `data/raw/accounting/`

2. Ejecutar el programa principal:
   ```bash
   python src/main.py
   ```

3. Los resultados se generarán en:
   - Datos normalizados: `data/processed/`
   - Reportes: `data/reports/`
   - Logs: `logs/`

## Documentación Adicional

- [Requisitos](docs/requirements.md)
- [Diseño](docs/design.md)
- [Roadmap](docs/roadmap.md)

## Contribución

1. Crear una rama para la nueva característica
2. Implementar los cambios
3. Ejecutar las pruebas
4. Enviar un pull request

## Licencia

Este proyecto está bajo la licencia MIT. 