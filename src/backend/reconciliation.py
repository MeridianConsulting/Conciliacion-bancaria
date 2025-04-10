import pandas as pd
import json
import os
from pathlib import Path
from datetime import datetime

class Reconciliation:
    def __init__(self):
        # Obtener la ruta absoluta del proyecto
        self.project_root = Path(__file__).parent.parent.parent
        self.accounting_path = self.project_root / 'data' / 'input' / 'accounting'
        self.output_path = self.project_root / 'data' / 'output'
        
        # Crear directorios si no existen
        self.accounting_path.mkdir(parents=True, exist_ok=True)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def extract_header_info(self, df):
        """Extrae la información del encabezado del reporte"""
        header_info = {
            "tipo_reporte": df.iloc[1, 0],  # "MOVIMIENTO CUENTAS - GENERAL"
            "periodo": df.iloc[2, 0],        # "De: MAR  1/2025 A: MAR 31/2025"
            "fecha_proceso": df.iloc[4, 0],  # "Procesado en: 2025/04/08  15:14:10:89"
        }
        return header_info

    def get_column_names(self, df):
        """Obtiene los nombres reales de las columnas del reporte"""
        # Buscar la fila que contiene los nombres de las columnas
        for idx, row in df.iterrows():
            if "CUENTA" in str(row[0]) and "DESCRIPCION" in str(row[0]):
                column_names = []
                for value in row:
                    if pd.notna(value) and str(value).strip():
                        column_names.append(str(value).strip())
                return column_names
        return None

    def extract_excel_to_json(self):
        """Extrae los archivos Excel de Siigo y los convierte a JSON con formato mejorado"""
        try:
            all_data = []
            excel_files = list(self.accounting_path.glob('*.xlsx'))
            
            if not excel_files:
                print(f"No se encontraron archivos Excel en {self.accounting_path}")
                return False

            for excel_file in excel_files:
                print(f"Procesando archivo: {excel_file.name}")
                
                try:
                    # Leer el archivo Excel
                    df = pd.read_excel(excel_file, header=None)
                    
                    # Extraer información del encabezado
                    header_info = self.extract_header_info(df)
                    
                    # Obtener nombres reales de columnas
                    column_names = self.get_column_names(df)
                    
                    if not column_names:
                        print(f"No se encontraron nombres de columnas en {excel_file.name}")
                        continue

                    # Encontrar el índice donde comienzan los datos reales
                    start_index = None
                    for idx, row in df.iterrows():
                        if "CUENTA" in str(row[0]) and "DESCRIPCION" in str(row[0]):
                            start_index = idx + 1
                            break

                    if start_index is None:
                        print(f"No se encontró el inicio de los datos en {excel_file.name}")
                        continue

                    # Procesar solo las filas con datos
                    data_rows = []
                    for idx, row in df.iloc[start_index:].iterrows():
                        # Verificar si la fila tiene datos significativos
                        if pd.notna(row[0]) and str(row[0]).strip():
                            record = {}
                            for col_idx, value in enumerate(row):
                                if col_idx < len(column_names):
                                    # Convertir NaN a cadena vacía
                                    if pd.isna(value):
                                        value = ""
                                    # Convertir números a float si es necesario
                                    elif isinstance(value, (int, float)):
                                        value = float(value)
                                    else:
                                        value = str(value).strip()
                                    
                                    record[column_names[col_idx]] = value
                            data_rows.append(record)

                    # Crear estructura final del documento
                    document = {
                        "metadata": header_info,
                        "movimientos": data_rows
                    }

                    # Guardar archivo JSON individual
                    json_filename = self.output_path / f"{excel_file.stem}.json"
                    with open(json_filename, 'w', encoding='utf-8') as f:
                        json.dump(document, f, ensure_ascii=False, indent=2)
                    
                    print(f"Archivo JSON creado: {json_filename}")
                    
                    # Agregar a la lista completa
                    all_data.append(document)
                
                except Exception as e:
                    print(f"Error procesando {excel_file.name}: {str(e)}")
                    continue

            # Guardar archivo JSON combinado
            combined_json_path = self.output_path / 'all_accounting_data.json'
            with open(combined_json_path, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
            
            print(f"\nProceso completado. Archivos procesados: {len(excel_files)}")
            print(f"Datos combinados guardados en: {combined_json_path}")
            
            # Mostrar muestra del resultado
            print("\nMuestra del formato JSON generado:")
            if all_data:
                print(json.dumps(all_data[0]["metadata"], indent=2, ensure_ascii=False))
                print("\nPrimeros 2 movimientos:")
                print(json.dumps(all_data[0]["movimientos"][:2], indent=2, ensure_ascii=False))
            
            return True

        except Exception as e:
            print(f"Error en el proceso de extracción: {str(e)}")
            return False

    def get_excel_info(self):
        """
        Obtiene información sobre los archivos Excel disponibles
        """
        try:
            excel_files = list(self.accounting_path.glob('*.xlsx'))
            info = []
            
            for excel_file in excel_files:
                df = pd.read_excel(excel_file)
                info.append({
                    "filename": excel_file.name,
                    "rows": len(df),
                    "columns": list(df.columns),
                    "size": f"{excel_file.stat().st_size / 1024:.2f} KB"
                })
            
            return info
        
        except Exception as e:
            print(f"Error obteniendo información de archivos: {str(e)}")
            return []

def main():
    # Crear instancia y ejecutar
    reconciliation = Reconciliation()
    reconciliation.extract_excel_to_json()

if __name__ == "__main__":
    main()
