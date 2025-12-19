import streamlit as st
import datetime
import random
import urllib.parse

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Mudanza Prime", page_icon="🚚", layout="centered")

# --- TOGGLE MODO OSCURO ---
st.sidebar.header("⚙️ Configuración")
modo_oscuro = st.sidebar.toggle("🌙 Modo Oscuro", value=False)

# --- COLORES ---
COLOR_PRIMARIO = "#2E004E"   
COLOR_SECUNDARIO = "#FFC300" 

if modo_oscuro:
    FONDO_APP = "#0E1117"        
    COLOR_TEXTO = "#FFFFFF"      
    SIDEBAR_BG = "#1A1F2C"       
    SIDEBAR_TEXT = "#FFFFFF"     
    COLOR_TITULO = "#A970FF"     
    COLOR_INPUTS = "#262730"     
    COLOR_CARD = "#1A1F2C"       
else:
    FONDO_APP = "#FFFFFF"        
    COLOR_TEXTO = "#000000"      
    SIDEBAR_BG = "#F3F4F6"       
    SIDEBAR_TEXT = "#000000"     
    COLOR_TITULO = "#2E004E"     
    COLOR_INPUTS = "#FFFFFF"     
    COLOR_CARD = "#F9FAFB"       

# --- CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700;800&display=swap');
    .stApp {{ background-color: {FONDO_APP}; font-family: 'Montserrat', sans-serif; }}
    h1, h2, h3, h4, p, li, .stMarkdown {{ color: {COLOR_TEXTO} !important; }}
    section[data-testid="stSidebar"] {{ background-color: {SIDEBAR_BG}; }}
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] label {{ color: {SIDEBAR_TEXT} !important; }}
    div[data-testid="stImage"] img {{ background-color: white; padding: 8px; border-radius: 12px; }}
    .titulo-principal {{ font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 45px; color: {COLOR_TITULO} !important; margin-bottom: 0; line-height: 1; }}
    .slogan {{ font-family: 'Montserrat', sans-serif; font-size: 18px; color: {COLOR_TEXTO}; opacity: 0.8; font-style: italic; margin-top: -10px; }}
    div[data-testid="stMetricValue"] {{ color: {COLOR_TITULO} !important; font-size: 36px !important; }}
    div[data-testid="stMetricLabel"] {{ color: {COLOR_TEXTO} !important; }}
    ul[data-testid="stSelectboxVirtualDropdown"] {{ background-color: white !important; }}
    ul[data-testid="stSelectboxVirtualDropdown"] li {{ color: black !important; background-color: white !important; }}
    ul[data-testid="stSelectboxVirtualDropdown"] li:hover {{ background-color: #FFC300 !important; }}
    .stNumberInput input, .stTextArea textarea {{ color: {COLOR_TEXTO} !important; background-color: {COLOR_INPUTS}; }}
    .stButton>button {{ background-color: {COLOR_SECUNDARIO} !important; color: {COLOR_PRIMARIO} !important; border-radius: 12px; font-weight: 800; font-size: 18px; width: 100%; padding: 15px 0; }}
    .horario-box {{ padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 8px; font-weight: bold; font-size: 14px; }}
    .disponible {{ background-color: #D1FAE5; color: #065F46; border: 1px solid #34D399; }}
    .ocupado {{ background-color: #FEE2E2; color: #991B1B; border: 1px solid #F87171; }}
    .beneficio-card {{ background-color: {COLOR_CARD}; padding: 15px; border-radius: 10px; border-left: 5px solid {COLOR_SECUNDARIO}; margin-bottom: 10px; color: {COLOR_TEXTO}; }}
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

# --- SIDEBAR ---
st.sidebar.header("🛠️ Configura tu Servicio")
opciones_vehiculo = {
    "Furgoneta (Pequeña)": {"precio": 30}, "Camión 2 Toneladas": {"precio": 40},
    "Camión 3.5 Toneladas": {"precio": 50}, "Camión 6 Toneladas": {"precio": 60}
}
seleccion = st.sidebar.selectbox("Vehículo:", list(opciones_vehiculo.keys()))
datos_camion = opciones_vehiculo[seleccion]

st.sidebar.markdown("---")
distancia = st.sidebar.number_input("Distancia (km):", 1, 500, 10)
personal = st.sidebar.slider("Ayudantes:", 0, 10, 2)
st.sidebar.markdown("---")
cajas = st.sidebar.number_input("Cartones ($1.50):", 0, 100, 10)
rollos = st.sidebar.number_input("Rollos ($20):", 0, 20, 1)
proteccion = st.sidebar.checkbox("Protección Delicados (+$50)")
costo_proteccion = 50 if proteccion else 0
empaque = st.sidebar.radio("Empaque:", ["Cliente ($0)", "Básico (+$30)", "Completo (+$50)"])
costo_empaque = 30 if "Básico" in empaque else (50 if "Completo" in empaque else 0)

# --- LOGICA DE PISOS Y ESCALERAS (NUEVO) ---
st.subheader("🏢 Accesos")
col_piso1, col_piso2 = st.columns(2)

with col_piso1:
    piso_salida = st.selectbox("Piso de SALIDA:", ["Planta Baja", "Piso 1", "Piso 2", "Piso 3", "Piso 4+"])
    ascensor_salida = st.checkbox("¿Hay Ascensor en Salida?")

with col_piso2:
    piso_llegada = st.selectbox("Piso de LLEGADA:", ["Planta Baja", "Piso 1", "Piso 2", "Piso 3", "Piso 4+"])
    ascensor_llegada = st.checkbox("¿Hay Ascensor en Llegada?")

# Cálculo de recargo por escaleras
recargo_escaleras = 0
# Si no es planta baja y NO hay ascensor, cobramos extra
def calcular_recargo(piso, tiene_ascensor):
    if tiene_ascensor or piso == "Planta Baja": return 0
    if piso == "Piso 1": return 10
    if piso == "Piso 2": return 20
    if piso == "Piso 3": return 30
    if piso == "Piso 4+": return 40
    return 0

recargo_salida = calcular_recargo(piso_salida, ascensor_salida)
recargo_llegada = calcular_recargo(piso_llegada, ascensor_llegada)
total_recargo_pisos = recargo_salida + recargo_llegada

st.divider()

# --- INVENTARIO ---
st.markdown("### 📝 Inventario")
col_sala, col_cuarto, col_cocina = st.columns(3)
with col_sala:
    st.markdown("**🛋️ Sala**")
    sofas = st.number_input("Sofás:", 0, 5, 0)
    mesas = st.number_input("Mesas:", 0, 3, 0)
with col_cuarto:
    st.markdown("**🛏️ Cuarto**")
    camas = st.number_input("Camas:", 0, 5, 0)
    armarios = st.number_input("Armarios:", 0, 5, 0)
with col_cocina:
    st.markdown("**🍳 Cocina**")
    refris = st.number_input("Refris:", 0, 2, 0)
    lavadoras = st.number_input("Lavadoras:", 0, 2, 0)

lista_objetos = []
if sofas: lista_objetos.append(f"{sofas} Sofás")
if mesas: lista_objetos.append(f"{mesas} Mesas")
if camas: lista_objetos.append(f"{camas} Camas")
if refris: lista_objetos.append(f"{refris} Refris")
if lavadoras: lista_objetos.append(f"{lavadoras} Lavadoras")
resumen_inv = ", ".join(lista_objetos) if lista_objetos else "Varios"

st.divider()
# --- AGENDA ---
st.subheader("📅 Disponibilidad")
col_cal, col_hor = st.columns(2)
with col_cal:
    fecha = st.date_input("Fecha:", min_value=datetime.date.today())
with col_hor:
    random.seed(f"{fecha}_{seleccion}") 
    ocup = random.choice([[False,False,False], [True,False,False], [False,True,False]])
    horarios = [{"h": "08:00-12:00", "oc": ocup[0]}, {"h": "11:00-15:00", "oc": ocup[1]}, {"h": "14:00-18:00", "oc": ocup[2]}]
    opts = [h["h"] for h in horarios if not h["oc"]]
    for h in horarios:
        st.markdown(f'<div class="horario-box {"ocupado" if h["oc"] else "disponible"}">{"🔴" if h["oc"] else "🟢"} {h["h"]}</div>', unsafe_allow_html=True)
    hora_final = st.selectbox("Hora:", opts) if opts else "Lleno"

st.divider()
# --- BENEFICIOS ---
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.markdown(f"""<div class="beneficio-card"><b>🛡️ Garantía</b><br>Cuidado total.</div>""", unsafe_allow_html=True)
with col_m2:
    st.markdown(f"""<div class="beneficio-card"><b>👷 Expertos</b><br>Personal capacitado.</div>""", unsafe_allow_html=True)

# --- CÁLCULOS ---
total = datos_camion["precio"] + (personal*15) + (distancia*1) + (cajas*1.5) + (rollos*20) + costo_proteccion + costo_empaque + total_recargo_pisos

# --- RESUMEN ---
st.divider()
col_res1, col_res2 = st.columns(2)
with col_res1:
    st.subheader("Resumen")
    st.write(f"**🗓️** {fecha} | {hora_final}")
    st.write(f"**🚛** {seleccion}")
    if total_recargo_pisos > 0:
        st.caption(f"⚠️ Recargo por escaleras: ${total_recargo_pisos}")

with col_res2:
    st.subheader("Presupuesto")
    st.metric("TOTAL ESTIMADO", f"${total:.2f}")

# --- LEGAL Y WHATSAPP ---
st.write("")
acepta_terminos = st.checkbox("✅ Acepto que los objetos de valor y dinero deben ser transportados personalmente por el cliente.")

msg = f"Hola Mudanza Prime! 🚛\nReserva: {fecha} - {hora_final}\nCamión: {seleccion}\nItems: {resumen_inv}\nAcceso: Salida({piso_salida}), Llegada({piso_llegada})\nTotal: ${total:.2f}"
link = f"https://wa.me/593999999999?text={urllib.parse.quote(msg)}"

if hora_final != "Lleno" and acepta_terminos:
    st.markdown(f"""<a href="{link}" target="_blank"><button>SOLICITAR MUDANZA 📲</button></a>""", unsafe_allow_html=True)
elif hora_final != "Lleno" and not acepta_terminos:
    st.warning("⚠️ Debes aceptar los términos para continuar.")
