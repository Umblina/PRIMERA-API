from pymongo import MongoClient  # Se importa la clase MongoClient para conectarse a MongoDB


class Database:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://Lina:Umb2025*@micluster.os4w9.mongodb.net/?retryWrites=true&w=majority&appName=MiCluster",tlsallowinvalidcertificates=True) #El mismo cluster
        self.db = self.client ["LinaAPI"] # nombre de la BD que creé en Mongo :D y poder acceder a ella
        # tlsallowinvalidcertificates=True (truco que nos dió el profe) permite conexiones con certificados TLS no válidos 
       
    def get_collection(self, collection):
        return self.db[collection]
     # Método que recibe el nombre de una colección y devuelve una referencia a esa colección

    
database = Database()
# Se crea una instancia de la clase Database, que se importar y usar en cualquier parte del proyecto para acceder a la BD

      