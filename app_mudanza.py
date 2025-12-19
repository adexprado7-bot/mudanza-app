import streamlit as st
import datetime
import random
import urllib.parse

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Mudanza Prime", page_icon="🚚", layout="centered")

# --- TOGGLE MODO OSCURO ---
st.sidebar.header("⚙️ Configuración")
modo_oscuro = st.sidebar.toggle("🌙 Modo Oscuro", value=False)

# --- DEFINICIÓN DE COLORES ---
COLOR_PRIMARIO = "#2E004E"   # Morado
COLOR_SECUNDARIO = "#FFC300" # Amarillo

if modo_oscuro:
    # NOCTURNO
    FONDO_APP = "#0E1117"        
    COLOR_TEXTO = "#FFFFFF"      
    SIDEBAR_BG = "#1A1F2C"       
    SIDEBAR_TEXT = "#FFFFFF"     
    COLOR_TITULO = "#A970FF"     # Morado Neón para resaltar
    COLOR_INPUTS = "#262730"     
    COLOR_CARD = "#1A1F2C"       
else:
    # DIURNO
    FONDO_APP = "#FFFFFF"        
    COLOR_TEXTO = "#000000"      # Negro puro para evitar fantasmas
    SIDEBAR_BG = "#F3F4F6"       
    SIDEBAR_TEXT = "#000000"     
    COLOR_TITULO = "#2E004E"     
    COLOR_INPUTS = "#FFFFFF"     
    COLOR_CARD = "#F9FAFB"       

# --- ESTILOS CSS BLINDADOS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700;800&display=swap');

    .stApp {{ background-color: {FONDO_APP}; font-family: 'Montserrat', sans-serif; }}
    
    /* Textos Generales */
    h1, h2, h3, h4, p, li, .stMarkdown, .stTable {{ color: {COLOR_TEXTO} !important; }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{ background-color: {SIDEBAR_BG}; }}
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] div, section[data-testid="stSidebar"] label {{ color: {SIDEBAR_TEXT} !important; }}
    
    /* Logo Insignia */
    div[data-testid="stImage"] img {{ background-color: white; padding: 8px; border-radius: 12px; }}

    /* Títulos */
    .titulo-principal {{
        font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 45px;
        color: {COLOR_TITULO} !important; text-transform: uppercase; line-height: 1.0; margin-bottom: 0;
    }}
    .slogan {{
        font-family: 'Montserrat', sans-serif; font-size: 18px; font-weight: 500;
        color: {COLOR_TEXTO}; opacity: 0.8; font-style: italic; margin-top: -10px;
    }}

    /* CORRECCIÓN PRECIO FANTASMA */
    div[data-testid="stMetricValue"] {{ color: {COLOR_TITULO} !important; font-size: 36px !important; }}
    div[data-testid="stMetricLabel"] {{ color: {COLOR_TEXTO} !important; font-weight: bold !important; }}

    /* CORRECCIÓN MENÚS DESPLEGABLES (DROPDOWNS) */
    ul[data-testid="stSelectboxVirtualDropdown"] {{ background-color: white !important; }}
    ul[data-testid="stSelectboxVirtualDropdown"] li {{ color: black !important; background-color: white !important; }}
    ul[data-testid="stSelectboxVirtualDropdown"] li:hover {{ background-color: #FFC300 !important; color: black !important; }}
    div[data-baseweb="select"] > div {{ background-color: {COLOR_INPUTS} !important; color: {COLOR_TEXTO} !important; }}
    
    /* Inputs */
    .stNumberInput input, .stTextArea textarea {{ color: {COLOR_TEXTO} !important; background-color: {COLOR_INPUTS}; }}

    /* Botón */
    .stButton>button {{
        background-color: {COLOR_SECUNDARIO} !important; color: {COLOR_PRIMARIO} !important;
        border-radius: 12px; border: none; font-weight: 800; font-size: 18px; width: 100%; padding: 15px 0;
        box-shadow: 0 4px 14px 0 rgba(255, 195, 0, 0.4);
    }}
    
    /* Cajas Horarios */
    .horario-box {{ padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 8px; font-weight: bold; font-size: 14px; }}
    .disponible {{ background-color: #D1FAE5; color: #065F46; border: 1px solid #34D399; }}
    .ocupado {{ background-color: #FEE2E2; color: #991B1B; border: 1px solid #F87171; }}
    
    /* Tarjetas de Beneficios */
    .beneficio-card {{
        background-color: {COLOR_CARD}; padding: 15px; border-radius: 10px;
        border-left: 5px solid {COLOR_SECUNDARIO}; margin-bottom: 10px;
        color: {COLOR_TEXTO};
    }}
    .beneficio-card b {{ color: {COLOR_TITULO}; }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_logo, col_titulo = st.columns([1, 3])
with col_logo:
    try: st.image("logo.jpg", width=130)
    except: st.write("🚚") 
with col_titulo:
    st.markdown('<p class="titulo-principal">MUDANZA PRIME</p>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">Movemos lo que más quieres.</p>', unsafe_allow_html=True)

st.divider()

# --- SIDEBAR (CONFIGURACIÓN) ---
st.sidebar.header("🛠️ Configura tu Servicio")

opciones_vehiculo = {
    "Furgoneta (Pequeña)": {"precio": 30, "cap": 6},
    "Camión 2 Toneladas": {"precio": 40, "cap": 12},
    "Camión 3.5 Toneladas": {"precio": 50, "cap": 20},
    "Camión 6 Toneladas": {"precio": 60, "cap": 35}
}
seleccion = st.sidebar.selectbox("Vehículo:", list(opciones_vehiculo.keys()))
datos_camion = opciones_vehiculo[seleccion]

st.sidebar.markdown("---")
distancia = st.sidebar.number_input("Distancia (km):", 1, 500, 10)
personal = st.sidebar.slider("Ayudantes:", 0, 6, 2)

st.sidebar.subheader("📦 Materiales")
cajas = st.sidebar.number_input("Cartones ($1.50):", 0, 100, 10)
rollos = st.sidebar.number_input("Rollos ($20):", 0, 20, 1)

st.sidebar.subheader("💎 Extras")
proteccion = st.sidebar.checkbox("Protección Delicados (+$50)")
costo_proteccion = 50 if proteccion else 0
empaque = st.sidebar.radio("Empaque:", ["Cliente ($0)", "Básico (+$30)", "Completo (+$50)"])
costo_empaque = 30 if "Básico" in empaque else (50 if "Completo" in empaque else 0)

# --- INVENTARIO INTERACTIVO ---
st.markdown("### 📝 ¿Qué vamos a llevar?")
st.caption("Agrega los objetos grandes para calcular mejor el espacio.")

col_sala, col_cuarto, col_cocina = st.columns(3)
with col_sala:
    st.markdown("**🛋️ Sala**")
    sofas = st.number_input("Sofás:", 0, 5, 0)
    mesas = st.number_input("Mesas:", 0, 3, 0)
    sillas = st.number_input("Sillas:", 0, 12, 0)
with col_cuarto:
    st.markdown("**🛏️ Cuarto**")
    camas = st.number_input("Camas:", 0, 5, 0)
    armarios = st.number_input("Armarios:", 0, 5, 0)
    tv = st.number_input("TVs:", 0, 5, 0)
with col_cocina:
    st.markdown("**🍳 Cocina**")
    refris = st.number_input("Refris:", 0, 2, 0)
    cocinas = st.number_input("Cocinas:", 0, 2, 0)
    lavadoras = st.number_input("Lavadoras:", 0, 2, 0)

lista_objetos = []
if sofas > 0: lista_objetos.append(f"{sofas} Sofás")
if mesas > 0: lista_objetos.append(f"{mesas} Mesas")
if camas > 0: lista_objetos.append(f"{camas} Camas")
if refris > 0: lista_objetos.append(f"{refris} Refris")
if lavadoras > 0: lista_objetos.append(f"{lavadoras} Lavadoras")
resumen_inventario = ", ".join(lista_objetos) if lista_objetos else "Varios (No especificado)"

st.divider()

# --- AGENDA ---
st.subheader("📅 Disponibilidad")
col_cal, col_hor = st.columns(2)
with col_cal:
    fecha = st.date_input("Fecha:", min_value=datetime.date.today())
with col_hor:
    random.seed(f"{fecha}_{seleccion}") 
    ocup = random.choice([[False,False,False], [True,False,False], [False,True,False]])
    horarios = [
        {"h": "08:00 - 12:00", "oc": ocup[0]},
        {"h": "11:00 - 15:00", "oc": ocup[1]},
        {"h": "14:00 - 18:00", "oc": ocup[2]},
    ]
    opts = [h["h"] for h in horarios if not h["oc"]]
    
    for h in horarios:
        st.markdown(f'<div class="horario-box {"ocupado" if h["oc"] else "disponible"}">{"🔴" if h["oc"] else "🟢"} {h["h"]}</div>', unsafe_allow_html=True)
    
    hora_final = st.selectbox("Elige hora:", opts) if opts else "Lleno"

# --- MARKETING MEJORADO (SIN PUNTUALIDAD) ---
st.divider()
st.subheader("🌟 ¿Por qué Mudanza Prime?")
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.markdown(f"""
    <div class="beneficio-card">
    <b>🛡️ Garantía de Cuidado</b><br>
    Tus muebles son tratados con máxima delicadeza.
    </div>
    """, unsafe_allow_html=True)
    
    # CAMBIO AQUÍ: PUNTUALIDAD -> PERSONAL EXPERTO
    st.markdown(f"""
    <div class="beneficio-card">
    <b>👷 Personal Experto</b><br>
    Equipo capacitado para maniobras difíciles.
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.info("💡 **Tip de Experto:** Descongela tu refrigeradora 24 horas antes y sécala bien para evitar fugas de agua durante el viaje.")

# --- CÁLCULOS ---
total = datos_camion["precio"] + (personal*15) + (distancia*1) + (cajas*1.5) + (rollos*20) + costo_proteccion + costo_empaque

# --- RESUMEN FINAL ---
st.divider()
col_res1, col_res2 = st.columns(2)
with col_res1:
    st.subheader("Resumen")
    st.write(f"**🗓️** {fecha} | {hora_final}")
    st.write(f"**🚛** {seleccion}")
    if lista_objetos:
        st.caption(f"**📦 Items:** {resumen_inventario}")

with col_res2:
    st.subheader("Presupuesto") # Título explícito para que no quede hueco
    st.metric("TOTAL ESTIMADO", f"${total:.2f}")

# --- WHATSAPP ---
msg = f"Hola Mudanza Prime! 🚛\nReserva: {fecha} - {hora_final}\nCamión: {seleccion}\nItems: {resumen_inventario}\nTotal: ${total:.2f}"
link = f"https://wa.me/593999999999?text={urllib.parse.quote(msg)}"

if hora_final != "Lleno":
    st.markdown(f"""<a href="{link}" target="_blank"><button>SOLICITAR MUDANZA 📲</button></a>""", unsafe_allow_html=True)
