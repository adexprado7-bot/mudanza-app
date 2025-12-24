import streamlit as st
import datetime
import urllib.parse
from fpdf import FPDF
import base64
import os
import tempfile

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mudanza Prime", page_icon="🚚", layout="wide")

# --- COLORES DE MARCA ---
COLOR_MORADO = "#2E004E"     # Color principal elegante
COLOR_MORADO_CLARO = "#5e2a85" # Para degradados
COLOR_AMARILLO = "#FFC300"   # Acento
COLOR_FONDO = "#F9FAFB"      # Fondo gris muy muy suave (moderno)
COLOR_BLANCO = "#FFFFFF"

# --- FUNCIÓN BASE64 ---
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded}"
    except Exception:
        return None

# --- FUNCIÓN LIMPIEZA TEXTO ---
def clean_text(text):
    return text.encode('latin-1', 'ignore').decode('latin-1')

# --- CLASE PDF ---
class PDF(FPDF):
    def header(self):
        if os.path.exists("logo.png"):
            try:
                self.image('logo.png', x=80, y=10, w=50) 
                self.ln(25) 
            except: pass
        self.set_font('Arial', 'B', 16)
        self.set_text_color(46, 0, 78) 
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, clean_text('Detalle de Cotización'), 0, 1, 'C')
        self.ln(10)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, clean_text('Mudanza Prime | Precio estimado sujeto a disponibilidad'), 0, 0, 'C')

def generar_pdf(fecha, camion, personal, materiales, accesos_txt, inventario_txt, total, pago_seleccionado, desglose, imagenes_usuario):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    pdf.set_fill_color(245, 245, 245)
    
    # Bloque Principal
    pdf.cell(0, 10, txt=clean_text(f"Fecha de Emisión: {datetime.date.today()}"), ln=1, fill=True)
    pdf.ln(5)
    
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, txt=clean_text(f"📅 Fecha Mudanza: {fecha}"), ln=1)
    nombre_camion = camion.split("-")[0]
    pdf.cell(0, 8, txt=clean_text(f"🚚 Vehículo: {nombre_camion}"), ln=1)
    pdf.cell(0, 8, txt=clean_text(f"🏢 Accesos: {accesos_txt}"), ln=1)
    pdf.cell(0, 8, txt=clean_text(f"💳 Pago: {pago_seleccionado}"), ln=1)
    pdf.ln(5)

    if len(inventario_txt) > 5:
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 8, clean_text("📦 Inventario Resumido:"), ln=1)
        pdf.set_font("Arial", size=9)
        pdf.multi_cell(0, 6, txt=clean_text(inventario_txt))
        pdf.ln(5)
        
    # Tabla de Precios
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(46, 0, 78)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(140, 10, clean_text(" Concepto"), 1, 0, 'L', True)
    pdf.cell(50, 10, clean_text("Valor "), 1, 1, 'R', True)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=11)
    
    def fila(texto, valor):
        pdf.cell(140, 10, clean_text(f" {texto}"), 1)
        pdf.cell(50, 10, f"${valor:.2f} ", 1, 1, 'R')
        
    fila(f"Transporte Base ({nombre_camion})", desglose['camion'])
    fila(f"Personal ({personal} ayudantes)", desglose['personal'])
    fila("Recargo por Pisos/Escaleras", desglose['pisos'])
    fila(f"Materiales ({materiales})", desglose['materiales'])
    fila("Tarifa Ciudad (Guayaquil)", 0.00)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(46, 0, 78)
    pdf.cell(140, 15, clean_text(" TOTAL A PAGAR"), 1)
    pdf.cell(50, 15, f"${total:.2f} ", 1, 1, 'R')

    # Fotos
    if imagenes_usuario:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, clean_text("Registro Fotográfico"), 0, 1, 'L')
        pdf.ln(5)
        for img_file in imagenes_usuario:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(img_file.getvalue())
                tmp_path = tmp.name
            try:
                pdf.image(tmp_path, x=30, w=150)
                pdf.ln(5)
            except: pass
            if os.path.exists(tmp_path): os.remove(tmp_path)

    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- CSS DE ALTA GAMA (AQUÍ ESTÁ LA MAGIA) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* FONDO Y FUENTE GLOBAL */
    .stApp {{
        background-color: {COLOR_FONDO};
        font-family: 'Poppins', sans-serif;
    }}
    
    /* INPUTS MODERNOS (REDONDOS Y LIMPIOS) */
    div[data-baseweb="input"], div[data-baseweb="base-input"], div[data-baseweb="select"] {{
        background-color: white !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 12px !important; /* Bordes más redondos */
        color: #333 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02) !important;
    }}
    
    /* CAJAS DE NÚMEROS */
    div[data-testid="stNumberInputContainer"] {{
        background-color: white !important;
        border-radius: 12px !important;
    }}
    
    /* LOGO FLOTANTE */
    .logo-container {{
        display: flex; justify-content: center; align-items: center;
        padding: 10px 0 30px 0;
    }}
    .logo-container img {{
        max-width: 260px; height: auto;
        filter: drop-shadow(0px 8px 15px rgba(46, 0, 78, 0.15)); /* Sombra morada suave */
        transition: transform 0.3s ease;
    }}
    .logo-container img:hover {{ transform: scale(1.02); }}

    /* TARJETAS PRINCIPALES (NEUMORFISMO SUAVE) */
    .control-panel {{
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04); /* Sombra difusa elegante */
        margin-bottom: 25px;
        border: 1px solid #f0f0f0;
    }}
    
    /* TITULOS */
    h1, h2, h3, h4, h5 {{ color: {COLOR_MORADO} !important; font-weight: 600 !important; }}
    
    /* TARJETAS DE PRECIO (GRADIENTES) */
    .hero-card {{
        border-radius: 16px;
        padding: 20px;
        color: white;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }}
    .hero-card:hover {{ transform: translateY(-3px); }}
    
    .card-purple {{
        background: linear-gradient(135deg, {COLOR_MORADO} 0%, {COLOR_MORADO_CLARO} 100%);
    }}
    .card-yellow {{
        background: linear-gradient(135deg, {COLOR_AMARILLO} 0%, #FFD54F 100%);
        color: {COLOR_MORADO} !important;
    }}
    .card-yellow div {{ color: {COLOR_MORADO} !important; }}
    
    /* BOTONES DE ACCIÓN (GRADIENTES Y BRILLO) */
    .action-btn {{
        background: linear-gradient(145deg, #ffffff, #f5f5f5);
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        box-shadow: 5px 5px 10px #e6e6e6, -5px -5px 10px #ffffff;
        transition: all 0.2s;
        border: 1px solid white;
        text-decoration: none;
        display: block;
    }}
    .action-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        border-color: {COLOR_AMARILLO};
    }}
    
    /* BOTÓN DE DESCARGA PDF */
    .stDownloadButton > button {{
        background-image: linear-gradient(to right, {COLOR_MORADO}, {COLOR_MORADO_CLARO}) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        width: 100%;
        box-shadow: 0 4px 10px rgba(46, 0, 78, 0.2);
    }}
    .stDownloadButton > button:hover {{
        opacity: 0.9;
        box-shadow: 0 6px 15px rgba(46, 0, 78, 0.3);
    }}

    /* FOOTER MINIMALISTA */
    .footer-custom {{
        text-align: center;
        font-size: 11px;
        color: #aaa;
        padding: 40px 0 20px 0;
        border-top: 1px solid #eaeaea;
        margin-top: 50px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }}
    
    /* IMAGEN PREVIEW REDONDEADA */
    .vehicle-preview {{
        width: 100%; 
        border-radius: 15px; 
        margin-top: 15px; 
        border: none;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }}

    header {{ visibility: hidden; }} footer {{ visibility: hidden; }}
    </style>
""", unsafe_allow_html=True)

# --- LOGO CENTRADO ---
img_base64 = get_image_base64("logo.png")
if img_base64:
    st.markdown(f"""<div class="logo-container"><img src="{img_base64}" alt="Mudanza Prime"></div>""", unsafe_allow_html=True)
else:
    st.markdown(f"""<h1 style='text-align:center; font-size:40px; margin-bottom:20px;'>MUDANZA PRIME</h1>""", unsafe_allow_html=True)

# --- PANEL PRINCIPAL (CARD EFECTO PAPEL) ---
st.markdown(f"<div class='control-panel'>", unsafe_allow_html=True)
st.markdown("### ⚙️ Personaliza tu Servicio")

c1, c2, c3, c4 = st.columns(4) 
with c1:
    st.markdown("**1. ¿Cuándo y en qué?**")
    fecha_seleccionada = st.date_input("Fecha de Mudanza", datetime.date.today(), min_value=datetime.date.today(), label_visibility="collapsed")
    
    vehiculos = {
        "👉 Elige Vehículo": {"precio": 0, "img": "❓", "foto": "https://cdn-icons-png.flaticon.com/512/7542/7542676.png"},
        "Furgoneta (Pequeña) - $30": {"precio": 30, "img": "🚐", "foto": "https://img.freepik.com/foto-gratis/furgoneta-reparto-blanco-sobre-fondo-blanco_123583-118.jpg"},
        "Camión 2 Toneladas - $40": {"precio": 40, "img": "🚛", "foto": "https://sc04.alicdn.com/kf/H856d4701297e4125866164223f03b290E.jpg"},
        "Camión 3.5 Toneladas - $50": {"precio": 50, "img": "🚚", "foto": "https://img.freepik.com/foto-gratis/camion-blanco-aislado-sobre-blanco_123583-128.jpg"},
        "Camión 6 Toneladas - $60": {"precio": 60, "img": "🚛🚛", "foto": "https://img.freepik.com/foto-gratis/camion-carga-blanco_1112-588.jpg"}
    }
    seleccion = st.selectbox("Vehículo", list(vehiculos.keys()), label_visibility="collapsed")
    dato_camion = vehiculos[seleccion]
    
    st.markdown(f"""<div style="text-align:center;"><img src="{dato_camion['foto']}" class="vehicle-preview" style="max-height:80px; object-fit:contain;"></div>""", unsafe_allow_html=True)

with c2:
    st.markdown("**2. Personal de Carga**")
    personal = st.slider("Ayudantes", 0, 10, 0, label_visibility="collapsed")
    st.markdown(f"<div style='text-align:center; font-weight:bold; color:{COLOR_MORADO};'>{personal} Ayudantes</div>", unsafe_allow_html=True)
    st.caption("Tarifa: $15 c/u")

with c3:
    st.markdown("**3. Pisos y Accesos**")
    col_sal, col_lleg = st.columns(2)
    with col_sal:
        st.caption("Salida")
        piso_salida = st.selectbox("S", ["PB", "1", "2", "3", "4", "5+"], key="ps")
        asc_salida = st.checkbox("Ascensor", key="as")
    with col_lleg:
        st.caption("Llegada")
        piso_llegada = st.selectbox("Ll", ["PB", "1", "2", "3", "4", "5+"], key="pl")
        asc_llegada = st.checkbox("Ascensor", key="all")

with c4:
    st.markdown("**4. Materiales**")
    cajas = st.number_input("📦 Cajas ($1.50)", 0, 100, 0) 
    rollos = st.number_input("🗞️ Rollos ($20)", 0, 20, 0) 

st.markdown("</div>", unsafe_allow_html=True)

# --- INVENTARIO ---
with st.expander("📝 Detallar Inventario (Opcional)", expanded=False):
    lista_objetos = []
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.markdown("**Electrodomésticos y Muebles**")
        refri = st.selectbox("Refrigeradora", ["No", "Pequeña", "Grande (Side by Side)"])
        if refri != "No": lista_objetos.append(f"Refri {refri}")
        cocina = st.checkbox("Cocina")
        if cocina: lista_objetos.append("Cocina")
        lavadora = st.checkbox("Lavadora")
        if lavadora: lista_objetos.append("Lavadora")
        juego_sala = st.checkbox("Juego de Sala")
        if juego_sala: lista_objetos.append("Juego Sala")
        juego_comedor = st.checkbox("Juego Comedor")
        if juego_comedor: lista_objetos.append("Juego Comedor")
    with col_i2:
        st.markdown("**Dormitorio y Otros**")
        camas = st.number_input("Camas", 0, 10, 0)
        if camas: lista_objetos.append(f"{camas} Camas")
        colchones = st.number_input("Colchones", 0, 10, 0)
        if colchones: lista_objetos.append(f"{colchones} Colchones")
        
        st.markdown("**Fotos de Referencia**")
        imagenes_usuario = st.file_uploader("Subir fotos", type=['png', 'jpg'], accept_multiple_files=True, label_visibility="collapsed")

inventario_final = ", ".join(lista_objetos) if lista_objetos else "Básico"

# --- CÁLCULOS ---
def calc_pisos(p, asc): return 0 if asc or p in ["PB", "1"] else (10 if p in ["2", "3"] else 20)
if dato_camion["precio"] == 0: precio_pisos = 0
else: precio_pisos = calc_pisos(piso_salida, asc_salida) + calc_pisos(piso_llegada, asc_llegada)

precio_camion = dato_camion["precio"]
precio_personal = personal * 15
precio_materiales = (cajas * 1.5) + (rollos * 20)
total = precio_camion + precio_personal + precio_materiales + precio_pisos

# --- TARJETAS DE RESULTADO ---
st.markdown("### 📊 Resumen de Cotización")
k1, k2, k3 = st.columns(3)
with k1:
    if total == 0:
        st.markdown(f"""<div class="hero-card card-purple" style="opacity:0.7;"><div><div class="card-label">EMPIEZA AQUÍ</div><div class="card-amount">$0.00</div></div><div>Selecciona un vehículo</div></div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="hero-card card-purple"><div><div class="card-label">TOTAL ESTIMADO</div><div class="card-amount">${total:.2f}</div></div><div style="font-size:12px;">Incluye recargos y servicios</div></div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""<div class="hero-card card-yellow"><div><div class="card-label">VEHÍCULO</div><div class="card-amount" style="font-size:24px;">{seleccion.split('-')[0]}</div></div><div>{dato_camion['img']}</div></div>""", unsafe_allow_html=True)

with k3:
    fecha_fmt = fecha_seleccionada.strftime("%d %b %Y")
    st.markdown(f"""<div class="hero-card" style="background:white; color:#333; border:1px solid #eee;"><div><div class="card-label" style="color:#999;">FECHA RESERVA</div><div class="card-amount" style="color:{COLOR_MORADO};">{fecha_fmt}</div></div><div>📅</div></div>""", unsafe_allow_html=True)

st.write("")

# --- FINALIZAR ---
c_izq, c_der = st.columns([1.5, 1])

with c_izq:
    st.markdown("##### 💳 Método de Pago")
    pago = st.radio("Pago", ["Efectivo", "Transferencia", "Deuna!"], horizontal=True, label_visibility="collapsed")
    
    st.markdown("##### ✅ Confirmación")
    check = st.checkbox("Acepto que el valor es estimado y sujeto a disponibilidad.")
    
    if check and total > 0:
        pdf_bytes = generar_pdf(
            fecha_fmt, seleccion, personal, f"{cajas} cajas, {rollos} rollos", 
            f"{piso_salida}->{piso_llegada}", inventario_final, total, pago, 
            {'camion': precio_camion, 'personal': precio_personal, 'materiales': precio_materiales, 'pisos': precio_pisos},
            imagenes_usuario
        )
        st.download_button("📄 Descargar PDF Oficial", data=pdf_bytes, file_name="Cotizacion.pdf", mime="application/pdf")

with c_der:
    st.write("")
    st.write("")
    txt_fotos = "📸 Con Fotos" if imagenes_usuario else ""
    msg = f"Hola *Mudanza Prime*. Deseo reservar:\n🚚 {seleccion}\n📅 {fecha_fmt}\n💰 Total: ${total:.2f}\n💳 Pago: {pago}\n{txt_fotos}"
    lnk = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
    
    if check and total > 0:
        st.markdown(f"""
        <a href="{lnk}" target="_blank" style="text-decoration:none;">
            <div style="background: linear-gradient(145deg, #25D366, #128C7E); color:white; padding:15px; border-radius:15px; text-align:center; box-shadow:0 5px 15px rgba(37, 211, 102, 0.3); font-weight:bold; transition:transform 0.2s;">
                📲 RESERVAR POR WHATSAPP
            </div>
        </a>
        """, unsafe_allow_html=True)
    else:
        st.info("Completa los datos para reservar.")

# --- FOOTER ---
st.markdown(f"""<div class="footer-custom">© 2025 MUDANZA PRIME | GUAYAQUIL EC<br>DISEÑO PREMIUM</div>""", unsafe_allow_html=True)
