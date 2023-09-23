import sqlite3
import os
import time
import sys

# conexion con la BDD
conn = sqlite3.connect('slang_panameno.db')
cursor = conn.cursor()

#
cursor.execute('''
    CREATE TABLE IF NOT EXISTS palabras (
        palabra TEXT PRIMARY KEY,
        significado TEXT
    )
''')

conn.commit()

# funciones para las opciones del menú , animaciones y limpiesa de pantalla
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def animacion_carga():
    # Caracteres que forman la animación
    animacion_chars = ['|', '/', '-', '\\']
    tempo = 0
    while True:
        tempo=tempo+1
        for char in animacion_chars:
            sys.stdout.write('\rCargando ' + char)
            sys.stdout.flush()
            time.sleep(0.1)
        if tempo == 5:
            break
def agregar_palabra():
    palabra = input("Ingrese la nueva palabra: ")
    significado = input("Ingrese el significado de la palabra: ")

    try:
        cursor.execute('INSERT INTO palabras VALUES (?, ?)', (palabra, significado))
        conn.commit()
        print("Palabra agregada correctamente.")
    except sqlite3.IntegrityError:
        print("La palabra ya existe en la base de datos.")
def editar_palabra():
    palabra = input("Ingrese la palabra que desea editar: ")
    cursor.execute('SELECT * FROM palabras WHERE palabra=?', (palabra,))
    row = cursor.fetchone()
    if row:
        nuevo_significado = input("Ingrese el nuevo significado de la palabra: ")
        cursor.execute('UPDATE palabras SET significado=? WHERE palabra=?', (nuevo_significado, palabra))
        conn.commit()
        print("Palabra editada correctamente.")
    else:
        print("La palabra no existe en la base de datos.")
def eliminar_palabra():
    palabra = input("Ingrese la palabra que desea eliminar: ")
    cursor.execute('SELECT * FROM palabras WHERE palabra=?', (palabra,))
    row = cursor.fetchone()
    if row:
        cursor.execute('DELETE FROM palabras WHERE palabra=?', (palabra,))
        conn.commit()
        print("Palabra eliminada correctamente.")
    else:
        print("La palabra no existe en la base de datos.")
def ver_listado_palabras():
    cursor.execute('SELECT * FROM palabras')
    palabras = cursor.fetchall()
    if palabras:
        limpiar_pantalla()
        print("\t\t\tListado de palabras y significados:")
        for palabra, significado in palabras:
            print(f"{palabra}: {significado}")
        input("\n\n\t\t Precione ENTER para continuar.....")
        animacion_carga()
    else:
        print("No hay palabras en la base de datos.")
        input("\n\n\t\t Precione ENTER tecla para continuar.....")
        animacion_carga()
def buscar_significado():
    palabra = input("Ingrese la palabra que desea buscar: ")

    cursor.execute('SELECT * FROM palabras WHERE palabra=?', (palabra,))
    row = cursor.fetchone()

    if row:
        print(f"Significado de '{palabra}': {row[1]}")
        input("\n\n\t\t Precione ENTER tecla para continuar.....")
    else:
        print("La palabra no existe en la base de datos.")
        animacion_carga()


# Menú de opciones

def mostrar_menu():
    limpiar_pantalla()
    print("\t\t\t\t DICCIONARIO")
    print("\nOpciones:")
    print("\t\ta) Agregar nueva palabra")
    print("\t\tb) Editar palabra existente")
    print("\t\tc) Eliminar palabra existente")
    print("\t\td) Ver listado de palabras")
    print("\t\te) Buscar significado de palabra")
    print("\t\tf) Salir")



# Función principal
if __name__ == "__main__":
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").lower()

        if opcion == 'a':
            agregar_palabra()
        elif opcion == 'b':
            editar_palabra()
        elif opcion == 'c':
            eliminar_palabra()
        elif opcion == 'd':
            ver_listado_palabras()
        elif opcion == 'e':
            buscar_significado()
        elif opcion == 'f':
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")
            animacion_carga()

