import streamlit as st
import datetime
import urllib.parse

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mudanza Prime | Panel", page_icon="🚚", layout="wide")

# --- COLORES ---
COLOR_MORADO = "#2E004E"
COLOR_AMARILLO = "#FFC300"
FONDO_GRIS = "#F4F6F8"

# --- CSS (ESTILO BANCO) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    
    .stApp {{ background-color: {FONDO_GRIS}; font-family: 'Montserrat', sans-serif; }}
    
    /* Textos oscuros */
    h1, h2, h3, p, span, div {{ color: #1F2937; }}
    
    /* TARJETAS HERO */
    .hero-card {{
        border-radius: 20px; padding: 25px; color: white; height: 180px;
        display: flex; flex-direction: column; justify-content: space-between;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08); transition: transform 0.2s;
    }}
    .hero-card:hover {{ transform: translateY(-5px); }}
    
    .card-purple {{ background: linear-gradient(135deg, {COLOR_MORADO} 0%, #4a148c 100%); color: white !important; }}
    .card-purple div {{ color: white !important; }}
    
    .card-yellow {{ background: linear-gradient(135deg, {COLOR_AMARILLO} 0%, #ffca28 100%); }}
    .card-yellow div {{ color: {COLOR_MORADO} !important; }}
    
    .card-white {{ background: white; border: 1px solid #E5E7EB; }}
    .card-white div {{ color: #374151 !important; }}

    .card-label {{ font-size: 13px; font-weight: 600; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; }}
    .card-amount {{ font-size: 38px; font-weight: 800; margin-top: 5px; }}
    .card-footer {{ font-size: 12px; opacity: 0.8; }}

    /* BOTONES ACCIÓN */
    .action-btn {{
        background-color: white; border-radius: 16px; padding: 20px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02); cursor: pointer; transition: all 0.2s; height: 100%;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }}
    .action-btn:hover {{ transform: scale(1.03); box-shadow: 0 10px 15px rgba(0,0,0,0.05); }}
    
    .icon-box {{
        width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-size: 24px; margin-bottom: 12px;
    }}
    .bg-green {{ background-color: #E8F5E9; }}
    .bg-blue {{ background-color: #E3F2FD; }}
    .bg-yellow {{ background-color: #FFF8E1; }}
    .bg-purple {{ background-color: #F3E5F5; }}
    .action-text {{ font-size: 14px; font-weight: 700; color: #374151; }}

    /* LISTA TRANSACCIONES (CSS PURO) */
    .transaccion-container {{
        background-color: white; border-radius: 20px; padding: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }}
    .t-row {{
        display: flex; align-items: center; justify-content: space-between;
        padding: 16px 0; border-bottom: 1px solid #F3F4F6;
    }}
    .t-row:last-child {{ border-bottom: none; }}
    .t-icon {{ 
        width: 42px; height: 42px; background-color: #F9FAFB; color: #333;
        border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 20px; margin-right: 15px;
    }}
    .t-title {{ font-weight: 700; font-size: 15px; color: #111827; }}
    .t-desc {{ font-size: 13px; color: #6B7280; }}
    .t-price {{ font-weight: 700; font-size: 16px; color: {COLOR_MORADO}; }}
    
    /* Ocultar elementos extraños */
    header {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    .stButton>button {{ width: 100%; background-color: {COLOR_AMARILLO}; color: {COLOR_MORADO}; border:none; border-radius:12px; font-weight:bold; }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    try: st.image("logo.jpg", width=140)
    except: st.markdown("## MUDANZA PRIME")
    st.write("---")
    
    vehiculos = {
        "Furgoneta (Pequeña)": {"precio": 30, "img": "🚐"},
        "Camión 2 Toneladas": {"precio": 40, "img": "🚛"},
        "Camión 3.5 Toneladas": {"precio": 50, "img": "🚚"},
        "Camión 6 Toneladas": {"precio": 60, "img": "🚛🚛"}
    }
    seleccion = st.selectbox("Vehículo", list(vehiculos.keys()))
    dato_camion = vehiculos[seleccion]

    distancia = st.number_input("Distancia (km)", 1, 500, 10)
    personal = st.slider("Ayudantes", 0, 10, 2)
    st.write("---")
    cajas = st.number_input("Cajas ($1.50)", 0, 100, 10)
    rollos = st.number_input("Rollos ($20)", 0, 20, 1)
    st.write("---")
    colA, colB = st.columns(2)
    with colA:
        piso_salida = st.selectbox("Salida", ["PB", "1", "2", "3+"])
        asc_salida = st.checkbox("Ascensor S.")
    with colB:
        piso_llegada = st.selectbox("Llegada", ["PB", "1", "2", "3+"])
        asc_llegada = st.checkbox("Ascensor L.")

# --- CÁLCULOS ---
def calc_recargo(piso, ascensor):
    if ascensor or piso == "PB": return 0
    mapa = {"1": 10, "2": 20, "3+": 30}
    return mapa.get(piso, 0)

recargo_pisos = calc_recargo(piso_salida, asc_salida) + calc_recargo(piso_llegada, asc_llegada)
costo_camion = dato_camion["precio"]
costo_personal = personal * 15
costo_materiales = (cajas * 1.5) + (rollos * 20)
costo_distancia = distancia * 1.0
total = costo_camion + costo_personal + costo_materiales + costo_distancia + recargo_pisos

# --- DEFINICIÓN DE HTML (ESTA ES LA SOLUCIÓN) ---
# Definimos el HTML aquí, pegado a la izquierda, sin sangría.
html_desglose = f"""
<div class="transaccion-container">
    <div class="t-row">
        <div style="display:flex; align-items:center;">
            <div class="t-icon">🚛</div>
            <div>
                <div class="t-title">Vehículo Base</div>
                <div class="t-desc">{seleccion}</div>
            </div>
        </div>
        <div class="t-price">${costo_camion:.2f}</div>
    </div>
    <div class="t-row">
        <div style="display:flex; align-items:center;">
            <div class="t-icon">👷</div>
            <div>
                <div class="t-title">Personal de Carga</div>
                <div class="t-desc">{personal} ayudantes x $15</div>
            </div>
        </div>
        <div class="t-price">${costo_personal:.2f}</div>
    </div>
    <div class="t-row">
        <div style="display:flex; align-items:center;">
            <div class="t-icon">📦</div>
            <div>
                <div class="t-title">Materiales</div>
                <div class="t-desc">{cajas} Cajas + {rollos} Rollos</div>
            </div>
        </div>
        <div class="t-price">${costo_materiales:.2f}</div>
    </div>
    <div class="t-row">
        <div style="display:flex; align-items:center;">
            <div class="t-icon">🏢</div>
            <div>
                <div class="t-title">Logística y Accesos</div>
                <div class="t-desc">Recargo Pisos/Escaleras</div>
            </div>
        </div>
        <div class="t-price">${recargo_pisos:.2f}</div>
    </div>
    <div class="t-row" style="border-top: 2px dashed #eee; margin-top:10px;">
        <div style="display:flex; align-items:center;">
            <div class="t-title" style="color:{COLOR_MORADO}; font-size:18px;">TOTAL FINAL</div>
        </div>
        <div class="t-price" style="font-size:22px;">${total:.2f}</div>
    </div>
</div>
"""

# --- DASHBOARD VISUAL ---
st.markdown("### Hola, Cliente Prime 👋")
st.markdown("Resumen financiero de tu mudanza.")
st.write("")

# 1. TARJETAS
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
    <div class="hero-card card-purple">
        <div><div class="card-label">PRESUPUESTO</div><div class="card-amount">${total:.2f}</div></div>
        <div style="display:flex; justify-content:space-between; align-items:end;"><div class="card-footer">**** 1234</div><div style="font-size:24px;">💳</div></div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="hero-card card-yellow">
        <div><div class="card-label">TRANSPORTE</div><div class="card-amount">{dato_camion['img']}</div><div style="font-weight:700;">{seleccion}</div></div>
        <div class="card-footer">CAPACIDAD MEDIA</div>
    </div>""", unsafe_allow_html=True)
with c3:
    fecha = datetime.date.today().strftime("%d %b")
    st.markdown(f"""
    <div class="hero-card card-white">
        <div><div class="card-label" style="color:#666;">FECHA</div><div class="card-amount" style="color:{COLOR_MORADO};">{fecha}</div></div>
        <div class="card-footer" style="color:#666;">COTIZACIÓN VÁLIDA 24H</div>
    </div>""", unsafe_allow_html=True)

st.write("")

# 2. ACCIONES
st.markdown("##### Acciones Rápidas")
ca, cb, cc, cd = st.columns(4)
msg = f"Hola Mudanza Prime. Quiero reservar: {seleccion} por ${total:.2f}"
lnk = f"https://wa.me/593999999999?text={urllib.parse.quote(msg)}"
def btn(i, t, c, l="#"): return f"""<a href="{l}" target="_blank" style="text-decoration:none;"><div class="action-btn"><div class="icon-box {c}">{i}</div><div class="action-text">{t}</div></div></a>"""

with ca: st.markdown(btn("📲", "Reservar", "bg-green", lnk), unsafe_allow_html=True)
with cb: st.markdown(btn("💬", "Soporte", "bg-blue", lnk), unsafe_allow_html=True)
with cc: st.markdown(btn("📦", "Inventario", "bg-yellow"), unsafe_allow_html=True)
with cd: st.markdown(btn("🛡️", "Seguros", "bg-purple"), unsafe_allow_html=True)

st.write("")

# 3. LISTA DE MOVIMIENTOS (Aquí usamos la variable limpia)
c_lista, c_info = st.columns([2, 1])
with c_lista:
    st.markdown("##### Desglose de Costos")
    st.markdown(html_desglose, unsafe_allow_html=True) # ¡Aquí ya no hay sangría que falle!

with c_info:
    st.markdown("##### Beneficios")
    st.info("**Ahorro Prime**\n\nReserva anticipada = descuentos.")
    st.success("**Garantía**\n\nTransporte asegurado.")
