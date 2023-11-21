
"""
Created on Fri Nov 17 18:16:04 2023

@author: Bryan
"""

import time,os
from pymongo import MongoClient as mongo

client = mongo("mongodb://127.0.0.1:27017")
db = client["slamp_Bcruz"]
diccionario = db["Diccionario"]


#FUNCIONES ----------------------------------------------------------------------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
def obtener_siguiente_id():
    # Encuentra el último _id en la colección y agrega 1
    ultima_palabra = diccionario.find_one(sort=[("_id", -1)])
    if ultima_palabra:
        siguiente_id = ultima_palabra["_id"] + 1
    else:
        siguiente_id = 1  
    return siguiente_id

def agregar_palabra(palabra, significado):
    _id = obtener_siguiente_id()
    nueva_palabra = {
        "_id": _id,
        "Palabra": palabra,
        "Concepto": significado
        }
    diccionario.insert_one(nueva_palabra)
    print("Agregado con exito!")
    
def eliminar(palabra):
    result = diccionario.delete_one({"Palabra": palabra})
    if result.deleted_count > 0:
        print(f"Palabra  eliminada con éxito.")
    else:
        print(f"No se encontró {palabra} en la base de datos.")
        
def verificar_palabra(palabra):
    resultado = diccionario.find_one({"Palabra": palabra})
    if resultado:
        return 1
    else:
        return 0
    
def ver_listado_palabras():
    palabras= diccionario.find({}, {"Palabra": 1})
    print("\t\t\t LISTA DE PALABRAS \n\n")
    for palabra_doc in palabras:
        palabra = palabra_doc["Palabra"]
        print(f"\t{palabra}")

    # Esperar la entrada del usuario antes de regresar al menú
    input("Presiona enter para regresar al menú...")
    
def buscar(palabra):
    objeto = diccionario.find_one({"Palabra": palabra})
    if objeto:
        print(f"Palabra encontrada:")
        print(f"{'Palabra':<12}: {objeto['Palabra']}")
        print(f"{'Concepto':<12}: {objeto['Concepto']}")
    else:
        print(f"No se encontró '{palabra}' en la colección.")
        
def editar_concepto(palabra, nuevo_concepto):
    palabra_objeto = diccionario.find_one({"Palabra": palabra})
    if palabra_objeto:
        diccionario.update_one({"Palabra": palabra}, {"$set": {"Concepto": nuevo_concepto}})
        print(f"Concepto de '{palabra}' actualizado correctamente.")
    else:
        print(f"No se encontró '{palabra}' en la colección.")
#MENU ---------------------------------------------------------------------------


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
        palabra = input("Ingrese nueva palabra : ").upper()
        significado = input("concepto : ")
        agregar_palabra(palabra, significado)
    elif opcion == 'b':
           palabra=input("Ingrese la palabra a Editar : ").upper()
           nue_con=input("concepto : ")
           resultado = verificar_palabra(palabra)
           if resultado == 0:
               print("La palagra ingresada no se encuentra en la base de datos ..")
               time.sleep(2)
           else:
               editar_concepto(palabra, nue_con)
    elif opcion == 'c':
           delete=input("Ingrese la palabra a eliminar : ").upper()
           resultado = verificar_palabra(delete)
           if resultado == 0:
               print("La palagra ingresada no se encuentra en la base de datos ..")
               time.sleep(2)
           else:
               eliminar(delete)
    elif opcion == 'd':
           ver_listado_palabras()
    elif opcion == 'e':
           search=input("Ingrese la palabra a buscar : ").upper()
           resultado = verificar_palabra(search)
           if resultado == 0:
               print("La palagra ingresada no se encuentra en la base de datos ..")
               time.sleep(2)
           else:
               buscar(search)
               stop=input()
    elif opcion == 'f':
         print("Saliendo del diccionario. ¡Hasta luego!")
         break
    else:
         print("Opción no válida. Por favor, seleccione una opción válida.")
    
    