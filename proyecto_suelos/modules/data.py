#!/usr/bin/env python
# modules/data.py

import pandas as pd
import os

def load_data(filepath):
    """
    Carga los datos desde un archivo Excel.
    
    Args:
        filepath (str): Ruta al archivo Excel con los datos de suelos
        
    Returns:
        pandas.DataFrame: DataFrame con los datos cargados
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El archivo {filepath} no existe")
    
    try:
        # Cargar datos desde Excel
        data_df = pd.read_excel(filepath)
        return data_df
    except Exception as e:
        raise Exception(f"Error al cargar los datos: {str(e)}")

def filter_data(data_df, departamento=None, municipio=None, cultivo=None, limit=None):
    """
    Filtra los datos según los criterios especificados.
    
    Args:
        data_df (pandas.DataFrame): DataFrame con los datos
        departamento (str, optional): Nombre del departamento para filtrar
        municipio (str, optional): Nombre del municipio para filtrar
        cultivo (str, optional): Nombre del cultivo para filtrar
        limit (int, optional): Número máximo de registros a devolver
        
    Returns:
        pandas.DataFrame: DataFrame filtrado según los criterios
    """
    filtered_df = data_df.copy()
    
    # Aplicar filtros si se proporcionan
    if departamento:
        filtered_df = filtered_df[filtered_df['departamento'].str.lower() == departamento.lower()]
    
    if municipio:
        filtered_df = filtered_df[filtered_df['municipio'].str.lower() == municipio.lower()]
    
    if cultivo:
        filtered_df = filtered_df[filtered_df['cultivo'].str.lower() == cultivo.lower()]
    
    # Limitar el número de registros
    if limit and isinstance(limit, int):
        filtered_df = filtered_df.head(limit)
    
    return filtered_df

def calculate_edaphic_stats(filtered_df):
    """
    Calcula estadísticas (mediana) de las variables edáficas.
    
    Args:
        filtered_df (pandas.DataFrame): DataFrame filtrado
        
    Returns:
        dict: Diccionario con las medianas de pH, Fósforo, Potasio
    """
    stats = {}
    
    # Calcular medianas para las variables edáficas
    if not filtered_df.empty:
        # Verificar qué columnas están presentes en el DataFrame
        edaphic_vars = {
            'pH': 'ph',
            'Fósforo (P)': 'fosforo_p',
            'Potasio (K)': 'potasio_k'
        }
        
        for label, column in edaphic_vars.items():
            # Verificar si la columna existe en el DataFrame
            if column in filtered_df.columns:
                # Convertir a numérico y calcular la mediana
                stats[label] = filtered_df[column].astype(float).median()
            else:
                stats[label] = None
    else:
        # Si no hay datos, establecer todos los valores a None
        stats = {
            'pH': None,
            'Fósforo (P)': None,
            'Potasio (K)': None
        }
    
    return stats

def get_unique_values(data_df, column):
    """
    Obtiene los valores únicos de una columna específica.
    
    Args:
        data_df (pandas.DataFrame): DataFrame con los datos
        column (str): Nombre de la columna
        
    Returns:
        list: Lista con los valores únicos ordenados
    """
    if column in data_df.columns:
        return sorted(data_df[column].dropna().unique().tolist())
    return []