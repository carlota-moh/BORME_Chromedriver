# BORME - Chromedriver

Este es un proyecto realizado como parte de un curso en Adquisición de datos. El objetivo es acceder a 
la página web del registro mercantil y descargar todos los registros de empresas recién creadas para
la fecha indicada en formato PDF y XML. El proyecto se compone de dos módulos:

+ main: permite descargar en local los documentos PDF y XML para la fecha introducida.
+ extra: permite cargar un documento XML a BeatifulSoup.

El proyecto se ejecuta desde el directorio mediante el comando:

`python3 SPIDER MAIN <date/>`

La fecha de entrada debe encontrarse en formato YYYY-MM-DD.
Dentro del script se formatea para poder ser enviada en el
formato que la página web espera.

Si se desea ejecutar el código extra, emplear el comando:

`python3 SPIDER EXTRA <date/>`

Una vez hecho esto, indicar en el terminal el nombre del
archivo que se desea parsear. Indicar únicamente el nombre
del archivo, no la ruta (el script se encarga de localizarlo).

Si se desea ejecutar tanto la práctica principal como el
extra, emplear:

`python3 SPIDER MAIN EXTRA <date/>`
