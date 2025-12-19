import streamlit as st
import datetime
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Mudanza Prime", page_icon="🚚", layout="centered")

# --- COLORES DE TU MARCA ---
COLOR_PRIMARIO = "#2E004E"   # Morado del logo (para textos y detalles)
COLOR_SECUNDARIO = "#FFC300" # Amarillo del logo (para botones)
COLOR_TEXTO = "#1F2937"      # Gris oscuro para lectura
COLOR_SIDEBAR = "#1A1F2C"    # NUEVO: Carbón oscuro para una barra lateral elegante

# --- ESTILOS CSS ---
st.markdown(f"""
    <style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&display=swap');

    /* Estilo general */
    .stApp {{ background-color: #FFFFFF; font-family: 'Montserrat', sans-serif; }}
    
    /* BARRA LATERAL - NUEVO COLOR */
    section[data-testid="stSidebar"] {{ background-color: {COLOR_SIDEBAR}; }}
    
    /* Textos de la barra lateral en BLANCO */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label {{
        color: #FFFFFF !important;
    }}
    /* Inputs de la barra lateral */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{ color: {COLOR_TEXTO}; }}

    /* TÍTULO PRINCIPAL - MÁS GRANDE */
    .titulo-principal {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 48px; /* Aumentado de 38px a 48px */
        color: {COLOR_PRIMARIO};
        text-transform: uppercase;
        letter-spacing: -1px;
        line-height: 1.2;
    }}

    /* BOTÓN PRINCIPAL */
    .stButton>button {{
        background-color: {COLOR_SECUNDARIO} !important;
        color: {COLOR_PRIMARIO} !important;
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
    
    /* Cajas de Horarios */
    .horario-box {{ padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 8px; font-weight: bold; }}
    .disponible {{ background-color: #D1FAE5; color: #065F46; border: 1px solid #34D399; }}
    .ocupado {{ background-color: #FEE2E2; color: #991B1B; border: 1px solid #F87171; }}
    
    /* Métricas de precio */
    div[data-testid="stMetricValue"] {{ color: {COLOR_PRIMARIO} !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
col_logo, col_titulo = st.columns([1, 3])
with col_logo:
    try: st.image("logo.jpg", width=140) # Logo un poco más grande para balancear
    except: st.write("🚚") 
with col_titulo:
    # Título más grande y sin subtítulo "2.0"
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

# --- LÓGICA DE AGENDA (SIMULADA) ---
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
    
    # Visualización mejorada de horarios con cajitas de colores
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
        st.warning("Día completo para este camión.")

st.divider()

# --- CÁLCULOS ---
costo_base = datos_camion["precio"]
costo_personal = personal * 15
costo_materiales = (cajas * 1.50) + (rollos * 20)
costo_distancia = distancia * 1.0
gran_total = costo_base + costo_personal + costo_materiales + costo_distancia

# --- RESUMEN FINAL ---
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
mi_numero = "593999999999"  # <--- TU NÚMERO AQUÍ
mensaje = f"Hola Mudanza Prime! Quiero reservar:\n📅 {fecha_seleccionada}\n⏰ {hora_final}\n🚛 {seleccion}\n💰 Total: ${gran_total:.2f}"
import urllib.parse
link_whatsapp = f"https://wa.me/{mi_numero}?text={urllib.parse.quote(mensaje)}"

if hora_final != "Sin disponibilidad":
    st.markdown(f"""<a href="{link_whatsapp}" target="_blank" style="text-decoration: none;"><button>CONFIRMAR RESERVA 📲</button></a>""", unsafe_allow_html=True)
else:
    st.error("Selecciona otra fecha o camión.")
