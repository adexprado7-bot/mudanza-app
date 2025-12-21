import streamlit as st
import datetime
import urllib.parse
from fpdf import FPDF

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mudanza Prime | Cotizador", page_icon="🚚", layout="wide")

# --- COLORES ---
COLOR_MORADO = "#2E004E"
COLOR_AMARILLO = "#FFC300"
FONDO_APP = "#F4F6F8"
COLOR_TEXTO = "#1F2937"
COLOR_CARD_BG = "#FFFFFF"

# --- FUNCIÓN GENERADORA DE PDF ---
class PDF(FPDF):
    def header(self):
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
        self.cell(0, 10, 'Mudanza Prime - Guayaquil | Documento Informativo', 0, 0, 'C')

def generar_pdf(fecha, camion, personal, materiales, inventario_txt, total, desglose):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Datos Generales
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, txt=f"Fecha Emisión: {datetime.date.today()}", ln=1, fill=True)
    pdf.ln(5)
    
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, txt=f"Fecha Programada: {fecha}", ln=1)
    pdf.cell(0, 10, txt=f"Vehículo: {camion}", ln=1)
    
    # Inventario (Si existe)
    if len(inventario_txt) > 5:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 8, "Inventario Declarado:", ln=1)
        pdf.set_font("Arial", size=9)
        pdf.multi_cell(0, 6, txt=inventario_txt)
        pdf.ln(5)
    
    # Tabla
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(140, 10, "Descripción", 1)
    pdf.cell(50, 10, "Valor", 1, 1, 'C')
    
    pdf.set_font("Arial", size=12)
    pdf.cell(140, 10, f"Transporte ({camion})", 1)
    pdf.cell(50, 10, f"${desglose['camion']:.2f}", 1, 1, 'R')
    pdf.cell(140, 10, f"Personal ({personal} ayudantes)", 1)
    pdf.cell(50, 10, f"${desglose['personal']:.2f}", 1, 1, 'R')
    pdf.cell(140, 10, f"Materiales ({materiales})", 1)
    pdf.cell(50, 10, f"${desglose['materiales']:.2f}", 1, 1, 'R')
    pdf.cell(140, 10, "Tarifa Ciudad", 1)
    pdf.cell(50, 10, "$0.00", 1, 1, 'R')
    
    # Total
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(46, 0, 78)
    pdf.cell(140, 15, "TOTAL A PAGAR", 1)
    pdf.cell(50, 15, f"${total:.2f}", 1, 1, 'R')
    
    return pdf.output(dest='S').encode('latin-1')

# --- CSS SUPER BLINDADO (MODO CLARO FORZADO) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    
    .stApp {{ background-color: {FONDO_APP}; font-family: 'Montserrat', sans-serif; }}
    
    /* Forzar texto negro en general */
    h1, h2, h3, h4, h5, p, span, div, label, li {{ color: {COLOR_TEXTO} !important; }}
    
    /* --- SOLUCIÓN INPUTS NEGROS (ELIMINAR TEMA OSCURO) --- */
    
    /* 1. Fondo blanco para inputs numéricos, de fecha y selectores */
    .stNumberInput div[data-baseweb="input"],
    .stDateInput div[data-baseweb="input"],
    .stSelectbox div[data-baseweb="select"] {{
        background-color: white !important;
        color: black !important;
        border-radius: 8px !important;
        border: 1px solid #d1d5db !important; /* Borde gris suave */
    }}
    
    /* 2. El texto dentro de los inputs debe ser negro */
    input {{
        color: black !important;
        caret-color: black !important;
    }}
    
    /* 3. El contenedor interno de los números */
    div[data-testid="stNumberInputContainer"] {{
        background-color: white !important;
    }}

    /* 4. Menús desplegables (Dropdowns) */
    ul[data-testid="stSelectboxVirtualDropdown"] {{
        background-color: white !important;
    }}
    li[role="option"] {{
        background-color: white !important;
        color: black !important;
    }}
    li[role="option"]:hover {{
        background-color: {COLOR_AMARILLO} !important;
        color: black !important;
    }}
    
    /* 5. Acordeón (Expander) */
    .streamlit-expanderHeader {{
        background-color: white !important;
        color: black !important;
        border-radius: 8px;
    }}
    div[data-testid="stExpanderDetails"] {{
        background-color: #f9fafb !important; /* Un gris muy clarito adentro */
        color: black !important;
        border: 1px solid #e5e7eb;
        border-radius: 0 0 8px 8px;
    }}

    /* ESTILOS DE DISEÑO */
    .control-panel {{
        background-color: {COLOR_CARD_BG}; padding: 20px; border-radius: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px;
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

    /* Botones Acción */
    .action-btn {{
        background-color: {COLOR_CARD_BG}; border-radius: 16px; padding: 15px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02); transition: all 0.2s; height: 100%;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        border: 1px solid rgba(0,0,0,0.05); text-decoration: none;
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

    /* Botón Descarga Pequeño */
    .stDownloadButton > button {{
        background-color: white !important;
        color: {COLOR_MORADO} !important;
        border: 1px solid {COLOR_MORADO} !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        padding: 5px 15px !important;
    }}
    .stDownloadButton > button:hover {{
        background-color: {COLOR_MORADO} !important;
        color: white !important;
    }}

    header {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("## 🚚 MUDANZA PRIME")

# --- PANEL DE CONFIGURACIÓN ---
st.markdown(f"<div class='control-panel'>", unsafe_allow_html=True)
st.markdown("### ⚙️ Configura tu Servicio")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**1. Fecha y Vehículo**")
    fecha_seleccionada = st.date_input("📅 Fecha", datetime.date.today())
    vehiculos = {
        "Furgoneta (Pequeña)": {"precio": 30, "img": "🚐"},
        "Camión 2 Toneladas": {"precio": 40, "img": "🚛"},
        "Camión 3.5 Toneladas": {"precio": 50, "img": "🚚"},
        "Camión 6 Toneladas": {"precio": 60, "img": "🚛🚛"}
    }
    seleccion = st.selectbox("🚛 Camión", list(vehiculos.keys()))
    dato_camion = vehiculos[seleccion]

with c2:
    st.markdown("**2. Personal**")
    personal = st.slider("👷 Ayudantes", 0, 10, 2)
    st.caption("Tarifa: $15 c/u")

with c3:
    st.markdown("**3. Materiales**")
    col_mat1, col_mat2 = st.columns(2)
    with col_mat1: cajas = st.number_input("📦 Cajas", 0, 100, 10)
    with col_mat2: rollos = st.number_input("🗞️ Rollos", 0, 20, 1)

st.markdown("</div>", unsafe_allow_html=True)

# --- INVENTARIO ESTRUCTURADO (NUEVO DISEÑO) ---
lista_objetos = []

# Usamos un expander que por CSS ahora será blanco
with st.expander("📝 LISTA DE INVENTARIO (Clic para desplegar)", expanded=True):
    col_inv_1, col_inv_2, col_inv_3, col_inv_4 = st.columns(4)
    
    # 1. LÍNEA BLANCA
    with col_inv_1:
        st.markdown("##### ❄️ Línea Blanca")
        st.caption("Electrodomésticos grandes")
        
        # Refrigeradora con selector de tipo
        tipo_refri = st.selectbox("Tipo de Refri", ["Ninguna", "Normal", "Side by Side (Grande)"])
        if tipo_refri != "Ninguna":
            lista_objetos.append(f"Refri {tipo_refri}")
            
        cocina = st.number_input("Cocina", 0, 5, 0, key="inv_cocina")
        lavadora = st.number_input("Lavadora", 0, 5, 0, key="inv_lavadora")
        secadora = st.number_input("Secadora", 0, 5, 0, key="inv_secadora")
        
        if cocina: lista_objetos.append(f"{cocina} Cocina")
        if lavadora: lista_objetos.append(f"{lavadora} Lavadora")
        if secadora: lista_objetos.append(f"{secadora} Secadora")

    # 2. SALA
    with col_inv_2:
        st.markdown("##### 🛋️ Sala")
        st.caption("Muebles principales")
        
        mesa_centro = st.number_input("Mesa de Centro", 0, 5, 0, key="inv_mesa_centro")
        muebles_sala = st.number_input("Muebles (Sofás)", 0, 10, 0, key="inv_sofas")
        esquinero = st.number_input("Esquinero", 0, 5, 0, key="inv_esquinero")
        
        if mesa_centro: lista_objetos.append(f"{mesa_centro} Mesa Centro")
        if muebles_sala: lista_objetos.append(f"{muebles_sala} Sofás")
        if esquinero: lista_objetos.append(f"{esquinero} Esquinero")

    # 3. COMEDOR
    with col_inv_3:
        st.markdown("##### 🍽️ Comedor")
        st.caption("Mesas y sillas")
        
        # Material de la mesa
        tiene_mesa = st.checkbox("¿Lleva Mesa?")
        if tiene_mesa:
            material_mesa = st.selectbox("Material Mesa", ["Madera", "Vidrio", "Mármol"])
            lista_objetos.append(f"Mesa Comedor ({material_mesa})")
            
        sillas = st.number_input("Sillas", 0, 12, 0, key="inv_sillas")
        bufetera = st.number_input("Bufetera", 0, 5, 0, key="inv_bufetera")
        
        if sillas: lista_objetos.append(f"{sillas} Sillas")
        if bufetera: lista_objetos.append(f"{bufetera} Bufetera")

    # 4. DORMITORIOS
    with col_inv_4:
        st.markdown("##### 🛏️ Dormitorios")
        st.caption("Habitaciones")
        
        camas = st.number_input("Camas (Todo tamaño)", 0, 10, 0, key="inv_camas")
        veladores = st.number_input("Veladores", 0, 10, 0, key="inv_veladores")
        comodas = st.number_input("Cómodas", 0, 5, 0, key="inv_comodas")
        
        if camas: lista_objetos.append(f"{camas} Camas")
        if veladores: lista_objetos.append(f"{veladores} Veladores")
        if comodas: lista_objetos.append(f"{comodas} Cómodas")

inventario_final = ", ".join(lista_objetos) if lista_objetos else "No especificado"

# --- CÁLCULOS ---
precio_camion = dato_camion["precio"]
precio_personal = personal * 15
precio_materiales = (cajas * 1.5) + (rollos * 20)
total = precio_camion + precio_personal + precio_materiales

# --- DASHBOARD ---
st.markdown("### 📊 Tu Cotización")
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"""
    <div class="hero-card card-purple">
        <div><div class="card-label">PRESUPUESTO ESTIMADO</div><div class="card-amount">${total:.2f}</div></div>
        <div style="display:flex; justify-content:space-between; align-items:end;"><div style="font-size:12px; opacity:0.8;">TARIFA FIJA CIUDAD</div><div style="font-size:24px;">💳</div></div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="hero-card card-yellow">
        <div><div class="card-label">VEHÍCULO</div><div class="card-amount">{dato_camion['img']}</div><div style="font-weight:700; color:{COLOR_MORADO};">{seleccion}</div></div>
    </div>""", unsafe_allow_html=True)
with k3:
    fecha_str = fecha_seleccionada.strftime("%d %B %Y")
    st.markdown(f"""
    <div class="hero-card" style="background-color:{COLOR_CARD_BG}; border: 1px solid #ddd;">
        <div><div class="card-label" style="color:#666 !important;">FECHA</div><div class="card-amount" style="color:{COLOR_MORADO} !important; font-size: 28px;">{fecha_str}</div></div>
    </div>""", unsafe_allow_html=True)

st.write("")

# --- ACCIONES RÁPIDAS ---
ac1, ac2, ac3 = st.columns(3)
msg = f"Hola Mudanza Prime. Reserva: {seleccion} ({fecha_str}). Total: ${total:.2f}. Inv: {inventario_final}"
lnk = f"https://wa.me/593999999999?text={urllib.parse.quote(msg)}"

def btn(i, t, c, l="#"): 
    return f"""<a href="{l}" target="_blank" style="text-decoration:none;"><div class="action-btn"><div class="icon-box {c}">{i}</div><div class="action-text">{t}</div></div></a>"""

with ac1: st.markdown(btn("📲", "Reservar WhatsApp", "bg-green", lnk), unsafe_allow_html=True)
with ac2: st.markdown(btn("🛡️", "Seguros y Tips", "bg-purple"), unsafe_allow_html=True)
with ac3: st.markdown(btn("⭐", "Calificanos", "bg-blue"), unsafe_allow_html=True)

st.write("")

# --- DESGLOSE DE COSTOS ---
html_desglose = f"""
<div style="background-color:{COLOR_CARD_BG}; padding:20px; border-radius:15px; box-shadow:0 4px 6px rgba(0,0,0,0.02); margin-bottom: 20px;">
    <h4 style="margin-bottom:20px; color:{COLOR_TEXTO};">🧾 Desglose de Servicios</h4>
    <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
        <span style="color:#666;">🚛 {seleccion}</span>
        <span style="font-weight:bold; color:{COLOR_TEXTO};">${precio_camion:.2f}</span>
    </div>
    <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
        <span style="color:#666;">👷 {personal} Cargadores</span>
        <span style="font-weight:bold; color:{COLOR_TEXTO};">${precio_personal:.2f}</span>
    </div>
    <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
        <span style="color:#666;">📦 Materiales</span>
        <span style="font-weight:bold; color:{COLOR_TEXTO};">${precio_materiales:.2f}</span>
    </div>
    <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
        <span style="color:#666;">📍 Cobertura Ciudad</span>
        <span style="font-weight:bold; color:#2E7D32;">Incluida</span>
    </div>
    <div style="display:flex; justify-content:space-between; padding:15px 0; margin-top:10px;">
        <span style="font-weight:bold; font-size:18px; color:{COLOR_MORADO};">TOTAL FINAL</span>
        <span style="font-weight:bold; font-size:18px; color:{COLOR_MORADO};">${total:.2f}</span>
    </div>
</div>
"""
st.markdown(html_desglose, unsafe_allow_html=True)

# --- BOTÓN FACTURA ---
col_pdf_left, col_pdf_space = st.columns([1, 4])
with col_pdf_left:
    pdf_bytes = generar_pdf(
        fecha=fecha_str,
        camion=seleccion,
        personal=personal,
        materiales=f"{cajas} cajas, {rollos} rollos",
        inventario_txt=inventario_final,
        total=total,
        desglose={'camion': precio_camion, 'personal': precio_personal, 'materiales': precio_materiales}
    )
    st.download_button(
        label="📄 Descargar Factura",
        data=pdf_bytes,
        file_name="Presupuesto_Mudanza.pdf",
        mime="application/pdf",
        use_container_width=True
    )
