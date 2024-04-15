# Importaciones
from fastapi import FastAPI
import pandas as pd

# leer archivos a utilizar

df_reviews = pd.read_parquet('3450e.parquet')
df_gastos_items = pd.read_parquet('3420b.parquet')
item_sim_df = pd.read_parquet('5110item_sim_df.parquet')

df_items_developer = pd.read_parquet('3410a.parquet')
df_generos=pd.read_parquet('3430c.parquet')

# tomar muestra 10%

df_reviews= df_reviews.sample(frac=0.1,random_state=42)
item_sim_df= item_sim_df.sample(frac=0.1,random_state=42)

df_generos= df_generos.sample(frac=0.1,random_state=42)

# instanciar
app = FastAPI()

# http://127.0.0.1:8000


@app.get("/")
def index():
    return "agregar: /docs y se podrá ingresar a cada una de las opciones "

#1 developer
@app.get('/developer/{desarrollador}')
def developer(desarrollador):
    '''
    ÇONSIGNA:
    def developer( desarrollador : str )
    Cantidad de items y 
    porcentaje de contenido Free por año según empresa desarrolladora. 
    Ejemplo de retorno:
    Año	    Cantidad de Items	Contenido Free
    2022    45	                25%
    2023    50	                27%
    xxxx    xx	                xx%
    '''
    # filtrar dataframe
    data_filtrada = df_items_developer[df_items_developer['developer'] == desarrollador]
    # Calcula la cantidad de items por año
    cantidad_por_año = data_filtrada.groupby('año_lanzamiento')['item_id'].count()
    # Calcula la cantidad de elementos gratis por año
    cantidad_gratis_por_año = data_filtrada[data_filtrada['price'] == 0.0].groupby('año_lanzamiento')['item_id'].count()
    # Calcula el porcentaje de elementos gratis por año
    porcentaje_gratis_por_año = (cantidad_gratis_por_año / cantidad_por_año * 100).fillna(0).astype(int)

    return {
        'cantidad_items_por_año': cantidad_por_año.to_dict(),
        'porcentaje_gratis_por_año': porcentaje_gratis_por_año.to_dict()
    }
    



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
    
    # filtrar dataframe
    cantidad_dinero = df_gastos_items[df_gastos_items['user_id']== user_id]['price'].iloc[0]
    
    # filtrar dataframe
    usuario = df_reviews[df_reviews['user_id'] == user_id]
    # contabilizar recomendaciones
    total_recomendaciones = usuario['reviews_recommend'].sum()
    # calcular el total de reviews realizada por todos los usuarios
    total_reviews = len(df_reviews['user_id'].unique())
    # calcular el porcentaje de recomendaciones realizadas por el usuario de interés
    porcentaje_recomendaciones = (total_recomendaciones / total_reviews) * 100
    
    # contabilizar la cantidad de items para el usuario de interés    
    count_items = df_gastos_items[df_gastos_items['user_id']== user_id]['items_count'].iloc[0]
    
    return {
        'usuario': user_id,
        'dinero gastado': int(cantidad_dinero),
        'porcentaje de recomendación': round(float(porcentaje_recomendaciones), 2),
        'cantidad de items': int(count_items)
    }

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
    try:
        if genero.lower() not in [x.lower() for x in df_generos['Género'].tolist()]:
            return "No se encontró ese genero"
        
        gen = df_generos[df_generos['Género'].str.lower() == genero.lower()] # Busco el genero especificado
        
        return { 
            'Usuario':gen['Usuario'].tolist(),
            'Horas jugadas':gen['Año_Horas'].tolist()
        }
    except Exception as e:
        return {"Error":str(e)}
    
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
    try:  
        # Carga los datos de los juegos de steam
        df_games = pd.read_csv('231_osg.csv')
        # Tomo solo un 10% de mi df:
        df_games= df_games.sample(frac=0.1,random_state=42)
        # Carga las revisiones de los usuarios
        df_reviews = pd.read_csv('232_aur.csv')
        # Tomo solo un 10% de mi df:
        df_reviews= df_reviews.sample(frac=0.1,random_state=42)
        # Elimino columnas que nos seran necesarias en el estudio
        df_games=df_games.drop(['publisher','title','early_access'],axis=1)
        # Elimina las filas con valores faltantes en los datos de los juegos
        df_games.dropna(inplace =True)
        # Convierte el año de lanzamiento,user_id,id a int
        df_games['año_lanzamiento'] = df_games['año_lanzamiento'].astype(int)
        df_games['id'] = df_games['id'].astype(int)
        df_reviews['reviews_item_id'] = df_reviews['reviews_item_id'].astype(int)
        # Une los datos de los juegos y las revisiones en 'id'
        func_4 = pd.merge(df_reviews,df_games,left_on='reviews_item_id',right_on='id',how='inner')
        # Filtra los datos para obtener solo los juegos lanzados en el año dado
        func_4 = func_4[func_4['año_lanzamiento'] == year]
        # Agrupa los datos por desarrollador 
        mejores_dev = func_4.groupby('developer')['reviews_recommend'].sum().reset_index().sort_values(by='reviews_recommend',ascending=False)
        # Verifica si no se encontraron desarrolladores con revisiones en ese año.
        if mejores_dev.empty:
            return 'No se encontraron reviews para items que hayan salido ese año'
        else:
            # Obtiene los tres primeros desarrolladores con más recomendaciones
            puesto1 = mejores_dev.iloc[0][0]
            puesto2 = mejores_dev.iloc[1][0]
            puesto3 = mejores_dev.iloc[2][0]
            puestos = {"Puesto 1": str(puesto1), "Puesto 2":str(puesto2), "Puesto 3": str(puesto3)}
            # Devuelve los tres primeros desarrolladores con más recomendaciones
            return puestos
    except Exception as e:
        return {"Error":str(e)}
    
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
    try:
        # Carga los datos de los juegos de steam
        df_games = pd.read_csv('231_osg.csv')
        # Tomo solo un 10% de mi df:
        df_games= df_games.sample(frac=0.1,random_state=42)
        # Carga las revisiones de los usuarios
        df_reviews = pd.read_csv('345e.csv')
        # Tomo solo un 10% de mi df:
        df_reviews= df_reviews.sample(frac=0.1,random_state=42)
        df_games['id'] = df_games['id'].astype(int)
        df_reviews['reviews_item_id'] = df_reviews['reviews_item_id'].astype(int)
        # Merging los dos datasets, con una combinación interna en sus respectivos 'id'
        func_5 = pd.merge(df_reviews,df_games,left_on='reviews_item_id',right_on='id',how='inner')
        # Convertir todos los nombres de los desarrolladores en letras minúsculas para evitar la duplicación de datos debido a las diferencias de mayúsculas y minúsculas
        func_5['developer'] = func_5['developer'].str.lower()

        # Convertir el nombre del desarrollador proporcionado en letras minúsculas
        desarrolladora2 = desarrolladora.lower()
        # Filtrar por desarrollador
        func_5 = func_5[func_5['developer'] == desarrolladora2]
        # Verificar si se encuentra los juegos del desarrollador en el dataset
        if func_5.empty:
            # En caso de que no se encuentre, se muestra mensaje indicando que no hay comentarios para este desarrollador
            return 'No se encontraron reviews para ese desarrollador'
        # En caso contrario, contar los sentimientos de análisis de comentarios
        # Cuenta los comentarios positivos
        true_value = func_5[func_5['sentiment_analysis']==2]['sentiment_analysis'].count()
        # Cuenta los comentarios negativos
        false_value = func_5[func_5['sentiment_analysis']==0]['sentiment_analysis'].count()
        # Devolver conteos en un diccionario
        return {desarrolladora2:[f'Negative = {int(false_value)}',f'Positive = {int(true_value)}']}
    except Exception as e:
        return {"Error":str(e)}
    
#6 recomendacion_juego
@app.get('/recomendacion_juego/{id_de_producto}')
def recomendacion_juego(id_de_producto: str):
    '''
    CONSIGNA
    def recomendacion_juego( id_de_producto ): 
    Ingresando el id de producto, deberíamos recibir 
    una lista con 5 juegos recomendados similares al ingresado.
    '''
    # Obtener lista de juegos similares ordenados
    similar_games = item_sim_df.sort_values(by=id_de_producto, ascending=False).iloc[1:6]

    count = 1
    contador = 1
    recomendaciones = {}
    
    for item in similar_games:
        if contador <= 5:
            item = str(item)
            recomendaciones[count] = item
            count += 1
            contador += 1 
        else:
            break
    return recomendaciones