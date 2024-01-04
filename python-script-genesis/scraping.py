# Librerias utilizadas, para ver las versiones ir a requirements.txt
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import pandas as pd
import time
import os
from io import StringIO


hora_inicio = time.time()
# Intencion de configuracion del driver
try:
    # Configuración de Selenium
    driver = webdriver.Chrome()
    # Página web de inicio de sesión
    url_login = 'https://superricas.celuwebcloud.com/web/login2.aspx'
    usuario = 'admincw'
    contrasena = 'cw2023'

    # Acceder a la página de inicio de sesión
    driver.get(url_login)
except:
    # Mensaje informativo
    print('Se presento un error en el navegador, por favor intente de nevo...')



# Ingresar usuario y contraseña
input_usuario = driver.find_element(By.NAME, 'txtUsuario')  
input_usuario.send_keys(usuario)
input_contrasena = driver.find_element(By.NAME, 'txtClave')  
input_contrasena.send_keys(contrasena)
input_contrasena.send_keys(Keys.RETURN)


# Ahora puedes interactuar con la página web para obtener información
# Buscar elementos y extraer texto
elemento_informacion = driver.find_element(By.ID, 'ctl00_lblNombre')
informacion = elemento_informacion.text

# Ir a facturacion electronica
facturacion_electronica = driver.find_element(By.LINK_TEXT, 'FACTURACIÓN ELECTRÓNICA')
facturacion_electronica.click()

wait = WebDriverWait(driver, 10)

# Ir a administrador
administracion_option = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'ADMINISTRACIÓN')))
administracion_option.click()

# Ir a ADMIN RESOLUCION FE
segunda_option = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'ADMIN RESOLUCIÓN FE')))
segunda_option.click()

# Obtencion de ID's para iteracion
lista_datos = []

try:
    # Leer archivo excel 
    df = pd.read_excel('datos/database.xlsx')

    # Separar solo la columna objetivo
    columna = df['Vendedor']

    # Eliminar duplicados de la columna
    df_sin_duplicados = columna.drop_duplicates()

    # Iteracion de datos uno por uno
    for prueba in df_sin_duplicados:
        lista_datos.append(prueba)

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

# Para probar con fraciones de la cantidad de datos en total
indice_medio = len(lista_datos)  // 1
mitad_datos = lista_datos[:indice_medio]

data_frame = pd.DataFrame()

for iteration, id in  enumerate(mitad_datos, start=1) :
    # Localizar el campo de entrada (input) y enviar un valor
    campo_busqueda = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtBusqueda')
    # Introducir ID's
    campo_busqueda.send_keys(id)

    # Localizar el botón de búsqueda y hacer clic
    boton_busqueda = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnFiltrar')
    # esperar_boton_busqueda = wait.until(EC.presence_of_element_located(boton_busqueda))
    boton_busqueda.click()
    # driver.execute_script("arguments[0].click();", boton_busqueda)

    
    time.sleep(8)
    
    # Localizar la tabla (ajusta según el código fuente de la página)
    tabla_locator = (By.XPATH, '//table[@id="ctl00_ContentPlaceHolder1_gvDatos"]')
    tabla = wait.until(EC.presence_of_element_located(tabla_locator))

    # Obtiene el HTML de la tabla
    tabla_html = tabla.get_attribute('outerHTML')

    tabla_html_oi = StringIO(tabla_html)

    # # Lee la tabla con Pandas
    df_tabla = pd.read_html(tabla_html_oi)[0]

    # Borrar filtro por ID
    boton_busqueda = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnFiltrar')
    # esperar_boton_busqueda = wait.until(EC.presence_of_element_located(boton_busqueda))
    boton_busqueda.click()
    # driver.execute_script("arguments[0].click();", boton_busqueda)
    
    time.sleep(5)

    # Selecciona solo las columnas 'Columna1' y 'Columna2'
    df_seleccionado = df_tabla[[
        'CodDistribuidora', 
        'CodVendedor', 
        'NumResolucion', 
        'ConsecutivoActual', 
        'LimiteInferior',
        'LimiteSuperior' ,
        'Fecha Inicio Resolución',
        'Fecha Fin Resolución',
        'Prefijo',
        'Prefijo NC',
        'Consecutivo Actual NC', 
        'Limite Inferior NC',
        'LimiteSuperiorNc',
        'Fecha Creación'
        ]]
    
    df_temp = pd.DataFrame(df_seleccionado)

    data_frame = pd.concat([data_frame, df_temp])

    print(df_temp)
    print(f'Extracciones completadas: {iteration} de {len(mitad_datos)} totales id: {id}')

# Cerrar el navegador al finalizar
driver.quit()

# Manejo de archivo excel
try:
    # Exportar a un archivo Excel
    data_frame.to_excel('datos/documeto_cruce.xlsx', index=False)

    # Obtener el directorio de trabajo actual
    directorio_trabajo = os.getcwd()

    # Imprimir la ubicación del archivo Excel
    print(f"🍀 El archivo Excel se guardó en: { directorio_trabajo } en carpeta 'datos' 🍀")

except PermissionError as permission:
    print(permission.strerror)
    print("No tienes permiso para escribir en este archivo.")
except FileNotFoundError as file:
    print(file.strerror)
    print("El archivo o la ruta del archivo no existen.")
except IsADirectoryError as isDirectory:
    print(isDirectory.strerror)
    print("Se esperaba un archivo, pero se proporcionó un directorio.")
except OSError as os:
    print(os.strerror)
    print("Hubo un error relacionado con el sistema operativo.")
except pd.errors.ExcelWriterError:
    print("Hubo un error al usar ExcelWriter.")
except ValueError as val:
    print(val)
    print("Se proporcionaron argumentos con valores incorrectos.")
except TimeoutException as time_out:
    print(time_out)
    print("Se proporcionaron argumentos con valores incorrectos.")

hora_fin = time.time()

print(f'Tiempo de ejecucion del script: { int(hora_fin - hora_inicio) } segundos')