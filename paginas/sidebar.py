import streamlit as st
import pandas as pd
import os

@st.dialog("  📤 Publicar Evento Sísmico")
def mostrar_imagen_reddit():
    """
    Función que muestra la imagen de r/Earthquakes en una ventana modal.
    """
    # Estilo personalizado para agrandar el contenido del diálogo
    st.markdown("""
        <style>
            .element-container:has(.stDialog) img {
                max-width: 100% !important;
                height: auto;
                border-radius: 15px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
                margin-top: 20px;
                margin-bottom: 20px;
            }

            .stDialog button {
                font-size: 1.2rem !important;
                padding: 0.6rem 1.5rem !important;
                background-color: #10b981 !important;
                color: white !important;
                border-radius: 10px !important;
                margin-top: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)
    image_path = os.path.join(os.getcwd(), "data", "r_Earthquakes.png")

    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)  # Expande imagen a lo ancho
        
        if st.button("✅ Cerrar", use_container_width=True):
            st.rerun()
    else:
        st.error("❌ No se pudo cargar la imagen.")
        st.info("🔍 Verifica que el archivo `data/r_Earthquakes.png` existe.")

def main_navigation():
    """
    Función que crea la navegación principal del sidebar con botones para
    cambiar entre las diferentes páginas de la aplicación.
    
    Returns:
        str: Nombre de la página actualmente seleccionada
    """
    st.sidebar.markdown("### 🧭 Navegación Principal")
    opciones = ["📊 Dashboard", "🔍 Exploración", "📢 Presentación"]
    if 'pagina_actual' not in st.session_state:
        st.session_state.pagina_actual = opciones[0]
    for opcion in opciones:
        if st.sidebar.button(opcion, use_container_width=True, key=f"nav_{opcion}"):
            st.session_state.pagina_actual = opcion
    st.sidebar.markdown("---")
    return st.session_state.pagina_actual

def sidebar_dashboard(df):
    """
    Función que crea los controles de filtrado del sidebar para la página del dashboard,
    incluyendo filtros de fecha, magnitud, ubicación y opciones de visualización.
    
    Args:
        df (pandas.DataFrame): DataFrame con datos de terremotos para crear filtros
        
    Returns:
        tuple: (date_range, mag_range, locations, solo_oficiales, mostrar_volcanes)
    """
    st.sidebar.markdown("### 🔍 Filtros de Dashboard")
    if df.empty:
        return [], (0, 10), [], False, False
    
    # Verificar que la columna fecha_crea existe y tiene datos válidos
    if "fecha_crea" not in df.columns:
        st.sidebar.error("⚠️ Columna 'fecha_crea' no encontrada")
        return [], (0, 10), [], False, False
    
    # Asegurar que fecha_crea es datetime y filtrar valores válidos
    df_fechas = df[df["fecha_crea"].notna()].copy()
    if df_fechas.empty:
        st.sidebar.warning("⚠️ No hay fechas válidas en los datos")
        return [], (0, 10), [], False, False
    
    min_date = df_fechas["fecha_crea"].min().date()
    max_date = df_fechas["fecha_crea"].max().date()
    date_range = st.sidebar.date_input("📅 Rango de fechas", [min_date, max_date], key="dashboard_date_range")
    
    # Verificar que magnitud existe y convertir a float
    if "magnitud" in df.columns:
        df_mag = df[df["magnitud"].notna()].copy()
        df_mag["magnitud"] = pd.to_numeric(df_mag["magnitud"], errors="coerce")
        df_mag = df_mag[df_mag["magnitud"].notna()]
        
        if not df_mag.empty:
            mag_range = st.sidebar.slider("📊 Rango de magnitud", 
                                        float(df_mag["magnitud"].min()), 
                                        float(df_mag["magnitud"].max()), 
                                        (float(df_mag["magnitud"].min()), float(df_mag["magnitud"].max())), 
                                        key="dashboard_mag_range")
        else:
            mag_range = (0.0, 10.0)
    else:
        mag_range = (0.0, 10.0)
    
    locations = st.sidebar.multiselect("📍 Filtrar por ubicaciones", sorted(df["ciudad_o_pais"].dropna().unique()), key="dashboard_locations")
    
    st.sidebar.markdown("### 🌋 Opciones de visualización")
    solo_oficiales = st.sidebar.checkbox("Mostrar solo oficiales", value=False, key="dashboard_solo_oficiales")
    mostrar_volcanes = st.sidebar.checkbox("Mostrar volcanes", value=False, key="dashboard_mostrar_volcanes")
    
    # Botón para mostrar imagen
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📸 Información Adicional")
    
    if st.sidebar.button(" Comunidad Reddit", use_container_width=True, key="btn_mostrar_imagen_reddit", help="Mostrar subreddit r/Earthquakes"):
        mostrar_imagen_reddit()
    
    return date_range, mag_range, locations, solo_oficiales, mostrar_volcanes

def sidebar_exploracion(df):
    """
    Función que crea los controles del sidebar para la página de exploración,
    permitiendo seleccionar columnas, número de filas y filtrar por fuentes oficiales.
    
    Args:
        df (pandas.DataFrame): DataFrame con datos para crear opciones de columnas
        
    Returns:
        tuple: (columnas_seleccionadas, max_rows, filtro_oficial)
    """
    st.sidebar.markdown("### 📊 Opciones de Exploración")
    if df.empty:
        return [], 20, "Todos"
    
    # Selector de columnas
    columnas = st.sidebar.multiselect("🏷️ Seleccionar columnas", df.columns.tolist(), default=[], key="exploracion_columns")
    
    # Número máximo de filas
    max_rows = st.sidebar.slider("📄 Número máximo de filas", 5, 100, 20, key="exploracion_max_rows")
    
    # Filtro por oficiales/no oficiales
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Filtros de Datos")
    
    filtro_oficial = st.sidebar.selectbox(
        "👥 Filtrar por fuente:",
        options=["Todos", "Solo Oficiales", "Solo No Oficiales"],
        index=0,
        key="exploracion_filtro_oficial",
        help="Filtra los datos según la fuente: BrainstormBot (oficial) vs otros usuarios"
    )
    
    return columnas, max_rows, filtro_oficial

def sidebar_presentacion():
    """
    Función que crea la navegación del sidebar para la página de presentación,
    con botones para navegar entre diferentes slides/secciones del proyecto.
    
    Returns:
        str: Slide/sección actualmente seleccionada
    """
    st.sidebar.markdown("### 📢 Navegación de Presentación")

    slides = [  # Opciones actualizadas con todas las secciones
        "📊 Introducción", 
        "🎯 Estructura del Proyecto", 
        "🔧 Desafíos",
        "📈 Resultados"
    ]
    
    selected = st.session_state.get("slide_seleccionado", slides[0])

    for slide in slides:  # Renderizar botones
        button_style = "" if slide != selected else "background-color: #1E88E5; color: white;"
        if st.sidebar.button(
            slide, 
            key=f"btn_{slide}", 
            use_container_width=True,
            help=f"Ver sección {slide},",
            on_click=lambda s=slide: st.session_state.update({"slide_seleccionado": s}) # actualizar estado de sesión
        ):
            st.session_state.slide_seleccionado = slide
            selected = slide  # actualizar variable local también



    st.sidebar.markdown("---")  # info
    st.sidebar.markdown("### ℹ️ Información")
    st.sidebar.info(
        "Este proyecto utiliza datos extraídos de Reddit para visualizar "
        "y analizar patrones sísmicos globales, con especial énfasis en "
        "el Cinturón de Fuego."
    )

    return selected
