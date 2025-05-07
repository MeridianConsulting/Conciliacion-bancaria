#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de prueba para validar la normalización de columnas en archivos Excel.
Este script crea un archivo Excel de prueba con columnas que tienen caracteres especiales,
mayúsculas, tildes y espacios, y luego lo procesa para verificar que la normalización
funciona correctamente.
"""

import os
import sys
import pandas as pd
from pathlib import Path
import unicodedata

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.reconciliation import Reconciliation

def create_test_excel():
    """Crea un archivo Excel de prueba con columnas que tienen caracteres especiales"""
    print("Creando archivo Excel de prueba...")
    
    # Crear directorio de prueba si no existe
    test_dir = Path("data/test")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Definir columnas con caracteres especiales
    columns = [
        "Día",
        "DESCRIPCIÓN del movimiento",
        "Oficina/Sucursal",
        "DÉBITOS $",
        "CRÉDITOS $",
        "Saldo Final"
    ]
    
    # Crear datos de ejemplo
    data = [
        [1, "Transferencia recibida", "Central", 0, 1500000, 1500000],
        [2, "Pago de servicios", "Norte", 350000, 0, 1150000],
        [3, "Depósito en efectivo", "Sur", 0, 500000, 1650000],
        [5, "Retiro cajero automático", "Este", 200000, 0, 1450000],
        [8, "Pago de nómina", "Oeste", 0, 2500000, 3950000],
        [10, "Transferencia enviada", "Central", 1200000, 0, 2750000],
    ]
    
    # Crear DataFrame
    df = pd.DataFrame(data, columns=columns)
    
    # Guardar como Excel
    excel_path = test_dir / "extracto_bancario_test.xlsx"
    df.to_excel(excel_path, index=False)
    
    print(f"Archivo Excel creado: {excel_path}")
    return excel_path

def test_column_normalization(excel_path):
    """Prueba la normalización de columnas con un archivo Excel"""
    print("\n=== Prueba de normalización de columnas ===")
    
    # Crear instancia de Reconciliation
    reconciliation = Reconciliation()
    
    # Mostrar ejemplos de normalización
    test_columns = [
        "DESCRIPCIÓN", 
        "Descripcion",
        "descripción",
        "DÉBITOS $",
        "Débitos",
        "CRÉDITOS $",
        "Créditos",
        "SALDO FINAL",
        "Saldo Final",
        "Día",
        "DIA",
        "Día del mes"
    ]
    
    print("Columnas originales vs normalizadas:")
    for col in test_columns:
        normalized = reconciliation.normalize_column_name(col)
        print(f"  {col:20} -> {normalized}")
    
    # Leer el archivo Excel creado
    print("\n=== Leyendo archivo Excel de prueba ===")
    df = pd.read_excel(excel_path)
    
    print("Columnas en el archivo Excel:")
    for col in df.columns:
        normalized = reconciliation.normalize_column_name(col)
        print(f"  {col:20} -> {normalized}")
    
    # Probar la búsqueda de columnas normalizadas
    print("\n=== Probando búsqueda de columnas normalizadas ===")
    column_map = {reconciliation.normalize_column_name(col): col for col in df.columns}
    
    search_terms = [
        "dia", 
        "descripcion", 
        "oficina", 
        "debitos", 
        "creditos", 
        "saldo"
    ]
    
    print("Búsqueda de columnas:")
    for term in search_terms:
        found = False
        for norm_name, orig_name in column_map.items():
            if term in norm_name:
                found = True
                print(f"  Buscando '{term}' -> Encontrado: '{orig_name}' (normalizado: '{norm_name}')")
                break
        
        if not found:
            print(f"  Buscando '{term}' -> No encontrado")
    
    # Procesar el archivo con la función de extracción
    print("\n=== Procesando archivo Excel con la función de extracción ===")
    result = reconciliation.extract_bank_excel_to_json([str(excel_path)])
    
    if result:
        print("Procesamiento exitoso!")
    else:
        print("Error en el procesamiento")

if __name__ == "__main__":
    excel_path = create_test_excel()
    test_column_normalization(excel_path) 