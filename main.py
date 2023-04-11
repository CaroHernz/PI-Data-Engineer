# Importo librerías necesarias:
from fastapi import FastAPI
import pandas as pd

# Creo la APP:
app = FastAPI(title = 'PI Data Engineer')

# Cargo la base de datos
df = pd.read_csv('plataformas.csv')

# Directorio 
@app.get("/")
async def presentacion():
    return "¡Hola! ¿Cuál es tu consulta? :)"

@app.get("/contacto")
def contacto():
    return "Linkedin: https://www.linkedin.com/in/carolinahernandezbarra / Github: CaroHernz"

@app.get("/menu")
def menu():
    return ("Funciones de mi API: (1) get_max_duration (2) get_score_count (3) get_count_platform (4) get_actor (5) No disponible (6) get_contents")

# Query 1
@app.get("/get_max_duration/")
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
    return title_max.iloc[0,2]

# Query 2
@app.get("/get_score_count/")
def get_score_count(platform:str, score, year):
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
    
    return df_platform['id'].count()

# Query 3
@app.get("/get_count_platform/")
def get_count_platform(platform):
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
    
    return df_platform['id'].count()

# Query 4
@app.get("/get_actor/")
def get_actor(platform,year):
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
    top = frecuencia.index[0]
    
    return top

# Query 5

# Query 6
@app.get("/get_contents/")
def get_contents(rating):
    filtro = df[df['rating'] == rating]
    return filtro.shape[0]