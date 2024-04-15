# PROYECTO INDIVIDUAL Nº1
## Machine Learning Operations (MLOps)

El objetivo de este proyecto es crear un sistema de recomendación de videojuegos para usuarios, desarrollando un modelo de MAchine Learning. Este repositorio contiene los recursos necesarios para implementarlo.
El proyecto abarcará los siguientes puntos:

### Transformaciones:
Se realizaron transformaciones de datos JSON para facilitar la manipulación y análisis de la información. Se eliminaron algunas columnas para responder las consultas y preparar los modelos de aprendizaje automático

### Feature Engineering: 
Se creo la columna 'sentiment_analysis' a partir del dataset user_reviews, reemplazando la columna user_reviews.review y aplicando análisis de sentimiento con NLP con la escala: 0 -> malo, 1 -> neutral y 2 -> positivo. Esta nueva columna debe reemplazar la de user_reviews.review para facilitar el trabajo de los modelos de machine learning y el análisis de datos. 

### Desarrollo API:  
Se ha implementado una API utilizando FastAPI. Las funciones, decoradores y consultas son las siguientes:

#1 developer
@app.get('/developer/{desarrollador}')
def developer(desarrollador):
    '''
    ÇONSIGNA:
    def developer( desarrollador : str )
    Cantidad de items y 
    porcentaje de contenido Free por año según empresa desarrolladora. 
    Ejemplo de retorno:
    Año     Cantidad de Items   Contenido Free
    2022    45                  25%
    2023    50                  27%
    xxxx    xx                  xx%
    '''

#2 userdata
@app.get('/userdata/{user_id}')
def userdata(user_id: str):
    '''   
    Debe devolver cantidad de dinero gastado por el usuario, 
    el porcentaje de recomendación en base a reviews.recommend 
    y cantidad de items.
    Ejemplo de retorno: 
    {"Usuario X" : us213ndjss09sdf, 
    "Dinero gastado": 200 USD, 
    "% de recomendación": 20%, 
    "cantidad de items": 5
    }  
    '''

#3 UserForGenre
@app.get('/UserForGenre/{genero}')
def UserForGenre(genero:str):
    """
    CONSIGNA:
    def UserForGenre( genero : str ): Debe devolver el 
    usuario que acumula más horas jugadas para el género dado y
    una lista de la acumulación de horas jugadas por año de lanzamiento.
    Ejemplo de retorno: 
    {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, 
    "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]
    }
    """

#4 best_developer_year
@app.get('/best_developer_year/{year}')   
def best_developer_year(year: int):
    """
    CONSIGNA:
    def best_developer_year( año : int ): 
    Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. 
    (reviews.recommend = True y comentarios positivos)
    Ejemplo de retorno:  
    [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
    """

#5 developer_reviews_analysis
@app.get('/developer_reviews_analysis/{desarrolladora}') 
def developer_reviews_analysis(desarrolladora:str):
    """
    CONSIGNA:
    def developer_reviews_analysis( desarrolladora : str ): 
    Según el desarrollador, se devuelve 
    un diccionario con el nombre del desarrollador como llave y 
    una lista con la cantidad total de registros de reseñas de usuarios 
    que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.
    Ejemplo de retorno: 
    {'Valve' : [Negative = 182, Positive = 278]}
    """

### Deployment: 
Para que la API pueda ser consumida desde la web se utilizó Render. Y para su implementación lo más importante son los archivos main.py, requirements.txt (contiene las librerías para que la API funcione correctamente) y los que contienen los datasets. El archivo .gitignore se utiliza para indicarle a Git que archivos o carpetas ignorar.

### Análisis exploratorio de los datos: 
Con los datos transformados y cargados se realizó un análisis exploratorio para comprender un poco más las características y patrones de los datos.Se emplearon gráficos y visualizaciones como nubes de palabras, las cuales dieron una buena idea de cuáles palabras son más frecuentes. 

### Modelo de aprendizaje automático:
Se eligió la propuesta para el sistema de recomendación con el modelo teniendo una relación ítem-ítem (se toma un item, en base a que tan similar es ese ítem al resto, se recomiendan similares). 

#6 recomendacion_juego
@app.get('/recomendacion_juego/{id_de_producto}')
def recomendacion_juego(id_de_producto: str):
    '''
    CONSIGNA
    def recomendacion_juego( id_de_producto ): 
    Ingresando el id de producto, deberíamos recibir 
    una lista con 5 juegos recomendados similares al ingresado.
    '''

### Video: 
El video muestra el resultado de las consultas requeridas y fue realizado utilizando la herramienta Zoom.  
