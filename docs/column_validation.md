# Validación de Columnas con Caracteres Especiales

## Descripción

Este documento explica la implementación de la funcionalidad de validación de columnas en archivos Excel de extractos bancarios, permitiendo caracteres especiales como mayúsculas, tildes, espacios, etc.

## Problema

En los archivos Excel de extractos bancarios, las columnas pueden tener diferentes formatos y nombres dependiendo del banco o la versión del extracto:

- Variaciones de mayúsculas/minúsculas: "DESCRIPCION" vs "Descripcion"
- Caracteres con tildes: "DESCRIPCIÓN" vs "DESCRIPCION"
- Espacios y símbolos: "DÉBITOS $" vs "Debitos"
- Diferentes nomenclaturas: "Día" vs "DIA" vs "Fecha día"

Esto causaba errores al procesar los archivos, ya que el sistema no reconocía las columnas correctamente.

## Solución

Se ha implementado una función de normalización de columnas que:

1. Convierte todo a minúsculas
2. Elimina tildes y caracteres diacríticos
3. Reemplaza espacios con guiones bajos
4. Elimina caracteres especiales y símbolos

### Función de normalización

```python
def normalize_column_name(self, column_name):
    """
    Normaliza un nombre de columna para hacerlo insensible a mayúsculas, tildes y espacios.
    
    Args:
        column_name: Nombre de columna a normalizar
        
    Returns:
        Nombre de columna normalizado
    """
    import unicodedata
    
    if not isinstance(column_name, str):
        return str(column_name).lower() if column_name is not None else ""
        
    # Convertir a minúsculas
    normalized = column_name.lower()
    
    # Eliminar tildes y otros caracteres diacríticos
    normalized = ''.join(c for c in unicodedata.normalize('NFD', normalized)
                        if unicodedata.category(c) != 'Mn')
    
    # Reemplazar espacios con guiones bajos
    normalized = normalized.replace(' ', '_')
    
    # Eliminar caracteres especiales y símbolos
    normalized = ''.join(c for c in normalized if c.isalnum() or c == '_')
    
    return normalized
```

### Ejemplos de normalización

| Columna Original | Columna Normalizada |
|------------------|---------------------|
| "DESCRIPCIÓN"    | "descripcion"       |
| "Descripción"    | "descripcion"       |
| "DÉBITOS $"      | "debitos_"          |
| "Créditos"       | "creditos"          |
| "Saldo Final"    | "saldo_final"       |
| "Día"            | "dia"               |

## Implementación

La normalización se aplica en dos momentos clave:

1. Al buscar columnas en los archivos Excel:
   ```python
   column_map = {self.normalize_column_name(col): col for col in df.columns}
   ```

2. Al comparar nombres de columnas:
   ```python
   for norm_name, col in column_map.items():
       if 'descrip' in norm_name:
           descripcion_col = col
           break
   ```

## Pruebas

Se ha creado un script de prueba (`src/test_column_validation.py`) que:

1. Crea un archivo Excel con columnas que tienen caracteres especiales
2. Muestra la normalización de diferentes nombres de columnas
3. Procesa el archivo Excel y verifica que las columnas se identifiquen correctamente

## Conclusión

Con esta implementación, el sistema ahora puede procesar correctamente archivos Excel de extractos bancarios con diferentes formatos de columnas, lo que mejora la robustez y usabilidad del sistema de conciliación bancaria. 