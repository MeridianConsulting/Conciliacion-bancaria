import pandas as pd
import json
import os
from pathlib import Path
from datetime import datetime
import traceback

class Reconciliation:
    def __init__(self):
        # Configurar rutas
        self.project_root = Path(__file__).parent.parent.parent
        self.input_accounting_path = self.project_root / 'data' / 'input' / 'accounting'
        self.input_bank_path = self.project_root / 'data' / 'input' / 'bank'
        self.output_path = self.project_root / 'data' / 'output'
        self.temp_path = self.project_root / 'data' / 'temp'
        
        # Crear directorios si no existen
        self.input_accounting_path.mkdir(parents=True, exist_ok=True)
        self.input_bank_path.mkdir(parents=True, exist_ok=True)
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.temp_path.mkdir(parents=True, exist_ok=True)

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

    def order_json_fields(self, data, campo_orden_comun=None):
        """
        Ordena los campos en los archivos JSON para tener un formato consistente.
        Coloca primero los campos comunes y después los diferentes.
        
        Args:
            data: Datos JSON a ordenar
            campo_orden_comun: Lista con el orden deseado para los campos comunes
        
        Returns:
            Datos JSON ordenados
        """
        if not campo_orden_comun:
            # Definir el orden común para los campos que aparecen en ambos tipos de archivos
            campo_orden_comun = ["FECHA", "DESCRIPCION", "DEBITOS", "CREDITOS"]
        
        # Si es un diccionario con 'metadata' y 'movimientos'
        if isinstance(data, dict) and "movimientos" in data:
            # Ordenar cada movimiento en la lista
            movimientos_ordenados = []
            for movimiento in data["movimientos"]:
                movimiento_ordenado = {}
                
                # Primero añadir los campos comunes en el orden establecido
                for campo in campo_orden_comun:
                    if campo in movimiento:
                        movimiento_ordenado[campo] = movimiento[campo]
                
                # Luego añadir los campos restantes ordenados alfabéticamente
                campos_restantes = sorted([campo for campo in movimiento if campo not in campo_orden_comun])
                for campo in campos_restantes:
                    movimiento_ordenado[campo] = movimiento[campo]
                
                movimientos_ordenados.append(movimiento_ordenado)
            
            # Crear nueva estructura con los movimientos ordenados
            data_ordenado = {
                "metadata": data["metadata"],
                "movimientos": movimientos_ordenados
            }
            return data_ordenado
        
        # Si es una lista de documentos
        elif isinstance(data, list):
            datos_ordenados = []
            for documento in data:
                datos_ordenados.append(self.order_json_fields(documento, campo_orden_comun))
            return datos_ordenados
        
        # Para otros tipos de datos, retornar sin cambios
        return data

    def extract_excel_to_json(self):
        """Extrae los archivos Excel de registros contables y los convierte a JSON con formato comparable"""
        try:
            # No modificar archivos en input/accounting, solo leerlos
            excel_files = list(self.input_accounting_path.glob("*.xlsx"))
            
            if not excel_files:
                print("No se encontraron archivos Excel en el directorio de registros contables")
                return False
            
            print(f"Procesando {len(excel_files)} archivos Excel de registros contables...")
            
            all_data = []
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
                    
                    # Campos requeridos
                    campos_requeridos = ["COMPROBANTE", "FECHA", "DESCRIPCION", "DEBITOS", "CREDITOS"]
                    
                    for idx, row in df.iloc[start_index:].iterrows():
                        # Verificar si la fila tiene datos significativos
                        if pd.notna(row[0]) and str(row[0]).strip():
                            # Verificar si llegamos a las filas de totales (generalmente contienen términos como "TOTAL", "SUMA", etc.)
                            primera_celda = str(row[0]).strip().upper()
                            if "TOTAL" in primera_celda or "SUMA" in primera_celda or "SALDO FINAL" in primera_celda:
                                print(f"Encontrado fin de datos en fila {idx}")
                                break
                                
                            # Crear nuevo registro con solo los campos solicitados
                            record = {}
                            
                            for campo in campos_requeridos:
                                if campo in column_names:
                                    col_idx = column_names.index(campo)
                                    value = row.iloc[col_idx] if col_idx < len(row) else ""
                                    
                                    # Convertir NaN a cadena vacía
                                    if pd.isna(value):
                                        value = ""
                                    # Formatear la fecha en el estilo YYYY-MM-DD HH:MM:SS
                                    elif campo == "FECHA":
                                        try:
                                            # Si es un número, considerarlo como el día del mes de marzo de 2025
                                            if isinstance(value, (int, float)) or (isinstance(value, str) and value.strip().isdigit()):
                                                day = int(float(value)) if isinstance(value, str) else int(value)
                                                # Formatear el día con dos dígitos
                                                day_str = f"{day:02d}"
                                                value = f"2025-03-{day_str} 00:00:00"
                                            else:
                                                # Si no es número, dejarlo como string
                                                value = str(value).strip()
                                        except (ValueError, TypeError):
                                            value = str(value).strip()
                                    # Convertir números a float si es necesario
                                    elif isinstance(value, (int, float)):
                                        value = float(value)
                                    else:
                                        value = str(value).strip()
                                    
                                    record[campo] = value
                            
                            data_rows.append(record)

                    # Crear estructura final del documento
                    document = {
                        "metadata": header_info,
                        "movimientos": data_rows
                    }
                    
                    # Ordenar los campos del JSON
                    document_ordenado = self.order_json_fields(document)

                    # Guardar archivo JSON individual
                    json_filename = self.output_path / f"{excel_file.stem}.json"
                    with open(json_filename, 'w', encoding='utf-8') as f:
                        json.dump(document_ordenado, f, ensure_ascii=False, indent=2)
                    
                    print(f"Archivo JSON creado: {json_filename}")
                    
                    # Agregar a la lista completa
                    all_data.append(document_ordenado)
                
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
            excel_files = list(self.input_accounting_path.glob('*.xlsx'))
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

    def extract_bank_excel_to_json(self):
        """Extrae los archivos Excel de extractos bancarios y los convierte a JSON con formato comparable"""
        try:
            # No modificar archivos en input/bank, solo leerlos
            excel_files = list(self.input_bank_path.glob("*.xlsx"))
            
            if not excel_files:
                print("No se encontraron archivos Excel en el directorio de extractos bancarios")
                return False
            
            print(f"Procesando {len(excel_files)} archivos Excel de extractos bancarios...")
            
            bank_data = []
            for excel_file in excel_files:
                print(f"Procesando extracto bancario: {excel_file.name}")
                
                try:
                    # Leer el archivo Excel completo
                    df = pd.read_excel(excel_file, header=None)
                    
                    # Extraer información del resumen (primeras filas)
                    resumen = {}
                    for idx, row in df.iterrows():
                        if pd.isna(row[0]) or 'Día' in str(row[0]):  # Detener cuando llegue al encabezado de la tabla
                            break
                        if len(row) >= 2 and pd.notna(row[0]) and pd.notna(row[1]):
                            concepto = str(row[0]).strip()
                            # Convertir el valor a float si es numérico
                            try:
                                # Remover comas de los números y convertir a float
                                valor_str = str(row[1]).replace(',', '')
                                valor = float(valor_str) if pd.notna(row[1]) else 0.0
                            except:
                                valor = str(row[1]).strip()
                            
                            if concepto:  # Solo agregar si hay concepto
                                resumen[concepto] = valor

                    # Buscar la fila que contiene "Día" como encabezado
                    header_row = None
                    for idx, row in df.iterrows():
                        if pd.notna(row[0]) and 'Día' in str(row[0]):
                            header_row = idx
                            break

                    if header_row is not None:
                        # Obtener los datos desde la siguiente fila después de los encabezados
                        data_df = df.iloc[header_row + 1:].copy()
                        data_df.columns = df.iloc[header_row]
                        
                        # Procesar los datos
                        normalized_data = []
                        for _, row in data_df.iterrows():
                            if pd.notna(row['Día']):  # Solo procesar filas con día válido
                                try:
                                    # Verificar que no estamos procesando una fila de encabezado repetida
                                    primera_celda = str(row.iloc[0]).strip().upper() if pd.notna(row.iloc[0]) else ""
                                    if "DÍA" in primera_celda or "DIA" in primera_celda or "DESCRIPCIÓN" in primera_celda:
                                        continue  # Saltar filas que son encabezados repetidos
                                    
                                    # Función auxiliar para convertir valores monetarios
                                    def convert_to_float(value):
                                        if pd.isna(value):
                                            return 0.0
                                        if isinstance(value, (int, float)):
                                            return float(value)
                                        # Verificar si la cadena solo contiene espacios o está vacía
                                        if isinstance(value, str) and value.strip() == "":
                                            return 0.0
                                        # Remover comas y convertir a float
                                        try:
                                            return float(str(value).replace(',', ''))
                                        except (ValueError, TypeError):
                                            # Si no se puede convertir, retornar 0.0
                                            print(f"No se pudo convertir '{value}' a número, usando 0.0 en su lugar")
                                            return 0.0

                                    # Formatear la fecha como YYYY-MM-DD HH:MM:SS
                                    try:
                                        day = int(row['Día']) if pd.notna(row['Día']) else 1
                                        day_str = f"{day:02d}"
                                        fecha_formateada = f"2025-03-{day_str} 00:00:00"
                                    except (ValueError, TypeError):
                                        fecha_formateada = "2025-03-01 00:00:00"  # Valor predeterminado

                                    # Función para buscar columna de forma segura
                                    def get_column_value(df_row, possible_names, default=""):
                                        for name in possible_names:
                                            if name in df_row:
                                                return df_row[name]
                                        return default

                                    # Buscar columnas con diferentes nombres posibles
                                    descripcion_col = None
                                    for col in row.index:
                                        if isinstance(col, str) and "descripci" in col.lower():
                                            descripcion_col = col
                                            break

                                    oficina_col = None
                                    for col in row.index:
                                        if isinstance(col, str) and ("oficina" in col.lower() or "sucursal" in col.lower()):
                                            oficina_col = col
                                            break

                                    debitos_col = None
                                    for col in row.index:
                                        if isinstance(col, str) and ("débit" in col.lower() or "debit" in col.lower() or "cargo" in col.lower()):
                                            debitos_col = col
                                            break

                                    creditos_col = None
                                    for col in row.index:
                                        if isinstance(col, str) and ("crédit" in col.lower() or "credit" in col.lower() or "abono" in col.lower()):
                                            creditos_col = col
                                            break

                                    saldo_col = None
                                    for col in row.index:
                                        if isinstance(col, str) and ("saldo" in col.lower() or "balance" in col.lower()):
                                            saldo_col = col
                                            break

                                    # Luego usa estas variables para acceder a los valores
                                    movement = {
                                        'FECHA': fecha_formateada,
                                        'DESCRIPCION': str(row[descripcion_col]).strip() if descripcion_col and pd.notna(row[descripcion_col]) else '',
                                        'OFICINA': str(row[oficina_col]).strip() if oficina_col and pd.notna(row[oficina_col]) else '',
                                        'DEBITOS': convert_to_float(row[debitos_col] if debitos_col else 0),
                                        'CREDITOS': convert_to_float(row[creditos_col] if creditos_col else 0),
                                        'SALDO': convert_to_float(row[saldo_col] if saldo_col else 0)
                                    }
                                    normalized_data.append(movement)
                                except Exception as e:
                                    print(f"Error procesando fila: {str(e)}")
                                    continue

                        # Crear estructura final del documento
                        document = {
                            "metadata": {
                                "archivo": excel_file.name,
                                "fecha_proceso": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "resumen_encabezado": resumen
                            },
                            "movimientos": normalized_data
                        }
                        
                        # Ordenar los campos del JSON
                        document_ordenado = self.order_json_fields(document)

                        # Guardar archivo JSON individual
                        json_filename = self.output_path / f"bank_{excel_file.stem}.json"
                        with open(json_filename, 'w', encoding='utf-8') as f:
                            json.dump(document_ordenado, f, ensure_ascii=False, indent=2)
                        
                        print(f"Archivo JSON de banco creado: {json_filename}")
                        print(f"Total de movimientos procesados: {len(normalized_data)}")
                        
                        # Agregar a la lista completa
                        bank_data.append(document_ordenado)
                    else:
                        print(f"No se encontró el encabezado 'Día' en {excel_file.name}")
                
                except Exception as e:
                    print(f"Error procesando extracto bancario {excel_file.name}: {str(e)}")
                    traceback.print_exc()
                    continue

            # Guardar archivo JSON combinado de bancos
            combined_json_path = self.output_path / 'all_bank_data.json'
            with open(combined_json_path, 'w', encoding='utf-8') as f:
                json.dump(bank_data, f, ensure_ascii=False, indent=2)
            
            print(f"\nProceso de extractos bancarios completado. Archivos procesados: {len(excel_files)}")
            print(f"Datos combinados guardados en: {combined_json_path}")
            
            return True

        except Exception as e:
            print(f"Error en el proceso de extracción bancaria: {str(e)}")
            traceback.print_exc()
            return False

def main():
    reconciliation = Reconciliation()
    
    print("=== Procesando archivos contables ===")
    reconciliation.extract_excel_to_json()
    
    print("\n=== Procesando extractos bancarios ===")
    reconciliation.extract_bank_excel_to_json()

if __name__ == "__main__":
    main()
