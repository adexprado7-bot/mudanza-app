import streamlit as st
import datetime
import random
import urllib.parse

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Mudanza Prime", page_icon="🚚", layout="centered")

# --- INTERRUPTOR DE MODO (TOGGLE) ---
# Esto debe ir al principio para definir los colores antes de pintar nada
st.sidebar.header("⚙️ Configuración Visual")
modo_oscuro = st.sidebar.toggle("🌙 Modo Oscuro", value=False)

# --- DEFINICIÓN DE PALETAS DE COLORES ---
COLOR_PRIMARIO_MARCA = "#2E004E"   # Morado (Logo)
COLOR_SECUNDARIO_MARCA = "#FFC300" # Amarillo (Botones)
COLOR_SIDEBAR = "#1A1F2C"          # Carbón oscuro (Siempre igual para identidad)

if modo_oscuro:
    # PALETA NOCTURNA
    FONDO_APP = "#0E1117"        # Negro suave
    COLOR_TEXTO = "#FAFAFA"      # Blanco casi puro
    COLOR_CAJAS = "#262730"      # Gris oscuro para inputs/cajas
    COLOR_TITULO = "#A970FF"     # Un morado más claro y brillante para que resalte en negro
else:
    # PALETA DIURNA (Original)
    FONDO_APP = "#FFFFFF"        # Blanco
    COLOR_TEXTO = "#1F2937"      # Gris oscuro
    COLOR_CAJAS = "#F0F2F6"      # Gris muy clarito
    COLOR_TITULO = "#2E004E"     # Morado original oscuro

# --- ESTILOS CSS DINÁMICOS ---
st.markdown(f"""
    <style>
    /* Importar fuente */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&display=swap');

    /* 1. FONDO DE LA APP (Dinámico) */
    .stApp {{
        background-color: {FONDO_APP};
        font-family: 'Montserrat', sans-serif;
    }}
    
    /* 2. TEXTOS GENERALES (Dinámico) */
    h1, h2, h3, h4, p, li, .stMarkdown {{
        color: {COLOR_TEXTO} !important;
    }}
    
    /* 3. BARRA LATERAL (Fija en Carbón para identidad de marca) */
    section[data-testid="stSidebar"] {{ background-color: {COLOR_SIDEBAR}; }}
    
    /* Textos del sidebar siempre blancos */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span {{
        color: #FFFFFF !important;
    }}
    
    /* 4. TÍTULO PRINCIPAL (Dinámico) */
    .titulo-principal {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 48px;
        color: {COLOR_TITULO} !important;
        text-transform: uppercase;
        letter-spacing: -1px;
        line-height: 1.2;
    }}

    /* 5. BOTÓN PRINCIPAL (Amarillo Brand) */
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
    
    /* 6. CAJAS DE HORARIOS */
    .horario-box {{ padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 8px; font-weight: bold; }}
    .disponible {{ background-color: #D1FAE5; color: #065F46; border: 1px solid #34D399; }}
    .ocupado {{ background-color: #FEE2E2; color: #991B1B; border: 1px solid #F87171; }}
    
    /* 7. MÉTRICAS (PRECIOS) */
    div[data-testid="stMetricValue"] {{ 
        color: {COLOR_TITULO} !important; /* El precio cambia de color según el fondo */
    }}
    div[data-testid="stMetricLabel"] {{ 
        color: {COLOR_TEXTO} !important; 
    }}
    
    /* 8. TABLAS (Bordes) */
    .stTable {{ color: {COLOR_TEXTO}; }}
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
    "Camión 3.5 Toneladas": {"precio": 50, "cap": 20, "icon": "🚚"},
    "Camión 6 Toneladas": {"precio": 60, "cap": 35, "icon": "🚛🚛"}
}
seleccion = st.sidebar.selectbox("Vehículo:", list(opciones_vehiculo.keys()))
datos_camion = opciones_vehiculo[seleccion]

st.sidebar.markdown("---")
distancia = st.sidebar.number_input("Distancia (km):", 1, 500, 10)
personal = st.sidebar.slider("Ayudantes:", 0, 6, 2)
st.sidebar.markdown("---")
cajas = st.sidebar.number_input("Cartones ($1.50):", 0, 100, 10)
rollos = st.sidebar.number_input("Rollos ($20):", 0, 20, 1)

# --- LÓGICA DE AGENDA ---
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
    st.write(f"Disponibilidad para: **{seleccion}**")
    opciones_disponibles = []
    
    for turno in horarios:
        if turno["ocupado"]:
            st.markdown(f'<div class="horario-box ocupado">🔴 {turno["hora"]} (Ocupado)</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="horario-box disponible">🟢 {turno["hora"]} (Disponible)</div>', unsafe_allow_html=True)
            opciones_disponibles.append(turno["hora"])

    if opciones_disponibles:
        hora_final = st.selectbox("Elige tu horario:", opciones_disponibles)
    else:
        hora_final = "Sin disponibilidad"
        st.warning("Día completo.")

st.divider()

# --- CÁLCULOS Y RESUMEN ---
costo_base = datos_camion["precio"]
costo_personal = personal * 15
costo_materiales = (cajas * 1.50) + (rollos * 20)
costo_distancia = distancia * 1.0
gran_total = costo_base + costo_personal + costo_materiales + costo_distancia

col1, col2 = st.columns(2)
with col1:
    st.subheader("Tu Reserva")
    st.info(f"""
    **📅 Fecha:** {fecha_seleccionada}  
    **⏰ Hora:** {hora_final}  
    **🚛 Vehículo:** {seleccion}
    """)
    st.write(f"**Distancia:** {distancia} km | **Ayudantes:** {personal}")
with col2:
    st.subheader("Presupuesto")
    st.markdown(f"""
    | Concepto | Valor |
    | :--- | :---: |
    | Vehículo | ${costo_base} |
    | Personal | ${costo_personal} |
    | Materiales | ${costo_materiales} |
    | Distancia | ${costo_distancia} |
    """)
    st.metric(label="TOTAL ESTIMADO", value=f"${gran_total:.2f}")

# --- BOTÓN WHATSAPP ---
mensaje = f"Hola Mudanza Prime! Quiero reservar:\n📅 {fecha_seleccionada}\n⏰ {hora_final}\n🚛 {seleccion}\n💰 Total: ${gran_total:.2f}"
link_whatsapp = f"https://wa.me/593999999999?text={urllib.parse.quote(mensaje)}"

if hora_final != "Sin disponibilidad":
    st.markdown(f"""<a href="{link_whatsapp}" target="_blank" style="text-decoration: none;"><button>CONFIRMAR RESERVA 📲</button></a>""", unsafe_allow_html=True)
