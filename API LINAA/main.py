from fastapi import FastAPI  # Importa la clase principal de FastAPI para crear la aplicación
from routes.celulares_routes import router as celulares_router  # Importa el router desde el archivo de rutas y lo renombra para usarlo localmente
from typing import Union  # (sirve para declarar tipos opcionales en FastAPI)


app = FastAPI()  # Se crea una instancia de la aplicación FastAPI


app.include_router(celulares_router, prefix="", tags=["celulares"])
# Se incluye el router de celulares (definido en routes/celulares_routes.py)
# El prefix "" indica que los endpoints del router no tienen prefijo adicional.
# La etiqueta "celulares" agrupa todos los endpoints bajo ese tag en la documentación automática de FastAPI.

# Creación del ENDPOINT (para levantar el servidor)
@app.get("/")
async def root():
    return {"Mensaje": "Bienvenido a mi primera APIIII :D"}
