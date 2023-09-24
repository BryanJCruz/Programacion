import sqlite3
import os
import time
import sys

# Conexion con la BDD
conn = sqlite3.connect('slang_panameno.db')
cursor = conn.cursor()

# Creacion de la tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS palabras (
        palabra TEXT PRIMARY KEY,
        significado TEXT
    )
''')

conn.commit()

# Funciones para las opciones del menu, animaciones y limpieza de pantalla
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_animation():
    # Caracteres que forman la animacion
    animation_chars = ['|', '/', '-', '\\']
    tempo = 0
    while True:
        tempo = tempo + 1
        for char in animation_chars:
            sys.stdout.write('\rCargando ' + char)
            sys.stdout.flush()
            time.sleep(0.1)
        if tempo == 5:
            break

# Funciones para las opciones del menu
def add_word():
    word = input("Ingrese la nueva palabra: ")
    meaning = input("Ingrese el significado de la palabra: ")

    try:
        cursor.execute('INSERT INTO palabras VALUES (?, ?)', (word, meaning))
        conn.commit()
        print("Palabra agregada correctamente.")
    except sqlite3.IntegrityError:
        print("La palabra ya existe en la base de datos.")

def edit_word():
    word = input("Ingrese la palabra que desea editar: ")
    cursor.execute('SELECT * FROM palabras WHERE palabra=?', (word,))
    row = cursor.fetchone()
    if row:
        new_meaning = input("Ingrese el nuevo concepto: ")
        cursor.execute('UPDATE palabras SET significado=? WHERE palabra=?', (new_meaning, word))
        conn.commit()
        print("Editada correctamente.")
    else:
        print("La palabra no existe en la base de datos.")
        loading_animation()

def delete_word():
    word = input("Ingrese la palabra que desea eliminar: ")
    cursor.execute('SELECT * FROM palabras WHERE palabra=?', (word,))
    row = cursor.fetchone()
    if row:
        cursor.execute('DELETE FROM palabras WHERE palabra=?', (word,))
        conn.commit()
        print("Palabra eliminada correctamente.")
        loading_animation()
    else:
        print("La palabra no existe en la base de datos.")
        loading_animation()

def view_word_list():
    cursor.execute('SELECT * FROM palabras')
    words = cursor.fetchall()
    if words:
        clear_screen()
        print("\t\t\tListado de palabras y significados:")
        for word, meaning in words:
            print(f"{word}: {meaning}")
        input("\n\n\t\t Precione ENTER para continuar.....")
        loading_animation()
    else:
        print("No hay palabras en la base de datos.")
        input("\n\n\t\t Precione ENTER tecla para continuar.....")
        loading_animation()

def search_meaning():
    word = input("Ingrese la palabra que desea buscar: ")

    cursor.execute('SELECT * FROM palabras WHERE palabra=?', (word,))
    row = cursor.fetchone()

    if row:
        print(f"Significado de '{word}': {row[1]}")
        input("\n\n\t\t Precione ENTER tecla para continuar.....")
    else:
        print("La palabra no existe en la base de datos.")
        loading_animation()

# Menu de opciones
def show_menu():
    clear_screen()
    print("\t\t\t\t DICCIONARIO")
    print("\nOpciones:")
    print("\t\ta) Agregar nueva palabra")
    print("\t\tb) Editar palabra existente")
    print("\t\tc) Eliminar palabra existente")
    print("\t\td) Ver listado de palabras")
    print("\t\te) Buscar significado de palabra")
    print("\t\tf) Salir")

# Funcion principal
if __name__ == "__main__":
    while True:
        show_menu()
        option = input("Seleccione una opción: ").lower()

        if option == 'a':
            add_word()
        elif option == 'b':
            edit_word()
        elif option == 'c':
            delete_word()
        elif option == 'd':
            view_word_list()
        elif option == 'e':
            search_meaning()
        elif option == 'f':
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")
            loading_animation()

