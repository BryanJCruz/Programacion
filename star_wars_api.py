import requests


def obtener_planetas_aridos():
    url = "https://swapi.dev/api/planets/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        planetas_aridos = [
            {
                'name': planeta['name'],
                'films': len(planeta.get('films', []))
            }
            for planeta in data['results']
            if 'arid' in planeta.get('climate', '').lower()
        ]
        return planetas_aridos
    else:
        print(f"No se pudo obtener la información de los planetas. Código de respuesta: {response.status_code}")
        return None

def pregunta_a():
    planetas_aridos = obtener_planetas_aridos()
    print("\t\t ¿En cuántas películas aparecen planetas cuyo clima sea árido? ")
    if planetas_aridos:
        print("\t Información de planetas con clima árido:")
        total_peliculas = 0

        for planeta in planetas_aridos:
            nombre_planeta = planeta['name']
            peliculas = planeta['films']
            print(f"- {nombre_planeta}: {peliculas} película(s).")
            total_peliculas += peliculas

        print(f"\nTotal de películas con al menos un planeta con clima árido: {total_peliculas} película(s).")

def obtener_aeronave_mas_grande():
    url = "https://swapi.dev/api/starships/"
    nombre_aeronave = ''
    maximo_tamano = 0
    while url:
        response = requests.get(url)
        data = response.json()
        for nave in data['results']:
            if nave['length'] != 'unknown':
                tamano_nave = float(nave['length'].replace(',', ''))
                if tamano_nave > maximo_tamano:
                    maximo_tamano = tamano_nave
                    nombre_aeronave = nave['name']
        url = data['next']
    return nombre_aeronave

def obtener_wookies_en_pelicula(pelicula_url):
    response = requests.get(pelicula_url)
    data = response.json()
    contador_wookies = 0
    for personaje in data['characters']:
        respuesta_personaje = requests.get(personaje)
        data_personaje = respuesta_personaje.json()
        if data_personaje['species']:
            for especie in data_personaje['species']:
                if 'wookiee' in requests.get(especie).json()['name'].lower():
                    contador_wookies += 1
    return contador_wookies

def pregunta_B():
    print("\n\t\t ¿Cuántos Wookies aparecen en la sexta película?")
    print(f"Wookies en la sexta película: {obtener_wookies_en_pelicula('https://swapi.dev/api/films/3/')}")
def pregunta_c():
    print("\n\t\t ¿Cuál es el nombre de la aeronave más grande en toda la saga?")
    print(f"La aeronave más grande: {obtener_aeronave_mas_grande()}")
#impreciones
if __name__ == "__main__":
    pregunta_a()
    pregunta_B()
    pregunta_c()

