from sqlalchemy import create_engine, text, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from getpass import getpass
import time,os



def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
def database_exists(user, password, host, port, database_name):
    try:
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}")
        engine.connect()
        return True
    except OperationalError as e:
        if "Unknown database" in str(e):
            return False
        else:
            raise

def create_database(user, password, host, port, new_database_name):
    try:
        # Crea el motor de la base de datos sin especificar la base de datos
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/")

        # Conecta al servidor MySQL
        connection = engine.connect()

        # Usa un objeto de instrucción SQL ejecutable
        stmt = text(f"CREATE DATABASE {new_database_name};")
        connection.execute(stmt)

        print(f"La base de datos '{new_database_name}' ha sido creada exitosamente.")

    except OperationalError as e:
        print(f"No se pudo crear la base de datos. Error: {e}")
    finally:
        if connection:
            connection.close()
            
Base = declarative_base()        
class Palabra(Base):
    __tablename__ = 'diccionario'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    palabras = Column(String(50))
    significado = Column(String(2000))

def create_table(user, password, host, port, database_name):
    try:
        # Crea el motor de la base de datos
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}")

        # Crea la tabla
        Base.metadata.create_all(engine)

        print("La tabla 'diccionario' ha sido creada exitosamente.")

    except Exception as e:
        print(f"No se pudo crear la tabla. Error: {e}")   
        
def agregar_palabra(session):
    palabra=input("Ingrese la palabra : ")
    concepto=input("Contexto de la palabra : ")
    nueva_palabra=Palabra(palabras=palabra,significado=concepto)
    session.add(nueva_palabra)
    session.commit()

def editar_palabra(session):
    try:
        identificador = int(input("Búsqueda por ID : "))
    except:
        identificador = 0
    selected_palabra = session.query(Palabra).filter_by(id=identificador).first()
    if selected_palabra is not None:
        print("DATO seleccionado: " + selected_palabra.palabras)
        act_pa=input("Nuevo Nombre de la palabra : ")
        act_sig=input("Nuevo significado : ")
        selected_palabra.palabras=act_pa
        selected_palabra.significado=act_sig
        session.commit()
    else:
        print("El ID ingresado no se encuentra en la base de datos ...")
        time.sleep(1)

def eliminar_palabra(session):
    try:
        identificador = int(input("Búsqueda por ID : "))
    except:
        identificador = 0
    selected_palabra = session.query(Palabra).filter_by(id=identificador).first()
    if selected_palabra is not None:
        print("\n\t Desea eliminarlo ? ")
        print("1-SI")
        print("2-NO")
        try:
            op=int(input("Seleccione : "))
        except:
            op = 2
        match op:
            case 1:
                session.delete(selected_palabra)
                session.commit()
                print("Palabra eliminada")
                time.sleep(2)
            case 2:
                print("Cancelando...")
                time.sleep(0.5)
    else:
        print("El ID ingresado no se encuentra en la base de datos ...")
        time.sleep(1)

def ver_listado_palabras(session):
    clear_screen()
    palabras = session.query(Palabra).all()
    if palabras:
        print("\t\t\t LISTA DE PALABRAS \n\n")
        for palabra in palabras:
            print(f"\t{palabra.palabras}")
        stop = input("Presiona enter para regresar al menú...")
    else:
        print("El diccionario está vacío.")
        time.sleep(3)
        
        

def buscar_significado(session):
    palabra_a_buscar = input("Ingrese la palabra en mayúsculas que desea buscar: ").upper()

    # Realiza una consulta insensible a mayúsculas y minúsculas
    palabra = session.query(Palabra).filter(Palabra.palabras.ilike(palabra_a_buscar)).first()

    if palabra:
        print(f"Significado de '{palabra.palabras}': {palabra.significado}")
        stop=input("\n\n presione enter para continuar...")
    else:
        print(f"La palabra '{palabra_a_buscar}' no existe en el diccionario.")  
        time.sleep(2)
            
def menu():
    while True:
        clear_screen()
        print("DICCIONARIO")
        print("Opciones:")
        print("    a) Agregar nueva palabra")
        print("    b) Editar palabra existente")
        print("    c) Eliminar palabra existente")
        print("    d) Ver listado de palabras")
        print("    e) Buscar significado de palabra")
        print("    f) Salir")
        try:
           opcion = input("Seleccione una opción: ").lower()
        except:
           opcion = 'g'
        if opcion == 'a':
           agregar_palabra(session)
        elif opcion == 'b':
           editar_palabra(session)
        elif opcion == 'c':
           eliminar_palabra(session)
        elif opcion == 'd':
           ver_listado_palabras(session)
        elif opcion == 'e':
           buscar_significado(session)
        elif opcion == 'f':
           print("Saliendo del diccionario. ¡Hasta luego!")
           break
        else:
           print("Opción no válida. Por favor, seleccione una opción válida.")

# CREDENCIALES
clear_screen()
print("\t\t INICIO ")
print("\n |Ingrese las credenciales para la conexcion con mysql|")
Usuario = input("Usuario: ")
password = getpass("Contraseña: ")
nombre_de_la_base_de_datos = 'slamp'
host = 'localhost'  
puerto = 3306 



# CONFIRMACION Y CREACION
if database_exists(Usuario, password, host, puerto, nombre_de_la_base_de_datos):
    print(f"La base de datos '{nombre_de_la_base_de_datos}' existe.")
    time.sleep(1)
    print("INICIANCO CONEXION")
    time.sleep(1)
    engine = create_engine(f"mysql+pymysql://{Usuario}:{password}@{host}:{puerto}/{nombre_de_la_base_de_datos}")
    Session = sessionmaker(bind=engine)
    session = Session()
    menu()
    
else:
    print(f"La base de datos '{nombre_de_la_base_de_datos}' no existe.")
    time.sleep(1)
    clear_screen()
    print("CREANDO BASE DE DATOS")
    create_database(Usuario, password, host, puerto, nombre_de_la_base_de_datos)
    clear_screen()
    print("BASE DE DATOS CREADA CON EXITO ")
    time.sleep(1)
    print("CREANDO TABLAS")
    create_table(Usuario, password, host, puerto, nombre_de_la_base_de_datos)
    time.sleep(1)
    print("INICIANDO CONEXION")
    time.sleep(1)
    engine = create_engine(f"mysql+pymysql://{Usuario}:{password}@{host}:{puerto}/{nombre_de_la_base_de_datos}")
    Session = sessionmaker(bind=engine)
    session = Session()
    menu()
    
    
