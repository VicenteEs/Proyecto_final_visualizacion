import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """
    Función que carga y procesa los datos de terremotos desde un archivo CSV.
    Realiza limpieza de datos, conversión de tipos y filtrado de coordenadas válidas.
    Utiliza cache de Streamlit para optimizar el rendimiento.
    
    Returns:
        pandas.DataFrame: DataFrame con datos de terremotos procesados y limpios,
                         o DataFrame vacío si hay error al cargar el archivo
    """
    path = os.path.join(os.getcwd(), "data", "Earthquakes_posts_new.csv")
    try:
        df = pd.read_csv(path)
        df["fecha_crea"] = pd.to_datetime(df["fecha_crea"], errors="coerce", utc=True)
        df["latitud"] = pd.to_numeric(df["latitud"].astype(str).str.replace(",", "."), errors="coerce")
        df["longitud"] = pd.to_numeric(df["longitud"].astype(str).str.replace(",", "."), errors="coerce")
        df = df.dropna(subset=["latitud", "longitud", "magnitud"])
        df = df[(df["latitud"] >= -90) & (df["latitud"] <= 90)]
        df = df[(df["longitud"] >= -180) & (df["longitud"] <= 180)]
        return df
    except FileNotFoundError:
        st.error("Archivo CSV no encontrado.")
        return pd.DataFrame()

def clear_sidebar():
    """
    Función auxiliar que limpia el contenido del sidebar almacenado en el session_state.
    Útil para resetear el estado del sidebar cuando se cambia de página.
    """
    if hasattr(st.session_state, 'sidebar_content'):
        del st.session_state.sidebar_content
