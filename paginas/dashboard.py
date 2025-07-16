import os
import pandas as pd
import streamlit as st
import plotly.io as pio
import json
import base64
from io import BytesIO

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
        df["magnitud"] = pd.to_numeric(df["magnitud"], errors="coerce")  # Asegurar que magnitud sea numérica
        df = df.dropna(subset=["latitud", "longitud", "magnitud"])
        df = df[(df["latitud"] >= -90) & (df["latitud"] <= 90)]
        df = df[(df["longitud"] >= -180) & (df["longitud"] <= 180)]
        # Aplicar filtros de magnitud consistentes con procesado.py
        df = df[(df["magnitud"] > 1) & (df["magnitud"] < 15)]
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


def download_plotly_chart(fig, filename="chart", chart_type="png"):
    """
    Función para crear un botón de descarga para gráficos de Plotly.
    
    Args:
        fig: Figura de Plotly
        filename (str): Nombre base del archivo (sin extensión)
        chart_type (str): Tipo de archivo ('html', 'json')
    """
    if fig is None:
        st.warning("No hay datos para descargar")
        return
    
    try:
        # Ofrecer HTML interactivo (siempre funciona sin Kaleido/Chrome)
        if chart_type == 'html' or chart_type in ['png', 'jpg', 'pdf', 'svg']:
            html_bytes = pio.to_html(fig, include_plotlyjs='cdn').encode()
            
            # Si pidieron un formato de imagen, ofrecer HTML pero avisar
            if chart_type in ['png', 'jpg', 'pdf', 'svg']:
                st.info(f"💡 La descarga como {chart_type.upper()} no está disponible en Streamlit Cloud. Se ofrece HTML como alternativa.")
            
            st.download_button(
                label="📥 Descargar como HTML",
                data=html_bytes,
                file_name=f"{filename}.html",
                mime="text/html",
                key=f"download_{filename}_html"
            )
            
        # Ofrecer JSON como alternativa (datos brutos para procesamiento posterior)
        elif chart_type == 'json':
            json_bytes = json.dumps(fig.to_dict()).encode()
            st.download_button(
                label="📥 Descargar como JSON",
                data=json_bytes,
                file_name=f"{filename}.json",
                mime="application/json",
                key=f"download_{filename}_json"
            )
            
    except Exception as e:
        st.error(f"Error al generar la descarga: {str(e)}")


def download_pydeck_map(deck_obj, filename="mapa"):
    """
    Función para crear un botón de descarga para mapas de PyDeck.
    Genera un archivo HTML con el mapa interactivo.
    
    Args:
        deck_obj: Objeto PyDeck Deck
        filename (str): Nombre base del archivo
    """
    if deck_obj is None:
        st.warning("No hay mapa para descargar")
        return
    
    try:
        # Convertir el mapa a HTML
        html_content = deck_obj.to_html(as_string=True)
        
        st.download_button(
            label="📥 Descargar Mapa como HTML",
            data=html_content.encode(),
            file_name=f"{filename}.html",
            mime="text/html",
            key=f"download_{filename}_map"
        )
        
    except Exception as e:
        st.error(f"Error al generar la descarga del mapa: {str(e)}")


def create_download_section(fig, chart_name, chart_type="chart"):
    """
    Crea una sección completa de descarga con múltiples formatos.
    
    Args:
        fig: Figura de Plotly o objeto PyDeck
        chart_name (str): Nombre descriptivo del gráfico
        chart_type (str): Tipo de gráfico ('chart' para Plotly, 'map' para PyDeck)
    """
    if fig is None:
        return
    
    # Crear un nombre de archivo limpio
    clean_name = chart_name.lower().replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    
    with st.expander(f"📥 Descargar {chart_name}", expanded=False):
        if chart_type == "chart":
            col1, col2 = st.columns(2)
            
            with col1:
                download_plotly_chart(fig, clean_name, "html")
            with col2:
                download_plotly_chart(fig, clean_name, "json")
                
        elif chart_type == "map":
            download_pydeck_map(fig, clean_name)
