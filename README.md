## PROGRAMACIÓN PARA LA CIENCIA DE DATOS

### Actividad 4 - Testing, mantenimiento y despliegue de aplicaciones

El objetivo principal es crear un código en Python capaz de analizar la información 
de una BBDD de Tweets, trabajando la correcta carga, el preprocesado y análisis de 
sentimientos para obtener una percepción del estado de ánimo reflejado en la 
frecuencia con que se repiten las palabras.

### *Este paquete contiene la solucion de la PEC4*

**El paquete incluye los siguientes archivos:**

- `main.py` contiene la ejecución principal con la llamada a todas las funciones para
que se ejecute el código completo y presente los resultados del análisis. 
**Importante**: Durante la ejecución del código se generarán 3 gráficos, los cuales
deben ser cerrados, tras su visualización, para que continúe el proceso.

- `utils.py` contiene las funciones de cada proceso.

- `test.py` contiene los test unitarios que garantizan el correcto funcionamiento de
las funciones.

- `requirements.txt` contiene el listado de librerías necesarias para ejecutar el código

**El paquete NO INCLUYE:**

- Los datos necesarios para el procesado ``twitter_reduced.zip`` dataset con 800.000 tweets y 6 variables. 
- Si quieres comprobar el funcionamiento del código fuera del entorno de esta PEC puedes acceder al dataset completo: 
[Sentiment140 dataset](https://www.kaggle.com/datasets/kazanova/sentiment140).


## Funcionamiento del código

El objetivo principal es correr el código desde una máquina virtual, el proceso a
seguir es:

1.Crea un nuevo entorno virtual:
```
virtualenv venv
```
2.Activa el entorno virtual:
```
source venv/bin/activate
```

3.Ubícate en la carpeta venv creada:
````
cd venv
````

4.Comprueba los archivos existentes:
````
ls
````
**Notas:** 

- *Asegúrate de tener los archivos del proyecto (`main.py`, `utils.py`, `test.py`, `requirements.txt`) en el directorio 
actual, debes copiar o mover los archivos desde su ubicación original a este directorio.*

- *Debes tener también una carpeta `data` que contenga los archivos en formato .zip, estos últimos NO proporcionados en 
el paquete.*

5.Instala las librerías necesarias descritas en el requirements.txt:
```
pip install -r requirements.txt
```
**Nota:** *en caso de no poder instalar `requirements.txt` con el comando, puedes ejecutarlo abriendo una
consola/terminal mediante  'click derecho' sobre el propio archivo requirements.txt*

6.El siguiente comando ejecuta todo el código de forma secuencial:

````
python3 main.py
````
Imprime por pantalla descripciones de registros del dataset a modo de ejemplo, tras de ejecutar cada función. 
Finalmente muestra las respuestas a preguntas del apartado 7 de la PEC4

**Nota:** *recuerda la advertencia de los gráficos descrita en `main.py`*

## Funcionamiento de los test

Los test se ejecutan de forma secuencal a través del siguiente comando:
````
python3 -m unittest test.py
````
Existe un test para cada función implementada, contemplando diversos casos de prueba para verificar
su óptimo funcionamiento.

El rendimiento de los test se evalúa a través de la herramienta 
[Coverage.py](https://coverage.readthedocs.io/en/coverage-5.3/)
observando qué partes del código se han ejecutado y, a continuación, analiza el 
código fuente para identificar el código que podría haberse ejecutado pero no se 
ejecutó.

Para instalar Coverage.py se ejecuta el siguiente comando:
````
pip install coverage
````

Para evaluar el rendimiento de los test se ejecuta el siguiente comando:
````
coverage run -m unittest test.py
````

Para obtener un reporte del resultado de los test se ejecuta el siguiente comando:
````
coverage report
````
El reporte contiene una tabla de todos los archivos.py ejecutados y una columna 'Cover' que representa el % de cobertura 
satisfecho en cada archivo.

El porcentaje obtenido en el report para el archivo `test.py` debería superar el 50% de cobertura, para 
considerar los test como válidos


## Licencia

Este proyecto se distribuye bajo la Licencia Atribución-NoComercial (CC BY-NC)

Puedes:

- Compartir: copiar y redistribuir el material en cualquier medio o formato.
- Adaptar: remezclar, transformar y construir sobre el material.

Bajo las siguientes condiciones:

- Atribución: debes dar crédito de manera adecuada, proporcionando un enlace a la 
licencia, e indicar si se han realizado cambios. Puedes hacerlo de cualquier manera 
razonable, pero no de una manera que sugiera que quien genera esta licencia, te 
respalda a ti o al uso que hagas del material.
- NoComercial: no puedes utilizar el material con fines comerciales.
- Compartir Igual: si remezclas, transformas o construyes sobre el material, debes 
distribuir tus contribuciones bajo la misma licencia que el original.

Puedes consultar el texto completo de la licencia en el archivo 
[LICENCIA](https://creativecommons.org/licenses/by-nc/4.0/legalcode).