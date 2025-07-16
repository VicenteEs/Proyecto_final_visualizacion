import os
import streamlit as st
from paginas.sidebar import sidebar_presentacion
import pandas as pd
import plotly.express as px
import pydeck as pdk
from graficos import map_m, mapa
from paginas.styles import *
inject_css()

def show(df):
    """
    Función que muestra la página de presentación del proyecto con diferentes slides
    informativos sobre el proyecto de análisis sísmico, incluyendo introducción,
    estructura, desafíos y resultados obtenidos.
    
    Args:
        df (pandas.DataFrame): DataFrame con datos de terremotos para mostrar estadísticas
    """
    slide = sidebar_presentacion()

    col_logo, col_title, col_info = st.columns([1, 3, 1])  # Header con logo y título
    with col_logo:
        logo_path = os.path.join(os.getcwd(), "data", "logocolor.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=100)
    with col_title:
        st.markdown('<h1 class="main-title">📢 Presentación del Proyecto</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Resumen y resultados • Universidad Tecnológica Metropolitana</p>', unsafe_allow_html=True)
    if slide == "📊 Introducción":
        st.markdown("## 📊 Introducción")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### 🎯 Motivación
            
            - **🔍 Exploración de datos sísmicos**: Descubrir el Cinturón de Fuego del Pacífico a través del análisis de terremotos
            - **📱 Datos de redes sociales**: Transformar publicaciones de Reddit en información valiosa y estructurada
            - **⚙️ Procesamiento avanzado**: Aplicar técnicas de limpieza y análisis para obtener resultados significativos
            - **🗺️ Visualización geoespacial**: Representar patrones sísmicos globales de forma interactiva
            
            ### 📋 Características principales
            - 🌍 **Visualización global**: Mapa interactivo mundial
            - 📊 **Análisis estadístico**: Distribuciones y tendencias
            - ⏰ **Tiempo real**: Datos actualizados constantemente
            """)
            st.markdown("### 🔄 Diagrama del Proyecto")  # Diagrama del proyecto
            st.image("data/flujo.png", use_container_width=False, width=800)
        with col2:
            if not df.empty and 'fecha_crea' in df.columns:
                event_count = len(df)
                # Filtrar fechas válidas y calcular rango
                fechas_validas = df[df['fecha_crea'].notna()]['fecha_crea']
                if len(fechas_validas) > 0:
                    date_range_days = (fechas_validas.max() - fechas_validas.min()).days
                else:
                    date_range_days = 0
                
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">🌍 Eventos Registrados</div>
                        <div class="metric-value">{event_count:,}</div>
                    </div>
                    <div class="metric-card" style="margin-top: 15px;">
                        <div class="metric-label">📅 Período de Datos</div>
                        <div class="metric-value">{date_range_days} días</div>
                    </div>
                """, unsafe_allow_html=True)
                

    elif slide == "🎯 Estructura del Proyecto":

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📁 Estructura del Proyecto")
            st.markdown("""
            ```
            📁 PROYECTO_FINAL_VISUALIZACION/
            ├── 📁 .streamlit/
            │   └── 📄 config.toml
            ├── 📁 data/
            │   ├── 📄 datos_reddit.csv (temporal)
            │   ├── 📄 Earthquakes_posts_new.csv
            │   ├── 🖼️ flujo.png
            │   ├── 🖼️ logocolor.png
            │   ├── 📄 terremotos_procesados.csv  (temporal)
            │   └── 📄 volcanoes_selected_columns.csv
            ├── 📁 paginas/
            │   ├── 📄 dashboard.py
            │   ├── 📄 exploracion.py
            │   ├── 📄 presentacion.py
            │   ├── 📄 sidebar.py
            │   ├── 📄 styles.py
            │   └── 📄 utils.py
            ├── 📄 credenciales.py
            ├── 📄 graficos.py
            ├── 📄 main.py
            ├── 📄 procesado.py
            ├── 📄 readme.md
            ├── 📄 requirement.txt
            └── 📄 scraping.py
            ```
            """)
        with col2:
            
            st.markdown("### 📚 Librerías Utilizadas")
            a,b,c,d,e = st.columns(5)
            with b:
                st.markdown("""
                <div style="display: flex; flex-direction: column; gap: 10px; align-items: flex-end; margin-bottom: 20px;">
                    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" style="width:150px;">
                    <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" style="width:150px;">
                    <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy" style="width:150px;">
                    <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly" style="width:150px;">
                    <img src="https://img.shields.io/badge/PyDeck-0A2540?style=for-the-badge&logo=deckdotgl&logoColor=white" alt="PyDeck" style="width:150px;">
                    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" style="width:150px;">
                    <img src="https://img.shields.io/badge/PRAW-FF4500?style=for-the-badge&logo=reddit&logoColor=white" alt="PRAW" style="width:150px;">
                    <img src="https://img.shields.io/badge/Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini" style="width:150px;">
                </div>
                """, unsafe_allow_html=True)




    elif slide == "🔧 Desafíos":
        st.markdown("### 🔧 Desafíos Encontrados")
        
        challenges_col1, challenges_col2 = st.columns(2)
        with challenges_col1:
            st.markdown("""
            #### 📊 Naturaleza de los datos
            
            - **🔄 Información no estructurada** en publicaciones de Reddit
            - **📝 Formatos inconsistentes** de coordenadas, fechas y magnitudes
            - **🔄 Múltiples fuentes** reportando el mismo evento sísmico
            
            #### 📈 Volumen y calidad
            
            - **📚 Gran cantidad** de datos a procesar (cientos de publicaciones)
            - **🧹 Ruido y datos irrelevantes** mezclados con información útil
            """)
        with challenges_col2:
            st.markdown("""
            #### 🗺️ Procesamiento geoespacial
            
            - **🌐 Normalización de coordenadas** para visualización global
            - **📏 Representación adecuada** de magnitudes en el mapa
            
            #### ⚡ Rendimiento
            
            - **⏱️ Optimización** para actualización en tiempo real
            - **💾 Carga eficiente** de datos históricos
            - **🧠 Gestión de memoria** con grandes conjuntos de datos
            """)


    elif slide == "📈 Resultados":
        st.markdown("### 📈 Resultados y Logros")
        if not df.empty:
            
            event_count = len(df)  # Calcular métricas
            unique_countries = df["ciudad_o_pais"].nunique() if "ciudad_o_pais" in df.columns else 0
            avg_magnitude = df['magnitud'].mean() if "magnitud" in df.columns else 0
            
            # Calcular rango de fechas de forma segura
            if 'fecha_crea' in df.columns:
                fechas_validas = df[df['fecha_crea'].notna()]['fecha_crea']
                if len(fechas_validas) > 0:
                    date_range_days = (fechas_validas.max() - fechas_validas.min()).days
                else:
                    date_range_days = 0
            else:
                date_range_days = 0

            col1, col2, col3, col4 = st.columns(4)  # Crear columnas

            with col1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Total Eventos</div>
                        <div class="metric-value">{event_count:,}</div>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Lugares Cubiertos</div>
                        <div class="metric-value">{unique_countries}</div>
                    </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Magnitud Promedio</div>
                        <div class="metric-value">{avg_magnitude:.1f}</div>
                    </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Período Analizado</div>
                        <div class="metric-value">{date_range_days} días</div>
                    </div>
                """, unsafe_allow_html=True)


            st.markdown("### 🌋 Comparación con el Cinturón de Fuego")  # Comparación entre Cinturón de Fuego y datos obtenidos
            
            comp_col1, comp_col2 = st.columns(2)
            with comp_col1:
                st.markdown("#### 🌋 Cinturón de Fuego (Referencia)")
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Pacific_Ring_of_Fire.svg/1200px-Pacific_Ring_of_Fire.svg.png", 
                         use_container_width=True)
            
            with comp_col2:
                st.markdown("#### 📊 Terremotos Detectados")
                map_chart = mapa(df, solo_oficiales=False, mostrar_volcanes=True) 
                if map_chart:
                    st.pydeck_chart(map_chart, use_container_width=True, height=400)
                else:
                    st.info("📍 Sin datos para mostrar en el mapa")

    

            
        else:
            st.warning("⚠️ No hay datos disponibles para mostrar resultados.")
