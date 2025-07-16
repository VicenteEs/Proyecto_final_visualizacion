import pandas as pd
import time 
import google.generativeai as genai
import os
import datetime
import numpy as np
import re
from credenciales import *

gemini_keys = [d]
genai.configure(api_key=gemini_keys[0])

def load_data_reddit():
    """
    Carga y procesa datos de terremotos desde un archivo CSV de Reddit.
    Maneja conversión de timestamps Unix y strings de fecha, extrae información
    temporal del contenido de los posts y normaliza formatos de fecha/hora.
    
    Returns:
        pandas.DataFrame: DataFrame con datos de Reddit procesados y columnas
                         de fecha/hora normalizadas
                         
    Raises:
        FileNotFoundError: Si el archivo datos_reddit.csv no existe
    """
    file_path = os.path.join(os.getcwd(), "data", "datos_reddit.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        
        df["fecha_creacion_dt"] = pd.NaT  # Crear una nueva columna para evitar el warning de tipos incompatibles
        
        try:
            df_temp = df.copy()  # Primero intentar convertir como timestamp Unix (números)
            df_temp["fecha_num"] = pd.to_numeric(df["fecha_creacion"], errors="coerce")
            
            mask_timestamp = df_temp["fecha_num"].notna()  # Crear máscara para identificar qué valores son timestamps
            
            if mask_timestamp.any():  # Convertir timestamps a datetime
                fechas_timestamp = pd.to_datetime(
                    df_temp.loc[mask_timestamp, "fecha_num"], 
                    unit='s',
                    utc=True
                ).dt.tz_localize(None)  # Convertir a tz-naive
                df.loc[mask_timestamp, "fecha_creacion_dt"] = fechas_timestamp
            
            if (~mask_timestamp).any():  # Para los que no son timestamps, intentar parsear como fecha
                fechas_string = pd.to_datetime(
                    df.loc[~mask_timestamp, "fecha_creacion"],
                    errors="coerce",
                    format="mixed"
                )
                df.loc[~mask_timestamp, "fecha_creacion_dt"] = fechas_string
            
            df["fecha_creacion"] = df["fecha_creacion_dt"]  # Reemplazar la columna original
            df = df.drop(columns=["fecha_creacion_dt"])
            
        except Exception as e:
            print(f"Error al procesar fechas: {e}")
            df["fecha_creacion"] = pd.to_datetime(df["fecha_creacion"], errors="coerce")  # Si falla, intentar conversión directa
        
        df["fecha_creacion"] = pd.to_datetime(df["fecha_creacion"], errors="coerce").dt.tz_localize(None)  # Asegurar que fecha_creacion sea datetime y sin zona horaria (tz-naive)
        
        df["fecha_crea"] = df["fecha_creacion"].dt.strftime("%Y-%m-%d")  # Crear columnas de fecha y hora solo si fecha_creacion es válida
        df["hora_crea"] = df["fecha_creacion"].dt.strftime("%H:%M:%S")
        
        def extraer_fecha_hora(texto):  # Extraer fecha y hora del texto_post si contiene formato "YYYY-MM-DD HH:MM:SS UTC"
            if pd.isna(texto):
                return None, None
            
            patron = r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s*UTC'  # Patrón para buscar fechas en formato "YYYY-MM-DD HH:MM:SS UTC"
            match = re.search(patron, texto)
            
            if match:
                fecha_hora_str = match.group(1)
                try:
                    fecha_hora = pd.to_datetime(fecha_hora_str)
                    return fecha_hora.strftime("%Y-%m-%d"), fecha_hora.strftime("%H:%M:%S")
                except:
                    return None, None
            return None, None
        
        df["fecha_texto"] = None  # Aplicar extracción a texto_post
        df["hora_texto"] = None
        
        df["texto_post"] = df["texto_post"].fillna("")  # Llenar valores nulos en texto
        df["titulo"] = df["titulo"].fillna("")
        
        for idx, row in df.iterrows():  # Extraer fechas del texto_post
            fecha, hora = extraer_fecha_hora(row["texto_post"])
            if fecha and hora:
                df.at[idx, "fecha_texto"] = fecha
                df.at[idx, "hora_texto"] = hora
        
        mask_fecha_texto = df["fecha_texto"].notna()  # Usar fechas extraídas del texto si están disponibles
        if mask_fecha_texto.any():
            df.loc[mask_fecha_texto, "fecha_crea"] = df.loc[mask_fecha_texto, "fecha_texto"]
            df.loc[mask_fecha_texto, "hora_crea"] = df.loc[mask_fecha_texto, "hora_texto"]
        
        df = df.drop(columns=["fecha_texto", "hora_texto"], errors="ignore")  # Eliminar columnas temporales
        
        print(f"Datos cargados - shape: {df.shape}")
        return df
    else:
        raise FileNotFoundError(f"El archivo {file_path} no existe.")

def procesar_con_gemini(df):
    """
    Procesa datos de terremotos usando la API de Google Gemini para extraer
    información estructurada (ubicación, magnitud, coordenadas) del texto libre.
    
    Args:
        df (pandas.DataFrame): DataFrame con columnas 'texto_post' y 'titulo'
        
    Returns:
        pandas.DataFrame: DataFrame enriquecido con columnas extraídas:
                         ciudad_o_pais, magnitud, latitud, longitud
    """
    model = genai.GenerativeModel("gemma-3-1b-it")  # Usar gemini-1.5-flash en lugar de gemini-pro gemma-3-1b-it
    resultados_ciudad = []
    resultados_magnitud = []
    resultados_latitud = []
    resultados_longitud = []
    resultados_fecha_texto = []
    resultados_hora_texto = []

    for index, row in df.iterrows():  # Procesar cada post
        texto = row["texto_post"]
        titulo = row["titulo"]

        try:
            fecha_texto = None  # Primero extraer fecha y hora del texto si existe
            hora_texto = None
            
            patron_fecha = r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s*UTC'
            match_fecha = re.search(patron_fecha, texto)
            if match_fecha:
                fecha_hora_str = match_fecha.group(1)
                try:
                    fecha_hora = pd.to_datetime(fecha_hora_str)
                    fecha_texto = fecha_hora.strftime("%Y-%m-%d")
                    hora_texto = fecha_hora.strftime("%H:%M:%S")
                except:
                    pass
            
            prompt = (  # Ahora extraer información del terremoto
                "Ejemplo: Texto: 'Un terremoto de magnitud 6.3 golpeó Lima, Perú.' → [Lima, 6.3, -12.0464, -77.0428]\n\n"
                "Formato de respuesta: [lugar, magnitud (decimal), latitud (decimal), longitud (decimal)]. "
                f"Extrae del siguiente texto la ciudad o país donde ocurrió el evento sísmico, detectalo en cualquier idioma: {texto}. "
                f"Si no hay ciudad, devuelve el país. Si ninguno está presente, proporciona una ciudad cercana, pero evita colocar indeterminado. "
                f"Usa números decimales con '.' para magnitud, latitud y longitud. "
                f"Si no hay texto, usa 'indeterminado'. Si el lugar es indeterminado, busca en el título: {titulo}. "
                f"Si no hay información en el título, devuelve 'indeterminado' para lugar y 0 para magnitud. "
                f"Si hay múltiples lugares, elige el más relevante. "
                f"Si hay un lugar, entrégame las coordenadas de latitud y longitud. "
                f"Devuelve solo los valores en el orden correcto, sin explicaciones."
            )

            response = model.generate_content(prompt)

            if "[" in response.text and "]" in response.text:
                resultado = response.text.split("[")[1].split("]")[0].split(",")
                resultado = [item.strip() for item in resultado]
                while len(resultado) < 4:
                    resultado.append("0")
            else:
                resultado = ["indeterminado", "0", "0", "0"]

        except Exception as e:
            print(f"Error procesando fila {index}: {e}")
            resultado = ["indeterminado", "0", "0", "0"]
            fecha_texto = None
            hora_texto = None

        resultados_ciudad.append(resultado[0])
        resultados_magnitud.append(resultado[1])
        resultados_latitud.append(resultado[2])
        resultados_longitud.append(resultado[3])
        resultados_fecha_texto.append(fecha_texto)
        resultados_hora_texto.append(hora_texto)

        if (index + 1) % 5 == 0:  # Mostrar progreso
            print(f"Procesados {index + 1} de {len(df)} posts...")

        time.sleep(4) 

    df["ciudad_o_pais"] = resultados_ciudad  # Añadir resultados al DataFrame
    
    df["magnitud"] = pd.Series(pd.to_numeric(resultados_magnitud, errors="coerce")).fillna(0)  # Convertir a Series primero, luego aplicar fillna
    df["latitud"] = pd.Series(pd.to_numeric(resultados_latitud, errors="coerce")).fillna(0)
    df["longitud"] = pd.Series(pd.to_numeric(resultados_longitud, errors="coerce")).fillna(0)
    
    df["fecha_texto"] = resultados_fecha_texto  # Añadir fechas y horas extraídas del texto
    df["hora_texto"] = resultados_hora_texto
    
    mask_fecha_texto = df["fecha_texto"].notna()  # Actualizar fecha_crea y hora_crea si se encontró en el texto
    if mask_fecha_texto.any():
        df.loc[mask_fecha_texto, "fecha_crea"] = df.loc[mask_fecha_texto, "fecha_texto"]
        df.loc[mask_fecha_texto, "hora_crea"] = df.loc[mask_fecha_texto, "hora_texto"]
    
    df = df.drop(columns=["fecha_texto", "hora_texto"], errors="ignore")  # Eliminar columnas temporales

    df["hora"] = df["fecha_creacion"].dt.strftime("%Y-%m-%d %H:%M:%S")  # Crear columna hora con formato consistente
    
    df = df[df["ciudad_o_pais"] != "indeterminado"].reset_index(drop=True)  # guardar todo menos las filas que tienen "indeterminado" en ciudad_o_pais
    

    processed_file_path = os.path.join(os.getcwd(), "data", "terremotos_procesados.csv")
    if os.path.exists(processed_file_path):  # borrar si existe
        os.remove(processed_file_path)

    df.to_csv(processed_file_path, index=False)  # Guardar resultados procesados
    print(f"Datos procesados - shape: {df.shape}")
    return df

def combinar_datos(df_nuevo):
    """
    Combina datos nuevos procesados con datos existentes, eliminando duplicados
    y manteniendo consistencia en tipos de datos y formatos de fecha.
    
    Args:
        df_nuevo (pandas.DataFrame): DataFrame con nuevos datos procesados
        
    Returns:
        pandas.DataFrame: DataFrame combinado, filtrado y ordenado por fecha
    """
    file_path = os.path.join(os.getcwd(), "data", "Earthquakes_posts_new.csv")

    if os.path.exists(file_path):
        df_existente = pd.read_csv(file_path)  # Leer datos existentes
        
        df_existente["fecha_creacion"] = pd.to_datetime(df_existente["fecha_creacion"], errors="coerce")  # Convertir fecha_creacion a datetime en df_existente y asegurar que sea tz-naive
        
        if df_existente["fecha_creacion"].dt.tz is not None:  # Convertir fechas con zona horaria a tz-naive
            df_existente["fecha_creacion"] = df_existente["fecha_creacion"].dt.tz_localize(None)
        
        if df_nuevo["fecha_creacion"].dt.tz is not None:  # Asegurar que fecha_creacion en df_nuevo también sea tz-naive
            df_nuevo["fecha_creacion"] = df_nuevo["fecha_creacion"].dt.tz_localize(None)
        
        columnas_requeridas = ["fecha_crea", "hora_crea", "ciudad_o_pais", "magnitud",   # Asegurar que todas las columnas necesarias existan en df_existente
                             "latitud", "longitud", "hora"]
        
        for col in columnas_requeridas:
            if col not in df_existente.columns:
                if col == "fecha_crea":
                    df_existente["fecha_crea"] = df_existente["fecha_creacion"].dt.strftime("%Y-%m-%d")
                elif col == "hora_crea":
                    df_existente["hora_crea"] = df_existente["fecha_creacion"].dt.strftime("%H:%M:%S")
                elif col == "hora":
                    df_existente["hora"] = df_existente["fecha_creacion"].dt.strftime("%Y-%m-%d %H:%M:%S")
                elif col in ["magnitud", "latitud", "longitud"]:
                    df_existente[col] = 0
                else:
                    df_existente[col] = ""
        
        for col in ["magnitud", "latitud", "longitud"]:  # Asegurar tipos de datos consistentes
            df_existente[col] = pd.to_numeric(df_existente[col], errors="coerce").fillna(0)
            df_nuevo[col] = pd.to_numeric(df_nuevo[col], errors="coerce").fillna(0)
        
        df_combinado = pd.concat([df_existente, df_nuevo], ignore_index=True)  # Combinar DataFrames
        
        df_combinado = df_combinado.drop_duplicates(subset=["titulo"], keep="first")  # Eliminar duplicados basados en título
        df_combinado = df_combinado[df_combinado["magnitud"] > 1 ].reset_index(drop=True)  # eliminar filas con magnitud <= 1 
        df_combinado = df_combinado[df_combinado["magnitud"] < 15].reset_index(drop=True)  # eliminar filas con magnitud > 15
        
    else:
        df_combinado = df_nuevo

    df_combinado["fecha_creacion"] = pd.to_datetime(df_combinado["fecha_creacion"], errors="coerce")  # Asegurar que todas las fechas son tz-naive antes de ordenar
    if df_combinado["fecha_creacion"].dt.tz is not None:
        df_combinado["fecha_creacion"] = df_combinado["fecha_creacion"].dt.tz_localize(None)
    
    df_combinado = df_combinado.sort_values("fecha_creacion", ascending=False)  # Ordenar por fecha más reciente


    df_combinado.to_csv(file_path, index=False)  # Guardar datos combinados
    print(f"Datos combinados - shape: {df_combinado.shape}")
    
    return df_combinado

def procesar_y_limpiar_datos():
    """
    Función principal que orquesta todo el pipeline de procesamiento de datos:
    carga desde Reddit, procesamiento con IA, y combinación con datos existentes.
    
    Returns:
        pandas.DataFrame: DataFrame final con todos los datos procesados y combinados
        
    Raises:
        Exception: Si ocurre algún error durante el procesamiento
    """
    try:
        print("Cargando datos de Reddit...")
        df = load_data_reddit()
        
        print("Procesando con Gemini...")
        df = procesar_con_gemini(df)
        
        print("Combinando con datos existentes...")
        df = combinar_datos(df)
        
        print("Proceso completado exitosamente")
        return df
        
    except Exception as e:
        print(f"Error en el proceso: {e}")
        raise


# if __name__ == "__main__":
#     print("\n" + "="*50 + "\n")
    
#     df_final = procesar_y_limpiar_datos()
#     print(f"\nResultado final:")
#     print(f"Shape: {df_final.shape}")
#     print(f"Columnas: {df_final.columns.tolist()}")
#     print(f"\nPrimeras 5 filas:")
#     print(df_final[["titulo", "fecha_creacion", "fecha_crea", "hora_crea", "ciudad_o_pais", "magnitud"]].head())




