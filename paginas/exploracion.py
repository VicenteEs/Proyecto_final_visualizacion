import os
import streamlit as st
from paginas.sidebar import sidebar_exploracion

def show(df):
    """
    Función que muestra la página de exploración detallada de datos sísmicos,
    permitiendo visualizar, filtrar, ordenar y exportar los datos en diferentes formatos.
    
    Args:
        df (pandas.DataFrame): DataFrame con datos de terremotos para explorar
    """
    columnas, max_rows, filtro_oficial = sidebar_exploracion(df)  

    if not columnas or len(columnas) == 0:  # Columnas predeterminadas si no se seleccionan
        default_columns = ['titulo', 'autor', 'ciudad_o_pais', 'magnitud']
        columnas = [col for col in default_columns if col in df.columns]
    
    st.markdown("""
    <style>
        /* Centrar encabezados */
        .main-title, .subtitle, h1, h2, h3, h4, h5, h6 {
            text-align: center !important;
        }
        
        /* Estilo para botones de descarga */
        .download-button {
            background-color: #10b981 !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 0.5rem 1rem !important;
            font-weight: bold !important;
            box-shadow: 0 4px 6px rgba(16, 185, 129, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        .download-button:hover {
            background-color: #059669 !important;
            box-shadow: 0 6px 8px rgba(16, 185, 129, 0.5) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Estilo para el selector de opciones de descarga */
        .download-options {
            background-color: #f0f9ff !important;
            border-radius: 10px !important;
            padding: 1rem !important;
            margin-top: 1rem !important;
            border-left: 5px solid #3b82f6 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col_logo, col_title, col_info = st.columns([1, 3, 1])  # Header con logo y título
    with col_logo:
        logo_path = os.path.join(os.getcwd(), "data", "logocolor.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=100)
    with col_title:
        st.markdown('<h1 class="main-title">🔍 Exploración Detallada de Datos</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Registros sísmicos • Universidad Tecnológica Metropolitana</p>', unsafe_allow_html=True)

    if not df.empty:
        # Aplicar filtro por oficiales/no oficiales
        filtered_df = df.copy()
        if filtro_oficial == "Solo Oficiales" and "autor" in df.columns:
            filtered_df = filtered_df[filtered_df["autor"] == "BrainstormBot"]
        elif filtro_oficial == "Solo No Oficiales" and "autor" in df.columns:
            filtered_df = filtered_df[filtered_df["autor"] != "BrainstormBot"]
        
        # Mostrar información del filtro aplicado
        if filtro_oficial != "Todos":
            total_original = len(df)
            total_filtrado = len(filtered_df)
            st.info(f"📊 **Filtro aplicado**: {filtro_oficial} | Mostrando {total_filtrado:,} de {total_original:,} registros")
        
        st.markdown("<h3>📋 Vista de Datos</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)  # Agregar opciones de ordenamiento
        with col1:
            sort_column = st.selectbox(
                "Ordenar por:",
                options=columnas,
                index=columnas.index('magnitud') if 'magnitud' in columnas else 0
            )
        
        with col2:
            sort_order = st.radio(
                "Orden:",
                options=["Descendente", "Ascendente"],
                horizontal=True,
                index=0
            )
        
        sorted_df = filtered_df[columnas].sort_values(  # Usar DataFrame filtrado en lugar de original
            by=sort_column,
            ascending=(sort_order == "Ascendente")
        )
        
        st.dataframe(  # Mostrar tabla con opciones avanzadas
            sorted_df.head(max_rows),
            use_container_width=True,
            column_config={
                "titulo": st.column_config.TextColumn(
                    "Título del Evento",
                    width="large"
                ),
                "autor": st.column_config.TextColumn(
                    "Autor/Fuente",
                    width="medium"
                ),
                "ciudad_o_pais": st.column_config.TextColumn(
                    "Ubicación",
                    width="medium"
                ),
                "magnitud": st.column_config.NumberColumn(
                    "Magnitud",
                    format="%.1f",
                    width="small"
                ),
                "fecha_crea": st.column_config.DateColumn(
                    "Fecha",
                    format="DD/MM/YYYY",
                    width="small"
                ),
                "hora_crea": st.column_config.TimeColumn(
                    "Hora",
                    format="HH:mm:ss",
                    width="small"
                ),
                "profundidad": st.column_config.NumberColumn(
                    "Profundidad (km)",
                    format="%.1f",
                    width="small"
                ),
                "latitud": st.column_config.NumberColumn(
                    "Latitud",
                    format="%.4f",
                    width="small"
                ),
                "longitud": st.column_config.NumberColumn(
                    "Longitud",
                    format="%.4f",
                    width="small"
                ),
                "oficial": st.column_config.CheckboxColumn(
                    "Oficial",
                    width="small"
                )
            }
        )
        
        st.caption(f"Mostrando {min(max_rows, len(sorted_df))} de {len(filtered_df):,} registros filtrados")  # Información sobre registros mostrados con filtro
        
        # Estadísticas del filtro aplicado
        if filtro_oficial != "Todos" and "autor" in df.columns:
            st.markdown("<h3>📊 Estadísticas de Filtrado</h3>", unsafe_allow_html=True)
            
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                total_oficiales = len(df[df["autor"] == "BrainstormBot"])
                st.metric(
                    label="🤖 Datos Oficiales",
                    value=f"{total_oficiales:,}",
                    help="Registros de BrainstormBot (fuente oficial)"
                )
            
            with col_stat2:
                total_no_oficiales = len(df[df["autor"] != "BrainstormBot"])
                st.metric(
                    label="👥 Datos No Oficiales", 
                    value=f"{total_no_oficiales:,}",
                    help="Registros de otros usuarios"
                )
            
            with col_stat3:
                porcentaje_filtrado = (len(filtered_df) / len(df)) * 100 if len(df) > 0 else 0
                st.metric(
                    label="📈 % Filtrado",
                    value=f"{porcentaje_filtrado:.1f}%",
                    help="Porcentaje de datos que pasan el filtro"
                )
        
        st.markdown("<h3>📥 Opciones de Exportación</h3>", unsafe_allow_html=True)  # Opciones de exportación mejoradas
        
        with st.expander("Configurar opciones de descarga", expanded=False):
            st.markdown('<div class="download-options">', unsafe_allow_html=True)
            
            export_option = st.radio(  # Selector de qué datos exportar
                "Datos a exportar:",
                options=["Datos filtrados y seleccionados", "Conjunto de datos completo", "Solo datos filtrados"],
                horizontal=False,
                index=0,
                help="Selecciona qué datos deseas exportar"
            )
            
            export_format = st.radio(  # Selector de formato
                "Formato de exportación:",
                options=["CSV", "Excel"],
                horizontal=True,
                index=0,
                help="Selecciona el formato del archivo a descargar"
            )
            
            if export_option == "Datos filtrados y seleccionados":  # Selector de columnas adicionales (solo para datos filtrados)
                include_all_columns = st.checkbox(
                    "Incluir todas las columnas disponibles", 
                    value=False,
                    help="Si se marca, se incluirán todas las columnas disponibles, no solo las seleccionadas"
                )
                
                if include_all_columns:
                    export_columns = filtered_df.columns.tolist()
                else:
                    export_columns = columnas
            elif export_option == "Solo datos filtrados":
                export_columns = filtered_df.columns.tolist()
            else:
                export_columns = df.columns.tolist()
            
            filename = st.text_input(  # Nombre personalizado para el archivo
                "Nombre del archivo (sin extensión):",
                value="datos_sismicos",
                help="Introduce un nombre para el archivo descargado"
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        if export_option == "Datos filtrados y seleccionados":  # Preparar datos para exportación
            if include_all_columns:
                export_data = filtered_df.loc[sorted_df.index]
            else:
                export_data = sorted_df
        elif export_option == "Solo datos filtrados":
            export_data = filtered_df
        else:
            export_data = df
        
        col1, col2 = st.columns(2)  # Botones de descarga
        
        with col1:
            if export_format == "CSV":
                st.download_button(
                    label="📥 Descargar CSV",
                    data=export_data.to_csv(index=False).encode('utf-8'),
                    file_name=f"{filename}.csv",
                    mime="text/csv",
                    help="Descargar los datos en formato CSV",
                    key="download_csv"
                )
            else:
                st.download_button(
                    label="📥 Descargar Excel",
                    data=export_data.to_excel(index=False).encode('utf-8'),
                    file_name=f"{filename}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    help="Descargar los datos en formato Excel",
                    key="download_excel"
                )
        
        with col2:
            st.info(f"Se exportarán {len(export_data):,} registros con {len(export_columns)} columnas")  # Mostrar información sobre lo que se va a descargar
            
    else:
        st.error("❌ No hay datos disponibles para explorar.")
        st.info("Por favor, asegúrate de que los datos se hayan cargado correctamente o actualiza los datos desde el Dashboard principal.")
