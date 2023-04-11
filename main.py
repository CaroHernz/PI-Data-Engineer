# Importo librerías necesarias:
from fastapi import FastAPI
import pandas as pd

# Creo la APP:
app = FastAPI(title = 'PI Data Engineer')

# Cargo la base de datos
df = pd.read_csv('plataformas.csv')

# Directorio 
@app.get("/")
def index():
    return {"message":"¡Hola! ¿Cuál es tu consulta? :)"}

@app.get("/contacto")
def contacto():
    return "Linkedin: https://www.linkedin.com/in/carolinahernandezbarra / Github: CaroHernz"

@app.get("/menu")
def menu():
    return ("Funciones de mi API: (1) get_max_duration (2) get_score_count (3) get_count_platform (4) get_actor (5) No disponible (6) get_contents")

# Query 1
@app.get("/get_max_duration/{year}/{platform}/{duration_type}")
def get_max_duration(year:int,platform:str,duration_type:str):
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
    query = df[(df['score'] > score) & (df['release_year'] == year)]

    if platform == 'amazon':
        df_platform = query[(query['type'] == 'movie') & (query['id'].str.startswith('a'))]
    elif platform == 'disney':
        df_platform = query[(query['type'] == 'movie') & (query['id'].str.startswith('d'))]
    elif platform == 'hulu':
        df_platform = query[(query['type'] == 'movie') & (query['id'].str.startswith('h'))]    
    elif platform == 'netflix':
        df_platform = query[(query['type'] == 'movie') & (query['id'].str.startswith('n'))]
    else:
        return ('La plataforma indicada no se encuentra o esta mal escrita. Por favor intente nuevamente :)')
    respuesta = df_platform['id'].count()
    return {'Plataforma': platform, 'Cantidad': respuesta, 'Año': year, 'Score': score}

# Query 3
@app.get("/get_count_platform/{platform}")
def get_count_platform(platform:str):
    if platform == 'amazon':
        df_platform = df[(df['type'] == 'movie') & (df['id'].str.startswith('a'))]
    elif platform == 'disney':
        df_platform = df[(df['type'] == 'movie') & (df['id'].str.startswith('d'))]
    elif platform == 'hulu':
        df_platform = df[(df['type'] == 'movie') & (df['id'].str.startswith('h'))]    
    elif platform == 'netflix':
        df_platform = df[(df['type'] == 'movie') & (df['id'].str.startswith('n'))]
    else:
        return ('La plataforma indicada no se encuentra o esta mal escrita. Por favor intente nuevamente :)')
    
    respuesta= df_platform['id'].count()
    return {'Plataforma': platform, 'Películas': respuesta}

# Query 4
@app.get("/get_actor/{platform}/{year}")
def get_actor(platform:str,year:int):
    if platform == 'amazon':
        filtro = df[(df['release_year'] == year) & (df['id'].str.startswith('a'))]
    elif platform == 'disney':
        filtro = df[(df['release_year'] == year) & (df['id'].str.startswith('d'))]
    elif platform == 'hulu':
        filtro = df[(df['release_year'] == year) & (df['id'].str.startswith('h'))]    
    elif platform == 'netflix':
        filtro = df[(df['release_year'] == year) & (df['id'].str.startswith('n'))]
    else:
        return ('La plataforma indicada no se encuentra o esta mal escrita. Por favor intente nuevamente :)')
    
    # Separo los nombres en una lista
    actor = filtro['cast'].str.split(', ')
    frecuencia = actor.explode().value_counts()
    respuesta = frecuencia.index[0]
    
    return {'Plataforma': platform, 'Año': year, 'Actor': respuesta, 'Apariciones': respuesta.count()}

# Query 5
@app.get("/prod_per_county/{tipo}/{pais}/{anio}")
def prod_per_county(tipo:str, pais:str, anio:int):
    filtro = df[(df['type'] == tipo) & (df['country'] == pais) & (df['release_year'] == anio)]
    respuesta = filtro['type'].count()
    return {'País': pais, 'Año': anio, 'Tipo contenido': tipo, 'Cantidad': respuesta}    

# Query 6
@app.get("/get_contents/{rating}")
def get_contents(rating:str):
    filtro = df[df['rating'] == rating]
    respuesta = filtro.shape[0]
    return {'rating': rating, 'contenido': respuesta}

# Sistema de recomendación
@app.get('/get_recomendation/{title}')
def get_recomendation(title):
    respuesta = 10
    return {'Recomendación': respuesta}