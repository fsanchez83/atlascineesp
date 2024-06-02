'''
Created on 30 abr. 2020

@author: fsanchez
'''
# -*- coding: utf-8 -*-

import tmdbsimple as tmdb
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import sys
import os.path

with open('secrets.cfg') as f:
    secrets = yaml.load(f, Loader=SafeLoader)

tmdb.API_KEY = secrets['TMDB']['API_KEY']

# Leer la lista básica de pelis

lista_con_id = pd.read_csv('movie_data_chinas.csv', sep=';')

Atributos_peli = ["tmdb_id", "Titulo", "Popularidad", 'Rating', 'Fecha', 'Duracion', 'Pais', 'Idioma',
                  'Presupuesto', 'Ganancia', 'Generos', 'Director', 'Director_genre',
                  'Casting', 'Guion', 'Montaje', 'DOP', 'Resumen', 'Productoras',
                  'Paises productores']
df_films = pd.DataFrame(columns=Atributos_peli)

search = tmdb.Search()

dataset_inicial = pd.read_csv('dataset_pelis_chinas.csv', sep=';')

dataset_nuevas = pd.merge(dataset_inicial,lista_con_id,left_on=['tmdb_id'],
                          right_on=['id'],how="outer",indicator=True)
dataset_nuevas = dataset_nuevas[dataset_nuevas['_merge'] == 'right_only']
dataset_nuevas_pelis = dataset_nuevas.copy()
dataset_nuevas_pelis = dataset_nuevas_pelis.rename(columns={"Name_x": "Name","tmdb_type_y":"tmdb_type","Rating_y": "Rating"})
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pelis_con_error = []

print("")
print("EXTRAE DATOS NUEVAS PELIS:")

for index, row in dataset_nuevas_pelis.iterrows():
    print(str(index)+": "+row['original_title'])
    tmdb_id = row['id']
    try:
        movie = tmdb.Movies(tmdb_id)
        movieInfo = movie.info()
        id_peli = tmdb_id
        titulo = movieInfo['title']
        popularidad = movieInfo['popularity']
        rating = movieInfo['vote_average']
        fecha = movieInfo['release_date']
        duracion = movieInfo['runtime']
        idioma = movieInfo['original_language']

        presupuesto = movieInfo['budget']
        ganancia = movieInfo['revenue']
        resumen = movieInfo['overview'].replace('\n', ' ').replace('\r', ' ')
        generos = []
        emp_productoras = []
        paises_productores = []
        pais = movieInfo['origin_country']

        for dic in movieInfo['genres']:
            generos.append(dic['name'])
        for dic in movieInfo['production_companies']:
            emp_productoras.append(dic['name']+"--"+dic['origin_country'])
        for dic in movieInfo['production_countries']:
            paises_productores.append(dic['name'])

        director = []
        director_genre = []
        guion = []
        montaje = []
        dop = []
        casting = []

        creditos = movie.credits()
        for dic in creditos['crew']:
            if dic['job'] == 'Director':
                director.append(dic['name'])
                director_genre.append(dic['gender'])
            if dic['job'] == 'Screenplay':
                guion.append(dic['name'])
            if dic['job'] == 'Editor':
                montaje.append(dic['name'])
            if dic['job'] == 'Director of Photography':
                dop.append(dic['name'])

        for dic in creditos['cast']:
            casting.append(dic['name'])

        lista_peli = [tmdb_id, titulo, popularidad, rating, fecha, duracion, pais, idioma,
                      presupuesto, ganancia, generos, director, director_genre,
                      casting, guion, montaje, dop, resumen, emp_productoras,
                      paises_productores]


        df_tamanio = len(dataset_inicial)
        dataset_inicial.loc[df_tamanio] = lista_peli

    except:
        print("Error en el nombre")
        pelis_con_error.append(row['original_title'])

dataset_inicial.to_csv('dataset_pelis_chinas.csv', sep=';', index=False)

df_pelis_con_error = pd.DataFrame(pelis_con_error, columns=['titulo'])
df_pelis_con_error.to_csv('pelis_con_error_chinas.csv', sep=';', index=False)

print('FIN')
