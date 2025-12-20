import streamlit as st
import datetime
import random
import urllib.parse

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Mudanza Prime Dashboard", page_icon="🚚", layout="wide") 
# Nota: Cambié layout="centered" a "wide" para que parezca más un dashboard de escritorio

# --- TOGGLE MODO OSCURO ---
with st.sidebar:
    st.header("⚙️ Configuración")
    modo_oscuro = st.toggle("🌙 Modo Oscuro", value=False)

# --- DEFINICIÓN DE COLORES (ESTILO BANCO) ---
COLOR_PRIMARIO = "#2E004E"   # Morado Brand
COLOR_SECUNDARIO = "#FFC300" # Amarillo Brand
COLOR_GRADIENTE_1 = "linear-gradient(135deg, #2E004E 0%, #4a0072 100%)" # Gradiente Morado
COLOR_GRADIENTE_2 = "linear-gradient(135deg, #FFC300 0%, #FFD60A 100%)" # Gradiente Amarillo

if modo_oscuro:
    FONDO_APP = "#0E1117"        
    COLOR_TEXTO = "#FFFFFF"      
    SIDEBAR_BG = "#1A1F2C"       
    SIDEBAR_TEXT = "#FFFFFF"     
    COLOR_CARD_BG = "#1A1F2C" # Fondo de tarjetas en modo oscuro
    COLOR_LIST_HOVER = "#262730"
else:
    FONDO_APP = "#F3F4F6" # Gris muy suave estilo banco        
    COLOR_TEXTO = "#1F2937"      
    SIDEBAR_BG = "#FFFFFF"       
    SIDEBAR_TEXT = "#000000"     
    COLOR_CARD_BG = "#FFFFFF" # Tarjetas blancas limpias
    COLOR_LIST_HOVER = "#F9FAFB"

# --- CSS AVANZADO (ESTILO BANCO GUAYAQUIL) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700;800&display=swap');

    .stApp {{ background-color: {FONDO_APP}; font-family: 'Montserrat', sans-serif; }}
    
    /* Textos */
    h1, h2, h3, h4, p, li, span {{ color: {COLOR_TEXTO} !important; }}
    
    /* Sidebar limpio */
    section[data-testid="stSidebar"] {{ background-color: {SIDEBAR_BG}; border-right: 1px solid rgba(0,0,0,0.05); }}
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] label {{ color: {SIDEBAR_TEXT} !important; }}
    
    /* LOGO */
    div[data-testid="stImage"] img {{ background-color: white; padding: 10px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}

    /* --- TARJETAS TIPO BANCO (HERO CARDS) --- */
    .bank-card {{
        padding: 20px;
        border-radius: 20px;
        color: white !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }}
    .bank-card:hover {{ transform: translateY(-5px); }}
    
    .card-purple {{ background: {COLOR_GRADIENTE_1}; }}
    .card-yellow {{ background: {COLOR_GRADIENTE_2}; color: {COLOR_PRIMARIO} !important; }}
    
    .card-title {{ font-size: 14px; opacity: 0.9; font-weight: 500; }}
    .card-value {{ font-size: 32px; font-weight: 800; }}
    .card-icon {{ font-size: 24px; align-self: flex-end; }}
    .card-sub {{ font-size: 12px; opacity: 0.8; }}

    /* --- BOTONES DE ACCIÓN RÁPIDA --- */
    .quick-action-btn {{
        background-color: {COLOR_CARD_BG};
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        cursor: pointer;
        transition: all 0.2s;
        border: 1px solid rgba(0,0,0,0.05);
        height: 100%;
    }}
    .quick-action-btn:hover {{ background-color: {COLOR_SECUNDARIO}; transform: scale(1.05); border: none; }}
    .action-icon {{ font-size: 24px; margin-bottom: 5px; display: block; }}
    .action-label {{ font-size: 12px; font-weight: 600; color: {COLOR_TEXTO}; }}

    /* --- LISTA DE TRANSACCIONES (DETALLE DE COSTOS) --- */
    .transaction-list {{
        background-color: {COLOR_CARD_BG};
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    .transaction-item {{
        display: flex;
        justify_content: space-between;
        padding: 15px 0;
        border-bottom: 1px solid rgba(0,0,0,0.05);
    }}
    .transaction-item:last-child {{ border-bottom: none; }}
    .t-icon {{ background-color: #F3F4F6; padding: 10px; border-radius: 50%; margin-right: 15px; font-size: 18px; }}
    .t-info {{ flex-grow: 1; }}
    .t-title {{ font-weight: 700; font-size: 14px; display: block; color: {COLOR_TEXTO}; }}
    .t-desc {{ font-size: 12px; color: #6B7280; display: block; }}
    .t-amount {{ font-weight: 800; font-size: 16px; color: {COLOR_PRIMARIO}; }}
    
    /* Ajustes generales */
    .stButton>button {{ background-color: {COLOR_SECUNDARIO} !important; color: {COLOR_PRIMARIO} !important; border-radius: 12px; font-weight: 800; }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (INPUTS) ---
with st.sidebar:
    try: st.image("logo.jpg", width=120)
    except: st.write("🚚 MUDANZA PRIME")
    st.write("")
    
    st.header("1. Tu Transporte")
    opciones_vehiculo = {
        "Furgoneta": {"precio": 30, "img": "🚐"},
        "Camión 2T": {"precio": 40, "img": "🚛"},
        "Camión 3.5T": {"precio": 50, "img": "🚚"},
        "Camión 6T": {"precio": 60, "img": "🚛🚛"}
    }
    seleccion = st.selectbox("Vehículo", list(opciones_vehiculo.keys()), label_visibility="collapsed")
    datos_camion = opciones_vehiculo[seleccion]

    st.header("2. Detalles")
    distancia = st.number_input("Distancia (km):", 1, 500, 10)
    personal = st.slider("Ayudantes:", 0, 10, 2)
    
    st.header("3. Accesos")
    piso_salida = st.selectbox("Salida:", ["PB", "Piso 1", "Piso 2", "Piso 3+"])
    asc_salida = st.checkbox("Ascensor Salida")
    piso_llegada = st.selectbox("Llegada:", ["PB", "Piso 1", "Piso 2", "Piso 3+"])
    asc_llegada = st.checkbox("Ascensor Llegada")
    
    # Lógica precio pisos
    def calc_pisos(piso, asc):
        if asc or piso == "PB": return 0
        return 10 if piso == "Piso 1" else (20 if piso == "Piso 2" else 30)
    recargo_pisos = calc_pisos(piso_salida, asc_salida) + calc_pisos(piso_llegada, asc_llegada)

    st.header("4. Materiales")
    cajas = st.number_input("Cartones ($1.50):", 0, 50, 10)
    rollos = st.number_input("Rollos ($20):", 0, 10, 1)

# --- CÁLCULOS ---
base = datos_camion["precio"]
costo_personal = personal * 15
costo_dist = distancia * 1
costo_mat = (cajas * 1.5) + (rollos * 20)
total = base + costo_personal + costo_dist + costo_mat + recargo_pisos

# --- DASHBOARD PRINCIPAL ---
# Título estilo saludo
st.markdown(f"## Hola, Cliente 👋")
st.markdown("Aquí tienes el resumen de tu proyecto de mudanza.")
st.write("")

# FILA 1: TARJETAS HERO (Estilo Tarjeta de Crédito)
col1, col2, col3 = st.columns([1.5, 1.5, 1])

with col1:
    # Tarjeta Morada (Precio Total)
    st.markdown(f"""
    <div class="bank-card card-purple">
        <div class="card-icon">💳</div>
        <div>
            <div class="card-title">PRESUPUESTO ESTIMADO</div>
            <div class="card-value">${total:.2f}</div>
            <div class="card-sub">Incluye impuestos y servicios</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Tarjeta Amarilla (Vehículo)
    st.markdown(f"""
    <div class="bank-card card-yellow">
        <div class="card-icon">{datos_camion['img']}</div>
        <div style="color: #2E004E;">
            <div class="card-title">TU TRANSPORTE</div>
            <div class="card-value">{seleccion}</div>
            <div class="card-sub">{distancia} km de recorrido</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # Tarjeta Informativa (Nivel/Puntos - Simulado)
    st.markdown(f"""
    <div class="bank-card" style="background-color: {COLOR_CARD_BG}; color: {COLOR_TEXTO} !important; border: 1px solid #e5e7eb;">
        <div class="card-icon" style="color: #FFC300;">⭐</div>
        <div>
            <div class="card-title" style="color: {COLOR_TEXTO};">NIVEL PRIME</div>
            <div class="card-value" style="color: {COLOR_PRIMARIO}; font-size: 24px;">Estándar</div>
            <div class="card-sub" style="color: {COLOR_TEXTO};">¡Reserva para subir!</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# FILA 2: ACCIONES RÁPIDAS
st.markdown("### Acciones Rápidas")
ac1, ac2, ac3, ac4 = st.columns(4)

# Links para botones
msg = f"Hola Mudanza Prime. Quiero reservar: {seleccion} por ${total:.2f}."
link_wa = f"https://wa.me/593999999999?text={urllib.parse.quote(msg)}"

with ac1:
    st.markdown(f"""<a href="{link_wa}" target="_blank" style="text-decoration: none;">
        <div class="quick-action-btn">
            <span class="action-icon">📲</span>
            <span class="action-label">Reservar Ahora</span>
        </div></a>
    """, unsafe_allow_html=True)

with ac2:
    st.markdown(f"""<a href="{link_wa}" target="_blank" style="text-decoration: none;">
        <div class="quick-action-btn">
            <span class="action-icon">💬</span>
            <span class="action-label">Hablar con Asesor</span>
        </div></a>
    """, unsafe_allow_html=True)

with ac3:
    st.markdown(f"""
        <div class="quick-action-btn">
            <span class="action-icon">📦</span>
            <span class="action-label">Tips de Empaque</span>
        </div>
    """, unsafe_allow_html=True)

with ac4:
    st.markdown(f"""
        <div class="quick-action-btn">
            <span class="action-icon">📋</span>
            <span class="action-label">Ver Inventario</span>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# FILA 3: ACTIVIDAD RECIENTE (Desglose de Costos) + BARRA LATERAL (Publicidad)
col_main, col_side = st.columns([2, 1])

with col_main:
    st.markdown("### 📊 Desglose de Costos")
    
    # HTML puro para la lista de "transacciones"
    st.markdown(f"""
    <div class="transaction-list">
        <div class="transaction-item">
            <div style="display:flex; align-items:center;">
                <div class="t-icon">🚛</div>
                <div class="t-info">
                    <span class="t-title">Vehículo Base</span>
                    <span class="t-desc">{seleccion} - Tarifa estándar</span>
                </div>
            </div>
            <span class="t-amount">${base:.2f}</span>
        </div>

        <div class="transaction-item">
            <div style="display:flex; align-items:center;">
                <div class="t-icon">👷</div>
                <div class="t-info">
                    <span class="t-title">Personal de Carga</span>
                    <span class="t-desc">{personal} Ayudantes x $15</span>
                </div>
            </div>
            <span class="t-amount">${costo_personal:.2f}</span>
        </div>

        <div class="transaction-item">
            <div style="display:flex; align-items:center;">
                <div class="t-icon">📦</div>
                <div class="t-info">
                    <span class="t-title">Materiales y Empaque</span>
                    <span class="t-desc">{cajas} Cajas + {rollos} Rollos</span>
                </div>
            </div>
            <span class="t-amount">${costo_mat:.2f}</span>
        </div>

        <div class="transaction-item">
            <div style="display:flex; align-items:center;">
                <div class="t-icon">🏢</div>
                <div class="t-info">
                    <span class="t-title">Logística de Accesos</span>
                    <span class="t-desc">Recargo por pisos/escaleras</span>
                </div>
            </div>
            <span class="t-amount">${recargo_pisos:.2f}</span>
        </div>
        
        <div class="transaction-item" style="border-top: 2px dashed #ddd; margin-top: 10px;">
            <div style="display:flex; align-items:center;">
                <div class="t-info">
                    <span class="t-title" style="font-size: 18px; color: {COLOR_PRIMARIO};">TOTAL A PAGAR</span>
                </div>
            </div>
            <span class="t-amount" style="font-size: 24px;">${total:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_side:
    st.markdown("### 🛡️ Tus Beneficios")
    st.info("**Garantía Prime**\n\nTodos tus muebles viajan asegurados contra daños básicos de transporte.")
    st.success("**Personal Experto**\n\nNuestro equipo está capacitado para desmontar y armar camas.")
    st.warning("**Tip del Día**\n\nRecuerda descongelar tu refrigeradora 24h antes del viaje.")
