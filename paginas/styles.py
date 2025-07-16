import streamlit as st

def inject_css():
    """
    Función que inyecta estilos CSS personalizados para toda la aplicación,
    incluyendo estilos para métricas, botones, títulos, navegación y layout general.
    Define variables CSS y estilos responsivos para mejorar la apariencia visual.
    """
    st.markdown("""
    <style>
        :root {  /* Variables CSS */
            --utem-blue: #1e40af;
            --utem-light-blue: #3b82f6;
            --utem-green: #10b981;
            --utem-dark-green: #059669;
            --utem-bg: #f8fafc;
        }
            button[data-testid="stButton"] {  /* Estilo para el botón "Actualizar datos" */
                background-color: #10b981 !important;  /* verde */
                color: white !important;
                font-size: 1.3rem !important;  /* más grande */
                padding: 0.8rem 1.5rem !important;
                border-radius: 10px !important;
                border: none !important;
                box-shadow: 0 4px 8px rgba(16, 185, 129, 0.5) !important;
                transition: background-color 0.3s ease;
            }
            button[data-testid="stButton"]:hover {
                background-color: #059669 !important; /* verde oscuro */
            }

        .main .block-container {  /* Estilos generales */
            padding-top: 0.1rem;
            padding-bottom: 0rem;
        }
        
        .metric-card {
            background: linear-gradient(135deg, var(--utem-blue), var(--utem-light-blue));
            color: white;
            padding: 10px;
            border-radius: 25px;
            box-shadow: 0 8px 25px rgba(30, 64, 175, 0.15);
            text-align: center;
            border: 2px solid rgba(16, 185, 129, 0.3);
            transition: transform 0.3s ease;
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 120px;
        }

        .metric-card:hover {
            transform: translateY(-10px) !important;
            box-shadow: 0 120px 35px rgba(30, 64, 175, 0.25) !important;
        }

        .metric-card .metric-label {
            font-size: 1.5rem !important;
            opacity: 0.9 !important;
            margin-bottom: 0 px !important;
            color: white !important;
            font-weight: 600 !important;
        }

        .metric-card .metric-value {
            font-size: 2.2rem !important;
            font-weight: bold !important;
            margin: 0 !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
            color: white !important;
        }

        .chart-container {
            background: white !important;
            font-size: 1.5rem !important;
            text-align: center !important;
            border-radius: 15px !important;
            padding: 0rem !important;
            box-shadow: 0 10px 15px rgba(0,0,0,0.3) !important;
            border-left: 10px solid var(--utem-green) !important;
            margin-bottom: 0rem !important;
            margin-top: 0.5rem !important;
            min-height: 5px !important;

            position: relative !important;  /* Posicionar para que z-index funcione */
            z-index: 10 !important;          /* Número alto para estar al frente */
        }

        .main-title {  /* Títulos principales */
            background: linear-gradient(90deg, var(--utem-blue), var(--utem-green)) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            text-align: center !important;
            font-size: 3rem !important;
            font-weight: bold !important;
            margin-bottom: 0.2rem !important;
            margin-top: 0rem !important;
        } 

        .subtitle {  /* Subtítulos */
            text-align: center !important;
            color: var(--utem-blue) !important;
            font-size: 1.2rem !important;
            margin-bottom: 1rem !important;
        }

        .slide-nav {  /* Navegación de diapositivas */
            padding: 0.5rem 1rem !important;
            margin-bottom: 0.5rem !important;
            border-radius: 10px !important;
            cursor: pointer !important;
            transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease !important;
            background: #f1f5f9 !important;
            border: 1px solid #e2e8f0 !important;
            font-size: 16px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
        }

        .slide-nav.active {
            background: rgba(0, 123, 255, 0.3) !important; 
            color: white !important;
            font-weight: bold !important;
            box-shadow: 0 4px 12px rgba(0, 123, 255, 0.5) !important; 
            border-color: rgba(0, 123, 255, 0.5) !important;
        }

        .slide-nav:hover {
            background: var(--utem-light-blue) !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(0, 123, 255, 0.4) !important;
        }

        .css-1d391kg {  /* Sidebar personalizada */
            padding-top: 0rem !important;
        }


        [data-testid="metric-container"] {  /* Métricas de Streamlit personalizadas */
            background: linear-gradient(135deg, var(--utem-blue), var(--utem-light-blue)) !important;
            border: 2px solid rgba(16, 185, 129, 0.3) !important;
            padding: 1rem !important;
            border-radius: 15px !important;
            color: white !important;
            box-shadow: 0 8px 25px rgba(30, 64, 175, 0.15) !important;
        }

        [data-testid="metric-container"] > div {
            color: white !important;
        }

        [data-testid="metric-container"] label {
            color: white !important;
            opacity: 0.9 !important;
        }

        .stTabs [data-baseweb="tab-list"] {  /* Tabs personalizadas */
            gap: 8px !important;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: #f1f5f9 !important;
            border-radius: 10px !important;
            color: var(--utem-blue) !important;
            font-weight: 600 !important;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--utem-blue), var(--utem-green)) !important;
            color: white !important;
        }
        
        footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background: linear-gradient(90deg, #1e3c72, #2a5298, #4CAF50);
            color: white;
            text-align: center;
            padding: 15px;
            font-size: 14px;
            z-index: 1000; /* más alto para sobreponer */
            opacity: 0.9; /* opcional, para que se vea un poco transparente */
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
    
    
def hide_streamlit_header():
    """
    Función que oculta el header por defecto de Streamlit para tener
    un diseño más limpio y personalizado en la aplicación.
    """
    st.markdown("""
        <style>
            header.stAppHeader {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)
