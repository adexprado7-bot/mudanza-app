import streamlit as st
import datetime
import random
import urllib.parse

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Mudanza Prime", page_icon="🚚", layout="centered")

# --- INTERRUPTOR DE MODO (TOGGLE) ---
st.sidebar.header("⚙️ Configuración Visual")
modo_oscuro = st.sidebar.toggle("🌙 Activar Modo Oscuro", value=False)

# --- DEFINICIÓN DE COLORES ---
COLOR_PRIMARIO_MARCA = "#2E004E"   # Morado
COLOR_SECUNDARIO_MARCA = "#FFC300" # Amarillo

if modo_oscuro:
    # === PALETA NOCTURNA ===
    FONDO_APP = "#0E1117"        
    COLOR_TEXTO = "#FFFFFF"      
    SIDEBAR_BG = "#1A1F2C"       
    SIDEBAR_TEXT = "#FFFFFF"     
    COLOR_TITULO = "#A970FF"     # Morado neón
    COLOR_INPUTS = "#262730"     
else:
    # === PALETA DIURNA ===
    FONDO_APP = "#FFFFFF"        
    COLOR_TEXTO = "#1F2937"      
    SIDEBAR_BG = "#F3F4F6"       
    SIDEBAR_TEXT = "#000000"     
    COLOR_TITULO = "#2E004E"     
    COLOR_INPUTS = "#FFFFFF"     

# --- ESTILOS CSS (SOLUCIÓN DE LETRAS FANTASMAS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700;800&display=swap');

    /* 1. FONDO GENERAL */
    .stApp {{ background-color: {FONDO_APP}; font-family: 'Montserrat', sans-serif; }}
    
    /* 2. TEXTOS */
    h1, h2, h3, h4, p, li, .stMarkdown, .stTable, .stMetricLabel {{ color: {COLOR_TEXTO} !important; }}
    
    /* 3. BARRA LATERAL */
    section[data-testid="stSidebar"] {{ background-color: {SIDEBAR_BG}; }}
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] div {{
        color: {SIDEBAR_TEXT} !important;
    }}
    
    /* 4. SOLUCIÓN LOGO (Estilo Insignia) */
    div[data-testid="stImage"] img {{
        background-color: white;
        padding: 8px;
        border-radius: 12px;
    }}

    /* 5. TÍTULO Y SLOGAN */
    .titulo-principal {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 45px;
        color: {COLOR_TITULO} !important;
        text-transform: uppercase;
        letter-spacing: -1px;
        line-height: 1.0;
        margin-bottom: 0;
    }}
    .slogan {{
        font-family: 'Montserrat', sans-serif;
        font-size: 18px;
        font-weight: 500;
        color: {COLOR_TEXTO};
        opacity: 0.8;
        font-style: italic;
        margin-top: -10px;
    }}

    /* 6. CORRECCIÓN SUPREMA DE DROPDOWNS (Menús Desplegables) */
    /* Esto fuerza a que la lista desplegable SIEMPRE sea blanca con letras negras */
    ul[data-testid="stSelectboxVirtualDropdown"] {{
        background-color: white !important;
    }}
    ul[data-testid="stSelectboxVirtualDropdown"] li {{
        color: black !important;
        background-color: white !important;
    }}
    /* Color al pasar el mouse por encima de una opción */
    ul[data-testid="stSelectboxVirtualDropdown"] li:hover {{
        background-color: #FFC300 !important; /* Amarillo marca */
        color: black !important;
    }}
    
    /* El texto de la caja cerrada */
    div[data-baseweb="select"] > div {{
        background-color: {COLOR_INPUTS} !important;
        color: {COLOR_TEXTO} !important;
    }}
    
    /* 7. INPUTS GENERALES */
    .stNumberInput input, .stTextArea textarea {{
        color: {COLOR_TEXTO} !important;
        background-color: {COLOR_INPUTS};
    }}

    /* 8. BOTÓN AMARILLO */
    .stButton>button {{
        background-color: {COLOR_SECUNDARIO_MARCA} !important;
        color: {COLOR_PRIMARIO_MARCA} !important;
        border-radius: 12px; border: none; font-weight: 800; font-size: 18px; width: 100%; padding: 15px 0;
        box-shadow: 0 4px 14px 0 rgba(255, 195, 0, 0.4);
    }}
    
    /* 9. CAJAS DE HORARIOS */
    .horario-box {{ padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 8px; font-weight: bold; font-size: 14px; }}
    .disponible {{ background-color: #D1FAE5; color: #065F46; border: 1px solid #34D399; }}
    .ocupado {{ background-color: #FEE2E2; color: #991B1B; border: 1px solid #F87171; }}
    
    /* 10. MÉTRICAS */
    div[data-testid="stMetricValue"] {{ color: {COLOR_TITULO} !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
col_logo, col_titulo = st.columns([1, 3])
with col_logo:
    try: st.image("logo.jpg", width=130)
    except: st.write("🚚") 
with col_titulo:
    st.markdown('<p class="titulo-principal">MUDANZA PRIME</p>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">Movemos lo que más quieres.</p>', unsafe_allow_html=True)

st.divider()

# --- SIDEBAR ---
st.sidebar.header("🛠️ Cotización")

# SELECCIÓN DE VEHÍCULO
opciones_vehiculo = {
    "Furgoneta (Pequeña)": {"precio": 30, "cap": 6},
    "Camión 2 Toneladas": {"precio": 40, "cap": 12},
    "Camión 3.5 Toneladas": {"precio": 50, "cap": 20},
    "Camión 6 Toneladas": {"precio": 60, "cap": 35}
}
seleccion = st.sidebar.selectbox("Selecciona Vehículo:", list(opciones_vehiculo.keys()))
datos_camion = opciones_vehiculo[seleccion]

st.sidebar.markdown("---")
distancia = st.sidebar.number_input("Distancia (km):", 1, 500, 10)
personal = st.sidebar.slider("Ayudantes:", 0, 6, 2)

st.sidebar.markdown("---")
st.sidebar.subheader("📦 Materiales")
cajas = st.sidebar.number_input("Cartones ($1.50):", 0, 100, 10)
rollos = st.sidebar.number_input("Rollos ($20):", 0, 20, 1)

# --- SERVICIOS PREMIUM ---
st.sidebar.markdown("---")
st.sidebar.subheader("💎 Servicios Extra")

proteccion_delicada = st.sidebar.checkbox("Protección Delicados (+$50)")
costo_delicados = 50 if proteccion_delicada else 0

servicio_empaque = st.sidebar.radio(
    "Servicio de Empaque:",
    ["Cliente empaca ($0)", "Básico (+$30)", "Completo (+$50)"]
)
if "Básico" in servicio_empaque: costo_empaque = 30
elif "Completo" in servicio_empaque: costo_empaque = 50
else: costo_empaque = 0

# --- AGENDA ---
st.subheader("📅 Agenda tu Fecha y Hora")
col_fecha, col_hora = st.columns(2)
with col_fecha:
    fecha_seleccionada = st.date_input("Selecciona el día:", min_value=datetime.date.today())

random.seed(f"{fecha_seleccionada}_{seleccion}") 
ocupacion_simulada = random.choice([[False,False,False], [True,False,False], [False,True,False]])
horarios = [
    {"hora": "08:00 AM - 12:00 PM", "ocupado": ocupacion_simulada[0]},
    {"hora": "11:00 AM - 03:00 PM", "ocupado": ocupacion_simulada[1]},
    {"hora": "02:00 PM - 06:00 PM", "ocupado": ocupacion_simulada[2]},
]

with col_hora:
    st.write(f"Disponibilidad: **{seleccion}**")
    opciones_disponibles = []
    for turno in horarios:
        if turno["ocupado"]:
            st.markdown(f'<div class="horario-box ocupado">🔴 {turno["hora"]} (Ocupado)</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="horario-box disponible">🟢 {turno["hora"]} (Libre)</div>', unsafe_allow_html=True)
            opciones_disponibles.append(turno["hora"])

    if opciones_disponibles:
        hora_final = st.selectbox("Elige tu horario:", opciones_disponibles)
    else:
        hora_final = "Sin disponibilidad"
        st.warning("Día completo.")

st.divider()

# --- CÁLCULOS ---
costo_base = datos_camion["precio"]
costo_personal = personal * 15
costo_materiales = (cajas * 1.50) + (rollos * 20) + costo_delicados
costo_distancia = distancia * 1.0
gran_total = costo_base + costo_personal + costo_materiales + costo_distancia + costo_empaque

# --- RESUMEN ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("Tu Reserva")
    st.info(f"""
    **📅 Fecha:** {fecha_seleccionada}  
    **⏰ Hora:** {hora_final}  
    **🚛 Vehículo:** {seleccion}
    """)
    st.write(f"**Extras:** {servicio_empaque} | Protec: {'Sí' if proteccion_delicada else 'No'}")

with col2:
    st.subheader("Presupuesto")
    st.markdown(f"""
    | Concepto | Valor |
    | :--- | :---: |
    | Vehículo | ${costo_base} |
    | Personal | ${costo_personal} |
    | Materiales/Extras | ${costo_materiales + costo_empaque} |
    | Distancia | ${costo_distancia} |
    """)
    st.metric(label="TOTAL ESTIMADO", value=f"${gran_total:.2f}")

# --- BOTÓN WHATSAPP ---
mensaje = f"Hola Mudanza Prime! 🚛\nReserva: {fecha_seleccionada} a las {hora_final}\nVehículo: {seleccion}\nTotal: ${gran_total:.2f}\n(Incluye {servicio_empaque})"
link_whatsapp = f"https://wa.me/593999999999?text={urllib.parse.quote(mensaje)}"

if hora_final != "Sin disponibilidad":
    st.markdown(f"""<a href="{link_whatsapp}" target="_blank" style="text-decoration: none;"><button>CONFIRMAR RESERVA 📲</button></a>""", unsafe_allow_html=True)
