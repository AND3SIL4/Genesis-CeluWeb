import os
import shutil



extenciones_dict = {
    '.txt': 'documentos',
    '.docx':'documentos',
    '.pdf':'documentos',
    '.jpg':'imagenes',
    '.png':'imagenes',
    '.exe':'ejecutables',
}
predeterminada = 'otros'
# carpeta_organizadora_ruta = r'C:\Users\asilva\OneDrive - COMESTIBLES RICOS S.A\asilva\Downloads'

print('Nota: por favor indicar la ruta con backslash')
carpeta_organizadora_ruta = input('Por favor ingrese la ruta para organizar: ')

archivos = os.listdir(carpeta_organizadora_ruta)

for archivo in archivos:
    archivo_origen_ruta = os.path.join(carpeta_organizadora_ruta, archivo)

    if os.path.isfile(archivo_origen_ruta):
        _, extension = os.path.splitext(archivo)
        nombre_carpeta = extenciones_dict.get(extension.lower(), predeterminada)

        archivo_destino_ruta = os.path.join(carpeta_organizadora_ruta, nombre_carpeta)

        if not os.path.exists(archivo_destino_ruta):
            os.makedirs(archivo_destino_ruta)

        shutil.move(archivo_origen_ruta, archivo_destino_ruta)

print('Archivos organizados correctamente...')