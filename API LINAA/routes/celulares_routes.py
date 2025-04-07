from fastapi import APIRouter, HTTPException, status  # Manejo de rutas, excepciones HTTP y estados
from services.celulares_servicios import (obtener_celulares,obtener_celulares_id,crear_celular,actualizar_celular,eliminar_celular)
from fastapi.responses import JSONResponse  # personalizar las respuestas de error
from models.celulares_models import Celular

router = APIRouter()  # Agrupar las rutas para modularizar el código

# ---------- Endpoints ----------

# GET /celulares → Lista todos los celulares disponibles
@router.get("/celulares", response_model=list, status_code=status.HTTP_200_OK)
async def get_celulares():
    celulares = obtener_celulares()
    if not celulares:
        # Si la lista está vacía, devuelvo una excepción HTTP 404 con un mensaje personalizado
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay stock de celulares")
    return celulares

# GET /celulares/{celular_id} → Obtiene un celular por su ID
@router.get("/celulares/{celular_id}", response_model=Celular, status_code=status.HTTP_200_OK)
def get_celulares_id(celular_id: str):
    try:
        celular = obtener_celulares_id(celular_id)
        if celular is None:
            # Si no se encuentra el celular, lanzo error 404 con detalle
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Celular no encontrado")
        return celular
    except Exception as e:
        # Si algo falla (por ejemplo, ID inválido), devuelvo una respuesta personalizada
        return JSONResponse(content={"mensaje de error": str(e)}, status_code=status.HTTP_404_NOT_FOUND)

# POST /celulares → Crea un nuevo celular
@router.post("/celulares")
async def post_celulares(celular: Celular, status_code=status.HTTP_201_CREATED):
    try:
        # Validación manual: ejemplo si el precio es negativo
        if celular.precio < 0:
            raise HTTPException(status_code=400, detail="El precio no puede ser negativo")  # 400: Datos inválidos
        celular_id = crear_celular(celular)
        return {"mensaje": "Celular insertado correctamente", "celular_id": celular_id}
    except Exception as e:
        return JSONResponse(content={"mensaje de error": str(e)}, status_code=400)  # 400: Error de validación


# PUT /celulares/{celular_id} → Actualiza un celular existente
@router.put("/celulares/{celular_id}")
async def put_celulares(celular_id: str, celular: Celular, status_code=status.HTTP_200_OK):
    try:
        resultado = actualizar_celular(celular_id, celular)
        if resultado.get("mensaje") == "celular no encontrado":
            # Si el celular no se encontró para actualizar, devuelvo error 404 no encontrado
            return JSONResponse(content={"mensaje de error": "Celular no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)
        return resultado
    except Exception as e:
        # Si falla algo más (como un error en la base de datos), devuelvo error 500
        return JSONResponse(content={"mensaje de error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# DELETE /celulares/{celular_id} → Elimina un celular existente
@router.delete("/celulares/{celular_id}")
async def delete_celulares(celular_id: str, status_code=status.HTTP_200_OK):
    try:
        resultado = eliminar_celular(celular_id)
        if resultado.get("mensaje") == "celular no encontrado":
            # Si el celular no existe, notifico con código 404
            return JSONResponse(content={"mensaje de error": "Celular no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)
        return resultado
    except Exception as e:
        # Si ocurre un error inesperado (por ejemplo, ID malformado), retorno código 500 (Error del servidor)
        return JSONResponse(content={"mensaje de error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
