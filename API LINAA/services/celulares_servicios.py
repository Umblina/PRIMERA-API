from db.database_celulares import database # Importa la instancia de conexión a la base de datos MongoDB 
from bson import ObjectId  # Importa ObjectId que se usa para convertir cadenas en IDs válidos de MongoDB (las que aparecen arriba de cuando escribo el Json)
from models.celulares_models import Celular  # Importa el modelo Celular definido con Pydantic (estructura del celular)

# definición de funciones (CRUD) <3 


# Crear un recurso
# POST --> Permite crear un celular a la base de datos
def crear_celular(celular: Celular):
    collection = database.get_collection('Celulares')
    celular_dict = celular.dict()  # Convierto el objeto Celular a un diccionario para que se pueda guardar en MongoDB
    insertar = collection.insert_one(celular_dict)  # Inserto ese diccionario en la colección
    return {"_id": str(insertar.inserted_id), "mensajes": "Celular insertado"}  # Retorno el ID del nuevo documento como string


# Leer un recurso específico
# GET --> Permite obtener un celular específico de la base de datos (por su ID)
def obtener_celulares_id(id: str):
    collection = database.get_collection('Celulares')
    try:
        cel_id = ObjectId(id)  # Aquí convierto el ID que recibo (que es un string) en un ObjectId, como los que usa MongoDB internamente
    except:
        return None
    Celular_id = collection.find_one({"_id": cel_id})  # Busco en la colección un celular cuyo _id coincida
    if Celular_id:
        return Celular(**Celular_id)  # Si lo encuentro, lo convierto en un objeto Celular usando doble asterisco (esto pasa cada campo como argumento)
    return None


# Leer todos los recursos
# GET --> Permite obtener todos los celulares de la base de datos (general)
def obtener_celulares():
    collection = database.get_collection('Celulares')
    celulares = list(collection.find({}, {"_id": 0}))  # Hago una búsqueda de todos los documentos, pero oculto el campo _id con {"_id": 0}
    return celulares


# Actualizar un recurso
# PUT --> Modifica los datos de un celular que ya creé.
def actualizar_celular(celular_id: str, celular: Celular):
    collection = database.get_collection('Celulares')
    update_celular = {}
    celular_dict = celular.dict()
    # Recorro cada campo del celular que me llega y solo agrego al diccionario de actualización los que no son None
    for llave, valor in celular_dict.items():
        if valor is not None:
            update_celular[llave] = valor
    if not update_celular:
        return {"mensajes": "Celular actualizado"}  # Si no hay campos para actualizar, simplemente devuelvo el mensaje
    # Aquí uso "$set" para decirle a MongoDB que solo actualice los campos que le paso, sin borrar los demás
    resultado = collection.update_one({"_id": ObjectId(celular_id)}, {"$set": update_celular})
    if resultado.modified_count == 0:
        return {"mensaje": "No se encontró el celular"}  # Si no se actualizó nada, puede ser que el ID no exista o que los datos sean iguales
    return {"mensajes": "Celular actualizado"}


# Eliminar un recurso
# DELETE --> Elimina el celular que ya existe
def eliminar_celular(celular_id: str):
    collection = database.get_collection('Celulares')
    try:
        celular_id = ObjectId(celular_id)  # Convierto el string recibido en ObjectId para que MongoDB lo entienda
    except:
        return None
    resultado = collection.delete_one({"_id": celular_id})  # Intento eliminar el documento con ese ID
    if resultado.deleted_count == 0:
        return {"mensajes": "No se encontró el celular"}  # Si no eliminó nada, es porque no lo encontró
    return {"mensajes": "Celular eliminado"}
