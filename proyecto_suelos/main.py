#!/usr/bin/env python
# main.py

import os
import sys
from modules.ui import clear_screen, show_header, show_options_menu, get_limit, display_results, confirm_action
from modules.data import load_data, filter_data, calculate_edaphic_stats, get_unique_values

def main():
    """Función principal del programa."""
    # Solicitar la ruta del archivo Excel
    clear_screen()
    show_header()
    
    # Solicitar la ruta del archivo Excel
    while True:
        excel_path = input("Ingrese la ruta al archivo Excel con los datos de suelos: ")
        try:
            # Intentar cargar los datos
            data_df = load_data(excel_path)
            print(f"Datos cargados correctamente. Total de registros: {len(data_df)}")
            break
        except FileNotFoundError:
            print(f"El archivo {excel_path} no existe. Por favor, verifique la ruta.")
        except Exception as e:
            print(f"Error al cargar los datos: {str(e)}")
            sys.exit(1)
    
    # Bucle principal del programa
    while True:
        clear_screen()
        show_header()
        print(f"Archivo de datos: {os.path.basename(excel_path)}")
        
        # Obtener departamentos disponibles
        departamentos = get_unique_values(data_df, 'departamento')
        departamento = show_options_menu(departamentos, "Seleccione un Departamento")
        
        # Filtrar municipios por departamento
        municipios_df = data_df[data_df['departamento'] == departamento]
        municipios = get_unique_values(municipios_df, 'municipio')
        municipio = show_options_menu(municipios, f"Seleccione un Municipio de {departamento}")
        
        # Filtrar cultivos por departamento y municipio
        cultivos_df = municipios_df[municipios_df['municipio'] == municipio]
        cultivos = get_unique_values(cultivos_df, 'cultivo')
        cultivo = show_options_menu(cultivos, f"Seleccione un Cultivo en {municipio}, {departamento}")
        
        # Obtener límite de registros
        limit = get_limit()
        
        # Realizar la consulta
        filtered_results = filter_data(data_df, departamento, municipio, cultivo, limit)
        
        # Calcular estadísticas edáficas
        edaphic_stats = calculate_edaphic_stats(filtered_results)
        
        # Mostrar resultados
        clear_screen()
        show_header()
        print(f"Consulta: {cultivo} en {municipio}, {departamento}")
        display_results(filtered_results, edaphic_stats)
        
        # Preguntar si desea realizar otra consulta
        if not confirm_action("¿Desea realizar otra consulta?"):
            break
    
    print("\nGracias por utilizar el Sistema de Consulta de Propiedades Edáficas de Cultivos.")

if __name__ == "__main__":
    main()