# Librerias utilizadas, para ver las versiones ir a requirements.txt
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium import webdriver
import pandas as pd
import time
import os
from io import StringIO

def iniciar_sesion(driver, url, usuario, contrasena):
    try:
        driver.get(url)
        
        # Verificar si la página de inicio de sesión se cargó correctamente
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, 'txtUsuario')))
        
        input_usuario = driver.find_element(By.NAME, 'txtUsuario')
        input_contrasena = driver.find_element(By.NAME, 'txtClave')

        input_usuario.send_keys(usuario)
        input_contrasena.send_keys(contrasena)
        input_contrasena.send_keys(Keys.RETURN)

        # Verificar si el inicio de sesión fue exitoso
        wait.until(EC.presence_of_element_located((By.ID, 'ctl00_lblNombre')))
        
         # Navegar hasta la interfaz objetivo
        driver.find_element(By.LINK_TEXT, 'FACTURACIÓN ELECTRÓNICA').click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'ADMINISTRACIÓN'))).click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'ADMIN RESOLUCIÓN FE'))).click()

        return True
    except TimeoutException:
        print('Error: La página de inicio de sesión no se cargó correctamente o el inicio de sesión falló.')
        return False

def obtener_datos(driver, id):
    try:
        # Esperar a que el campo de búsqueda esté presente y visible
        campo_busqueda = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_txtBusqueda'))
        )
        
        campo_busqueda.clear()  # Limpiar el campo de búsqueda antes de ingresar el nuevo valor
        campo_busqueda.send_keys(id)

        boton_busqueda = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'ctl00_ContentPlaceHolder1_btnFiltrar'))
        )
        boton_busqueda.click()

        time.sleep(6)

        tabla_locator = (By.XPATH, '//table[@id="ctl00_ContentPlaceHolder1_gvDatos"]')
        tabla = WebDriverWait(driver, 10).until(EC.presence_of_element_located(tabla_locator))

        tabla_html = tabla.get_attribute('outerHTML')
        tabla_html_oi = StringIO(tabla_html)

        df_tabla = pd.read_html(tabla_html_oi)[0]

        boton_busqueda = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'ctl00_ContentPlaceHolder1_btnFiltrar'))
        )
        boton_busqueda.click()

        time.sleep(6)

        df_seleccionado = df_tabla[['CodDistribuidora', 'CodVendedor', 'NumResolucion', 'ConsecutivoActual', 'LimiteInferior',
                                     'LimiteSuperior', 'Fecha Inicio Resolución', 'Fecha Fin Resolución', 'Prefijo',
                                     'Prefijo NC', 'Consecutivo Actual NC', 'Limite Inferior NC', 'LimiteSuperiorNc',
                                     'Fecha Creación']]

        return df_seleccionado
    except TimeoutException:
        print(f'Error: No se pudo obtener datos para el ID: {id}')
        return pd.DataFrame()
    except NoSuchElementException:
        print("Error: No se pudo encontrar el elemento de búsqueda.")
        return pd.DataFrame()
    except StaleElementReferenceException:
        print("Error: Elemento de la página ha quedado obsoleto. Actualizando y volviendo a intentar...")
        return obtener_datos(driver, id)  # Llamar recursivamente a la función después de actualizar

def main():
    hora_inicio = time.time()

    try:
        # Configuración de Selenium
        driver = webdriver.Chrome()

        # Página web de inicio de sesión
        url_login = 'https://superricas.celuwebcloud.com/web/login2.aspx'
        usuario = 'admincw'
        contrasena = 'cw2023'

        if not iniciar_sesion(driver, url_login, usuario, contrasena):
            return

        # Leer archivo excel 
        df = pd.read_excel('datos/database.xlsx')

        # Separar solo la columna objetivo
        columna = df['Vendedor']

        # Eliminar duplicados de la columna
        df_sin_duplicados = columna.drop_duplicates()

        # Iteración de datos uno por uno
        lista_datos = []

        # Iteración de datos uno por uno
        for prueba in df_sin_duplicados:
            lista_datos.append(prueba)

         # Para probar con fracciones de la cantidad de datos en total
        indice_medio = len(lista_datos)  // 1
        mitad_datos = lista_datos[:indice_medio]

        data_frame = pd.DataFrame()

        for iteration, id in enumerate(mitad_datos, start=1):
            df_temp = obtener_datos(driver, id)

            data_frame = pd.concat([data_frame, df_temp])

            print(df_temp)
            print(f'Extracciones completadas: {iteration} de {len(mitad_datos)} totales id: {id}')

    finally:
        # Cerrar el navegador al finalizar, asegurándose de manejar correctamente las excepciones
        if 'driver' in locals():
            driver.quit()

    # Manejo de archivo excel
    try:
        # Exportar a un archivo Excel
        data_frame.to_excel('datos/documento_cruce.xlsx', index=False)

        # Obtener el directorio de trabajo actual
        directorio_trabajo = os.getcwd()

        # Imprimir la ubicación del archivo Excel
        print(f"🍀 El archivo Excel se guardó en: { directorio_trabajo } en carpeta 'datos' 🍀")

    except pd.errors.PandasExcelWriterError:
        print("Hubo un error al usar ExcelWriter.")
    except ValueError as val:
        print(val)
        print("Se proporcionaron argumentos con valores incorrectos.")
    except TimeoutException as time_out:
        print(time_out)
        print("Se proporcionaron argumentos con valores incorrectos.")
    except Exception as e:
        print(f"Otro error inesperado: {e}")

    hora_fin = time.time()

    print(f'Tiempo de ejecución del script: {int(hora_fin - hora_inicio)} segundos')

if __name__ == "__main__":
    main()
