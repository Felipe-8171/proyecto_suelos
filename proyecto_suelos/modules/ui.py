#!/usr/bin/env python
# modules/ui.py

import os

def clear_screen():
    """Limpia la pantalla de la consola."""
    # Verifica el sistema operativo para usar el comando apropiado
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    """Muestra el encabezado de la aplicación."""
    print("=" * 80)
    print(" SISTEMA DE CONSULTA DE PROPIEDADES EDÁFICAS DE CULTIVOS EN COLOMBIA ".center(80))
    print("=" * 80)
    print()

def show_options_menu(options_list, prompt_text):
    """
    Muestra un menú de opciones y obtiene la selección del usuario.
    
    Args:
        options_list (list): Lista de opciones a mostrar
        prompt_text (str): Texto para solicitar la entrada
        
    Returns:
        str: Opción seleccionada por el usuario
    """
    print(f"\n{prompt_text}:")
    
    # Si hay muchas opciones, mostrarlas en varias columnas
    if len(options_list) > 10:
        for i, option in enumerate(options_list, 1):
            print(f"{i}. {option}", end="\t")
            if i % 3 == 0:
                print()
        print()
    else:
        for i, option in enumerate(options_list, 1):
            print(f"{i}. {option}")
    
    # Permitir al usuario ingresar el número o el texto de la opción
    selection = input("\nIngrese el número o el nombre de su selección: ")
    
    # Interpretar la selección
    try:
        # Si el usuario ingresó un número
        idx = int(selection) - 1
        if 0 <= idx < len(options_list):
            return options_list[idx]
    except ValueError:
        # Si el usuario ingresó un texto
        if selection in options_list:
            return selection
    
    # Si llegamos aquí, la selección no fue válida
    print("Selección no válida. Por favor intente de nuevo.")
    return show_options_menu(options_list, prompt_text)

def get_limit():
    """
    Solicita al usuario el número de registros a mostrar.
    
    Returns:
        int: Número de registros
    """
    while True:
        try:
            limit = int(input("\nIngrese el número de registros a consultar (1-100): "))
            if 1 <= limit <= 100:
                return limit
            else:
                print("Por favor ingrese un número entre 1 y 100.")
        except ValueError:
            print("Por favor ingrese un número válido.")

def display_results(results_df, stats):
    """
    Muestra los resultados de la consulta en formato tabular.
    
    Args:
        results_df (pandas.DataFrame): DataFrame con los resultados filtrados
        stats (dict): Diccionario con estadísticas de variables edáficas
    """
    if results_df.empty:
        print("\nNo se encontraron resultados para los criterios especificados.")
        return
    
    # Mostrar información de la consulta
    print("\nRESULTADOS DE LA CONSULTA")
    print(f"Total de registros encontrados: {len(results_df)}")
    
    # Mostrar estadísticas edáficas
    print("\nMEDIANAS DE VARIABLES EDÁFICAS:")
    for var, value in stats.items():
        if value is not None:
            print(f"{var}: {value:.2f}")
        else:
            print(f"{var}: No disponible")
    
    # Mostrar los resultados en formato tabular
    print("\nDETALLE DE REGISTROS:")
    print("-" * 100)
    
    # Determinar las columnas a mostrar
    display_columns = ['Departamento', 'Municipio', 'Cultivo', 'Topografia']
    
    # Crear encabezados con espacios fijos
    header = "| " + " | ".join([col.upper().ljust(15) for col in display_columns]) + " |"
    print(header)
    print("-" * len(header))
    
    # Mostrar cada fila
    for _, row in results_df.iterrows():
        row_str = "| " + " | ".join([str(row.get(col, '')).ljust(15) for col in display_columns]) + " |"
        print(row_str)
    
    print("-" * len(header))

def confirm_action(prompt):
    """
    Solicita confirmación al usuario para realizar una acción.
    
    Args:
        prompt (str): Mensaje de solicitud
        
    Returns:
        bool: True si el usuario confirma, False en caso contrario
    """
    response = input(f"\n{prompt} (s/n): ").lower()
    return response in ['s', 'si', 'sí', 'y', 'yes']