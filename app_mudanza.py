import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Cotizador Mudanza Prime", page_icon="🚚", layout="centered")

# --- ESTILOS CSS (DISEÑO PREMIUM & CORRECCIÓN DE COLORES) ---
st.markdown("""
    <style>
    /* 1. Fondo principal BLANCO */
    .stApp {
        background-color: #FFFFFF;
        color: #000000; /* Forzar texto negro general */
    }
    
    /* 2. Sidebar (Menú lateral) GRIS SUAVE */
    section[data-testid="stSidebar"] {
        background-color: #F8F9FA;
        border-right: 1px solid #E5E7EB;
    }
    
    /* 3. Forzar colores de TEXTOS para que se vean siempre */
    h1, h2, h3, h4, h5, h6, .css-10trblm {
        color: #111827 !important; /* Negro casi puro */
    }
    
    p, label, span, div.stMarkdown {
        color: #374151 !important; /* Gris oscuro muy legible */
    }
    
    /* Texto dentro de los inputs del sidebar */
    .stSelectbox label, .stNumberInput label, .stSlider label, .stRadio label, .stCheckbox label {
        color: #111827 !important;
    }
    
    /* 4. Estilo de las métricas (Cajitas de precio) */
    div[data-testid="stMetricValue"] {
        color: #2E86C1 !important; /* Azul corporativo */
    }
    
    /* 5. Botón personalizado */
    .stButton>button {
        background-color: #2E86C1;
        color: white !important;
        border-radius: 8px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO ---
st.title("🚚 Mudanza Prime")
st.write("Cotizador oficial | Rápido, Seguro y Transparente")
st.divider()

# --- BARRA LATERAL (INPUTS) ---
st.sidebar.header("1. Configura tu Mudanza")

# Selección de Vehículo
opciones_vehiculo = {
    "Furgoneta (Carga Ligera)": {"precio": 30, "cap": 6, "icon": "🚐"},
    "Camión 2 Toneladas": {"precio": 40, "cap": 12, "icon": "🚛"},
    "Camión 3.5 Toneladas": {"precio": 50, "cap": 20, "icon": "🚛🚛"},
    "Camión 6 Toneladas": {"precio": 60, "cap": 35, "icon": "🚛🚛🚛"}
}

seleccion = st.sidebar.selectbox("Tamaño del Vehículo:", list(opciones_vehiculo.keys()))
datos_camion = opciones_vehiculo[seleccion]

st.sidebar.markdown("---")

# Inputs Básicos
st.sidebar.subheader("📍 Distancia y Equipo")
distancia = st.sidebar.number_input("Distancia aprox (km):", min_value=1, value=10)
costo_km = 1.0 
personal = st.sidebar.slider("Ayudantes de Carga ($15 c/u):", 0, 6, 2)

st.sidebar.markdown("---")

# Inputs de Materiales
st.sidebar.subheader("📦 Materiales")
cajas = st.sidebar.number_input("Cartones ($1.50 c/u):", 0, 50, 10)
rollos = st.sidebar.number_input("Rollos Embalaje ($20 c/u):", 0, 10, 1)

# Servicios Premium
st.sidebar.markdown("---")
st.sidebar.subheader("💎 Extras")
proteccion_delicada = st.sidebar.checkbox("Protección Objetos Delicados (+$50)")
costo_delicados = 50 if proteccion_delicada else 0

servicio_empaque = st.sidebar.radio(
    "¿Servicio de Empacado?",
    ["Yo empaco ($0)", 
     "Básico (+$30)", 
     "Completo (+$50)"]
)

if "Básico" in servicio_empaque:
    costo_empaque = 30
elif "Completo" in servicio_empaque:
    costo_empaque = 50
else:
    costo_empaque = 0

# --- NUEVO CAMPO: DETALLE DE CARGA ---
st.sidebar.markdown("---")
st.sidebar.subheader("📝 ¿Qué vamos a mover?")
detalle_inventario = st.sidebar.text_area(
    "Ej: Una refri, cama king, sofá de 3 puestos...",
    placeholder="Escribe aquí los muebles principales..."
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
    st.subheader("Tu Resumen")
    st.info(f"{datos_camion['icon']} **{seleccion}**")
    
    st.write(f"📍 **Distancia:** {distancia} km")
    st.write(f"👷 **Personal:** {personal} ayudantes")
    if detalle_inventario:
        st.caption(f"**Notas:** {detalle_inventario}")
    
    st.write("---")
    st.caption("Ocupación sugerida:")
    st.progress(porcentaje_ocupacion)
    if porcentaje_ocupacion > 0.85:
        st.warning("⚠️ Camión casi lleno")

with col2:
    st.subheader("Presupuesto Estimado")
    
    # Usamos markdown simple para evitar errores de color
    st.markdown(f"""
    * **Vehículo:** ${costo_base_camion}
    * **Personal:** ${costo_total_personal}
    * **Distancia:** ${costo_distancia:.2f}
    * **Materiales:** ${total_materiales:.2f}
    * **Empaque:** ${costo_empaque}
    """)
    
    st.divider()
    st.metric(label="TOTAL A PAGAR", value=f"${gran_total:.2f}")

# --- BOTÓN DE WHATSAPP INTELIGENTE ---
# Importante: Reemplaza el 593999999 por tu número REAL
mi_numero = "593999999999" 

mensaje = f"""Hola Mudanza Prime 🚛
Quiero reservar:
- Vehículo: {seleccion}
- Total estimado: ${gran_total:.2f}
- Distancia: {distancia}km
- Inventario: {detalle_inventario if detalle_inventario else 'No especificado'}

¿Tienen disponibilidad?
"""

import urllib.parse
mensaje_encoded = urllib.parse.quote(mensaje)
link_whatsapp = f"https://wa.me/{mi_numero}?text={mensaje_encoded}"

st.markdown(f"""
    <br>
    <a href="{link_whatsapp}" target="_blank" style="text-decoration: none;">
        <button style="
            width: 100%; 
            background-color: #25D366; 
            color: white; 
            padding: 18px; 
            border: none; 
            border-radius: 12px; 
            font-size: 20px; 
            font-weight: bold; 
            cursor: pointer;
            box-shadow: 0px 4px 10px rgba(37, 211, 102, 0.4);
            transition: transform 0.2s;">
            📲 Enviar Pedido por WhatsApp
        </button>
    </a>
    <div style="text-align: center; margin-top: 10px; color: #666; font-size: 12px;">
        *Al dar clic se abrirá tu WhatsApp con los datos listos.
    </div>
    """, unsafe_allow_html=True)
