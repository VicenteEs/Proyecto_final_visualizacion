# 🌍 Dashboard de Análisis Sísmico Global
### Visualización y Análisis de Datos de Terremotos en Tiempo Real

<div align="center">
  
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)

</div>

---

## 📖 **Motivación y Contexto Académico**

Este proyecto fue desarrollado por **David Sepúlveda** y **Vicente Escudero**, estudiantes de **Ingeniería Civil en Ciencia de Datos** de la **Universidad Tecnológica Metropolitana (UTEM)**, como parte del curso de **Visualización de Datos**.

### 🎯 **Objetivo del Proyecto**

El proyecto implementa el **ciclo completo de los datos** en el contexto de análisis sísmico global:

1. **🔍 Minería de Datos**: Extracción automatizada de información sísmica desde Reddit
2. **⚙️ Procesamiento**: Limpieza, transformación y enriquecimiento con IA
3. **📊 Presentación**: Visualización interactiva y análisis geoespacial

### 🌋 **Motivación Científica**

- **Exploración del Cinturón de Fuego del Pacífico**: Análisis de patrones sísmicos globales
- **Datos de fuentes no convencionales**: Transformar información social en datos científicos
- **Visualización geoespacial avanzada**: Representación interactiva de fenómenos naturales
- **Análisis en tiempo real**: Monitoreo continuo de actividad sísmica

---

## ✨ **Características Principales**

### 📊 **Dashboard Interactivo**
- **Mapa global 3D** con visualización de terremotos y volcanes
- **Métricas en tiempo real** de actividad sísmica
- **Filtros avanzados** por fecha, magnitud, ubicación y fuentes oficiales
- **Análisis de tendencias** temporales (mensual, semanal, horaria)

### 🔍 **Exploración de Datos**
- **Tabla interactiva** con todos los eventos sísmicos
- **Exportación de datos** filtrados
- **Análisis estadístico** detallado

### 📢 **Presentación del Proyecto**
- **Slides informativos** sobre metodología y resultados
- **Comparación visual** con el Cinturón de Fuego
- **Métricas de rendimiento** del sistema

### 🤖 **Tecnologías Avanzadas**
- **PRAW**: Scraping automatizado de Reddit
- **Google Gemini AI**: Procesamiento inteligente de texto
- **PyDeck**: Visualización 3D geoespacial
- **Streamlit**: Interface web interactiva

---

## 🏗️ **Arquitectura del Proyecto**

```
📁 PROYECTO_FINAL_VISUALIZACION/
├── 📁 data/                          # Datos y recursos
│   ├── 📄 Earthquakes_posts_new.csv   # Dataset principal
│   ├── 📄 volcanoes_selected_columns.csv # Datos de volcanes
│   ├── 🖼️ flujo.png                   # Diagrama del flujo
│   ├── 🖼️ logocolor.png               # Logo de UTEM
│   └── 🖼️ r_Earthquakes.png           # Mapa del subreddit
├── 📁 paginas/                       # Módulos de la interfaz
│   ├── 📄 dashboard.py                # Página principal
│   ├── 📄 exploracion.py              # Análisis de datos
│   ├── 📄 presentacion.py             # Slides del proyecto
│   ├── 📄 sidebar.py                  # Navegación lateral
│   ├── 📄 styles.py                   # Estilos CSS
│   └── 📄 utils.py                    # Utilidades
├── 📄 main.py                        # Aplicación principal
├── 📄 graficos.py                    # Funciones de visualización
├── 📄 scraping.py                    # Extracción de Reddit
├── 📄 procesado.py                   # Procesamiento con IA
├── 📄 credenciales.py                # Configuración de APIs
└── 📄 requirement.txt                # Dependencias
```

---

## 🚀 **Guía de Instalación y Configuración**

### 📋 **Requisitos Previos**
- **Python 3.12.4**
- **Conexión a Internet** (para APIs de Reddit y Gemini)
- **Cuentas en**: Reddit y Google AI Studio (ambas gratuitas)

---

### **Paso 1: 📥 Clonar o Descargar el Proyecto**

```bash
# Opción A: Clonar repositorio
git clone https://github.com/VicenteEs/Proyecto_final_visualizacion
cd Proyecto_final_visualizacion

```

---

### **Paso 2: 🐍 Configurar Entorno Virtual**

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Windows:
.venv\Scripts\activate
# En macOS/Linux:
source .venv/bin/activate
```

---

### **Paso 3: 📦 Instalar Dependencias**

```bash
# Instalar todas las librerías necesarias
pip install -r requirement.txt

# O instalar manualmente:
pip install streamlit pandas numpy plotly matplotlib pydeck praw google-generativeai 
```

---

### **Paso 4: 🔑 Configurar APIs (CRÍTICO)**

#### **4.1 Configurar Reddit API (PRAW)**

1. **Ir a Reddit Apps**: [https://www.reddit.com/prefs/apps/](https://www.reddit.com/prefs/apps/)
2. **Crear nueva aplicación**:
   - Hacer clic en **"Create App"** o **"Create Another App"**
   - **Name**: `Dashboard-Sismica-UTEM` (o el nombre que prefieras)
   - **App type**: Seleccionar **"script"**
   - **Description**: `Análisis de datos sísmicos para proyecto universitario`
   - **About URL**: Dejar vacío
   - **Redirect URI**: `http://localhost:8501` (requerido pero no usado)
3. **Obtener credenciales**:
   - **Client ID**: Texto pequeño bajo el nombre de la app
   - **Client Secret**: Texto largo después de "secret"
   - **User Agent**: Tu nombre de usuario de Reddit

#### **4.2 Configurar Google Gemini AI**

1. **Ir a Google AI Studio**: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. **Crear API Key**:
   - Hacer clic en **"Create API Key"**
   - Seleccionar tu proyecto de Google Cloud (o crear uno nuevo)
   - Copiar la **API Key** generada

#### **4.3 Actualizar archivo de credenciales**

Editar el archivo `credenciales.py`:

```python
####   Credenciales de las API  ####

""" REDDIT """
a = "TU_CLIENT_ID_AQUI"           # Client ID de Reddit
b = "TU_CLIENT_SECRET_AQUI"       # Client Secret de Reddit  
c = "TU_USERNAME_REDDIT_AQUI"     # Tu username de Reddit

""" GEMINI  """
d = "TU_API_KEY_GEMINI_AQUI"      # API Key de Google Gemini
```

⚠️ **IMPORTANTE**: 
- **NO compartas estas credenciales** en repositorios públicos
- Mantén el archivo `credenciales.py` privado
- Las credenciales deben ser **reales y activas**

---

### **Paso 5: 🎮 Ejecutar la Aplicación**

```bash
# Asegúrate de estar en el directorio del proyecto
cd Proyecto_final_visualizacion

# Activar entorno virtual (si no está activo)
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Ejecutar la aplicación
streamlit run main.py
```

**La aplicación se abrirá automáticamente en**: `http://localhost:8501`

---

## 🔧 **Configuraciones Adicionales**

### **📊 Datos Iniciales**
- El proyecto incluye un dataset con **4,400+ eventos sísmicos**
- Los datos están en `data/Earthquakes_posts_new.csv`
- **No es necesario** descargar datos adicionales para la primera ejecución

### **🔄 Actualización de Datos en Tiempo Real**
- Usar el botón **"🔄 Actualizar datos"** en el dashboard
- Requiere **credenciales configuradas** correctamente
- Extrae los **últimos 10-15 posts** del subreddit r/Earthquakes

### **🌋 Datos de Volcanes**
- Incluidos en `data/volcanoes_selected_columns.csv`
- Se muestran cuando activas **"Mostrar volcanes"** en el sidebar

---

## 🎯 **Uso de la Aplicación**

### **📊 Dashboard Principal**
1. **Filtros disponibles**:
   - 📅 **Rango de fechas**: Seleccionar período específico
   - 📊 **Magnitud**: Filtrar por intensidad sísmica
   - 📍 **Ubicaciones**: Seleccionar países/regiones
   - ✅ **Solo oficiales**: Mostrar solo datos de BrainstormBot

2. **Visualizaciones**:
   - 🗺️ **Mapa 3D interactivo** con eventos sísmicos
   - 📊 **Distribución de magnitudes**
   - 📍 **Top 5 ubicaciones más activas**
   - 📅 **Tendencias temporales** (mensual, semanal, horaria)

### **🔍 Exploración de Datos**
- **Tabla interactiva** con todos los eventos
- **Selección de columnas** a mostrar
- **Exportación** de datos filtrados

### **📢 Presentación**
- **Slides informativos** sobre el proyecto
- **Comparación** con el Cinturón de Fuego del Pacífico
- **Métricas y resultados** obtenidos

---

## 🛠️ **Solución de Problemas Comunes**

### **❌ Error: "No se pueden obtener datos de Reddit"**
- ✅ Verificar credenciales de Reddit en `credenciales.py`
- ✅ Comprobar conexión a internet
- ✅ Asegurar que la aplicación de Reddit esté activa

### **❌ Error: "Google API Error"**
- ✅ Verificar API Key de Gemini sin espacion dentro de la comillas
- ✅ Comprobar que el proyecto de Google Cloud esté activo
- ✅ Verificar cuota de la API

### **❌ Error: "Module not found"**
- ✅ Activar el entorno virtual
- ✅ Reinstalar dependencias: `pip install -r requirement.txt`

### **❌ Error: "Permission denied"**
- ✅ Ejecutar como administrador (si es necesario)
- ✅ Verificar permisos del directorio

---

## 📈 **Características Técnicas**

### **🔧 Stack Tecnológico**
- **Frontend**: Streamlit (Python)
- **Visualización**: Plotly, PyDeck, Matplotlib
- **Datos**: Pandas, NumPy
- **APIs**: PRAW (Reddit), Google Generative AI
- **Procesamiento**: Regex, NLP básico

### **⚡ Rendimiento**
- **Carga inicial**: ~3-5 segundos
- **Actualización de datos**: ~10-30 segundos
- **Filtros en tiempo real**: Instantáneo
- **Memoria requerida**: ~200-500 MB

### **🎨 Interfaz**
- **Diseño responsivo** adaptable a diferentes pantallas
- **Tema oscuro/claro** automático según preferencias del sistema
- **CSS personalizado** para mejorar la experiencia visual

---

## 👥 **Créditos y Autoría**

**Desarrolladores**: 
- 👨‍💻 **David Sepúlveda** - Estudiante de Ingeniería Civil en Ciencia de Datos
- 👨‍💻 **Vicente Escudero** - Estudiante de Ingeniería Civil en Ciencia de Datos

**Institución**: 
- 🏫 **Universidad Tecnológica Metropolitana (UTEM)**
- 📚 **Curso**: Visualización de Datos
- 📅 **Año**: 2025

**Agradecimientos**:
- 🌍 **Comunidad r/Earthquakes** por proporcionar datos sísmicos
- 🤖 **Google Gemini AI** por el procesamiento inteligente de texto
- 📊 **Streamlit Community** por la plataforma de desarrollo

---

## 📄 **Licencia y Uso Académico**

Este proyecto es de **uso académico** desarrollado para fines educativos en el curso de Visualización de Datos de UTEM.

**Términos de uso**:
- ✅ Libre para **uso educativo y académico**
- ✅ Se permite **modificación y mejora**
- ⚠️ **Creditar** a los autores originales
- ❌ **No para uso comercial** sin autorización

---

## 🚀 **Próximas Mejoras**

- 🔄 **Actualización automática** cada X minutos
- 📱 **Versión móvil** optimizada
- 🌐 **Soporte multiidioma** (Inglés/Español)
- 📊 **Más fuentes de datos** sísmicos
- 🤖 **IA avanzada** para predicción sísmica

---

<div align="center">

### 🌟 **¡Gracias por explorar nuestro proyecto!** 🌟

Si tienes preguntas o sugerencias, no dudes en contactarnos.

**Universidad Tecnológica Metropolitana** | **Ingeniería Civil en Ciencia de Datos** | **2025**

</div>
