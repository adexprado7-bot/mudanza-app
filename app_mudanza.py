import streamlit as st
import datetime
import random
import urllib.parse

# --- CONFIGURACIÓN DE PÁGINA "WIDE" (TIPO ESCRITORIO) ---
st.set_page_config(page_title="Mudanza Prime | Tu Panel", page_icon="🚚", layout="wide")

# --- ESTILOS CSS (DISEÑO BANCO GUAYAQUIL) ---
# Definimos los colores exactos de tu marca
COLOR_MORADO = "#2E004E"
COLOR_AMARILLO = "#FFC300"
FONDO_GRIS = "#F4F6F8" # El gris suave de fondo de los bancos

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    
    /* 1. FONDO GENERAL */
    .stApp {{
        background-color: {FONDO_GRIS};
        font-family: 'Montserrat', sans-serif;
    }}
    
    /* 2. TARJETAS SUPERIORES (Estilo Tarjeta Crédito/Débito) */
    .hero-card {{
        border-radius: 20px;
        padding: 25px;
        color: white;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }}
    .hero-card:hover {{ transform: translateY(-5px); }}
    
    .card-purple {{
        background: linear-gradient(135deg, {COLOR_MORADO} 0%, #4a148c 100%);
    }}
    .card-yellow {{
        background: linear-gradient(135deg, {COLOR_AMARILLO} 0%, #ffca28 100%);
        color: {COLOR_MORADO} !important; /* Texto morado en fondo amarillo */
    }}
    
    .card-label {{ font-size: 14px; opacity: 0.9; font-weight: 500; }}
    .card-amount {{ font-size: 36px; font-weight: 700; margin-top: 5px; }}
    .card-chip {{ font-size: 24px; }}
    .card-footer {{ font-size: 12px; opacity: 0.8; letter-spacing: 1px; }}

    /* 3. BOTONES DE ACCIÓN RÁPIDA (Estilo Banco) */
    .action-btn {{
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        cursor: pointer;
        transition: all 0.2s;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 1px solid transparent;
    }}
    .action-btn:hover {{
        border: 1px solid {COLOR_AMARILLO};
        transform: scale(1.02);
    }}
    .icon-circle {{
        width: 45px; height: 45px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 20px;
        margin-bottom: 10px;
    }}
    /* Colores específicos para los íconos */
    .bg-purple {{ background-color: #F3E5F5; color: {COLOR_MORADO}; }}
    .bg-yellow {{ background-color: #FFF8E1; color: #F57F17; }}
    .bg-green {{ background-color: #E8F5E9; color: #2E7D32; }}
    .bg-blue {{ background-color: #E3F2FD; color: #1565C0; }}
    
    .action-text {{ font-size: 13px; font-weight: 600; color: #374151; }}

    /* 4. LISTA DE MOVIMIENTOS (Desglose limpio) */
    .transaccion-container {{
        background-color: white;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }}
    .transaccion-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 15px 0;
        border-bottom: 1px solid #F3F4F6;
    }}
    .transaccion-row:last-child {{ border-bottom: none; }}
    
    .t-left {{ display: flex; align-items: center; gap: 15px; }}
    .t-icon {{ 
        width: 40px; height: 40px; background-color: #F9FAFB; 
        border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 18px; 
    }}
    .t-title {{ font-weight: 700; color: #1F2937; font-size: 14px; display: block; }}
    .t-desc {{ font-size: 12px; color: #9CA3AF; display: block; margin-top: 2px; }}
    .t-price {{ font-weight: 700; font-size: 16px; color: {COLOR_MORADO}; }}
    
    /* Ajustes generales de Streamlit */
    section[data-testid="stSidebar"] {{ background-color: white; border-right: 1px solid #E5E7EB; }}
    .stButton>button {{ background-color: {COLOR_AMARILLO} !important; color: {COLOR_MORADO} !important; border-radius: 10px; font-weight: 800; }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: DATOS DEL CLIENTE (INPUTS) ---
with st.sidebar:
    # Logo simulado
    try: st.image("logo.jpg", width=140)
    except: st.markdown(f"<h2 style='color:{COLOR_MORADO}'>MUDANZA PRIME</h2>", unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Configura tu servicio")
    
    # 1. Vehículo
    vehiculos = {
        "Furgoneta (Pequeña)": {"precio": 30, "img": "🚐"},
        "Camión 2 Toneladas": {"precio": 40, "img": "🚛"},
        "Camión 3.5 Toneladas": {"precio": 50, "img": "🚚"},
        "Camión 6 Toneladas": {"precio": 60, "img": "🚛🚛"}
    }
    seleccion = st.selectbox("Vehículo", list(vehiculos.keys()))
    dato_camion = vehiculos[seleccion]

    st.markdown("---")
    
    # 2. Detalles
    distancia = st.number_input("Distancia (km)", 1, 500, 10)
    personal = st.slider("Ayudantes", 0, 10, 2)
    
    st.markdown("---")
    
    # 3. Materiales
    cajas = st.number_input("Cajas ($1.50)", 0, 100, 10)
    rollos = st.number_input("Rollos ($20)", 0, 20, 1)

    # 4. Accesos (Pisos)
    st.markdown("### 🏢 Accesos")
    piso_salida = st.selectbox("Piso Salida", ["PB", "1", "2", "3", "4+"])
    asc_salida = st.checkbox("Ascensor Salida?")
    piso_llegada = st.selectbox("Piso Llegada", ["PB", "1", "2", "3", "4+"])
    asc_llegada = st.checkbox("Ascensor Llegada?")

# --- CÁLCULOS INTERNOS ---
def calc_recargo(piso, ascensor):
    if ascensor or piso == "PB": return 0
    mapa = {"1": 10, "2": 20, "3": 30, "4+": 40}
    return mapa.get(piso, 0)

recargo_pisos = calc_recargo(piso_salida, asc_salida) + calc_recargo(piso_llegada, asc_llegada)
costo_camion = dato_camion["precio"]
costo_personal = personal * 15
costo_materiales = (cajas * 1.5) + (rollos * 20)
costo_distancia = distancia * 1.0
total = costo_camion + costo_personal + costo_materiales + costo_distancia + recargo_pisos

# --- DASHBOARD PRINCIPAL (ÁREA DE TRABAJO) ---

# Saludo
st.markdown(f"<h2 style='color:#1F2937; margin-bottom: 20px;'>Hola, Cliente Prime 👋</h2>", unsafe_allow_html=True)

# 1. SECCIÓN TARJETAS (HERO SECTION)
col1, col2, col3 = st.columns(3)

with col1:
    # Tarjeta Morada (Presupuesto)
    st.markdown(f"""
    <div class="hero-card card-purple">
        <div>
            <div class="card-label">PRESUPUESTO TOTAL</div>
            <div class="card-amount">${total:.2f}</div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:end;">
            <div class="card-footer">**** 1234</div>
            <div class="card-chip">💳</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Tarjeta Amarilla (Vehículo)
    st.markdown(f"""
    <div class="hero-card card-yellow">
        <div>
            <div class="card-label">TU TRANSPORTE</div>
            <div class="card-amount" style="font-size: 24px; color:{COLOR_MORADO};">{dato_camion['img']}</div>
            <div style="font-weight:bold; font-size:18px; color:{COLOR_MORADO};">{seleccion}</div>
        </div>
        <div class="card-footer" style="color:{COLOR_MORADO};">CAPACIDAD MEDIA</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # Tarjeta Informativa (Fecha/Info)
    fecha_hoy = datetime.date.today().strftime("%d %b, %Y")
    st.markdown(f"""
    <div class="hero-card" style="background:white; color:#333; border:1px solid #ddd;">
        <div>
            <div class="card-label" style="color:#666;">FECHA COTIZACIÓN</div>
            <div class="card-amount" style="color:{COLOR_MORADO}; font-size:28px;">{fecha_hoy}</div>
        </div>
        <div class="card-footer" style="color:#666;">COTIZACIÓN VÁLIDA 24H</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# 2. ACCIONES RÁPIDAS
st.markdown("#### Acciones rápidas")
ac1, ac2, ac3, ac4 = st.columns(4)

# Link de WhatsApp
msg = f"Hola Mudanza Prime. Deseo reservar: {seleccion} por ${total:.2f}."
link_wa = f"https://wa.me/593999999999?text={urllib.parse.quote(msg)}"

# Definimos el HTML de los botones para que queden perfectos
def crear_boton(icono, texto, color_bg, link="#"):
    return f"""
    <a href="{link}" target="_blank" style="text-decoration:none;">
    <div class="action-btn">
        <div class="icon-circle {color_bg}">{icono}</div>
        <div class="action-text">{texto}</div>
    </div>
    </a>
    """

with ac1: st.markdown(crear_boton("📲", "Reservar Ahora", "bg-green", link_wa), unsafe_allow_html=True)
with ac2: st.markdown(crear_boton("💬", "Soporte", "bg-blue", link_wa), unsafe_allow_html=True)
with ac3: st.markdown(crear_boton("📦", "Ver Inventario", "bg-yellow"), unsafe_allow_html=True)
with ac4: st.markdown(crear_boton("🛡️", "Seguros y Tips", "bg-purple"), unsafe_allow_html=True)

st.write("")

# 3. LISTA DE MOVIMIENTOS (DETALLE DE COSTOS)
col_izq, col_der = st.columns([2, 1])

with col_izq:
    st.markdown("#### Actividad reciente (Desglose)")
    
    # HTML DE LA LISTA (Ahora sí indentado correctamente para que no rompa)
    html_lista = f"""
    <div class="transaccion-container">
        <div class="transaccion-row">
            <div class="t-left">
                <div class="t-icon">🚛</div>
                <div>
                    <span class="t-title">Vehículo Base</span>
                    <span class="t-desc">Tarifa por tipo de camión</span>
                </div>
            </div>
            <span class="t-price">${costo_camion:.2f}</span>
        </div>
        
        <div class="transaccion-row">
            <div class="t-left">
                <div class="t-icon">👷</div>
                <div>
                    <span class="t-title">Personal de Carga</span>
                    <span class="t-desc">{personal} ayudantes x $15</span>
                </div>
            </div>
            <span class="t-price">${costo_personal:.2f}</span>
        </div>

        <div class="transaccion-row">
            <div class="t-left">
                <div class="t-icon">📦</div>
                <div>
                    <span class="t-title">Materiales</span>
                    <span class="t-desc">{cajas} Cajas + {rollos} Rollos</span>
                </div>
            </div>
            <span class="t-price">${costo_materiales:.2f}</span>
        </div>

        <div class="transaccion-row">
            <div class="t-left">
                <div class="t-icon">🏢</div>
                <div>
                    <span class="t-title">Logística de Accesos</span>
                    <span class="t-desc">Recargo Pisos/Escaleras</span>
                </div>
            </div>
            <span class="t-price">${recargo_pisos:.2f}</span>
        </div>
    </div>
    """
    st.markdown(html_lista, unsafe_allow_html=True)

with col_der:
    st.markdown("#### Mis Metas")
    st.info("**Ahorro Prime**\n\nSi reservas con 15 días de anticipación, obtienes un 5% de descuento en materiales.")
    st.success("**Garantía**\n\nTu mudanza viaja asegurada.")
