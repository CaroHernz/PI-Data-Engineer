# Importo librerías necesarias:
from fastapi import FastAPI
import pandas as pd

# Creo la APP:
app = FastAPI(title = 'PI Data Engineer')

@app.get("/")
async def root():
    return {"message": "Hello World"}