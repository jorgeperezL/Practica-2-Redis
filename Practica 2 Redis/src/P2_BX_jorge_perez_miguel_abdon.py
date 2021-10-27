'''
Created on 26 oct 2021

@author: jorge

'''
import redis
from pymongo import MongoClient
__author__ = 'jorge_perez y miguel_abdon'


class Model:
    """ Prototipo de la clase modelo
        Copiar y pegar tantas veces como modelos se deseen crear (cambiando
        el nombre Model, por la entidad correspondiente), o bien crear tantas
        clases como modelos se deseen que hereden de esta clase. Este segundo 
        metodo puede resultar mas compleja
    """
    required_vars = []
    admissible_vars = []
    dbmongo = None
    dbredis = None

    def __init__(self, **kwargs):      
        #for required in cls.required_vars:  
            #if required in kwargs:
                #self.__dict__.update(kwargs)
                #print("Coleccion creada")
            #else:
                #print("Coleccion no creada")      
        for required in self.required_vars:
            if not kwargs.get(required.lower()):
                print("Falta Campo requerido")
                return          
        self.__dict__.update(kwargs)

    def save(self):
        for required in self.required_vars:
            if self.__dict__.get(required.lower()) is None:
                print("Coleccion no guardada en base de datos")
                return
                       
        if self.db.find({"ref": self.ref}).count() > 0:
            self.db.update({"ref": self.ref}, self.__dict__)
            print("Se ha actualizado")
        else:
            self.db.insert_one(self.__dict__)
            print("Coleccion guardada en base de datos")

    def set(self, **kwargs):
        self.__dict__.update(kwargs)
    
    @classmethod
    def ind_by_id(cls, filter):
        """ Devuelve un cursor de modelos        
        """ 
        if not cls.dbredis.get(filter):
            documento = cls.db.find_one(filter)
            cls.dbredis.hmset(filter, documento, ex = 60)
            return documento
        else:
            documento = cls.dbredis.get(filter)
        return documento

        # cls es el puntero a la clase

    @classmethod
    def init_class(cls, dbmongo,dbredis, vars_path="model_name.vars"):
        """ Inicializa las variables de clase en la inicializacion del sistema.
        Argumentos:
            db (MongoClient) -- Conexion a la base de datos.
            vars_path (str) -- ruta al archivo con la definicion de variables
            del modelo.
        """      
        cls.dbmongo = dbmongo
        cls.dbredis = dbredis
        with open(vars_path) as f:
            mylist = f.read().splitlines() 
            cls.required_vars = mylist[0].split(" ")
            cls.admissible_vars = mylist[1].split(" ")
            #print(lines[0])     
            #required_vars = lines[0].split(" ")
            #admissible_vars = lines[1].split(" ")
            
            #print(required_vars)
            #print(admissible_vars)
            
class Persona(Model):
    pass

if __name__ == '__main__':
    client = MongoClient('localhost')
    redis = redis.Redis(host= 'localhost')
    client.p1
    Persona.init_class(client.p1.persona, redis, 'persona.txt')
    
    #redis.set('prueba', 'Hello from Python!', ex = 1)
    #value = redis.get('prueba')
    
