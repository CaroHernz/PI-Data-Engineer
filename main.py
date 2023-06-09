# Importo librerías necesarias:
from fastapi import FastAPI
import pandas as pd

from surprise import Dataset, Reader, SVD

# Creo la APP:
app = FastAPI(title = 'PI Data Engineer')

# Cargo la base de datos
df = pd.read_csv('plataformas.csv')

# Directorio 
@app.get("/")
async def index():
    return {"¡Hola!":"¿Cuál es tu consulta? :)"}
@app.get("/")
async def contact():
    return {"Contacto": "Linkedin: https://www.linkedin.com/in/carolinahernandezbarra / Github: CaroHernz"}
 
# Query 1
@app.get("/get_max_duration/{year}/{platform}/{duration_type}")
def get_max_duration(year:int,platform:str,duration_type:str):
    df = pd.read_csv('plataformas.csv')

    if platform == 'amazon':
        filtro = df[(df['type'] == 'movie') & (df['release_year'] == year) & (df['duration_type'] == duration_type) &(df['id'].str.startswith('a'))]
    elif platform == 'disney':
        filtro = df[(df['type'] == 'movie') & (df['release_year'] == year) & (df['duration_type'] == duration_type) &(df['id'].str.startswith('d'))]
    elif platform == 'hulu':
        filtro = df[(df['type'] == 'movie') & (df['release_year'] == year) & (df['duration_type'] == duration_type) &(df['id'].str.startswith('h'))]
    elif platform == 'netflix':
        filtro = df[(df['type'] == 'movie') & (df['release_year'] == year) & (df['duration_type'] == duration_type) &(df['id'].str.startswith('n'))]
    else:
        return ('Algo salió mal. Por favor intente nuevamente :)')
    
    title_max = filtro[filtro['duration_int'] == (filtro['duration_int'].max())]
    respuesta = title_max.iloc[0,2]

    return {'Película':respuesta}

# Query 2
@app.get("/get_score_count/{platform}/{score}/{year}")
def get_score_count(platform:str, score:float, year:int):    
    df = pd.read_csv('plataformas.csv')

    if platform == 'amazon':
        filtro = df[(df['score'] > score) & (df['release_year'] == year) & (df['type'] == 'movie') & (df['id'].str.startswith('a'))]
    elif platform == 'disney':
        filtro = df[(df['score'] > score) & (df['release_year'] == year) & (df['type'] == 'movie') & (df['id'].str.startswith('d'))]
    elif platform == 'hulu':
        filtro = df[(df['score'] > score) & (df['release_year'] == year) & (df['type'] == 'movie') & (df['id'].str.startswith('h'))]    
    elif platform == 'netflix':
        filtro = df[(df['score'] > score) & (df['release_year'] == year) & (df['type'] == 'movie') & (df['id'].str.startswith('n'))]
    else:
        return ('La plataforma indicada no se encuentra o esta mal escrita. Por favor intente nuevamente :)')
    
    respuesta = filtro['title'].count()
    if not respuesta == 0:
        return {'Plataforma': platform, 'Cantidad': int(respuesta), 'Año': year, 'Score': score}
    else:
        return ('No hay películas con ese puntaje')

# Query 3
@app.get("/get_count_platform/{platform}")
def get_count_platform(platform:str):
    df = pd.read_csv('plataformas.csv')

    if platform == 'amazon':
        filtro = df[(df['type'] == 'movie') & (df['id'].str.startswith('a'))]
    elif platform == 'disney':
        filtro = df[(df['type'] == 'movie') & (df['id'].str.startswith('d'))]
    elif platform == 'hulu':
        filtro = df[(df['type'] == 'movie') & (df['id'].str.startswith('h'))]    
    elif platform == 'netflix':
        filtro = df[(df['type'] == 'movie') & (df['id'].str.startswith('n'))]
    else:
        return ('La plataforma indicada no se encuentra o esta mal escrita. Por favor intente nuevamente :)')
    
    respuesta= filtro['id'].count()
    return {'Plataforma': platform, 'Películas': int(respuesta)}

# Query 4
@app.get("/get_actor/{platform}/{year}")
def get_actor(platform:str,year:int):
    df = pd.read_csv('plataformas.csv')
    
    if platform == 'amazon':
        filtro = df[(df['release_year'] == year) & (df['id'].str.startswith('a'))]
    if platform == 'disney':
        filtro = df[(df['release_year'] == year) & (df['id'].str.startswith('d'))]
    # el total de datos en campo 'cast' de la plataforma hulu son nulos, por lo que debe retornar que no hay información
    elif platform == 'hulu':
        filtro = df[(df['release_year'] == year) & (df['id'].str.startswith('h'))]
        respuesta = apariciones = 'sin información'
        return {'Plataforma': platform, 'Año': year, 'Actor': respuesta, 'Apariciones': apariciones}     
    elif platform == 'netflix':
        filtro = df[(df['release_year'] == year) & (df['id'].str.startswith('n'))]
    else:
        return ('La plataforma indicada no se encuentra o esta mal escrita. Por favor intente nuevamente :)')

    # Separlo los dos datos del campo 'cast'
    actores_sin_nulos = filtro['cast'].dropna() # elimino nulos
    actores_str = ','.join(actores_sin_nulos.astype(str))
    actores_lista = actores_str.split(',')
    
    # Calculo la cantidad de apariciones de cada actor en la lista
    frecuencia = {}
    for actor in actores_lista:
        if actor in frecuencia:
            frecuencia[actor] +=1
        else:
            frecuencia[actor] = 1
    
    respuesta = max(frecuencia, key=frecuencia.get)
    apariciones = frecuencia[respuesta]

    return {'Plataforma': platform, 'Año': year, 'Actor': respuesta, 'Apariciones': apariciones}   

# Query 5
@app.get("/prod_per_county/{tipo}/{pais}/{anio}")
def prod_per_county(tipo:str, pais:str, anio:int):
    df = pd.read_csv('plataformas.csv')
    filtro = df[(df['type'] == tipo) & (df['country'].str.contains(pais)) & (df['release_year'] == anio)]
    respuesta = filtro['type'].count()
    
    return {'País': pais, 'Año': anio, 'Contenido': int(respuesta)}    

# Query 6
@app.get("/get_contents/{rating}")
def get_contents(rating:str):
    df = pd.read_csv('plataformas.csv')
    filtro = df[df['rating'] == rating]
    respuesta = filtro.shape[0]
    return {'rating': rating, 'contenido': respuesta}

#Sistema de recomendación:
# cargo los datos y defino reader
df = pd.read_parquet('dataset_ml.parquet')
reader = Reader(rating_scale=(1,5))
data = Dataset.load_from_df(df[['userId','id','score']],reader)

# Entreno el modelo de filtrado colaborativo
model = SVD()
trainset = data.build_full_trainset()
model.fit(trainset)

#Query 7
@app.get('/get_recomendation/{title}')
def get_recomendation(title:str):
    movie_id = df[df['title']==title]['id'].iloc[0]
    movie_inner_id = trainset.to_inner_iid(movie_id)
    prediccion = []

    if movie_id is None:
        return 'Esta pelicula no se encuentra, intente con otro titulo'

    for uid in range(trainset.n_users):
        prediccion.append((uid, model.predict(uid,movie_inner_id).est))
    
    prediccion.sort(key=lambda x: x[1], reverse=True)

    respuesta = []
    for item in prediccion[:5]:
        titulos = df[df['id']==item[0]]
        pelicula = titulos['title'].iloc[0]
        respuesta.append(pelicula)

    return {'Recomendación': respuesta}
