import pandas as pd

lista_datos = []

try:
    # Leer archivo excel 
    df = pd.read_excel('datos/data.xlsx')

    # Separar solo la columna objetivo
    columna = df['Vendedor']

    # Eliminar duplicados de la columna
    df_sin_duplicados = columna.drop_duplicates()

    # Iteracion de datos uno por uno
    for prueba in df_sin_duplicados:
        lista_datos.append(prueba)

    print(lista_datos)

    # Mensaje informativo
    print(f'Longitud normal de la columna: { len(columna) }')
    print(f'Longitud de la columna sin duplicados: { len(df_sin_duplicados) }')
    print(f'Se eliminaron { len(columna) - len(df_sin_duplicados) } datos duplicados')
except FileNotFoundError as fnf:
    print(fnf.strerror)
    print('No se ha encontrado el archivo, por favor intente de nuevo')
except FileExistsError as fne:
    print(fne.strerror)
    print('El archivo no exite, por favor valide e intente de nuevo')
except PermissionError as p:
    print(p.strerror)
    print('Permiso denegado, por favor cierre todos los archivos e intente de nuevo')
finally:
    print('La preparación de datos terminó')