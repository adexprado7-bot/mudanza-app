import streamlit as st
import datetime
import random
import urllib.parse

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Mudanza Prime", page_icon="🚚", layout="centered")

# --- INTERRUPTOR DE MODO (TOGGLE) ---
st.sidebar.header("⚙️ Configuración Visual")
modo_oscuro = st.sidebar.toggle("🌙 Modo Oscuro", value=False)

# --- DEFINICIÓN DE PALETAS DE COLORES DINÁMICAS ---
COLOR_PRIMARIO_MARCA = "#2E004E"   # Morado (Logo)
COLOR_SECUNDARIO_MARCA = "#FFC300" # Amarillo (Botones)

if modo_oscuro:
    # === PALETA NOCTURNA ===
    FONDO_APP = "#0E1117"        # Fondo principal negro suave
    COLOR_TEXTO = "#FAFAFA"      # Texto general blanco
    
    # Barra Lateral Oscura
    SIDEBAR_BG = "#1A1F2C"       # Carbón oscuro
    SIDEBAR_TEXT = "#FFFFFF"     # Texto blanco en barra
    
    # Detalles
    COLOR_TITULO = "#A970FF"     # Morado brillante (Neón)
    COLOR_INPUTS = "#262730"     # Fondo de cajas de texto
else:
    # === PALETA DIURNA (CLARO) ===
    FONDO_APP = "#FFFFFF"        # Fondo principal blanco puro
    COLOR_TEXTO = "#1F2937"      # Texto general gris oscuro
    
    # Barra Lateral Clara
    SIDEBAR_BG = "#F8F9FA"       # Gris muy suave (casi blanco) para diferenciar
    SIDEBAR_TEXT = "#1F2937"     # Texto oscuro en barra
    
    # Detalles
    COLOR_TITULO = "#2E004E"     # Morado original elegante
    COLOR_INPUTS = "#FFFFFF"     # Fondo de cajas blanco

# --- ESTILOS CSS DINÁMICOS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&display=swap');

    /* 1. FONDO GENERAL */
    .stApp {{
        background-color: {FONDO_APP};
        font-family: 'Montserrat', sans-serif;
    }}
    
    /* 2. TEXTOS GENERALES (Cuerpo) */
    h1, h2, h3, h4, p, li, .stMarkdown, .stTable {{
        color: {COLOR_TEXTO} !important;
    }}
    
    /* 3. BARRA LATERAL (DINÁMICA) */
    section[data-testid="stSidebar"] {{
        background-color: {SIDEBAR_BG};
        border-right: 1px solid rgba(46, 0, 78, 0.1); /* Borde sutil */
    }}
    
    /* Textos dentro de la barra lateral */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div.stMarkdown {{
        color: {SIDEBAR_TEXT} !important;
    }}
    
    /* 4. TÍTULO PRINCIPAL */
    .titulo-principal {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 48px;
        color: {COLOR_TITULO} !important;
        text-transform: uppercase;
        letter-spacing: -1px;
        line-height: 1.2;
    }}

    /* 5. BOTÓN PRINCIPAL */
    .stButton>button {{
        background-color: {COLOR_SECUNDARIO_MARCA} !important;
        color: {COLOR_PRIMARIO_MARCA} !important;
        border-radius: 12px;
        border: none;
        font-weight: 800;
        font-size: 18px;
        text-transform: uppercase;
        box-shadow: 0 4px 14px 0 rgba(255, 195, 0, 0.39);
        width: 100%;
        padding: 15px 0;
        transition: transform 0.2s;
    }}
    .stButton>button:hover {{ transform: scale(1.02); }}
    
    /* 6. INPUTS Y CAJAS (Para que se lean en ambos modos) */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {{
        color: {COLOR_TEXTO} !important;
        background-color: {COLOR_INPUTS};
    }}
    
    /* 7. CAJAS DE HORARIOS */
    .horario-box {{ padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 8px; font-weight: bold; }}
    .disponible {{ background-color: #D1FAE5; color: #065F46; border: 1px solid #34D399; }}
    .ocupado {{ background-color: #FEE2E2; color: #991B1B; border: 1px solid #F87171; }}
    
    /* 8. MÉTRICAS (PRECIOS) */
    div[data-testid="stMetricValue"] {{ 
        color: {COLOR_TITULO} !important; 
    }}
    div[data-testid="stMetricLabel"] {{ 
        color: {COLOR_TEXTO} !important; 
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
col_logo, col_titulo = st.columns([1, 3])
with col_logo:
    try: st.image("logo.jpg", width=140)
    except: st.write("🚚") 
with col_titulo:
    st.markdown('<p class="titulo-principal">MUDANZA PRIME</p>', unsafe_allow_html=True)

st.divider()

# --- SIDEBAR (CONFIGURACIÓN) ---
st.sidebar.header("🛠️ Configura tu Mudanza")

opciones_vehiculo = {
    "Furgoneta (Pequeña)": {"precio": 30, "cap": 6, "icon": "🚐"},
    "Camión 2 Toneladas": {"precio": 40, "cap": 12, "icon": "🚛"},
    "Camión 3.5 Tonel
