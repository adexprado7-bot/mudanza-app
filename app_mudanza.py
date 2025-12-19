import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Cotizador Mudanza Prime", page_icon="🚚", layout="centered")

# --- ESTILOS CSS (DISEÑO LIMPIO Y BLANCO) ---
st.markdown("""
    <style>
    /* Forzar fondo blanco en toda la app */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Estilo del contenedor principal */
    .main {
        background-color: #FFFFFF;
    }
    
    /* Títulos y textos en color oscuro para contraste */
    h1, h2, h3 {
        color: #1F2937 !important;
    }
    p, label, .stMarkdown {
        color: #374151 !important;
    }

    /* Estilo de las métricas (Cajitas de precio) */
    div[data-testid="stMetricValue"] {
        color: #2E86C1; /* Azul corporativo */
    }
    
    /* Botón personalizado */
    .stButton>button {
        background-color: #2E86C1;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO ---
st.title("🚚 Mudanza Prime")
st.write("Cotizador oficial | Rápido y seguro")
st.divider()

# --- BARRA LATERAL (INPUTS) ---
st.sidebar.header("1. Elige tu Transporte")

# Selección de Vehículo
opciones_vehiculo = {
    "Furgoneta (Carga Ligera)": {"precio": 30, "cap": 6, "icon": "🚐"},
    "Camión 2 Toneladas": {"precio": 40, "cap": 12, "icon": "🚛"},
    "Camión 3.5 Toneladas": {"precio": 50, "cap": 20, "icon": "🚛🚛"},
    "Camión 6 Toneladas": {"precio": 60, "cap": 35, "icon": "🚛🚛🚛"}
}

seleccion = st.sidebar.selectbox("Tamaño del Vehículo:", list(opciones_vehiculo.keys()))
datos_camion = opciones_vehiculo[seleccion]

# Inputs Básicos
st.sidebar.header("2. Distancia y Personal")
distancia = st.sidebar.number_input("Distancia recorrida (km):", min_value=1, value=10)
costo_km = 1.0 
personal = st.sidebar.slider("Cargadores ($15 c/u):", 0, 6, 2)

# Inputs de Materiales y Servicios
st.sidebar.header("3. Materiales y Servicios")
cajas = st.sidebar.number_input("Cartones ($1.50 c/u):", 0, 50, 10)
rollos = st.sidebar.number_input("Rollos Embalaje ($20 c/u):", 0, 10, 1)

st.sidebar.markdown("---")
st.sidebar.subheader("💎 Servicios Premium")

# Checkbox para protección delicada
proteccion_delicada = st.sidebar.checkbox("Añadir Protección Objetos Delicados (+$50)")
costo_delicados = 50 if proteccion_delicada else 0

# Radio button para servicio de empaque
servicio_empaque = st.sidebar.radio(
    "¿Necesitas servicio de empacado (guardar en cajas)?",
    ["No, yo empaco mis cosas ($0)", 
     "Empaque Básico (+$30)", 
     "Empaque Completo (+$50)"]
)

if "Básico" in servicio_empaque:
    costo_empaque = 30
elif "Completo" in servicio_empaque:
    costo_empaque = 50
else:
    costo_empaque = 0

# --- CÁLCULOS MATEMÁTICOS ---
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

# --- PANTALLA PRINCIPAL (RESULTADOS) ---

col1, col2 = st.columns(2)

with col1:
    st.subheader("Tu Selección")
    st.info(f"{datos_camion['icon']} **{seleccion}**")
    
    st.write(f"📍 **Distancia:** {distancia} km")
    st.write(f"👷 **Personal:** {personal} cargadores")
    
    st.write("---")
    st.caption("Ocupación Estimada:")
    st.progress(porcentaje_ocupacion)

with col2:
    st.subheader("Presupuesto")
    
    # Desglose de precios
    lineas = [
        f"Base Vehículo: ${costo_base_camion}",
        f"Personal: ${costo_total_personal}",
        f"Distancia: ${costo_distancia:.2f}",
        f"Materiales: ${total_materiales:.2f}",
        f"Serv. Empaque: ${costo_empaque}"
    ]
    
    for linea in lineas:
        st.text(linea)
    
    st.divider()
    st.metric(label="TOTAL A PAGAR", value=f"${gran_total:.2f}")

# --- BOTÓN DE RESERVA ---
msg_whatsapp = f"Hola Mudanza Prime, coticé una mudanza por ${gran_total:.2f} con {seleccion}. ¿Tienen disponibilidad?"
link_whatsapp = f"https://wa.me/593999999999?text={msg_whatsapp.replace(' ', '%20')}"

st.markdown(f"""
    <a href="{link_whatsapp}" target="_blank">
        <button style="
            width: 100%; 
            background-color: #2E86C1; 
            color: white; 
            padding: 15px; 
            border: none; 
            border-radius: 10px; 
            font-size: 18px; 
            font-weight: bold; 
            cursor: pointer;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s;">
            📲 Reservar Ahora
        </button>
    </a>
    """, unsafe_allow_html=True)
