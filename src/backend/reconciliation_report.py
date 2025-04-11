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
                    # Verificar que tenga los campos requeridos
                    if all(k in movement for k in ['FECHA', 'DESCRIPCION', 'DEBITOS', 'CREDITOS']):
                        # Invertir débitos y créditos para comparación correcta
                        # Lo que es débito en banco se considera crédito en contabilidad y viceversa
                        bank_transactions.append({
                            'tipo': 'banco',
                            'archivo': doc.get('metadata', {}).get('archivo', ''),
                            'fecha': movement.get('FECHA', ''),
                            'descripcion': movement.get('DESCRIPCION', ''),
                            'debito': safe_float(movement.get('CREDITOS', 0)),  # Invertido: CREDITOS del banco como DEBITOS
                            'credito': safe_float(movement.get('DEBITOS', 0)),  # Invertido: DEBITOS del banco como CREDITOS
                            'valor': safe_float(movement.get('CREDITOS', 0)) if safe_float(movement.get('CREDITOS', 0)) > 0 else safe_float(movement.get('DEBITOS', 0)),
                            'oficina': movement.get('OFICINA', '')
                        })
            
            print(f"Transacciones extraídas: {len(accounting_transactions)} contables, {len(bank_transactions)} bancarias")
            
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
                        
                    # Criterios de coincidencia (valor exacto y fechas similares)
                    value_match = abs(row_acc['valor'] - row_bank['valor']) < 0.01
                    
                    # Extraer el día del mes de las fechas formateadas
                    try:
                        # Extraer los días de las fechas en formato "2025-03-DD 00:00:00"
                        dia_contabilidad = int(row_acc['fecha'].split('-')[2].split(' ')[0])
                        dia_banco = int(row_bank['fecha'].split('-')[2].split(' ')[0])
                        date_diff = abs(dia_contabilidad - dia_banco) <= 3  # Tolerancia de 3 días
                    except (ValueError, IndexError, AttributeError):
                        # Si hay error al extraer fechas, considerar fechas no compatibles
                        date_diff = False
                    
                    if value_match and date_diff:
                        conciliadas.append({
                            'fecha_contabilidad': row_acc['fecha'],
                            'fecha_banco': row_bank['fecha'],
                            'descripcion_contabilidad': row_acc['descripcion'],
                            'descripcion_banco': row_bank['descripcion'],
                            'valor': row_acc['valor'],
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
                        'oficina': row_bank['oficina'],
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
            
            # Formatos para datos
            conciliado_format = workbook.add_format({
                'bg_color': '#C6EFCE',
                'border': 1,
                'border_color': '#969696',
                'align': 'left',
                'valign': 'vcenter'
            })
            
            no_conciliado_format = workbook.add_format({
                'bg_color': '#FFC7CE',
                'border': 1,
                'border_color': '#969696',
                'align': 'left',
                'valign': 'vcenter'
            })
            
            number_format = workbook.add_format({
                'num_format': '#,##0.00',
                'align': 'right',
                'border': 1,
                'border_color': '#969696'
            })
            
            date_format = workbook.add_format({
                'num_format': 'yyyy-mm-dd',
                'align': 'center',
                'border': 1,
                'border_color': '#969696'
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
            df_resumen.to_excel(writer, sheet_name='Resumen', index=False, startrow=2)
            
            # Configurar hoja de resumen
            worksheet = writer.sheets['Resumen']
            worksheet.set_column('A:A', 25)
            worksheet.set_column('B:B', 15)
            worksheet.set_row(0, 30)
            
            # Añadir título
            worksheet.merge_range('A1:B1', 'RESUMEN DE CONCILIACIÓN BANCARIA', title_format)
            worksheet.write(1, 0, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Aplicar formatos
            for col_num, value in enumerate(df_resumen.columns.values):
                worksheet.write(2, col_num, value, header_format)
            
            # Agregar formato condicional para el resumen
            worksheet.conditional_format('A4:B4', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': conciliado_format})
            worksheet.conditional_format('A5:B6', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': no_conciliado_format})
            
            # Agregar gráfico de pastel
            chart = workbook.add_chart({'type': 'pie'})
            chart.add_series({
                'name': 'Resumen de Conciliación',
                'categories': ['Resumen', 3, 0, 5, 0],
                'values': ['Resumen', 3, 1, 5, 1],
                'data_labels': {'percentage': True, 'category': True},
            })
            chart.set_title({'name': 'Distribución de Transacciones'})
            chart.set_style(10)
            worksheet.insert_chart('D3', chart, {'x_scale': 1.2, 'y_scale': 1.2})
            
            # Hoja 2: Transacciones Conciliadas
            if comparison_result['conciliadas']:
                df_conciliadas = pd.DataFrame(comparison_result['conciliadas'])
                df_conciliadas.to_excel(writer, sheet_name='Conciliadas', index=False, startrow=2)
                
                # Configurar hoja
                worksheet = writer.sheets['Conciliadas']
                worksheet.set_column('A:B', 18)  # Fechas
                worksheet.set_column('C:D', 40)  # Descripciones
                worksheet.set_column('E:E', 15)  # Valor
                worksheet.set_column('F:F', 20)  # Comprobante
                worksheet.set_row(0, 30)
                
                # Añadir título
                worksheet.merge_range('A1:F1', 'TRANSACCIONES CONCILIADAS', title_format)
                worksheet.write(1, 0, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Aplicar formatos de encabezado
                for col_num, value in enumerate(df_conciliadas.columns.values):
                    worksheet.write(2, col_num, value, header_format)
                
                # Aplicar formato a las filas y columnas específicas
                for row_num in range(3, len(df_conciliadas) + 3):
                    worksheet.set_row(row_num, None)
                    for col_num in range(len(df_conciliadas.columns)):
                        if col_num in [0, 1]:  # Columnas de fecha
                            worksheet.write(row_num, col_num, df_conciliadas.iloc[row_num-3, col_num], date_format)
                        elif col_num == 4:  # Columna de valor
                            worksheet.write(row_num, col_num, df_conciliadas.iloc[row_num-3, col_num], number_format)
                        else:
                            worksheet.write(row_num, col_num, df_conciliadas.iloc[row_num-3, col_num], conciliado_format)
                
                # Añadir filtros
                worksheet.autofilter(2, 0, 2 + len(df_conciliadas), len(df_conciliadas.columns) - 1)
                
                # Congelar paneles para facilitar la navegación
                worksheet.freeze_panes(3, 0)
            
            # Hoja 3: Solo en Contabilidad (similar formato)
            if comparison_result['no_conciliadas_contabilidad']:
                df_conta = pd.DataFrame(comparison_result['no_conciliadas_contabilidad'])
                df_conta.to_excel(writer, sheet_name='Solo Contabilidad', index=False, startrow=2)
                
                # Configurar hoja
                worksheet = writer.sheets['Solo Contabilidad']
                worksheet.set_column('A:A', 18)  # Fecha
                worksheet.set_column('B:B', 40)  # Descripción
                worksheet.set_column('C:C', 15)  # Valor
                worksheet.set_column('D:E', 20)  # Comprobante y Estado
                worksheet.set_row(0, 30)
                
                # Añadir título
                worksheet.merge_range('A1:E1', 'TRANSACCIONES SOLO EN CONTABILIDAD', title_format)
                worksheet.write(1, 0, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Aplicar formatos de encabezado
                for col_num, value in enumerate(df_conta.columns.values):
                    worksheet.write(2, col_num, value, header_format)
                
                # Aplicar formato a las filas y columnas específicas
                for row_num in range(3, len(df_conta) + 3):
                    worksheet.set_row(row_num, None)
                    for col_num in range(len(df_conta.columns)):
                        if col_num == 0:  # Columna de fecha
                            worksheet.write(row_num, col_num, df_conta.iloc[row_num-3, col_num], date_format)
                        elif col_num == 2:  # Columna de valor
                            worksheet.write(row_num, col_num, df_conta.iloc[row_num-3, col_num], number_format)
                        else:
                            worksheet.write(row_num, col_num, df_conta.iloc[row_num-3, col_num], no_conciliado_format)
                
                # Añadir filtros
                worksheet.autofilter(2, 0, 2 + len(df_conta), len(df_conta.columns) - 1)
                
                # Congelar paneles para facilitar la navegación
                worksheet.freeze_panes(3, 0)
                
            # Hoja 4: Solo en Banco (similar formato)
            if comparison_result['no_conciliadas_banco']:
                df_banco = pd.DataFrame(comparison_result['no_conciliadas_banco'])
                df_banco.to_excel(writer, sheet_name='Solo Banco', index=False, startrow=2)
                
                # Configurar hoja
                worksheet = writer.sheets['Solo Banco']
                worksheet.set_column('A:A', 18)  # Fecha
                worksheet.set_column('B:B', 40)  # Descripción
                worksheet.set_column('C:C', 15)  # Valor
                worksheet.set_column('D:E', 20)  # Oficina y Estado
                worksheet.set_row(0, 30)
                
                # Añadir título
                worksheet.merge_range('A1:E1', 'TRANSACCIONES SOLO EN BANCO', title_format)
                worksheet.write(1, 0, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Aplicar formatos de encabezado
                for col_num, value in enumerate(df_banco.columns.values):
                    worksheet.write(2, col_num, value, header_format)
                
                # Aplicar formato a las filas y columnas específicas
                for row_num in range(3, len(df_banco) + 3):
                    worksheet.set_row(row_num, None)
                    for col_num in range(len(df_banco.columns)):
                        if col_num == 0:  # Columna de fecha
                            worksheet.write(row_num, col_num, df_banco.iloc[row_num-3, col_num], date_format)
                        elif col_num == 2:  # Columna de valor
                            worksheet.write(row_num, col_num, df_banco.iloc[row_num-3, col_num], number_format)
                        else:
                            worksheet.write(row_num, col_num, df_banco.iloc[row_num-3, col_num], no_conciliado_format)
                
                # Añadir filtros
                worksheet.autofilter(2, 0, 2 + len(df_banco), len(df_banco.columns) - 1)
                
                # Congelar paneles para facilitar la navegación
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
                
                # Encabezados
                data = [["Fecha Cont.", "Fecha Banco", "Descripción Contabilidad", "Descripción Banco", "Valor", "Comprobante"]]
                
                # Datos
                for trans in comparison_result['conciliadas']:
                    data.append([
                        str(trans['fecha_contabilidad']),
                        str(trans['fecha_banco']),
                        str(trans['descripcion_contabilidad']),
                        str(trans['descripcion_banco']),
                        f"{trans['valor']:,.2f}",
                        str(trans['comprobante'])
                    ])
                
                # Crear tabla con ajuste automático
                from reportlab.platypus import LongTable
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
                
                # Encabezados
                data = [["Fecha", "Descripción", "Valor", "Oficina"]]
                
                # Datos
                for trans in comparison_result['no_conciliadas_banco']:
                    data.append([
                        str(trans['fecha']),
                        str(trans['descripcion']),
                        f"{trans['valor']:,.2f}",
                        str(trans['oficina'])
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
