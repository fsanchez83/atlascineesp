# atlascineesp

Proyecto para crear un atlas del cine español a partir de los datos de TMDB, 
extrayendo la información a partir de su API.

Consta de 2 scripts.

- recuperaPeliculas.py recupera de la API, junto con su información básica, todas las 
  películas entre cuyos países de origen figura España. Esta información se guarda en 
  el archivo movie_data.csv.
- datasetEnriquecido.py coge una a una las películas de movie_data.csv y da 
  preguntando a la API de TMDB para sacar toda la información disponible, desde los 
  equipos técnicos y artísticos hasta otros datos como presupuesto, ganancia, resumen, 
  etc. Hay que tener en cuenta que no toda la información está completa, por lo que 
  algunos campos de ciertas películas se guardan vacíos. Todo esto se guarda en el 
  archivo dataset_pelis.csv


Se ha ampliado el proyecto para los cines chinos (China, Hong Kong, Taiwán, Macao). Para ello se incluyen en el proyectos los datasets correspondientes, pero no el pbix, dado que es análogo al del cine español.