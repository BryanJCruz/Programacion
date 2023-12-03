import time
import os
import redis

# Conexión a Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Funciones
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def obtener_siguiente_id():
    # Encuentra el último _id en la colección y agrega 1
    ultima_palabra = redis_client.get('ultima_palabra')
    if ultima_palabra:
        siguiente_id = int(ultima_palabra) + 1
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
    # Convertir el diccionario a cadena antes de almacenarlo en Redis
    redis_client.set(f'palabra:{_id}', str(nueva_palabra))
    redis_client.set('ultima_palabra', _id)
    print("Agregado con éxito!")

def eliminar(palabra):
    for key in redis_client.keys("palabra:*"):
        stored_palabra = eval(redis_client.get(key))
        if stored_palabra['Palabra'] == palabra:
            redis_client.delete(key)
            print(f"Palabra eliminada con éxito.")
            return
    print(f"No se encontró {palabra} en la base de datos.")

def verificar_palabra(palabra):
    for key in redis_client.keys("palabra:*"):
        stored_palabra = eval(redis_client.get(key))
        if stored_palabra['Palabra'] == palabra:
            return 1
    return 0

def ver_listado_palabras():
    print("\t\t\t LISTA DE PALABRAS \n\n")
    for key in redis_client.keys("palabra:*"):
        stored_palabra = eval(redis_client.get(key))
        palabra = stored_palabra['Palabra']
        print(f"\t{palabra}")
    # Esperar la entrada del usuario antes de regresar al menú
    input("Presiona enter para regresar al menú...")

def buscar(palabra):
    for key in redis_client.keys("palabra:*"):
        stored_palabra = eval(redis_client.get(key))
        if stored_palabra['Palabra'] == palabra:
            print(f"Palabra encontrada:")
            print(f"{'Palabra':<12}: {stored_palabra['Palabra']}")
            print(f"{'Concepto':<12}: {stored_palabra['Concepto']}")
            return
    print(f"No se encontró '{palabra}' en la base de datos.")

def editar_concepto(palabra, nuevo_concepto):
    for key in redis_client.keys("palabra:*"):
        stored_palabra = eval(redis_client.get(key))
        if stored_palabra['Palabra'] == palabra:
            stored_palabra['Concepto'] = nuevo_concepto
            # Convertir el diccionario a cadena antes de almacenarlo en Redis
            redis_client.set(key, str(stored_palabra))
            print(f"Concepto de '{palabra}' actualizado correctamente.")
            return
    print(f"No se encontró '{palabra}' en la base de datos.")

    
# Menú
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
        palabra = input("Ingrese la palabra a Editar : ").upper()
        nuevo_concepto = input("concepto : ")
        resultado = verificar_palabra(palabra)
        if resultado == 0:
            print("La palabra ingresada no se encuentra en la base de datos ..")
            time.sleep(2)
        else:
            editar_concepto(palabra, nuevo_concepto)
    elif opcion == 'c':
        palabra = input("Ingrese la palabra a eliminar : ").upper()
        resultado = verificar_palabra(palabra)
        if resultado == 0:
            print("La palabra ingresada no se encuentra en la base de datos ..")
            time.sleep(2)
        else:
            eliminar(palabra)
    elif opcion == 'd':
        ver_listado_palabras()
    elif opcion == 'e':
        search = input("Ingrese la palabra a buscar : ").upper()
        resultado = verificar_palabra(search)
        if resultado == 0:
            print("La palabra ingresada no se encuentra en la base de datos ..")
            time.sleep(2)
        else:
            buscar(search)
            stop = input()
    elif opcion == 'f':
        print("Saliendo del diccionario. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")