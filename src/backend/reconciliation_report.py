import pandas as pd
import json
import os
from pathlib import Path
from datetime import datetime
import xlsxwriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class ReconciliationReport:
    def __init__(self):
        # Obtener la ruta absoluta del proyecto
        self.project_root = Path(__file__).parent.parent.parent
        self.input_path = self.project_root / 'data' / 'input'
        self.output_path = self.project_root / 'data' / 'output'
        self.report_path = self.project_root / 'data' / 'reports'
        
        # Crear directorios si no existen
        self.report_path.mkdir(parents=True, exist_ok=True)
        
        # Nombres de archivos JSON
        self.accounting_json = self.output_path / 'all_accounting_data.json'
        self.bank_json = self.output_path / 'all_bank_data.json'

    def load_json_data(self):
        """Carga los datos JSON de contabilidad y banco"""
        try:
            # Verificar si existen los archivos
            if not self.accounting_json.exists():
                print(f"Error: No se encontró el archivo {self.accounting_json}")
                return None, None
                
            if not self.bank_json.exists():
                print(f"Error: No se encontró el archivo {self.bank_json}")
                return None, None
            
            # Cargar datos
            with open(self.accounting_json, 'r', encoding='utf-8') as f:
                accounting_data = json.load(f)
                
            with open(self.bank_json, 'r', encoding='utf-8') as f:
                bank_data = json.load(f)
                
            print(f"Datos cargados correctamente: {len(accounting_data)} archivos contables y {len(bank_data)} extractos bancarios")
            return accounting_data, bank_data
                
        except Exception as e:
            print(f"Error cargando datos JSON: {str(e)}")
            return None, None

    def compare_transactions(self):
        """Compara las transacciones entre registros contables y extractos bancarios"""
        print("\n=== CRITERIOS DE CONCILIACIÓN ===")
        print("Las transacciones se marcan como conciliadas si cumplen CUALQUIERA de estos criterios:")
        print("\nCRITERIO 1 (Original):")
        print("- La diferencia de importe es menor a 1.0 unidades")
        print("- La diferencia entre fechas es menor o igual a 3 días")
        print("\nCRITERIO 2 (Por comprobante):")
        print("- El número de comprobante es EXACTAMENTE igual")
        print("- La diferencia de importe es menor a 1.0 unidades")
        print("===========================\n")
        
        accounting_data, bank_data = self.load_json_data()
        if not accounting_data or not bank_data:
            return False
            
        try:
            # Función auxiliar para convertir valores a float de forma segura
            def safe_float(value):
                if value == '' or value is None or pd.isna(value):
                    return 0.0
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return 0.0
            
            # Crear listas para almacenar las transacciones
            accounting_transactions = []
            bank_transactions = []
            
            # Extraer transacciones contables
            for doc in accounting_data:
                for movement in doc.get('movimientos', []):
                    # VALIDACIÓN MEJORADA: Filtrar impuestos específicos
                    description = str(movement.get('DESCRIPCION', '')).lower()
                    if any(tax_term in description for tax_term in [
                        'impuesto trans', 'impuesto al valor agregado', 'iva', 
                        'retencion en la fuente', 'retención en la fuente',
                        'impuesto de renta', 'impuesto', 'pago de intereses capitalizados',
                        'retención en la fuente ahorros', 'nd intereses', 'com. transferencia ach'
                    ]):
                        continue  # Saltar esta transacción
                        
                    # Verificar que tenga los campos requeridos
                    if all(k in movement for k in ['FECHA', 'DESCRIPCION', 'DEBITOS', 'CREDITOS']):
                        accounting_transactions.append({
                            'tipo': 'contabilidad',
                            'archivo': doc.get('metadata', {}).get('archivo', ''),
                            'fecha': movement.get('FECHA', ''),
                            'descripcion': movement.get('DESCRIPCION', ''),
                            'debito': safe_float(movement.get('DEBITOS', 0)),
                            'credito': safe_float(movement.get('CREDITOS', 0)),
                            'valor': safe_float(movement.get('DEBITOS', 0)) if safe_float(movement.get('DEBITOS', 0)) > 0 else safe_float(movement.get('CREDITOS', 0)),
                            'comprobante': movement.get('COMPROBANTE', '')
                        })
            
            # Extraer transacciones bancarias
            for doc in bank_data:
                for movement in doc.get('movimientos', []):
                    # VALIDACIÓN MEJORADA: Filtrar impuestos específicos
                    description = str(movement.get('DESCRIPCION', '')).lower()
                    if any(tax_term in description for tax_term in [
                        'impuesto trans', 'impuesto al valor agregado', 'iva', 
                        'retencion en la fuente', 'retención en la fuente',
                        'impuesto de renta', 'impuesto', 'pago de intereses capitalizados',
                        'retención en la fuente ahorros', 'nd intereses', 'com. transferencia ach'
                    ]):
                        continue  # Saltar esta transacción
                        
                    # Verificar que tenga los campos requeridos
                    if all(k in movement for k in ['FECHA', 'DESCRIPCION', 'DEBITOS', 'CREDITOS']):
                        # Invertir débitos y créditos para mantener consistencia con contabilidad
                        # Débitos del banco corresponden a créditos en contabilidad
                        # Créditos del banco corresponden a débitos en contabilidad
                        debito = safe_float(movement.get('CREDITOS', 0))  # Créditos del banco como débitos
                        credito = safe_float(movement.get('DEBITOS', 0))  # Débitos del banco como créditos
                        
                        # El valor es el monto diferente de cero
                        valor = debito if debito > 0 else credito
                        
                        # FILTRO: Omitir movimientos con valor absoluto 0
                        if abs(valor) == 0:
                            continue
                        bank_transactions.append({
                            'tipo': 'banco',
                            'archivo': doc.get('metadata', {}).get('archivo', ''),
                            'fecha': movement.get('FECHA', ''),
                            'descripcion': movement.get('DESCRIPCION', ''),
                            'debito': debito,
                            'credito': credito,
                            'valor': valor,
                            'oficina': movement.get('OFICINA', ''),
                            'comprobante': movement.get('COMPROBANTE', '')  # Añadir campo comprobante
                        })
            
            print(f"Transacciones extraídas (excluyendo impuestos específicos): {len(accounting_transactions)} contables, {len(bank_transactions)} bancarias")
            
            # Crear DataFrames para facilitar la comparación
            df_accounting = pd.DataFrame(accounting_transactions)
            df_bank = pd.DataFrame(bank_transactions)
            
            # Identificar transacciones conciliadas (coincidentes)
            conciliadas = []
            no_conciliadas_contabilidad = []
            no_conciliadas_banco = []
            
            # Marcar transacciones ya conciliadas
            accounting_matched = [False] * len(df_accounting)
            bank_matched = [False] * len(df_bank)
            
            # Comparar para encontrar coincidencias
            for i, row_acc in df_accounting.iterrows():
                for j, row_bank in df_bank.iterrows():
                    # Si ya está conciliada, continuar con la siguiente
                    if accounting_matched[i] or bank_matched[j]:
                        continue
                        
                    # CRITERIO ORIGINAL: valor casi exacto y fechas cercanas
                    value_match_original = abs(row_acc['valor'] - row_bank['valor']) < 1.0
                    
                    # Extraer el día del mes de las fechas formateadas
                    try:
                        # Extraer los días de las fechas en formato "2025-03-DD 00:00:00"
                        dia_contabilidad = int(row_acc['fecha'].split('-')[2].split(' ')[0])
                        dia_banco = int(row_bank['fecha'].split('-')[2].split(' ')[0])
                        date_diff = abs(dia_contabilidad - dia_banco) <= 3  # Tolerancia de 3 días
                    except (ValueError, IndexError, AttributeError):
                        # Si hay error al extraer fechas, considerar fechas no compatibles
                        date_diff = False
                    
                    # NUEVO CRITERIO: comprobante idéntico y mayor tolerancia en el valor
                    comprobante_acc = str(row_acc['comprobante']).strip()
                    comprobante_bank = str(row_bank.get('comprobante', '')).strip()
                    comprobante_match = comprobante_acc and comprobante_bank and comprobante_acc == comprobante_bank
                    value_match_tolerant = abs(row_acc['valor'] - row_bank['valor']) < 1.0
                    
                    # Calcular la diferencia de valor para mostrarla en el reporte
                    value_diff = abs(row_acc['valor'] - row_bank['valor'])
                    
                    # Conciliar si cumple el criterio original O el nuevo criterio de comprobante
                    if (value_match_original and date_diff) or (comprobante_match and value_match_tolerant):
                        conciliadas.append({
                            'fecha_contabilidad': row_acc['fecha'],
                            'fecha_banco': row_bank['fecha'],
                            'descripcion_contabilidad': row_acc['descripcion'],
                            'descripcion_banco': row_bank['descripcion'],
                            'valor_contabilidad': row_acc['valor'],
                            'valor_banco': row_bank.get('valor', row_acc['valor']),
                            'diferencia': value_diff,
                            'comprobante': row_acc['comprobante'],
                            'estado': 'Conciliado'
                        })
                        accounting_matched[i] = True
                        bank_matched[j] = True
            
            # Identificar transacciones no conciliadas
            for i, row_acc in df_accounting.iterrows():
                if not accounting_matched[i]:
                    no_conciliadas_contabilidad.append({
                        'fecha': row_acc['fecha'],
                        'descripcion': row_acc['descripcion'],
                        'valor': row_acc['valor'],
                        'comprobante': row_acc['comprobante'],
                        'estado': 'No Conciliado - Solo en Contabilidad'
                    })
                    
            for j, row_bank in df_bank.iterrows():
                if not bank_matched[j]:
                    no_conciliadas_banco.append({
                        'fecha': row_bank['fecha'],
                        'descripcion': row_bank['descripcion'],
                        'valor': row_bank['valor'],
                        'debito': row_bank['debito'],
                        'credito': row_bank['credito'],
                        'comprobante': row_bank.get('comprobante', ''),
                        'oficina': row_bank.get('oficina', ''),
                        'estado': 'No Conciliado - Solo en Banco'
                    })
            
            print(f"Análisis completado:")
            print(f"- Transacciones conciliadas: {len(conciliadas)}")
            print(f"- Transacciones solo en contabilidad: {len(no_conciliadas_contabilidad)}")
            print(f"- Transacciones solo en banco: {len(no_conciliadas_banco)}")
            
            return {
                'conciliadas': conciliadas,
                'no_conciliadas_contabilidad': no_conciliadas_contabilidad,
                'no_conciliadas_banco': no_conciliadas_banco
            }
            
        except Exception as e:
            print(f"Error durante la comparación de transacciones: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def ajustar_formato_tabla(self, worksheet, df, start_row, formats, has_date=False, has_number=True):
        """Función auxiliar para aplicar formatos consistentes a todas las tablas"""
        # Ajustar automáticamente el ancho de las columnas basado en el contenido
        for col_num, column in enumerate(df.columns):
            # Calcular el ancho máximo necesario (considerando tanto el encabezado como los datos)
            column_width = max(
                len(str(column)),
                df[column].astype(str).map(len).max()
            )
            # Añadir un margen extra y establecer un mínimo
            adjusted_width = max(column_width + 3, 12)
            # Limitar el ancho máximo para no tener columnas demasiado anchas
            final_width = min(adjusted_width, 40)
            worksheet.set_column(col_num, col_num, final_width)
        
        # Aplicar formatos a las celdas
        header_format, data_format, date_format, number_format = formats
        
        # Lista de columnas numéricas para aplicar formato de número
        numeric_columns = ['valor', 'valor_contabilidad', 'valor_banco', 'diferencia', 'Débito', 'Crédito']
        
        # Aplicar formato a todas las filas de datos
        for row_num in range(start_row, len(df) + start_row):
            worksheet.set_row(row_num, None)
            for col_num in range(len(df.columns)):
                cell_value = df.iloc[row_num-start_row, col_num]
                column_name = df.columns[col_num]
                
                # Aplicar formato según el tipo de datos
                if has_date and (column_name == 'fecha' or column_name == 'fecha_contabilidad' or column_name == 'fecha_banco'):  
                    worksheet.write(row_num, col_num, cell_value, date_format)
                elif has_number and column_name in numeric_columns:  # Columnas de valores numéricos
                    worksheet.write(row_num, col_num, cell_value, number_format)
                else:
                    worksheet.write(row_num, col_num, cell_value, data_format)

    def generate_excel_report(self, comparison_result):
        """Genera un reporte Excel con los resultados de la conciliación con formato profesional"""
        if not comparison_result:
            print("No hay resultados de comparación para generar el reporte")
            return False
            
        try:
            # Crear un archivo Excel con XlsxWriter
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            excel_path = self.report_path / f"conciliacion_{timestamp}.xlsx"
            
            # Crear un escritor de Excel
            writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
            workbook = writer.book
            
            # --- NUEVOS FORMATOS SOLO PARA LA HOJA RESUMEN ---
            # Paleta de colores profesional para hoja de resumen
            COLOR_HEADER = '#3366CC'       # Azul profesional para encabezados
            COLOR_CONCILIADO = '#27AE60'   # Verde para conciliadas
            COLOR_CONTABILIDAD = '#E74C3C' # Rojo para solo contabilidad
            COLOR_BANCO = '#F39C12'        # Naranja para solo banco
            
            # Formatos mejorados
            title_format = workbook.add_format({
                'bold': True,
                'font_size': 16,
                'font_color': '#1F497D',
                'align': 'center',
                'valign': 'vcenter',
                'border': 0
            })
            
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4F81BD',
                'font_color': 'white',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'text_wrap': True,
                'font_size': 11
            })
            
            # Formatos para datos con ajuste de texto
            conciliado_format = workbook.add_format({
                'bg_color': '#C6EFCE',
                'border': 1,
                'border_color': '#969696',
                'align': 'left',
                'valign': 'vcenter',
                'text_wrap': True  # Activar ajuste de texto
            })
            
            no_conciliado_format = workbook.add_format({
                'bg_color': '#FFC7CE',
                'border': 1,
                'border_color': '#969696',
                'align': 'left',
                'valign': 'vcenter',
                'text_wrap': True  # Activar ajuste de texto
            })
            
            # Formato contable para campos numéricos
            number_format = workbook.add_format({
                'num_format': '#,##0.00_);[Red](#,##0.00)',  # Formato contable: negativo en rojo y entre paréntesis
                'align': 'right',
                'border': 1,
                'border_color': '#969696',
                'bg_color': '#FFC7CE'  # Mismo color de fondo que no_conciliado_format
            })
            
            # Formato contable para conciliados
            conciliado_number_format = workbook.add_format({
                'num_format': '#,##0.00_);[Red](#,##0.00)',  # Formato contable: negativo en rojo y entre paréntesis
                'align': 'right',
                'border': 1,
                'border_color': '#969696',
                'bg_color': '#C6EFCE'  # Mismo color de fondo que conciliado_format
            })
            
            date_format = workbook.add_format({
                'num_format': 'yyyy-mm-dd',
                'align': 'center',
                'border': 1,
                'border_color': '#969696',
                'text_wrap': True,
                'bg_color': '#FFC7CE'  # Mismo color de fondo que no_conciliado_format
            })
            
            conciliado_date_format = workbook.add_format({
                'num_format': 'yyyy-mm-dd',
                'align': 'center',
                'border': 1,
                'border_color': '#969696',
                'text_wrap': True,
                'bg_color': '#C6EFCE'  # Mismo color de fondo que conciliado_format
            })
            
            # Formato para tabla de resumen
            resumen_header_format = workbook.add_format({
                'bold': True,
                'bg_color': COLOR_HEADER,
                'font_color': 'white',
                'border': 1,
                'border_color': '#CCCCCC',
                'align': 'center',
                'valign': 'vcenter',
                'text_wrap': True,
                'font_size': 11
            })
            
            # Formatos para celdas de datos del resumen
            resumen_number_format = workbook.add_format({
                'num_format': '#,##0_);[Red](#,##0)',  # Formato contable para cantidades enteras
                'align': 'center',
                'border': 1,
                'border_color': '#CCCCCC'
            })
            
            resumen_percent_format = workbook.add_format({
                'num_format': '0.00%',
                'align': 'center',
                'border': 1,
                'border_color': '#CCCCCC'
            })
            
            # Formatos por categoría
            resumen_conciliado_format = workbook.add_format({
                'bg_color': '#D5F5E3',  # Verde claro
                'border': 1,
                'border_color': '#CCCCCC',
                'align': 'left',
                'valign': 'vcenter'
            })
            
            resumen_contabilidad_format = workbook.add_format({
                'bg_color': '#FADBD8',  # Rojo claro
                'border': 1,
                'border_color': '#CCCCCC',
                'align': 'left',
                'valign': 'vcenter'
            })
            
            resumen_banco_format = workbook.add_format({
                'bg_color': '#FCF3CF',  # Amarillo claro
                'border': 1,
                'border_color': '#CCCCCC',
                'align': 'left',
                'valign': 'vcenter'
            })
            
            resumen_total_format = workbook.add_format({
                'bold': True,
                'bg_color': '#EBF5FB',  # Azul muy claro
                'border': 1,
                'border_color': '#CCCCCC',
                'align': 'left',
                'valign': 'vcenter'
            })
            
            # Hoja 1: Resumen
            df_resumen = pd.DataFrame({
                'Categoría': ['Transacciones Conciliadas', 'Solo en Contabilidad', 'Solo en Banco'],
                'Cantidad': [
                    len(comparison_result['conciliadas']), 
                    len(comparison_result['no_conciliadas_contabilidad']), 
                    len(comparison_result['no_conciliadas_banco'])
                ]
            })

            # Calcular el porcentaje de conciliación
            total_transacciones = sum(df_resumen['Cantidad'])
            df_resumen['Porcentaje'] = (df_resumen['Cantidad'] / total_transacciones)

            # Crear dataframe para Excel
            df_resumen_excel = df_resumen.copy()
            # Formatear los porcentajes como cadenas para evitar problemas
            df_resumen_excel['Porcentaje'] = df_resumen_excel['Porcentaje'].apply(
                lambda x: f"{x:.2%}"
            )
            
            # Crear la hoja de resumen a través de pandas
            df_resumen_excel.to_excel(writer, sheet_name='Resumen', index=False, startrow=2)
            
            # Obtener la hoja creada
            worksheet = writer.sheets['Resumen']
            
            # Configurar columnas
            worksheet.set_column('A:A', 35)  # Columna categoría
            worksheet.set_column('B:B', 15)  # Columna cantidad
            worksheet.set_column('C:C', 15)  # Columna porcentaje
            worksheet.set_column('D:D', 3)   # Espacio
            worksheet.set_column('E:J', 20)  # Espacio para gráfico
            
            # Configurar filas
            worksheet.set_row(0, 30)  # Fila de título
            worksheet.set_row(1, 20)  # Fila de fecha
            
            # Añadir título
            worksheet.merge_range('A1:J1', 'RESUMEN DE CONCILIACIÓN BANCARIA', title_format)
            worksheet.write(1, 0, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Reemplazar encabezados con formato personalizado
            for col_num, value in enumerate(df_resumen.columns.values):
                worksheet.write(2, col_num, value, resumen_header_format)
            
            # Aplicar formatos a las celdas de datos
            # Para evitar errores con porcentajes, aplicamos formatos celda por celda
            for row_idx, (_, row) in enumerate(df_resumen.iterrows(), start=3):
                # Determinamos el formato según la categoría
                if row_idx == 3:  # Transacciones Conciliadas
                    cell_format = resumen_conciliado_format
                elif row_idx == 4:  # Solo en Contabilidad
                    cell_format = resumen_contabilidad_format
                else:  # Solo en Banco
                    cell_format = resumen_banco_format
                
                # Aplicar formatos celda por celda
                worksheet.write(row_idx, 0, row['Categoría'], cell_format)
                worksheet.write(row_idx, 1, row['Cantidad'], resumen_number_format)
                
                # Para porcentajes, escribimos el valor como decimal y aplicamos formato de porcentaje
                value_decimal = row['Porcentaje']  # El valor ya es decimal (ej: 0.85)
                worksheet.write(row_idx, 2, value_decimal, resumen_percent_format)
            
            # Añadir fila de total
            total_row = 6
            worksheet.write(total_row, 0, 'Total', resumen_total_format)
            worksheet.write(total_row, 1, total_transacciones, resumen_number_format)
            worksheet.write(total_row, 2, 1.0, resumen_percent_format)  # 100%
            
            # Crear un gráfico tipo pie (pastel) para porcentajes - más simple y menos problemas
            pie_chart = workbook.add_chart({'type': 'pie'})
            
            # Agregar datos al gráfico, usando referencias de celdas simples
            pie_chart.add_series({
                'name': 'Distribución de Transacciones',
                'categories': ['Resumen', 3, 0, 5, 0],  # Referencia directa a celdas (sin usar strings)
                'values': ['Resumen', 3, 1, 5, 1],  # Referencia directa a celdas (sin usar strings)
                'points': [
                    {'fill': {'color': COLOR_CONCILIADO}},   # Verde para conciliadas
                    {'fill': {'color': COLOR_CONTABILIDAD}}, # Rojo para solo contabilidad
                    {'fill': {'color': COLOR_BANCO}}         # Naranja para solo banco
                ]
            })
            
            # Configurar el gráfico
            pie_chart.set_title({'name': 'Distribución de Transacciones'})
            pie_chart.set_style(10)  # Estilo profesional
            pie_chart.set_size({'width': 440, 'height': 300})
            
            # Posicionar el gráfico a la derecha de la tabla
            worksheet.insert_chart('E3', pie_chart)
            
            # ------------------------------------------------------------------------
            # CREAR UN FORMATO DE TEXTO SIMPLE PARA EL VELOCÍMETRO EN LUGAR DE UN GRÁFICO
            # ------------------------------------------------------------------------
            
            # Obtener el porcentaje de transacciones conciliadas
            porcentaje_conciliadas = df_resumen['Porcentaje'].iloc[0]  # Porcentaje como decimal (0-1)
            
            # Determinar el nivel y color según el porcentaje de conciliación
            if porcentaje_conciliadas >= 0.9:
                nivel_texto = "EXCELENTE"
                nivel_color = "#27AE60"  # Verde
            elif porcentaje_conciliadas >= 0.7:
                nivel_texto = "BUENO"
                nivel_color = "#F39C12"  # Amarillo/Naranja
            else:
                nivel_texto = "BAJO"
                nivel_color = "#E74C3C"  # Rojo
            
            # Formato para el bloque de indicador
            indicador_titulo_format = workbook.add_format({
                'bold': True,
                'font_size': 16,
                'font_color': '#333333',
                'align': 'center',
                'valign': 'vcenter',
                'top': 1,
                'left': 1,
                'right': 1
            })
            
            indicador_valor_format = workbook.add_format({
                'bold': True,
                'font_size': 28,
                'font_color': nivel_color,
                'align': 'center',
                'valign': 'vcenter',
                'num_format': '0.0%',
                'left': 1,
                'right': 1
            })
            
            indicador_nivel_format = workbook.add_format({
                'bold': True,
                'font_size': 18,
                'align': 'center',
                'valign': 'vcenter',
                'bg_color': nivel_color,
                'font_color': 'white',
                'left': 1,
                'right': 1,
                'bottom': 1
            })
            
            # Añadir indicador de nivel de conciliación en forma de bloque de texto
            nivel_row = 18
            worksheet.merge_range(f'E{nivel_row}:J{nivel_row}', 'INDICADOR DE CONCILIACIÓN', indicador_titulo_format)
            worksheet.merge_range(f'E{nivel_row+1}:J{nivel_row+1}', porcentaje_conciliadas, indicador_valor_format)
            worksheet.merge_range(f'E{nivel_row+2}:J{nivel_row+2}', nivel_texto, indicador_nivel_format)
            
            # Aumentar altura de filas para mejor visualización
            worksheet.set_row(nivel_row, 30)    # Título
            worksheet.set_row(nivel_row+1, 45)  # Valor
            worksheet.set_row(nivel_row+2, 35)  # Nivel
            
            # Añadir leyenda de colores
            leyenda_row = nivel_row + 4
            
            # Formato para título de la leyenda
            leyenda_titulo_format = workbook.add_format({
                'bold': True,
                'font_size': 14,
                'font_color': '#333333',
                'align': 'center',
                'valign': 'vcenter',
                'top': 1,
                'left': 1,
                'right': 1
            })
            
            # Formatos para los niveles
            verde_format = workbook.add_format({
                'bg_color': '#27AE60',
                'border': 1,
                'pattern': 1
            })
            
            amarillo_format = workbook.add_format({
                'bg_color': '#F39C12',
                'border': 1,
                'pattern': 1
            })
            
            rojo_format = workbook.add_format({
                'bg_color': '#E74C3C',
                'border': 1,
                'pattern': 1
            })
            
            leyenda_texto_format = workbook.add_format({
                'font_size': 12,
                'align': 'left',
                'valign': 'vcenter'
            })
            
            # Título de la leyenda
            worksheet.merge_range(f'E{leyenda_row}:J{leyenda_row}', 'NIVELES DE CONCILIACIÓN', leyenda_titulo_format)
            
            # Color verde - Excelente
            worksheet.write(f'E{leyenda_row+1}', '', verde_format)
            worksheet.merge_range(f'F{leyenda_row+1}:J{leyenda_row+1}', 'EXCELENTE: ≥ 90% conciliado', leyenda_texto_format)
            
            # Color amarillo - Bueno
            worksheet.write(f'E{leyenda_row+2}', '', amarillo_format)
            worksheet.merge_range(f'F{leyenda_row+2}:J{leyenda_row+2}', 'BUENO: 70% - 89% conciliado', leyenda_texto_format)
            
            # Color rojo - Bajo
            worksheet.write(f'E{leyenda_row+3}', '', rojo_format)
            worksheet.merge_range(f'F{leyenda_row+3}:J{leyenda_row+3}', 'BAJO: < 70% conciliado', leyenda_texto_format)
            
            # Ajustar tamaño para la columna de muestra de color
            worksheet.set_column('E:E', 8)
            
            # Hoja 2: Transacciones Conciliadas
            if comparison_result['conciliadas']:
                df_conciliadas = pd.DataFrame(comparison_result['conciliadas'])
                df_conciliadas.to_excel(writer, sheet_name='Conciliadas', index=False, startrow=2)
                
                # Configurar hoja
                worksheet = writer.sheets['Conciliadas']
                worksheet.set_row(0, 30)
                
                # Ajustar título para incluir todas las columnas
                worksheet.merge_range('A1:H1', 'TRANSACCIONES CONCILIADAS', title_format)
                worksheet.write(1, 0, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Aplicar formatos de encabezado
                for col_num, value in enumerate(df_conciliadas.columns.values):
                    worksheet.write(2, col_num, value, header_format)
                
                # Aplicar formatos usando la función auxiliar
                formats = (header_format, conciliado_format, conciliado_date_format, conciliado_number_format)
                self.ajustar_formato_tabla(worksheet, df_conciliadas, 3, formats, has_date=True)
                
                # Añadir filtros
                worksheet.autofilter(2, 0, 2 + len(df_conciliadas), len(df_conciliadas.columns) - 1)
                
                # Congelar paneles para facilitar navegación
                worksheet.freeze_panes(3, 0)
            
            # Hoja 3: Solo en Contabilidad
            if comparison_result['no_conciliadas_contabilidad']:
                # Ordenar los datos por valor antes de crear el DataFrame
                sorted_contabilidad = sorted(comparison_result['no_conciliadas_contabilidad'], key=lambda x: x.get('valor', 0))
                # Crear DataFrame con columnas explícitas
                df_conta = pd.DataFrame(sorted_contabilidad)
                # Agregar columnas Débito y Crédito
                df_conta['Débito'] = df_conta['valor'].where(df_conta['valor'] < 0, 0).abs()
                df_conta['Crédito'] = df_conta['valor'].where(df_conta['valor'] > 0, 0)
                # Reordenar columnas - Mantener la columna de descripción como solicitado
                cols_conta = ['fecha', 'descripcion', 'Débito', 'Crédito', 'comprobante', 'estado']
                df_conta = df_conta.reindex(columns=cols_conta)
                df_conta.to_excel(writer, sheet_name='Solo Contabilidad', index=False, startrow=2)
                
                # Configurar hoja
                worksheet = writer.sheets['Solo Contabilidad']
                worksheet.set_row(0, 30)
                
                # Añadir título
                worksheet.merge_range('A1:F1', 'TRANSACCIONES SOLO EN CONTABILIDAD', title_format)
                worksheet.write(1, 0, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Aplicar formatos de encabezado
                for col_num, value in enumerate(df_conta.columns.values):
                    worksheet.write(2, col_num, value, header_format)
                
                # Aplicar formatos usando la función auxiliar
                formats = (header_format, no_conciliado_format, date_format, number_format)
                self.ajustar_formato_tabla(worksheet, df_conta, 3, formats, has_date=True)
                
                # Añadir filtros
                worksheet.autofilter(2, 0, 2 + len(df_conta), len(df_conta.columns) - 1)
                
                # Congelar paneles
                worksheet.freeze_panes(3, 0)
            
            # Hoja 4: Solo en Banco
            if comparison_result['no_conciliadas_banco']:
                # Ordenar los datos por valor antes de crear el DataFrame
                sorted_banco = sorted(comparison_result['no_conciliadas_banco'], key=lambda x: x.get('valor', 0))
                # Crear DataFrame con columnas explícitas
                df_banco = pd.DataFrame(sorted_banco)
                
                # Invertir Débitos y Créditos para mantener consistencia con contabilidad
                # Nota: Ya están invertidos en los datos originales (debito = CREDITOS del banco, credito = DEBITOS del banco)
                # Usar los campos debito y credito ya invertidos
                df_banco['Débito'] = df_banco['debito']
                df_banco['Crédito'] = df_banco['credito']
                
                # Reordenar columnas - quitar comprobante y oficina como solicitado
                cols_banco = ['fecha', 'descripcion', 'Débito', 'Crédito', 'estado']
                df_banco = df_banco.reindex(columns=cols_banco)
                df_banco.to_excel(writer, sheet_name='Solo Banco', index=False, startrow=2)
                
                # Configurar hoja
                worksheet = writer.sheets['Solo Banco']
                worksheet.set_row(0, 30)
                
                # Añadir título (actualizado para incluir todas las columnas)
                worksheet.merge_range('A1:E1', 'TRANSACCIONES SOLO EN BANCO', title_format)
                worksheet.write(1, 0, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Aplicar formatos de encabezado
                for col_num, value in enumerate(df_banco.columns.values):
                    worksheet.write(2, col_num, value, header_format)
                
                # Aplicar formatos usando la función auxiliar
                formats = (header_format, no_conciliado_format, date_format, number_format)
                self.ajustar_formato_tabla(worksheet, df_banco, 3, formats, has_date=True)
                
                # Añadir filtros
                worksheet.autofilter(2, 0, 2 + len(df_banco), len(df_banco.columns) - 1)
                
                # Congelar paneles
                worksheet.freeze_panes(3, 0)
            
            # Guardar el archivo Excel
            writer.close()
            
            print(f"Reporte Excel generado con éxito: {excel_path}")
            return excel_path
            
        except Exception as e:
            print(f"Error generando reporte Excel: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def generate_pdf_report(self, comparison_result):
        """Genera un reporte PDF con los resultados de la conciliación"""
        if not comparison_result:
            print("No hay resultados de comparación para generar el reporte PDF")
            return False
            
        try:
            # Crear un archivo PDF con ReportLab
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_path = self.report_path / f"conciliacion_{timestamp}.pdf"
            
            # Usar orientación horizontal (landscape) para más espacio
            from reportlab.lib.pagesizes import landscape
            from reportlab.platypus import LongTable
            doc = SimpleDocTemplate(
                str(pdf_path), 
                pagesize=landscape(letter),
                rightMargin=36, 
                leftMargin=36,
                topMargin=36, 
                bottomMargin=36
            )
            
            # Contenido del PDF
            elements = []
            styles = getSampleStyleSheet()
            
            # Título
            elements.append(Paragraph("Reporte de Conciliación Bancaria", styles["Title"]))
            elements.append(Paragraph(f"Generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
            elements.append(Spacer(1, 12))
            
            # Resumen
            elements.append(Paragraph("Resumen de Conciliación", styles["Heading2"]))
            elements.append(Spacer(1, 6))
            
            data = [
                ["Categoría", "Cantidad"],
                ["Transacciones Conciliadas", str(len(comparison_result['conciliadas']))],
                ["Solo en Contabilidad", str(len(comparison_result['no_conciliadas_contabilidad']))],
                ["Solo en Banco", str(len(comparison_result['no_conciliadas_banco']))]
            ]
            
            # Crear tabla de resumen
            table = Table(data, colWidths=[300, 100])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, 3), colors.lightgreen),
                ('BACKGROUND', (0, 2), (-1, 3), colors.lightcoral),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            elements.append(Spacer(1, 12))
            
            # Mostrar transacciones conciliadas
            if comparison_result['conciliadas']:
                elements.append(Paragraph("Transacciones Conciliadas", styles["Heading2"]))
                elements.append(Spacer(1, 6))
                
                # Encabezados actualizados para mostrar ambos valores y la diferencia
                data = [["Fecha Cont.", "Fecha Banco", "Descripción Contabilidad", "Descripción Banco", "Valor Contabilidad", "Valor Banco", "Diferencia", "Comprobante"]]
                
                # Datos
                for trans in comparison_result['conciliadas']:
                    data.append([
                        str(trans['fecha_contabilidad']),
                        str(trans['fecha_banco']),
                        str(trans['descripcion_contabilidad']),
                        str(trans['descripcion_banco']),
                        f"{trans['valor_contabilidad']:,.2f}",
                        f"{trans['valor_banco']:,.2f}",
                        f"{trans['diferencia']:,.2f}",
                        str(trans['comprobante'])
                    ])
                
                # Crear tabla con ajuste automático
                table = LongTable(data, repeatRows=1)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('WORDWRAP', (0, 0), (-1, -1), True)
                ]))
                elements.append(table)
                elements.append(Spacer(1, 12))
            
            # Mostrar transacciones solo en contabilidad
            if comparison_result['no_conciliadas_contabilidad']:
                elements.append(Paragraph("Transacciones Solo en Contabilidad", styles["Heading2"]))
                elements.append(Spacer(1, 6))
                
                # Encabezados
                data = [["Fecha", "Descripción", "Valor", "Comprobante"]]
                
                # Datos
                for trans in comparison_result['no_conciliadas_contabilidad']:
                    data.append([
                        str(trans['fecha']),
                        str(trans['descripcion']),
                        f"{trans['valor']:,.2f}",
                        str(trans['comprobante'])
                    ])
                
                # Crear tabla con ajuste automático
                table = LongTable(data, repeatRows=1)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightcoral),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('WORDWRAP', (0, 0), (-1, -1), True)
                ]))
                elements.append(table)
                elements.append(Spacer(1, 12))
            
            # Mostrar transacciones solo en banco
            if comparison_result['no_conciliadas_banco']:
                elements.append(Paragraph("Transacciones Solo en Banco", styles["Heading2"]))
                elements.append(Spacer(1, 6))
                
                # Encabezados actualizados - quitar comprobante y oficina
                data = [["Fecha", "Descripción", "Valor"]]
                
                # Datos
                for trans in comparison_result['no_conciliadas_banco']:
                    data.append([
                        str(trans['fecha']),
                        str(trans['descripcion']),
                        f"{trans['valor']:,.2f}"
                    ])
                
                # Crear tabla con ajuste automático
                table = LongTable(data, repeatRows=1)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightcoral),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('WORDWRAP', (0, 0), (-1, -1), True)
                ]))
                elements.append(table)
            
            # Construir el PDF
            doc.build(elements)
            
            print(f"Reporte PDF generado con éxito: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            print(f"Error generando reporte PDF: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def process(self):
        """Proceso completo de comparación y generación de reportes"""
        print("=== Iniciando análisis de conciliación bancaria ===")
        comparison_result = self.compare_transactions()
        
        if comparison_result:
            print("\n=== Generando reportes ===")
            excel_path = self.generate_excel_report(comparison_result)
            pdf_path = self.generate_pdf_report(comparison_result)
            
            return {
                'comparison_result': comparison_result,
                'excel_report': excel_path,
                'pdf_report': pdf_path
            }
        else:
            print("No se pudo realizar la comparación. Verifique los datos.")
            return None

def main():
    report = ReconciliationReport()
    result = report.process()
    
    if result:
        print("\n=== Proceso completado con éxito ===")
        print(f"Excel generado: {result['excel_report']}")
        print(f"PDF generado: {result['pdf_report']}")
        print("\nResumen de resultados:")
        print(f"- Transacciones conciliadas: {len(result['comparison_result']['conciliadas'])}")
        print(f"- Solo en contabilidad: {len(result['comparison_result']['no_conciliadas_contabilidad'])}")
        print(f"- Solo en banco: {len(result['comparison_result']['no_conciliadas_banco'])}")
    else:
        print("\n=== El proceso no pudo completarse ===")

if __name__ == "__main__":
    main()
