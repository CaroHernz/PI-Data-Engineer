# Importo librerías necesarias:
from fastapi import FastAPI
import pandas as pd

# Creo la APP:
app = FastAPI(title = 'PI Data Engineer')

# Cargo la base de datos
df = pd.read_csv('plataformas.csv')

# Directorio 
@app.get("/")
async def index():
    return {"¡Hola!":"¿Cuál es tu consulta? :)",
    "Funciones de mi API:":
        ("(1) get_max_duration", 
        "(2) get_score_count",
        "(3) get_count_platform",
        "(4) get_actor",
        "(5) prod_per_county ",
        "(6) get_contents"), 
    "Contacto": "Linkedin: https://www.linkedin.com/in/carolinahernandezbarra / Github: CaroHernz"}

    return 
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
async def get_actor(platform,year):
    df = pd.read_csv('plataformas.csv')
    
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
    
    # Separo los nombres de la columna 'cast' y ordeno valores por cantidad de apariciones
    actor = filtro['cast'].str.split(', ').explode().value_counts()

    respuesta = actor.index[0]
    apariciones = actor.iloc[0]
    return {'Plataforma': platform, 'Año': year, 'Actor': respuesta, 'Apariciones': apariciones}   


# Query 5
@app.get("/prod_per_county/{tipo}/{pais}/{anio}")
def prod_per_county(tipo:str, pais:str, anio:int):
    df = pd.read_csv('plataformas.csv')
    filtro = df[(df['type'] == tipo) & (df['country'].str.contains(pais)) & (df['release_year'] == anio)]
    respuesta = filtro['type'].count()
    
    return {'País': pais, 'Año': anio, 'Peliculas': int(respuesta)}    

# Query 6
@app.get("/get_contents/{rating}")
def get_contents(rating:str):
    df = pd.read_csv('plataformas.csv')
    filtro = df[df['rating'] == rating]
    respuesta = filtro.shape[0]
    return {'rating': rating, 'contenido': respuesta}

# Sistema de recomendación
# @app.get('/get_recomendation/{title}')
# def get_recomendation(title):
#     respuesta = title
#     return {'Recomendación': respuesta}
