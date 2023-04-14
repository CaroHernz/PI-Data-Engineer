<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>
  
# <h1 align=center>**`Proyecto Individual - Data Engineer`**</h1>

Data Engineer: Carolina Hernández Barra

## Descripción del problema:
Nuestra start-up provee servicios de agregación de plataformas de streaming. A partir de datos obtenidos de diferentes plataformas de stream (Amazon, Disney, Hulu y Netflix) crearé un modelo de Machine Learnig que de solución a un problema de nuestro negocio: un Sistema de recomendación.

## Desarrollo:
El ciclo de vida de un proyecto de Machine Learning contempla desde el tratamiento y recolección de los datos (Data Engineer stuff) hasta el entrenamiento y mantenimiento del modelo de Machine Learning según llegan nuevos datos.

Por lo que acontinuación se detallara el proceso realizado desde 0:

## Proceso ETL 
**_Extracción de Datos_**: trabajaremos con los archivos(csv) provistos de la carpeta [Datasets](https://github.com/CaroHernz/PI-Data-Engineer/tree/main/Datasets)

**_Transformación de Datos_**: los datos entregados son procesados, según exigencias, de la siguiente manera:
1. Generación del campo 'id'
2. Concatenar los 4 archivos de Datasets en un solo archivo llamado 'plataformas'
3. Reemplazar de valores nulos del campo 'rating' por 'G'
4. Conversión del campo 'date_added' al formato (AAAA-mm-dd)
5. Conversión de los campos de texto a minúsculas 
6. Conversión del campo 'duration' en los campos: 'duration_int' y 'duration_type'
7. Normalización de algunos valores de la columna 'rating'
8. Reemplazar los valores nulos del campo 'cast' por 'sin información'
9. Combinación del dataset con el promedio de rating usando el método "merge"
10. Exportación del archivo csv final: [_plataformas.csv_](https://github.com/CaroHernz/PI-Data-Engineer/blob/main/plataformas.csv)

*El proceso de extracción, transformación y carga lo pueden encontrar en el archivo [ETL.ipynb](https://github.com/CaroHernz/PI-Data-Engineer/blob/main/ETL.ipynb)*

### Desarrollo de la API con _FastAPI_

Creamos 6 funciones:
* **get_max_duration:** Película con mayor duración según año, plataforma y tipo de duración
* **get_score_count:** Cantidad de películas según plataforma, según puntaje y año
* **get_count_platform:** Cantidad de películas según plataforma
* **get_actor:** Actor que más se repite según plataforma y año
* **prod_per_county:** Cantidad de contenidos que se publicó por país y año
* **get_contents:** Cantidad total de contenidos según rating

**Deployment: https://plataformas-9gqb.onrender.com/**

