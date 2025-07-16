import praw
from credenciales import *
import pandas as pd


def coneccion():
    """
    Establece la conexión con Reddit usando PRAW (Python Reddit API Wrapper).
    Utiliza credenciales almacenadas para autenticación y verifica la conexión
    realizando una consulta de prueba al subreddit de Chile.
    
    Returns:
        praw.Reddit: Objeto Reddit conectado y autenticado
    """
    reddit = praw.Reddit(
        client_id     = a,     # id de la aplicacion
        client_secret = b,     # clave secreta
        user_agent    = c      # user agent
    )

    try:
        for post in reddit.subreddit("chile").hot(limit=1):
            break
        print("Conexión exitosa a Reddit")
    except Exception as e:
        print(f"No se pudo acceder a Reddit: {e}")
    return reddit

def datos_post(post):
    """
    Extrae todos los atributos relevantes de un post de Reddit para análisis sísmico.
    Recopila información estructurada incluyendo metadatos, contenido y estadísticas
    del post que serán procesados posteriormente para extraer datos de terremotos.
    
    Args:
        post (praw.models.Submission): Objeto post de Reddit a procesar
        
    Returns:
        dict: Diccionario con todos los atributos extraídos del post
    """
    datos = {
        "titulo": post.title,                       # Título del post
        "id": post.id,                              # ID del post
        "nombre_completo": post.name,               # Nombre completo 
        "url": post.url,                            # URL del post o del enlace compartido
        "enlace_interno_reddit": post.permalink,    # Enlace interno a Reddit
        "subreddit": post.subreddit.display_name,   # Subreddit al que pertenece
        "autor": post.author.name if post.author else None,  # Autor del post
        "puntuacion": post.score,                   # Número de votos
        "ratio_votos_positivos": post.upvote_ratio, # Ratio de votos positivos
        "num_comentarios": post.num_comments,       # Número de comentarios
        "fecha_creacion": post.created_utc,         # Fecha de creación 
        "flair": post.flair,                        # Flair del post (si tiene)
        "link_flair_text": post.link_flair_text,    # Texto del flair
        "editado": post.edited,                     # True si fue editado, o timestamp de edición
        "media": post.media,                        # Info sobre contenido multimedia 
        "thumbnail": post.thumbnail,                # URL de miniatura
        "num_crossposts": post.num_crossposts,      # Cuántas veces fue cruzado a otros subs
        "comentarios": post.comments,               # Lista de comentarios 
        "view_count": post.view_count,              # Vistas 
        "es_texto": post.is_self,                   # True si es texto, False si es enlace
        "nsfw": post.over_18,                       # NSFW o no
        "stickied": post.stickied,                  # Stickied o no (fijado por mods)
        "spoiler": post.spoiler,                    # Si es spoiler
        "locked": post.locked,                      # Si está bloqueado para comentar
        "distinguished": post.distinguished,        # Si fue marcado como oficial por mod/admin
        "texto_post": post.selftext                 # Texto 
    }

    return datos

import os

def guardar_fila_csv(diccionario, ruta_csv):
    """
    Guarda un diccionario como una nueva fila en un archivo CSV.
    Si el archivo no existe, lo crea con headers. Si existe, añade la fila sin headers.
    
    Args:
        diccionario (dict): Diccionario con los datos a guardar
        ruta_csv (str): Ruta del archivo CSV donde guardar los datos
    """
    df = pd.DataFrame([diccionario])
    if not os.path.exists(ruta_csv):
        df.to_csv(ruta_csv, mode='w', header=True, index=False)
    else:
        df.to_csv(ruta_csv, mode='a', header=False, index=False)


import prawcore 

def obtener_datos(subreddit, cantidad=15):
    """
    Extrae datos masivos de posts de Reddit sobre terremotos para análisis sísmico.
    Obtiene posts relevantes de subreddits especializados usando PRAW y los guarda
    en formato CSV para posterior procesamiento con IA y análisis de datos.
    
    Args:
        subreddit (praw.models.Subreddit): Instancia del subreddit para extraer datos
        cantidad (int): Número de posts a extraer (15 por defecto)
        
    Returns:
        None: Guarda los datos directamente en archivo CSV usando guardar_fila_csv()
    """
    try:
        archivo_csv = "data/datos_reddit.csv"
        if os.path.exists(archivo_csv):  # Limpia datos previos
            os.remove(archivo_csv)
        reddit = coneccion()
        subreddit_obj = reddit.subreddit(subreddit)
        
        posts = []
        for post in subreddit_obj.hot(limit=cantidad):
            datos = datos_post(post)
            posts.append(datos)
            guardar_fila_csv(datos, "data/datos_reddit.csv")  # Guarda cada post en CSV
        
        return posts
    
    except prawcore.exceptions.ResponseException as e:  # Error de respuesta Reddit API
        print(f"Error en la respuesta de Reddit API: {e.response.status_code} - {e.response.reason}")
    except prawcore.exceptions.RequestException as e:  # Error de solicitud Reddit API
        print(f"Error en la solicitud a Reddit API: {e}")
    except Exception as e:  # Error inesperado
        print(f"Error inesperado: {e}")
    
    return None

# obtener_datos("Earthquakes", 15) # good 