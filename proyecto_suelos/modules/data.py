# modules/data.py

import pandas as pd
import os

def load_data(filepath):
    """Carga los datos desde un archivo Excel."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El archivo {filepath} no existe")
    
    try:
        data_df = pd.read_excel(filepath)
        return data_df
    except Exception as e:
        raise Exception(f"Error al cargar los datos: {str(e)}")

def filter_data(data_df, departamento=None, municipio=None, cultivo=None, limit=None):
    """Filtra los datos según los criterios especificados."""
    filtered_df = data_df.copy()

    # Aplicar filtros si se proporcionan
    if departamento:
        filtered_df = filtered_df[filtered_df['Departamento'].str.lower() == departamento.lower()]
    
    if municipio:
        filtered_df = filtered_df[filtered_df['Municipio'].str.lower() == municipio.lower()]
    
    if cultivo:
        filtered_df = filtered_df[filtered_df['Cultivo'].str.lower() == cultivo.lower()]
    
    # Limitar registros
    if limit and isinstance(limit, int):
        filtered_df = filtered_df.head(limit)
    
    return filtered_df

def calculate_edaphic_stats(filtered_df):
    """Calcula estadísticas (mediana) de las variables edáficas."""
    stats = {}

    # Mapeo de nombres de columnas en el archivo Excel
    edaphic_vars = {
        'pH': 'pH agua:suelo 2,5:1,0',
        'Fósforo (P)': 'Fósforo (P) Bray II mg/kg',
        'Potasio (K)': 'Potasio (K) intercambiable cmol(+)/kg'
    }

    if not filtered_df.empty:
        for label, column in edaphic_vars.items():
            if column in filtered_df.columns:
                # Convertir a numérico, manejando valores erróneos
                filtered_df[column] = pd.to_numeric(filtered_df[column], errors='coerce')
                stats[label] = filtered_df[column].median()
            else:
                stats[label] = None
    else:
        stats = {label: None for label in edaphic_vars.keys()}

    return stats

def get_unique_values(data_df, column):
    """Obtiene valores únicos de una columna."""
    if column in data_df.columns:
        return sorted(data_df[column].dropna().unique().tolist())
    return []
