from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

import os

import time
# Configuración de Selenium
driver = webdriver.Chrome()

# Página web de inicio de sesión
url_login = 'https://superricas.celuwebcloud.com/web/login2.aspx'
usuario = 'admincw'
contrasena = 'cw2023'

# Acceder a la página de inicio de sesión
driver.get(url_login)

# Ingresar usuario y contraseña

input_usuario = driver.find_element(By.NAME, 'txtUsuario')  
input_usuario.send_keys(usuario)

input_contrasena = driver.find_element(By.NAME, 'txtClave')  
input_contrasena.send_keys(contrasena)
input_contrasena.send_keys(Keys.RETURN)

# Esperar a que la página cargue (ajusta el tiempo según sea necesario)


# Ahora puedes interactuar con la página web para obtener información
# Por ejemplo, puedes buscar elementos y extraer texto
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

# Localizar el campo de entrada (input) y enviar un valor
campo_busqueda = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtBusqueda')
campo_busqueda.send_keys('20723')

# # Localizar el botón de búsqueda y hacer clic
boton_busqueda = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnFiltrar')
boton_busqueda.click()

# Localizar la tabla (ajusta según el código fuente de la página)
tabla_locator = (By.XPATH, '//table[@id="ctl00_ContentPlaceHolder1_gvDatos"]')
tabla = wait.until(EC.presence_of_element_located(tabla_locator))

print(tabla.text)

# Obtiene el HTML de la tabla
tabla_html = tabla.get_attribute('outerHTML')

# Lee la tabla con Pandas
df_tabla = pd.read_html(tabla_html)[0]

df =  pd.DataFrame(df_tabla)

time.sleep(10)

# Cerrar el navegador al finalizar
driver.quit()

# Exportar a un archivo Excel
df.to_excel('tabla_datos.xlsx', index=False)

# Obtener el directorio de trabajo actual
directorio_trabajo = os.getcwd()

# Imprimir la ubicación del archivo Excel
print(f"El archivo Excel se guardó en: {directorio_trabajo}")
