import os
import streamlit as st
import pandas as pd
from graficos import *
from paginas.sidebar import *
from paginas.utils import *
from scraping import *
from procesado import *
from paginas.styles import *

def show(df):
    """
    Función principal del dashboard que muestra la interfaz completa con métricas,
    filtros y visualizaciones de datos sísmicos en tiempo real.
    
    Args:
        df (pandas.DataFrame): DataFrame con datos de terremotos
    """
    inject_css()
    hide_streamlit_header()

    col_logo, col_title, col_btn = st.columns([1, 4, 1])  # Header con logo, título y botón
    with col_logo:
        logo_path = os.path.join(os.getcwd(), "data", "logocolor.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=100)

    with col_title:
        st.markdown('<h1 class="main-title">🌍 Dashboard de Terremotos</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Análisis en tiempo real • Universidad Tecnológica Metropolitana</p>', unsafe_allow_html=True)

    with col_btn:
        if st.button("🔄 Actualizar datos", key="data-testid"):
            with st.spinner("Actualizando datos..."):
                obtener_datos("Earthquakes", 10)  # cambiar a 15
                df_actualizado = procesar_y_limpiar_datos() 
                st.session_state.data = df_actualizado
                st.session_state.data_loaded = True
                st.balloons()
                st.success("Datos actualizados correctamente 🎉")
                st.rerun()

    df = st.session_state.get("data", df)  # Usar datos actualizados o originales

    if df.empty:
        st.warning("⚠️ No hay datos disponibles.")
        st.stop()

    # Asegurar que fecha_crea esté en formato datetime
    if "fecha_crea" in df.columns:
        df["fecha_crea"] = pd.to_datetime(df["fecha_crea"], errors="coerce", utc=True)

    if "hora_crea" in df.columns and df["hora_crea"].notna().any():  # Procesar 'hora_crea' solo si existe y tiene datos no nulos
        df["hora_crea"] = df["hora_crea"].apply(lambda x: x.strip() if isinstance(x, str) else x)  # Limpiar espacios solo en strings
        df["hora_crea"] = pd.to_datetime(df["hora_crea"], format="%H:%M:%S", errors="coerce").dt.time  # Convertir a datetime.time
    else:
        df["hora_crea"] = pd.NaT

    def combinar_fecha_hora(row):  # Función para combinar fecha y hora en un solo timestamp
        if pd.isna(row["fecha_crea"]):
            return pd.NaT
        if pd.isna(row["hora_crea"]):
            return row["fecha_crea"]  # Retornar el timestamp completo
        # Convertir fecha_crea a date para combine
        fecha_date = row["fecha_crea"].date()
        return pd.Timestamp.combine(fecha_date, row["hora_crea"]).tz_localize('UTC')

    df["fecha_hora"] = df.apply(combinar_fecha_hora, axis=1)

    date_range, mag_range, selected_locations, solo_oficiales, mostrar_volcanes = sidebar_dashboard(df)  # Sidebar filtros

    filtered = df.copy()  # Aplicar filtros

    if len(date_range) == 2:  # Filtrar por rango de fechas usando solo fecha_crea
        # Convertir date objects a datetime con UTC para compatibilidad
        start = pd.Timestamp(date_range[0], tz='UTC')
        end = pd.Timestamp(date_range[1], tz='UTC') + pd.Timedelta(days=1)

        filtered = filtered[(filtered["fecha_crea"] >= start) & (filtered["fecha_crea"] < end)]

    filtered = filtered[(filtered["magnitud"] >= mag_range[0]) & (filtered["magnitud"] <= mag_range[1])]  # Filtrar por magnitud

    if selected_locations:  # Filtrar por ubicaciones
        filtered = filtered[filtered["ciudad_o_pais"].isin(selected_locations)]

    if solo_oficiales and "autor" in filtered.columns:  # Filtrar solo oficiales (BrainstormBot) si aplica
        filtered = filtered[filtered["autor"] == "BrainstormBot"]

    col1, col2, col3, col4 = st.columns(4)  # Métricas
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Terremotos</div><div class="metric-value">{len(filtered):,}</div></div>', unsafe_allow_html=True)
    with col2:
        avg_mag = filtered['magnitud'].mean() if not filtered.empty else 0.0
        st.markdown(f'<div class="metric-card"><div class="metric-label">Magnitud Promedio</div><div class="metric-value">{avg_mag:.1f}</div></div>', unsafe_allow_html=True)
    with col3:
        max_mag = filtered['magnitud'].max() if not filtered.empty else 0.0
        st.markdown(f'<div class="metric-card"><div class="metric-label">Magnitud Máxima</div><div class="metric-value">{max_mag:.1f}</div></div>', unsafe_allow_html=True)
    with col4:
        top_location = filtered["ciudad_o_pais"].value_counts().index[0] if not filtered.empty and len(filtered["ciudad_o_pais"].value_counts()) > 0 else "N/A"
        st.markdown(f'<div class="metric-card"><div class="metric-label">Ubicación Más Activa</div><div class="metric-value">{top_location}</div></div>', unsafe_allow_html=True)

    map_col, dist_col = st.columns([2, 1])  # Gráficos
    with map_col:
        title = "🗺️ Mapa Global" + (" y Volcanes 🌋" if mostrar_volcanes else "")
        st.markdown(f'<div class="chart-container">{title}</div>', unsafe_allow_html=True)
        map_chart = mapa(filtered, solo_oficiales=solo_oficiales, mostrar_volcanes=mostrar_volcanes)
        if map_chart:
            st.pydeck_chart(map_chart, use_container_width=True, height=700)
            create_download_section(map_chart, "Mapa Global de Terremotos", "map")
        else:
            st.info("📍 Sin datos para mostrar en el mapa")

    with dist_col:
        st.markdown('<div class="chart-container">📊 Distribución de Magnitudes</div>', unsafe_allow_html=True)
        mag_fig = distr(filtered)
        if mag_fig:
            st.plotly_chart(mag_fig, use_container_width=True, config={"displayModeBar": False})
            create_download_section(mag_fig, "Distribución de Magnitudes", "chart")
        else:
            st.info("Sin datos de magnitud")

        st.markdown('<div class="chart-container">📍 Top 5 Ubicaciones</div>', unsafe_allow_html=True)
        loc_fig = torta(filtered)
        if loc_fig:
            st.plotly_chart(loc_fig, use_container_width=True, config={"displayModeBar": False})
            create_download_section(loc_fig, "Top 5 Ubicaciones", "chart")
        else:
            st.info("Sin datos de ubicación")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="chart-container">📅 Tendencia Mensual</div>', unsafe_allow_html=True)
        monthly = map_m(filtered)
        if monthly:
            st.plotly_chart(monthly, use_container_width=True, config={"displayModeBar": False})
            create_download_section(monthly, "Tendencia Mensual", "chart")
    with col2:
        st.markdown('<div class="chart-container">📅 Tendencia Semanal</div>', unsafe_allow_html=True)
        weekly = map_s(filtered)
        if weekly:
            st.plotly_chart(weekly, use_container_width=True, config={"displayModeBar": False})
            create_download_section(weekly, "Tendencia Semanal", "chart")
    with col3:
        st.markdown('<div class="chart-container">📅 Tendencia Horaria</div>', unsafe_allow_html=True)
        hourly = map_h(filtered)
        if hourly:
            st.plotly_chart(hourly, use_container_width=True, config={"displayModeBar": False})
            create_download_section(hourly, "Tendencia Horaria", "chart")

def show_footer():
    """
    Función que muestra el footer fijo en la parte inferior de la página
    con información de la universidad, creadores y versión del proyecto.
    """
    st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: linear-gradient(90deg, #1e3c72, #2a5298, #4CAF50);
        color: white;
        text-align: center;
        padding: 15px;
        font-size: 14px;
        z-index: 10000;
    }
    .footer-content {
        display: flex;
        justify-content: space-around;
        font-size: 16px;
        align-items: center;
        flex-wrap: wrap;
    }
    .footer-item {
        margin: 0 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    footer_html = f"""
    <div class="footer">
        <div class="footer-content">
            <div class="footer-item">
                <strong>🏫 Universidad Tecnológica Metropolitana</strong> | Proyecto de Visualización y Análisis de Datos Sísmicos
            </div>
            <div class="footer-item">
                <strong>👥 Creadores:</strong> David Sepúlveda & Vicente Escudero
            </div>
            <div class="footer-item">
                Versión: 999.1
            </div>
        </div>
    </div>
    """

    st.markdown(footer_html, unsafe_allow_html=True)
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
