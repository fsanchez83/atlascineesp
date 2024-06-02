import requests
import csv
import yaml
from yaml.loader import SafeLoader
import sys

with open('secrets.cfg') as f:
    secrets = yaml.load(f, Loader=SafeLoader)

with open('config.cfg') as c:
    dataConfig = yaml.load(c, Loader=SafeLoader)

headers = {
    "accept": "application/json",
    "Authorization": "Bearer "+secrets['TMDB']['BEARER']
}

date_in = dataConfig['Fechas']['date_in']
date_fin = dataConfig['Fechas']['date_fin']

def get_movie_data(page, date_in, date_fin, pais):
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false" \
          f"&include_video=true&page={page}&primary_release_date.gte=" \
          f"{date_in}&primary_release_date.lte={date_fin}&sort_by=primary_release_date" \
          f".asc&with_origin_country={pais}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data.get('results', [])

def save_to_csv(movie_data, filename):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "id", "genre_ids", "original_language", "original_title", "overview",
            "popularity", "poster_path", "release_date", "title", "video",
            "vote_average", "vote_count", "backdrop_path", "adult"
        ], delimiter=';')
        if file.tell() == 0:  # Verifica si el archivo está vacío
            writer.writeheader()
        for movie in movie_data:
            # Convertimos los géneros a una cadena separada por comas
            movie['genre_ids'] = ','.join(map(str, movie['genre_ids']))
            movie['overview'] = movie['overview'].replace('\n', ' ').replace('\r', ' ')
            writer.writerow(movie)

def main():
    filename = dataConfig['Resultados']['filename_lista']
    pais = dataConfig['Filtros']['pais']
    #for page in range(1, 3):  # Itera sobre las páginas de la API. MAXIMO, 500 PAGINAS
    for page in range(1, 501):  # Itera sobre las páginas de la API
        movie_data = get_movie_data(page, date_in, date_fin, pais)
        if movie_data:
            save_to_csv(movie_data, filename)
            #print(f"Guardando datos de la página {page} en {filename}")
            print(page)

if __name__ == "__main__":
    main()
