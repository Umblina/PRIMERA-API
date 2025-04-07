from pydantic import BaseModel

# los datos que ingreso con formato JSON
class ConversionRequest(BaseModel):
    moneda_origen: str
    moneda_destino: str
    cantidad: float

