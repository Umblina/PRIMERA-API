from pydantic import BaseModel  # BaseModel permite crear clases que validan datos de entrada/salida
from typing import Optional  # Para campos que no son obligatorios si no opcionales

#datos que voy a poner en la BD en formato JSOn
class Celular(BaseModel):
    marca: str
    modelo: str
    sistema_operativo: str
    ram_gb: int
    almacenamiento_gb: int
    precio: float
    descripcion: Optional[str] = None #como este :D

