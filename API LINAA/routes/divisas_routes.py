from fastapi import APIRouter, HTTPException  # Importo APIRouter para crear rutas y HTTPException para manejar errores
from models.divisas_models import ConversionRequest  # Importo el modelo que define los datos que debe enviar el usuario
from services.divisas_servicios import obtener_tasa_cambio  # Importo la función que obtiene la tasa de cambio

router = APIRouter()  # Creo una instancia del enrutador para las rutas relacionadas con divisas

@router.post("/convertir")  # Defino una ruta POST en "/convertir" para hacer la conversión de divisas
async def convertir_divisa(data: ConversionRequest):  # Esta función recibe los datos del cuerpo de la petición
    print("Datos recibidos:", data)  # Imprimo los datos para verificar que estén llegando correctamente
    
    tasa = await obtener_tasa_cambio(data.moneda_origen.upper(), data.moneda_destino.upper())  # Llamo a la función para obtener la tasa de cambio en tiempo real

    if not tasa:  # Si no recibo una tasa válida...
        raise HTTPException(status_code=400, detail="Moneda no válida o no disponible")  # ...devuelvo un error al cliente

    total = data.cantidad * tasa  # Calculo el total multiplicando la cantidad ingresada por la tasa

    return {  # Devuelvo un diccionario con los datos de la conversión
        "cantidad_original": data.cantidad,  # La cantidad original ingresada por el usuario
        "moneda_origen": data.moneda_origen.upper(),  # La moneda de origen, en mayúsculas
        "moneda_destino": data.moneda_destino.upper(),  # La moneda de destino, en mayúsculas
        "tasa_cambio": tasa,  # La tasa de cambio obtenida
        "convertido": total  # El resultado de la conversión
    }

