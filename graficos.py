import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk


from graficos import *
from scraping import *
from procesado import *


def mapa(data, solo_oficiales=False, mostrar_volcanes=False):
    """
    Crea un mapa interactivo 3D global mostrando la distribución de terremotos y opcionalmente volcanes.
    Utiliza PyDeck para visualización geoespacial con diferentes colores según la fuente de datos.
    
    El mapa es útil para:
    - Identificar patrones geográficos de actividad sísmica
    - Visualizar el Cinturón de Fuego del Pacífico
    - Comparar datos oficiales vs no oficiales
    - Correlacionar terremotos con ubicaciones volcánicas
    
    Args:
        data (pandas.DataFrame): DataFrame con datos de terremotos
        solo_oficiales (bool): Si True, muestra solo datos de fuentes oficiales
        mostrar_volcanes (bool): Si True, incluye volcanes en el mapa
        
    Returns:
        pdk.Deck: Objeto de mapa PyDeck o None si no hay datos
    """
    
    layers = []
    
    if not data.empty:  # Procesar datos de terremotos
        valid_data = data.dropna(subset=["latitud", "longitud", "magnitud", "autor"]).copy()

        
        valid_data['fecha_crea'] = pd.to_datetime(valid_data['fecha_crea'], errors='coerce')
        valid_data = valid_data.dropna(subset=["fecha_crea"])
        valid_data['fecha_crea'] = valid_data['fecha_crea'].dt.strftime('%Y-%m-%d %H:%M:%S')

        if 'hora_crea' in valid_data.columns:  # Convertir 'hora_crea' a string si existe
            valid_data['hora_crea'] = valid_data['hora_crea'].astype(str)

        if solo_oficiales:  # Filtrar solo oficiales si el checkbox está activo
            valid_data = valid_data[valid_data["autor"] == "BrainstormBot"]
            if not valid_data.empty:
                valid_data["color"] = [[255, 0, 0, 180]] * len(valid_data)
        else:
            def color_por_autor(autor):
                if autor == "BrainstormBot":
                    return [255, 0, 0, 180]
                else:
                    return [0, 255, 0, 180]

            valid_data["color"] = valid_data["autor"].apply(color_por_autor)

        valid_data["color"] = valid_data["color"].apply(lambda x: list(x) if not isinstance(x, list) else x)  # Asegurar que 'color' sea lista normal

        valid_data["radius"] = valid_data["magnitud"] ** 2 * 5000  # Calcular radius basado en magnitud

        copias = 2  # Repetición longitudinal para vista global
        dfs = []
        for offset in range(-copias, copias + 1):
            df_copy = valid_data.copy()
            df_copy["longitud"] = df_copy["longitud"] + (offset * 360)
            dfs.append(df_copy)

        final_data = pd.concat(dfs, ignore_index=True)

        earthquake_layer = pdk.Layer(  # Crear capa de terremotos
            "ScatterplotLayer",
            data=final_data,
            get_position=["longitud", "latitud"],
            get_radius="radius",
            get_fill_color="color",
            pickable=True,
            opacity=0.7,
        )
        
        layers.append(earthquake_layer)

    if mostrar_volcanes:  # Procesar datos de volcanes si se solicita
        volcanoes_path = os.path.join(os.getcwd(), "data", "volcanoes_selected_columns.csv")
        if os.path.exists(volcanoes_path):
            volcanoes_df = pd.read_csv(volcanoes_path)
            volcanoes_df = volcanoes_df.dropna(subset=["Latitude", "Longitude"]).copy()
            
            if not volcanoes_df.empty:
                volcanoes_df = volcanoes_df.rename(columns={
                    "Latitude": "latitud", 
                    "Longitude": "longitud",
                    "Volcano Name": "nombre"
                })
                volcanoes_df["color"] = [[0, 0, 0, 20]] * len(volcanoes_df)
                volcanoes_df["radius"] = 8000 * 22

                copias = 2
                volcano_dfs = []
                for offset in range(-copias, copias + 1):
                    df_copy = volcanoes_df.copy()
                    df_copy["longitud"] = df_copy["longitud"] + (offset * 360)
                    volcano_dfs.append(df_copy)
                
                final_volcanoes = pd.concat(volcano_dfs, ignore_index=True)
                
                volcano_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=final_volcanoes,
                    get_position=["longitud", "latitud"],
                    get_radius="radius",
                    get_fill_color="color",
                    pickable=True,
                    opacity=0.8,
                )
                
                layers.append(volcano_layer)
    
    if not layers:
        return None
        
    view = pdk.ViewState(latitude=20, longitude=180, zoom=1, pitch=0)
    
    tooltip = {
        "html": "<b>Lugar:</b> {ciudad_o_pais}<br><b>Magnitud:</b> {magnitud}<br>",
        "style": {"color": "white"}
    }
    
    return pdk.Deck(map_style=None, initial_view_state=view, layers=layers, tooltip=tooltip)


def distr(df):
    """
    Crea un histograma de distribución de magnitudes de terremotos.
    
    Este gráfico es fundamental para:
    - Analizar la frecuencia de diferentes magnitudes sísmicas
    - Identificar el rango más común de magnitudes
    - Detectar eventos extremos (magnitudes muy altas o bajas)
    - Validar si los datos siguen patrones esperados según la ley de Gutenberg-Richter
    
    Args:
        df (pandas.DataFrame): DataFrame con columna 'magnitud'
        
    Returns:
        plotly.graph_objects.Figure: Gráfico de histograma o None si no hay datos
    """
    if "magnitud" not in df.columns or df.empty:
        return None

    fig = px.histogram(df, x="magnitud", nbins=50, 
                      color_discrete_sequence=['#1e40af'])

    fig.update_layout(
        showlegend=False,
        height=300,
        width=800,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title=dict(
                text='Magnitud',
                font=dict(size=20, family='Arial, sans-serif')
            ),
            tickfont=dict(size=16)
        ),
        yaxis=dict(
            title=dict(
                text='Conteo',
                font=dict(size=20, family='Arial, sans-serif')
            ),
            tickfont=dict(size=16)
        )
    )

    return fig


def torta(df):
    """
    Crea un gráfico de pastel (pie chart) mostrando las top 5 ubicaciones con más actividad sísmica.
    
    Este gráfico es útil para:
    - Identificar rápidamente las zonas más sísmicamente activas
    - Comparar la proporción de actividad entre diferentes regiones
    - Destacar visualmente la ubicación con mayor actividad (con efecto pull)
    - Proporcionar una vista resumen de la distribución geográfica
    
    Args:
        df (pandas.DataFrame): DataFrame con columna 'ciudad_o_pais'
        
    Returns:
        plotly.graph_objects.Figure: Gráfico de pastel o None si no hay datos
    """
    if "ciudad_o_pais" not in df.columns or df.empty:
        return None

    top = df["ciudad_o_pais"].value_counts().head(5).reset_index()
    top.columns = ["ciudad_o_pais", "Cantidad"]

    max_idx = top["Cantidad"].idxmax()

    pull_values = [0.1 if i == max_idx else 0 for i in range(len(top))]

    def truncar_texto(texto, max_len=10):
        if len(texto) > max_len:
            return texto[:max_len] + "..."
        else:
            return texto

    labels_leyenda = [  # Crear etiquetas truncadas para la leyenda con cantidad al costado
        f"{truncar_texto(ciudad)} ({cantidad})"
        for ciudad, cantidad in zip(top["ciudad_o_pais"], top["Cantidad"])
    ]

    fig = go.Figure(data=[go.Pie(
        labels=labels_leyenda,
        values=top["Cantidad"],
        pull=pull_values,
        marker=dict(colors=px.colors.sequential.Blues_r[:len(top)]),
        hoverinfo='label+value',
        textinfo='percent',
        textfont=dict(size=18, family='Arial, sans-serif'),
        hoverlabel=dict(font_size=16, font_family='Arial, sans-serif'),
    )])

    fig.update_layout(
        height=400,
        width=600,
        legend=dict(
            x=1.005,
            y=0.7,
            orientation='v',
            xanchor='left',
            yanchor='middle',
            font=dict(size=18, family='Arial, sans-serif'),
        ),
        margin=dict(l=50, r=150, t=40, b=50),
    )

    return fig


def map_m(data):
    """
    Crea un gráfico de línea temporal mostrando la tendencia mensual de terremotos.
    
    Este gráfico es crucial para:
    - Identificar patrones estacionales en la actividad sísmica
    - Detectar periodos de mayor o menor actividad
    - Analizar tendencias temporales a largo plazo
    - Correlacionar actividad sísmica con eventos específicos o ciclos naturales
    
    Args:
        data (pandas.DataFrame): DataFrame con columna 'fecha_crea'
        
    Returns:
        plotly.graph_objects.Figure: Gráfico de línea temporal o None si no hay datos
    """
    data_copy = data.copy()
    data_copy["month_year"] = data_copy["fecha_crea"].dt.to_period("M")  # fecha_crea ya es datetime, convertir a periodo mes
    monthly_counts = data_copy.groupby("month_year").size().reset_index(name="count")
    monthly_counts["month_year"] = monthly_counts["month_year"].astype(str)

    if monthly_counts.empty:
        return None

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=monthly_counts["month_year"],
            y=monthly_counts["count"],
            mode="lines+markers",
            fill="tonexty",
            fillcolor="rgba(59, 130, 246, 0.3)",
            line=dict(color="#1e40af", width=3),
            marker=dict(size=8, color="#10b981"),
            hovertemplate=(
                '<b>Mes:</b> %{x}<br>' +
                '<b>Cantidad de Terremotos:</b> %{y}<extra></extra>'
            )
        )
    )

    fig.update_layout(
        xaxis_title="Mes",
        yaxis_title="Cantidad de Terremotos",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1e40af"),
        showlegend=False,
        height=400,
        width=800,
    )

    return fig


def map_s(data):
    """
    Crea un gráfico radar polar mostrando la distribución de terremotos por día de la semana.
    
    Este gráfico es valioso para:
    - Analizar si existe variación en reportes sísmicos según el día de la semana
    - Detectar posibles sesgos en la recopilación de datos
    - Identificar patrones de actividad relacionados con ciclos semanales
    - Visualizar de forma circular y clara la distribución temporal semanal
    
    Args:
        data (pandas.DataFrame): DataFrame con columna 'fecha_crea'
        
    Returns:
        plotly.graph_objects.Figure: Gráfico radar polar o None si no hay datos
    """
    data_copy = data.copy()
    data_copy["day_of_week"] = data_copy["fecha_crea"].dt.day_name()

    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_counts = data_copy["day_of_week"].value_counts().reindex(day_order, fill_value=0)

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=day_counts.values,
            theta=day_counts.index,
            fill="toself",
            fillcolor="rgba(59, 130, 246, 0.3)",
            line=dict(color="#1e40af", width=3),
            marker=dict(size=10, color="#10b981"),
            hovertemplate=(
                '<b>Día:</b> %{theta}<br>' +
                '<b>Cantidad:</b> %{r}<extra></extra>'
            ),
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(day_counts.max() * 1.3, 5)],
                gridcolor="rgba(30, 64, 175, 0.3)",
                tickfont=dict(color="#1e40af", size=16),  # letra agrandada
                linecolor="#1e40af",
                linewidth=1,
            ),
            angularaxis=dict(
                tickfont=dict(color="#1e40af", size=18),  # letra agrandada
                linecolor="#1e40af",
                linewidth=1,
            ),
        ),
        showlegend=False,
        font=dict(family="Arial, sans-serif", color="#1e40af", size=16),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        margin=dict(l=50, r=50, t=40, b=50),
        height=400,
        width=500,
    )

    return fig


def map_h(data):
    """
    Crea un gráfico radar polar mostrando la distribución de terremotos por hora del día.
    
    Este gráfico es importante para:
    - Analizar si hay patrones horarios en la ocurrencia de terremotos
    - Detectar sesgos temporales en la recopilación o reporte de datos
    - Identificar horas pico de actividad sísmica reportada
    - Visualizar ciclos circadianos en la distribución de eventos sísmicos
    - Formato circular ideal para representar las 24 horas del día
    
    Args:
        data (pandas.DataFrame): DataFrame con columna 'hora_crea'
        
    Returns:
        plotly.graph_objects.Figure: Gráfico radar polar horario o None si no hay datos/error
    """
    if "hora_crea" not in data.columns:
        return None

    data["hora_crea"] = data["hora_crea"].apply(lambda x: x.strip() if isinstance(x, str) else x)  # Limpiar espacios solo en strings para evitar error .str en no-string

    data["hora_crea"] = pd.to_datetime(data["hora_crea"], format="%H:%M:%S", errors="coerce").dt.time  # Convertir a datetime.time, valores inválidos se vuelven NaT

    try:
        data_copy = data.copy()
        data_copy["hour"] = data_copy["hora_crea"].apply(lambda x: x.hour if pd.notna(x) else None)

        hour_counts = data_copy["hour"].value_counts().sort_index()
        all_hours = pd.Series(range(24))
        hour_counts = hour_counts.reindex(all_hours, fill_value=0)

        theta_all = [f"{h}:00" for h in hour_counts.index]  # Todas las horas para theta (puntos completos)

        fig = go.Figure()
        fig.add_trace(
            go.Scatterpolar(
                r=hour_counts.values,
                theta=theta_all,
                fill="toself",
                fillcolor="rgba(16, 185, 129, 0.3)",
                line=dict(color="#059669", width=3),
                marker=dict(size=10, color="#1e40af"),
                hovertemplate=(
                    '<b>Hora:</b> %{theta}<br>' +
                    '<b>Cantidad:</b> %{r}<extra></extra>'
                ),
            )
        )

        fig.update_layout(  # Mostrar ticks solo en horas pares, sin eliminar puntos
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(hour_counts.max() * 1.3, 5)],
                    gridcolor="rgba(5, 150, 105, 0.3)",
                    tickfont=dict(color="#059669", size=16),
                    linecolor="#059669",
                    linewidth=1,
                ),
                angularaxis=dict(
                    tickvals=[f"{h}:00" for h in range(0, 24, 2)],  # ticks solo en horas pares
                    ticktext=[f"{h}:00" for h in range(0, 24, 2)],
                    tickfont=dict(color="#059669", size=18),
                    linecolor="#059669",
                    linewidth=1,
                ),
            ),
            showlegend=False,
            font=dict(family="Arial, sans-serif", color="#059669", size=16),
            plot_bgcolor="rgba(255,255,255,0)",
            paper_bgcolor="rgba(255,255,255,0)",
            margin=dict(l=50, r=50, t=40, b=50),
            height=400,
            width=500,
        )

        return fig

    except Exception as e:
        print(f"Error al generar gráfico: {e}")
        return None
