#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para visualizar el contenido de un archivo JSON generado.
"""

import json
import sys
from pathlib import Path
import pprint

def view_json(json_path):
    """Visualiza el contenido de un archivo JSON"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"=== Contenido del archivo JSON: {json_path} ===\n")
        
        # Usar pretty print para mostrar el contenido de manera más legible
        pp = pprint.PrettyPrinter(indent=2, width=100)
        pp.pprint(data)
            
    except Exception as e:
        print(f"Error al leer el archivo JSON: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    else:
        json_path = "data/output/bank_extracto_bancario_test.json"
    
    view_json(json_path) 