"""
Aplicación principal del Dashboard de Terremotos UTEM.

Este módulo configura y ejecuta la aplicación web de Streamlit para visualización
y análisis de datos sísmicos. Maneja la navegación entre páginas, carga de datos
y configuración general de la interfaz.

Páginas disponibles:
- Dashboard: Visualizaciones interactivas y métricas en tiempo real
- Exploración: Análisis detallado y exportación de datos
- Presentación: Información del proyecto y resultados
"""

import os
import streamlit as st
from paginas.utils import load_data, clear_sidebar
from paginas.sidebar import main_navigation
from paginas.styles import * 
import paginas.dashboard as dashboard
import paginas.exploracion 
import paginas.presentacion


hide_streamlit_header()
st.set_page_config(
    page_title="Dashboard Terremotos UTEM", 
    page_icon="🌍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()  # Inyectar estilos CSS

if "data" not in st.session_state:  # Cargar datos (usando cache)
    st.session_state.data = load_data()

df = st.session_state.data

pagina_actual = main_navigation()  # Navegación principal

if pagina_actual == "📊 Dashboard":  # Mostrar contenido según página seleccionada
    clear_sidebar()
    dashboard.show(df)

elif pagina_actual == "🔍 Exploración":
    clear_sidebar()
    paginas.exploracion.show(df)

elif pagina_actual == "📢 Presentación":
    clear_sidebar()
    paginas.presentacion.show(df)


dashboard.show_footer()
