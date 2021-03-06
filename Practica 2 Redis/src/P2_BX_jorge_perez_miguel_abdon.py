import redis
from pymongo import MongoClient
from bson.objectid import ObjectId
import random 
import uuid

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
        if not self.__dict__.get('_id'):
            item_id = self.dbmongo.insert_one(self.__dict__).inserted_id
            self.__dict__.update(_id = item_id)
            self.dbredis.hmset(str(self._id),{'nombre':self.nombre,'apellido':self.apellido,'edad':self.edad,'ciudad':self.ciudad})
            self.dbredis.expire(str(self._id), 3600)
            f = open ("id.txt", "a")
            f.write(str(item_id)+"\n")
            f.close()
            print("Coleccion guardada en base de datos")
        else:
            self.dbmongo.update({"_id": self._id}, self.__dict__)
            self.dbredis.hmset(str(self._id),{'nombre':self.nombre,'apellido':self.apellido,'edad':self.edad,'ciudad':self.ciudad})
            print("Se ha actualizado")
            
            

    def set(self, **kwargs):
        self.__dict__.update(kwargs)
    
    @classmethod
    def find_by_id(cls, filter):
        """ Devuelve un cursor de modelos        
        """ 
        if not cls.dbredis.exists(str(filter)):
            documento = cls.dbmongo.find_one({"_id" : ObjectId(filter)})
            f = open ("id.txt", "a")
            f.write(str(documento.get('_id'))+"\n")
            f.close()
            cls.dbredis.hmset(str(documento.get('_id')), {'nombre':documento.get('nombre'),'apellido':documento.get('apellido')
            ,'edad':documento.get('edad'),'ciudad':documento.get('ciudad')})
            cls.dbredis.expire(str(documento.get('_id')), 3600)
            return documento
        else:
            documento = cls.dbredis.hmget(str(filter),'nombre','apellido','edad','ciudad')
            
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

personas = []

def insertar():
    nombre_in = input("Nombre: ")
    apellido_in = input("Apellido: ")
    edad_in = int(input("Edad: "))
    ciudad_in = input("Ciudad: ")
    
    persona = Persona(nombre = nombre_in, apellido = apellido_in, edad = edad_in, ciudad = ciudad_in)
    persona.save()
    
    personas.append(persona)

def actualizar():
    cont = 0
    for persona in personas:
        print(str(cont)+" - "+str(persona.__dict__))
        cont = cont + 1
        
    numeros = int(input("Introduce persona: "))
        
    diccionario = {}
    
    nombre_in = input("Nombre: ")
    if bool(nombre_in):
        diccionario['nombre'] = nombre_in
    apellido_in = input("Apellido: ")
    if bool(apellido_in):
        diccionario['apellido'] = apellido_in
    edad_in = input("Edad: ")
    if bool(edad_in):
        diccionario['edad'] = int(edad_in)
    ciudad_in = input("Ciudad: ")
    if bool(ciudad_in):
        diccionario['ciudad'] = ciudad_in
            
    personas[numeros].set(**diccionario)
    personas[numeros].save()
    
def menu_cache():
    semaforo = True
    while(semaforo):
        print("1-Insetar\n2-Actualizar\n3-Buscar\n4-Salir\n")
        
        opcion = int(input("Elige una opcion: "))
        
        if opcion == 1:
            insertar()
        elif opcion == 2:
            actualizar()
        elif opcion == 3:
            id_ = input("Introduce id: ") 
            documento = Persona.find_by_id(id_)
            print(documento)
        elif opcion == 4:
            semaforo = False
    

def ejemplos_cache():
    Persona(nombre = "Ana", apellido = "ligero", edad = 56, ciudad = "Madrid").save()
    Persona(nombre = "jorge", apellido = "perez", edad = 24 , ciudad = "Toledo").save()
    Persona(nombre = "Miguel", apellido = "Abdon",
    edad = 20, ciudad = "Madrid").save()
    Persona(nombre = "Laura", apellido = "diaz", edad = 23, ciudad = "Murcia").save()



credenciales = {}    
arrayToken = []



for x in range(100):  #genero 100 token
    token = str(uuid.uuid4())
    arrayToken.append(token) # meto 1 a 1 en el arrayToken



def introducirCredenciales():
     
    nombre = input("Nombre: ")
    apellido= input("Apellido: ")
    user = input("User: ")
    password = input("Password: ")
    print()
    privilegio=random.randrange(20)  #numero aleatorio del 0 al 19
    tokenEscogido = random.choice(arrayToken) 

    credenciales = {"nombre":nombre,"apellido":apellido,"user":user,"password":password,"privilegio":int(privilegio)}
    #redis.hmset(str(tokenEscogido),credenciales)
    resultado=redis.hmset(tokenEscogido, credenciales)
    redis.expire(tokenEscogido,2592000)
    print("\nPrivilegio: "+str(privilegio))
    print("Token: "+tokenEscogido)
    print()
     
    if(resultado==1):
        return {"tokenEscogido":tokenEscogido,"privilegio":privilegio}
    else:
        return -1

def buscarCredenciales():
     
     tokenBuscado = input("Introduce el token: ")
     print()

     privilegio=redis.hget(tokenBuscado,"privilegio")

     if(privilegio is not None):
          print(redis.hgetall(tokenBuscado))
          return privilegio
     else:
          return -1

def actualizarCredenciales(tokenn):

    if not redis.exists(tokenn):
        print("no existe ese token")
        return -1

    nombre = input("Nombre: ")
    apellido= input("Apellido: ")
    user = input("User: ")
    password = input("Password: ")

    credenciales = {"nombre":nombre,"apellido":apellido,"user":user,"password":password}
   
    redis.hmset(tokenn, credenciales)
    redis.expire(token,2592000)
    print(redis.hgetall(tokenn))

    return redis.hgetall(tokenn)

class HelpDesK:

    def funcionRegistar(self):
        user_id= input("pide usuario: ")
        redis.zadd("setPriority",{user_id:random.randrange(20)})
        #redis.zrange("setPriority",0,-1,withscores=True)

    def funcionUsuarios(self):
        #print(redis.bzpopmax("setPriority",timeout=0)[1])
        return redis.bzpopmax("setPriority",timeout=0)[1]
a=HelpDesK()

def menu_API():

    semaforo = True
    while(semaforo):

        print("1-Sesiones\n2-HelpDesk\n3-Salir\n")
        opcion = int(input("Elige una opcion: "))
        
         
        if opcion == 1:
          menu_API_Sesiones()
          pass
        elif opcion == 2:
          menu_API_HelpDesk()
          pass              
        elif opcion == 3:
          print(opcion)
          semaforo = False
          
          

def menu_API_Sesiones():

    semaforo = True
    while(semaforo):

        print("1-Introducir Credenciales\n2-Actualizar\n3-Buscar\n4-Salir\n")
        opcion = int(input("Elige una opcion: "))
        
         
        if opcion == 1:
          introducirCredenciales()
          pass
        elif opcion == 2:
          token = input("dime token: ")
          actualizarCredenciales(token)
          pass              
        elif opcion == 3:
          buscarCredenciales()
          pass
        elif opcion == 4:
          semaforo = False

def menu_API_HelpDesk():

    semaforo = True
    while(semaforo):

        print("1-Peticion\n2-Atencion\n3-Salir\n")
        opcion = int(input("Elige una opcion: "))
        
         
        if opcion == 1:
          a.funcionRegistar()
          pass
        elif opcion == 2:
          a.funcionUsuarios() 
          pass             
        elif opcion == 3:
          semaforo = False


if __name__ == '__main__':
    client = MongoClient('localhost')
    redis = redis.Redis(host= 'localhost',db = 0,decode_responses=True)
    redis.config_set('maxmemory','150mb')
    redis.config_set('maxmemory-policy','volatile-ttl')
    Persona.init_class(client.p1.persona, redis, 'persona.txt')
    ejemplos_cache()
    semaforo = True
    
    while(semaforo):

        print("1-Cache\n2-API\n3-Salir\n")
        opcion = int(input("Elige una opcion: "))
        
        while(semaforo):
            if opcion == 1:
                menu_cache()
            elif opcion == 2:
                menu_API()             #<----------------AQUI TU PARTE
            elif opcion == 3:
                semaforo = False
