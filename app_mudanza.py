import streamlit as st
import datetime
import urllib.parse
from fpdf import FPDF

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mudanza Prime | Panel", page_icon="🚚", layout="wide")

# --- COLORES FIJOS (MODO CLARO ESTILO BANCO) ---
COLOR_MORADO = "#2E004E"
COLOR_AMARILLO = "#FFC300"
FONDO_APP = "#F4F6F8"
COLOR_TEXTO = "#1F2937"
COLOR_CARD_BG = "#FFFFFF"
COLOR_INPUT_BG = "#FFFFFF"

# --- FUNCIÓN GENERADORA DE PDF ---
class PDF(FPDF):
    def header(self):
        # self.image('logo.jpg', 10, 8, 33) 
        self.set_font('Arial', 'B', 20)
        self.set_text_color(46, 0, 78) 
        self.cell(0, 10, 'MUDANZA PRIME', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, 'Presupuesto de Servicios Logísticos', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Mudanza Prime - Guayaquil, Ecuador | Documento no válido como factura tributaria', 0, 0, 'C')

def generar_pdf(fecha, camion, personal, materiales, total, desglose):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Información
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, txt=f"Fecha de Emisión: {datetime.date.today()}", ln=1, fill=True)
    pdf.ln(5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, txt=f"Fecha Programada: {fecha}", ln=1)
    pdf.cell(0, 10, txt=f"Vehículo Solicitado: {camion}", ln=1)
    pdf.ln(10)
    
    # Tabla de Costos
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(140, 10, "Descripción", 1)
    pdf.cell(50, 10, "Valor", 1, 1, 'C')
    
    pdf.set_font("Arial", size=12)
    pdf.cell(140, 10, f"Servicio de Transporte ({camion})", 1)
    pdf.cell(50, 10, f"${desglose['camion']:.2f}", 1, 1, 'R')
    
    pdf.cell(140, 10, f"Personal de Carga ({personal} personas)", 1)
    pdf.cell(50, 10, f"${desglose['personal']:.2f}", 1, 1, 'R')
    
    pdf.cell(140, 10, f"Materiales ({materiales})", 1)
    pdf.cell(50, 10, f"${desglose['materiales']:.2f}", 1, 1, 'R')
    
    pdf.cell(140, 10, "Tarifa Plana (Distancia incluida)", 1)
    pdf.cell(50, 10, "$0.00", 1, 1, 'R')
    
    # Total
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(46, 0, 78)
    pdf.cell(140, 15, "TOTAL A PAGAR", 1)
    pdf.cell(50, 15, f"${total:.2f}", 1, 1, 'R')
    
    return pdf.output(dest='S').encode('latin-1')

# --- CSS BLINDADO (ESTILO BANCO + SOLUCIÓN FANTASMAS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    
    .stApp {{ background-color: {FONDO_APP}; font-family: 'Montserrat', sans-serif; }}
    h1, h2, h3, h4, p, span, div, label {{ color: {COLOR_TEXTO} !important; }}
    
    /* --- SOLUCIÓN DEFINITIVA PARA LETRAS FANTASMA --- */
    /* Fuerza el color del texto y fondo de los inputs y selectores */
    .stSelectbox > div > div, 
    .stDateInput > div > div,
    .stNumberInput > div > div {{
        background-color: white !important;
        color: black !important;
        border-color: #E5E7EB !important;
    }}
    /* Color del texto dentro del input */
    input[type="text"], input[type="number"] {{
        color: black !important;
    }}
    /* Estilo de la lista desplegable */
    ul[data-testid="stSelectboxVirtualDropdown"] {{
        background-color: white !important;
        border: 1px solid #E5E7EB !important;
    }}
    /* Estilo de las opciones de la lista */
    li[role="option"] {{
        color: black !important;
        background-color: white !important;
    }}
    /* Estilo al pasar el mouse por una opción */
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {{
        background-color: {COLOR_AMARILLO} !important;
        color: black !important;
    }}
    /* Estilo del calendario */
    div[data-baseweb="calendar"] {{
        background-color: white !important;
    }}
    /* --- FIN SOLUCIÓN FANTASMAS --- */

    /* PANELES */
    .control-panel {{
        background-color: {COLOR_CARD_BG}; padding: 20px; border-radius: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);
    }}
    
    /* TARJETAS HERO */
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

    /* BOTONES DE ACCIÓN */
    .action-btn {{
        background-color: {COLOR_CARD_BG}; border-radius: 16px; padding: 15px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02); cursor: pointer; transition: all 0.2s; height: 100%;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        border: 1px solid rgba(0,0,0,0.05);
        text-decoration: none;
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

    /* ESTILO BOTÓN DE DESCARGA STREAMLIT */
    .stDownloadButton > button {{
        background-color: {COLOR_MORADO} !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        border: none !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        transition: background-color 0.2s !important;
    }}
    .stDownloadButton > button:hover {{
        background-color: #4a148c !important;
    }}

    header {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    </style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("## 🚚 MUDANZA PRIME")

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
camion_precio = dato_camion["precio"]
personal_precio = personal * 15
materiales_precio = (cajas * 1.5) + (rollos * 20)
total = camion_precio + personal_precio + materiales_precio

# --- DASHBOARD VISUAL ---
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

# --- ACCIONES RÁPIDAS (SIN BOTÓN PDF GRANDE) ---
ca, cb, cc = st.columns(3) # Ahora son 3 columnas en vez de 4
msg = f"Hola Mudanza Prime. Quiero reservar: {seleccion} para el {fecha_str}. Total: ${total:.2f} (Tarifa Fija Ciudad)"
lnk = f"https://wa.me/593999999999?text={urllib.parse.quote(msg)}"

def btn(i, t, c, l="#"): 
    return f"""<a href="{l}" target="_blank" style="text-decoration:none;"><div class="action-btn"><div class="icon-box {c}">{i}</div><div class="action-text">{t}</div></div></a>"""

with ca: st.markdown(btn("📲", "Reservar WhatsApp", "bg-green", lnk), unsafe_allow_html=True)
with cb: st.markdown(btn("📦", "Ver Inventario", "bg-yellow"), unsafe_allow_html=True)
with cc: st.markdown(btn("⭐", "Calificanos", "bg-blue"), unsafe_allow_html=True)

st.write("")

# --- DESGLOSE DE FACTURA ---
html_desglose = f"""
<div style="background-color:{COLOR_CARD_BG}; padding:20px; border-radius:15px; box-shadow:0 4px 6px rgba(0,0,0,0.02); margin-bottom: 20px;">
    <h4 style="margin-bottom:20px; color:{COLOR_TEXTO};">🧾 Desglose de Servicios</h4>
    <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
        <span style="color:#666;">🚛 {seleccion} (Base)</span>
        <span style="font-weight:bold; color:{COLOR_TEXTO};">${camion_precio:.2f}</span>
    </div>
    <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
        <span style="color:#666;">👷 {personal} Cargadores</span>
        <span style="font-weight:bold; color:{COLOR_TEXTO};">${personal_precio:.2f}</span>
    </div>
    <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
        <span style="color:#666;">📦 Materiales ({cajas} cajas, {rollos} rollos)</span>
        <span style="font-weight:bold; color:{COLOR_TEXTO};">${materiales_precio:.2f}</span>
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

# --- BOTÓN DE DESCARGA PDF (PEQUEÑO Y SOFISTICADO) ---
# Usamos columnas para alinearlo a la derecha
col_space, col_btn = st.columns([3, 1])

with col_btn:
    # Generamos el PDF
    pdf_bytes = generar_pdf(
        fecha=fecha_str,
        camion=seleccion,
        personal=personal,
        materiales=f"{cajas} cajas, {rollos} rollos",
        total=total,
        desglose={'camion': camion_precio, 'personal': personal_precio, 'materiales': materiales_precio}
    )
    # Botón nativo de Streamlit, estilizado con CSS
    st.download_button(
        label="📄 Descargar Presupuesto (PDF)",
        data=pdf_bytes,
        file_name=f"Presupuesto_MudanzaPrime_{fecha_str}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
