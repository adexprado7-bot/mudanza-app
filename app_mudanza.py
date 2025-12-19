import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Mudanza Prime", page_icon="🚚", layout="centered")

# --- COLORES DE TU MARCA (Extraídos del Logo) ---
COLOR_PRIMARIO = "#2E004E"  # Morado oscuro del escudo
COLOR_SECUNDARIO = "#FFC300" # Amarillo intenso del arco
COLOR_TEXTO = "#1F2937"      # Gris oscuro para lectura

# --- ESTILOS CSS (DISEÑO VISUAL ACTUALIZADO) ---
st.markdown(f"""
    <style>
    /* IMPORTAR FUENTE MODERNA (Google Fonts) */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&display=swap');

    /* 1. FONDO GENERAL */
    .stApp {{
        background-color: #FFFFFF;
        font-family: 'Montserrat', sans-serif;
    }}
    
    /* 2. BARRA LATERAL (SIDEBAR) - AHORA ES MORADA */
    section[data-testid="stSidebar"] {{
        background-color: {COLOR_PRIMARIO};
    }}
    
    /* Textos de la barra lateral en BLANCO para contraste */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p {{
        color: #FFFFFF !important;
    }}
    
    /* Inputs de la barra lateral */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        color: {COLOR_TEXTO};
    }}

    /* 3. TÍTULO MODERNO (TIPOGRAFÍA ACTUAL) */
    .titulo-principal {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 800; /* Extra negrita */
        font-size: 40px;
        color: {COLOR_PRIMARIO};
        text-transform: uppercase;
        letter-spacing: -1px;
        margin-bottom: 0px;
    }}
    .subtitulo {{
        font-family: 'Montserrat', sans-serif;
        color: #666;
        font-size: 18px;
        margin-top: -10px;
    }}

    /* 4. CORRECCIÓN DE VISIBILIDAD DE TEXTOS (LADO DERECHO) */
    h1, h2, h3, p, span, div {{
        color: {COLOR_TEXTO};
    }}
    
    /* Métricas (Precios) grandes en Morado */
    div[data-testid="stMetricValue"] {{
        color: {COLOR_PRIMARIO} !important;
        font-weight: bold;
    }}
    div[data-testid="stMetricLabel"] {{
        color: {COLOR_TEXTO} !important;
    }}

    /* 5. BOTÓN AMARILLO (ESTILO "PRIME") */
    .stButton>button {{
        background-color: {COLOR_SECUNDARIO} !important;
        color: {COLOR_PRIMARIO} !important; /* Texto morado sobre amarillo */
        border-radius: 12px;
        border: none;
        font-weight: 800;
        font-size: 18px;
        text-transform: uppercase;
        box-shadow: 0 4px 14px 0 rgba(255, 195, 0, 0.39);
        transition: transform 0.2s;
    }}
    .stButton>button:hover {{
        transform: scale(1.02);
        background-color: #FFD60A !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA CON LOGO ---
col_logo, col_titulo = st.columns([1, 3])

with col_logo:
    # Intentamos mostrar el logo
    try:
        st.image("logo.jpg", width=130)
    except:
        st.write("🚚") 

with col_titulo:
    st.markdown('<p class="titulo-principal">MUDANZA PRIME</p>', unsafe_allow_html=True)
    st.write("Cotizador Inteligente 2.0")

st.divider()

# --- BARRA LATERAL (INPUTS) ---
st.sidebar.header("🛠️ Configuración")

# Selección de Vehículo
opciones_vehiculo = {
    "Furgoneta (Pequeña)": {"precio": 30, "cap": 6, "icon": "🚐"},
    "Camión 2 Toneladas": {"precio": 40, "cap": 12, "icon": "🚛"},
    "Camión 3.5 Toneladas": {"precio": 50, "cap": 20, "icon": "🚚"},
    "Camión 6 Toneladas": {"precio": 60, "cap": 35, "icon": "🚛🚛"}
}

seleccion = st.sidebar.selectbox("Selecciona Vehículo:", list(opciones_vehiculo.keys()))
datos_camion = opciones_vehiculo[seleccion]

st.sidebar.markdown("---")

# Inputs Básicos
st.sidebar.subheader("📍 Ruta y Equipo")
distancia = st.sidebar.number_input("Distancia (km):", min_value=1, value=10)
costo_km = 1.0 
personal = st.sidebar.slider("Ayudantes:", 0, 6, 2)

st.sidebar.markdown("---")

# Inputs de Materiales
st.sidebar.subheader("📦 Materiales")
cajas = st.sidebar.number_input("Cartones ($1.50):", 0, 50, 10)
rollos = st.sidebar.number_input("Rollos Embalaje ($20):", 0, 10, 1)

# Servicios Premium
st.sidebar.markdown("---")
st.sidebar.subheader("💎 Servicios Extra")
proteccion_delicada = st.sidebar.checkbox("Protección Delicados (+$50)")
costo_delicados = 50 if proteccion_delicada else 0

servicio_empaque = st.sidebar.radio(
    "Servicio de Empaque:",
    ["Cliente empaca ($0)", 
     "Básico (+$30)", 
     "Completo (+$50)"]
)

if "Básico" in servicio_empaque:
    costo_empaque = 30
elif "Completo" in servicio_empaque:
    costo_empaque = 50
else:
    costo_empaque = 0

# --- INVENTARIO ---
st.sidebar.markdown("---")
detalle_inventario = st.sidebar.text_area(
    "📝 Lista de muebles principales:",
    placeholder="Ej: Cama, Refri, Sofá..."
)

# --- CÁLCULOS ---
costo_base_camion = datos_camion["precio"]
costo_total_personal = personal * 15
costo_total_cajas = cajas * 1.50
costo_total_rollos = rollos * 20
costo_distancia = distancia * costo_km

total_materiales = costo_total_cajas + costo_total_rollos + costo_delicados
total_servicios = costo_base_camion + costo_total_personal + costo_empaque + costo_distancia

gran_total = total_materiales + total_servicios

# Lógica visual de llenado
volumen_estimado = (cajas * 0.1) + (personal * 1.5)
porcentaje_ocupacion = min(volumen_estimado / datos_camion["cap"], 1.0)

# --- PANTALLA PRINCIPAL ---

col1, col2 = st.columns(2)

with col1:
    st.subheader("Tu Selección")
    # Tarjeta visual con estilo
    st.info(f"""
    **Vehículo:** {seleccion}  
    **Distancia:** {distancia} km  
    **Personal:** {personal} ayudantes
    """)
    
    if detalle_inventario:
        st.caption(f"**📦 Inventario:** {detalle_inventario}")
    
    st.write("")
    st.write("**Ocupación del Camión:**")
    st.progress(porcentaje_ocupacion)
    if porcentaje_ocupacion > 0.85:
        st.warning("⚠️ ¡Espacio crítico!")

with col2:
    st.subheader("Presupuesto Final")
    
    # Tabla de desglose limpia
    st.markdown(f"""
    | Concepto | Precio |
    | :--- | :---: |
    | 🚛 Vehículo | ${costo_base_camion} |
    | 👷 Personal | ${costo_total_personal} |
    | 🛣️ Distancia | ${costo_distancia:.2f} |
    | 📦 Materiales | ${total_materiales:.2f} |
    | ✨ Servicios | ${costo_empaque} |
    """)
    
    st.divider()
    st.metric(label="TOTAL A PAGAR", value=f"${gran_total:.2f}")

# --- BOTÓN WHATSAPP ---
mi_numero = "593999999999"  # <--- TU NÚMERO AQUÍ

mensaje = f"""Hola Mudanza Prime 🚛
Solicito reserva:
- *Total:* ${gran_total:.2f}
- *Vehículo:* {seleccion}
- *Distancia:* {distancia}km
- *Detalle:* {detalle_inventario}
"""
import urllib.parse
link_whatsapp = f"https://wa.me/{mi_numero}?text={urllib.parse.quote(mensaje)}"

st.write("")
st.markdown(f"""
    <a href="{link_whatsapp}" target="_blank" style="text-decoration: none;">
        <button style="width: 100%; padding: 15px; font-size: 20px; cursor: pointer;">
            RESERVAR AHORA 📲
        </button>
    </a>
    """, unsafe_allow_html=True)
