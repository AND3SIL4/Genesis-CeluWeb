from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

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
time.sleep(5)

# Ahora puedes interactuar con la página web para obtener información
# Por ejemplo, puedes buscar elementos y extraer texto
elemento_informacion = driver.find_element(By.ID, 'ctl00_lblNombre')
informacion = elemento_informacion.text

# Imprimir o procesar la información según tus necesidades
print(informacion)

# Cerrar el navegador al finalizar
driver.quit()
