import streamlit as st
import datetime
import urllib.parse

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mudanza Prime | Panel", page_icon="🚚", layout="wide")

# --- CABECERA ---
col_h1, col_h2 = st.columns([4, 1])
with col_h1: st.markdown("## 🚚 MUDANZA PRIME")
with col_h2: modo_oscuro = st.toggle("🌙 Modo Oscuro", value=False)

# --- COLORES ---
COLOR_MORADO = "#2E004E"
COLOR_AMARILLO = "#FFC300"

if modo_oscuro:
    FONDO_APP = "#0E1117"
    COLOR_TEXTO = "#FFFFFF"
    COLOR_CARD_BG = "#1A1F2C"
else:
    FONDO_APP = "#F4F6F8"
    COLOR_TEXTO = "#1F2937"
    COLOR_CARD_BG = "#FFFFFF"

# --- CSS BLINDADO (SOLUCIÓN FANTASMAS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    
    .stApp {{ background-color: {FONDO_APP}; font-family: 'Montserrat', sans-serif; }}
    h1, h2, h3, h4, p, span, div, label {{ color: {COLOR_TEXTO} !important; }}
    
    /* 1. SOLUCIÓN DEFINITIVA PARA INPUTS Y SELECTORES */
    /* Forzamos que la caja cerrada sea siempre blanca con texto negro */
    .stSelectbox div[data-baseweb="select"] > div, 
    .stDateInput div[data-baseweb="input"] > div,
    .stNumberInput div[data-baseweb="input"] > div {{
        background-color: white !important;
        color: black !important;
        border: 1px solid #ddd !important;
    }}
    
    /* Forzamos que el TEXTO dentro de los inputs sea negro */
    input {{ color: black !important; }}
    
    /* 2. SOLUCIÓN PARA EL MENÚ DESPLEGABLE (EL FANTASMA) */
    /* El contenedor de la lista desplegable */
    ul[data-testid="stSelectboxVirtualDropdown"] {{
        background-color: white !important;
    }}
    
    /* Las opciones de la lista */
    li[role="option"] {{
        color: black !important; /* TEXTO NEGRO SIEMPRE */
        background-color: white !important; /* FONDO BLANCO SIEMPRE */
    }}
    
    /* Cuando pasas el mouse por encima */
    li[role="option"]:hover {{
        background-color: {COLOR_AMARILLO} !important;
        color: {COLOR_MORADO} !important;
    }}
    
    /* 3. SOLUCIÓN PARA EL CALENDARIO */
    div[data-baseweb="calendar"] {{
        background-color: white !important;
    }}
    div[data-baseweb="calendar"] div {{
        color: black !important; /* Todo el texto del calendario negro */
    }}
    button[data-baseweb="day"] {{
        color: black !important; /* Los números de los días negros */
    }}
    
    /* PANELES Y TARJETAS */
    .control-panel {{
        background-color: {COLOR_CARD_BG}; padding: 20px; border-radius: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);
    }}
    
    .hero-card {{
        border-radius: 20px; padding: 25px; color: white; height: 160px;
        display: flex; flex-direction: column; justify-content: space-between;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08); transition: transform 0.2s;
    }}
    .hero-card:hover {{ transform: translateY(-5px); }}
    
    .card-purple {{ background: linear-gradient(135deg, {COLOR_MORADO} 0%, #4a148c 100%); }}
    .card-purple div {{ color: white !important; }}
    
    .card-yellow {{ background: linear-gradient(135deg, {COLOR_AMARILLO} 0%, #ffca28 100%); }}
    .card-yellow div {{ color: {COLOR_MORADO} !important; }}
    
    .card-label {{ font-size: 12px; font-weight: 700; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; }}
    .card-amount {{ font-size: 32px; font-weight: 800; margin-top: 5px; }}

    /* BOTONES */
    .action-btn {{
        background-color: {COLOR_CARD_BG}; border-radius: 16px; padding: 15px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02); cursor: pointer; transition: all 0.2s; height: 100%;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        border: 1px solid rgba(0,0,0,0.05);
    }}
    .action-btn:hover {{ transform: scale(1.03); border-color: {COLOR_AMARILLO}; }}
    
    .icon-box {{
        width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-size: 20px; margin-bottom: 10px;
    }}
    .bg-green {{ background-color: #E8F5E9; }}
    .bg-blue {{ background-color: #E3F2FD; }}
    .bg-yellow {{ background-color: #FFF8E1; }}
    .bg-purple {{ background-color: #F3E5F5; }}
    .action-text {{ font-size: 13px; font-weight: 700; color: #374151; }}

    header {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    </style>
""", unsafe_allow_html=True)

# --- PANEL DE CONTROL ---
st.markdown(f"<div class='control-panel'>", unsafe_allow_html=True)
st.markdown("### ⚙️ Configura tu Servicio")

col_inp1, col_inp2, col_inp3 = st.columns(3)

with col_inp1:
    st.markdown("**1. Fecha y Vehículo**")
    fecha_seleccionada = st.date_input("📅 Fecha de Mudanza", datetime.date.today())
    
    vehiculos = {
        "Furgoneta (Pequeña)": {"precio": 30, "img": "🚐"},
        "Camión 2 Toneladas": {"precio": 40, "img": "🚛"},
        "Camión 3.5 Toneladas": {"precio": 50, "img": "🚚"},
        "Camión 6 Toneladas": {"precio": 60, "img": "🚛🚛"}
    }
    seleccion = st.selectbox("🚛 Tamaño del Camión", list(vehiculos.keys()))
    dato_camion = vehiculos[seleccion]

with col_inp2:
    st.markdown("**2. Personal de Carga**")
    personal = st.slider("👷 Número de Ayudantes", 0, 10, 2)
    st.caption("Tarifa por ayudante: $15.00")

with col_inp3:
    st.markdown("**3. Materiales**")
    col_mat1, col_mat2 = st.columns(2)
    with col_mat1:
        cajas = st.number_input("📦 Cajas ($1.50)", 0, 100, 10)
    with col_mat2:
        rollos = st.number_input("🗞️ Rollos ($20)", 0, 20, 1)

st.markdown("</div>", unsafe_allow_html=True)

# --- CÁLCULOS ---
costo_camion = dato_camion["precio"]
costo_personal = personal * 15
costo_materiales = (cajas * 1.5) + (rollos * 20)
total = costo_camion + costo_personal + costo_materiales

# --- RESULTADOS ---
st.markdown("### 📊 Tu Cotización (Tarifa Ciudad)")

# TARJETAS
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
    <div class="hero-card card-purple">
        <div><div class="card-label">PRESUPUESTO ESTIMADO</div><div class="card-amount">${total:.2f}</div></div>
        <div style="display:flex; justify-content:space-between; align-items:end;"><div style="font-size:12px; opacity:0.8;">TARIFA FIJA CIUDAD</div><div style="font-size:24px;">💳</div></div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="hero-card card-yellow">
        <div><div class="card-label">VEHÍCULO SELECCIONADO</div><div class="card-amount">{dato_camion['img']}</div><div style="font-weight:700; color:{COLOR_MORADO};">{seleccion}</div></div>
        <div style="font-size:12px; color:{COLOR_MORADO}; opacity:0.8;">CAPACIDAD IDEAL</div>
    </div>""", unsafe_allow_html=True)
with c3:
    fecha_str = fecha_seleccionada.strftime("%d %B %Y")
    st.markdown(f"""
    <div class="hero-card" style="background-color:{COLOR_CARD_BG}; border: 1px solid #ddd;">
        <div><div class="card-label" style="color:#666 !important;">FECHA PROGRAMADA</div><div class="card-amount" style="color:{COLOR_MORADO} !important; font-size: 28px;">{fecha_str}</div></div>
        <div style="font-size:12px; color:#666 !important;">RESERVA DISPONIBLE</div>
    </div>""", unsafe_allow_html=True)

st.write("")

# ACCIONES
ca, cb, cc, cd = st.columns(4)
msg = f"Hola Mudanza Prime. Quiero reservar: {seleccion} para el {fecha_str}. Total: ${total:.2f} (Tarifa Fija Ciudad)"
lnk = f"https://wa.me/593999999999?text={urllib.parse.quote(msg)}"
def btn(i, t, c, l="#"): return f"""<a href="{l}" target="_blank" style="text-decoration:none;"><div class="action-btn"><div class="icon-box {c}">{i}</div><div class="action-text">{t}</div></div></a>"""

with ca: st.markdown(btn("📲", "Reservar WhatsApp", "bg-green", lnk), unsafe_allow_html=True)
with cb: st.markdown(btn("📦", "Ver Inventario", "bg-yellow"), unsafe_allow_html=True)
with cc: st.markdown(btn("🛡️", "Seguros y Tips", "bg-purple"), unsafe_allow_html=True)
with cd: st.markdown(btn("⭐", "Calificanos", "bg-blue"), unsafe_allow_html=True)

st.write("")

# DESGLOSE
html_desglose = f"""
<div style="background-color:{COLOR_CARD_BG}; padding:20px; border-radius:15px; box-shadow:0 4px 6px rgba(0,0,0,0.02);">
    <h4 style="margin-bottom:20px; color:{COLOR_TEXTO};">🧾 Desglose de Servicios</h4>
    <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
        <span style="color:#666;">🚛 {seleccion} (Base)</span>
        <span style="font-weight:bold; color:{COLOR_TEXTO};">${costo_camion:.2f}</span>
    </div>
    <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
        <span style="color:#666;">👷 {personal} Cargadores</span>
        <span style="font-weight:bold; color:{COLOR_TEXTO};">${costo_personal:.2f}</span>
    </div>
    <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
        <span style="color:#666;">📦 Materiales ({cajas} cajas, {rollos} rollos)</span>
        <span style="font-weight:bold; color:{COLOR_TEXTO};">${costo_materiales:.2f}</span>
    </div>
    <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
        <span style="color:#666;">📍 Cobertura / Distancia</span>
        <span style="font-weight:bold; color:#2E7D32;">Tarifa Plana (Incluida)</span>
    </div>
    <div style="display:flex; justify-content:space-between; padding:15px 0; margin-top:10px;">
        <span style="font-weight:bold; font-size:18px; color:{COLOR_MORADO};">TOTAL FINAL</span>
        <span style="font-weight:bold; font-size:18px; color:{COLOR_MORADO};">${total:.2f}</span>
    </div>
</div>
"""
st.markdown(html_desglose, unsafe_allow_html=True)
