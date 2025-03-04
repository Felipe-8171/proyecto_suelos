# main.py

import os
import sys
from modules.ui import clear_screen, show_header, show_options_menu, get_limit, display_results, confirm_action
from modules.data import load_data, filter_data, calculate_edaphic_stats, get_unique_values

# Definir la ruta fija del archivo Excel
EXCEL_PATH = "C:/Users/felip/Downloads/resultado_laboratorio_suelo.xlsx"

def main():
    """Función principal del programa."""
    clear_screen()
    show_header()

    # Cargar datos una sola vez
    try:
        data_df = load_data(EXCEL_PATH)
        print(f"Datos cargados correctamente. Total de registros: {len(data_df)}")
    except FileNotFoundError:
        print(f"Error: El archivo {EXCEL_PATH} no existe. Verifica la ruta.")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar los datos: {str(e)}")
        sys.exit(1)

    # Bucle principal del programa
    while True:
        clear_screen()
        show_header()
        print(f"Archivo de datos: {os.path.basename(EXCEL_PATH)}")

        # Selección de departamento
        departamentos = get_unique_values(data_df, 'Departamento')
        departamento = show_options_menu(departamentos, "Seleccione un Departamento")

        # Filtrar municipios por departamento
        municipios_df = data_df[data_df['Departamento'] == departamento]
        municipios = get_unique_values(municipios_df, 'Municipio')
        municipio = show_options_menu(municipios, f"Seleccione un Municipio de {departamento}")

        # Filtrar cultivos por municipio
        cultivos_df = municipios_df[municipios_df['Municipio'] == municipio]
        cultivos = get_unique_values(cultivos_df, 'Cultivo')
        cultivo = show_options_menu(cultivos, f"Seleccione un Cultivo en {municipio}, {departamento}")

        # Obtener el límite de registros
        limit = get_limit()

        # Filtrar los datos
        filtered_results = filter_data(data_df, departamento, municipio, cultivo, limit)

        # Calcular estadísticas edáficas
        edaphic_stats = calculate_edaphic_stats(filtered_results)

        # Mostrar resultados
        clear_screen()
        show_header()
        print(f"Consulta: {cultivo} en {municipio}, {departamento}")
        display_results(filtered_results, edaphic_stats)

        # Preguntar si el usuario quiere hacer otra consulta
        if not confirm_action("¿Desea realizar otra consulta?"):
            break

    print("\nGracias por utilizar el Sistema de Consulta de Propiedades Edáficas de Cultivos.")

if __name__ == "__main__":
    main()
