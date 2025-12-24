import streamlit as st
import datetime
import urllib.parse
from fpdf import FPDF
import base64
import os
import tempfile

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Mudanza Prime", page_icon="🚚", layout="wide")

# --- VARIABLES GLOBALES ---
NUMERO_WHATSAPP = "593998994518"  # ¡Corregido!
COLOR_PRINCIPAL = "#2E004E"
COLOR_SECUNDARIO = "#FFC300"

# --- 2. FUNCIONES UTILITARIAS ---

def get_image_base64(path):
    """Convierte una imagen local a base64 para mostrarla en HTML/CSS"""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        # Determinar tipo mime
        if path.lower().endswith('.webp'): mime = 'image/webp'
        elif path.lower().endswith('.jpg') or path.lower().endswith('.jpeg') or path.lower().endswith('.jfif'): mime = 'image/jpeg'
        else: mime = 'image/png'
        return f"data:{mime};base64,{encoded}"
    except Exception:
        return None

def clean_text(text):
    """Limpia caracteres especiales para el PDF"""
    return text.encode('latin-1', 'ignore').decode('latin-1')

# --- 3. CLASE PARA PDF ---
class PDF(FPDF):
    def header(self):
        if os.path.exists("logo.png"):
            try: self.image('logo.png', x=10, y=8, w=40)
            except: pass
        self.set_font('Arial', 'B', 20)
        self.cell(0, 10, clean_text('MUDANZA PRIME'), 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, clean_text('Cotización de Servicio'), 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, clean_text('Página %s - Mudanza Prime Guayaquil' % self.page_no()), 0, 0, 'C')

def generar_pdf_completo(datos, desglose, total, imagenes):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Datos Generales
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, clean_text(f"Fecha de Cotización: {datetime.date.today()}"), ln=1, fill=True)
    pdf.ln(5)
    
    pdf.cell(0, 8, clean_text(f"Cliente: Usuario Web"), ln=1)
    pdf.cell(0, 8, clean_text(f"Fecha Mudanza: {datos['fecha']}"), ln=1)
    pdf.cell(0, 8, clean_text(f"Camión: {datos['camion']}"), ln=1)
    pdf.cell(0, 8, clean_text(f"Ruta: {datos['ruta']}"), ln=1)
    pdf.cell(0, 8, clean_text(f"Forma de Pago: {datos['pago']}"), ln=1)
    pdf.ln(5)
    
    # Inventario
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Resumen de Inventario:", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, clean_text(datos['inventario']))
    pdf.ln(5)

    # Tabla de Costos
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(140, 10, "Detalle", 1)
    pdf.cell(50, 10, "Valor", 1, 1, 'C')
    
    pdf.set_font("Arial", size=12)
    pdf.cell(140, 10, clean_text(f"Vehículo Base"), 1)
    pdf.cell(50, 10, f"${desglose['camion']:.2f}", 1, 1, 'R')
    
    pdf.cell(140, 10, clean_text(f"Personal ({datos['personal']} ayudantes)"), 1)
    pdf.cell(50, 10, f"${desglose['personal']:.2f}", 1, 1, 'R')
    
    pdf.cell(140, 10, clean_text(f"Accesos/Pisos"), 1)
    pdf.cell(50, 10, f"${desglose['pisos']:.2f}", 1, 1, 'R')
    
    pdf.cell(140, 10, clean_text(f"Materiales ({datos['materiales']})"), 1)
    pdf.cell(50, 10, f"${desglose['materiales']:.2f}", 1, 1, 'R')
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(140, 15, "TOTAL ESTIMADO", 1)
    pdf.cell(50, 15, f"${total:.2f}", 1, 1, 'R')

    # Fotos Adjuntas
    if imagenes:
        pdf.add_page()
        pdf.cell(0, 10, "Evidencia Fotográfica:", ln=1)
        for img_file in imagenes:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(img_file.getvalue())
                tmp_path = tmp.name
            try:
                pdf.image(tmp_path, x=20, w=150)
                pdf.ln(5)
            except: pass
            if os.path.exists(tmp_path): os.remove(tmp_path)

    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 4. CSS LIMPIO (SIN ROMPER TEXTOS) ---
st.markdown("""
    <style>
    /* Ocultar menú de streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Contenedores con estilo de tarjeta limpia */
    .stExpander, div[data-testid="stForm"] {
        border: 1px solid #ddd;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        background-color: white;
    }
    
    /* Encabezados Morados */
    h1, h2, h3 {
        color: #2E004E !important;
    }

    /* Botón de WhatsApp destacado */
    .wa-btn {
        display: block;
        width: 100%;
        background-color: #25D366;
        color: white;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        font-size: 18px;
        box-shadow: 0 4px 10px rgba(37, 211, 102, 0.4);
    }
    .wa-btn:hover {
        background-color: #128C7E;
        color: white;
    }
    
    /* Reseñas */
    .review-box {
        background-color: #f9f9f9;
        padding: 15px;
        border-left: 5px solid #FFC300;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. ENCABEZADO Y LOGO ---
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    # Intenta cargar logo, si no usa emoji
    if os.path.exists("logo.png"):
        st.image("logo.png", width=150)
    else:
        st.markdown("# 🚚")

with col_titulo:
    st.title("Cotizador Mudanza Prime")
    st.markdown("**Cotiza tu mudanza profesional en segundos. Sin compromisos.**")

st.divider()

# --- 6. CUERPO PRINCIPAL (2 COLUMNAS PARA MEJOR ORDEN) ---
col_izq, col_der = st.columns([1.2, 0.8], gap="large")

with col_izq:
    st.subheader("1. 📅 Fecha y Vehículo")
    with st.container(border=True):
        fecha = st.date_input("Fecha de Mudanza", datetime.date.today(), min_value=datetime.date.today())
        
        # Diccionario de Camiones (Con tus imágenes locales)
        camiones = {
            "Seleccionar...": {"precio": 0, "foto": None},
            "Camión 2.5 Toneladas ($40)": {"precio": 40, "foto": "camion 2.5.jfif"},
            "Camión 3.5 Toneladas ($50)": {"precio": 50, "foto": "camion 3.5.webp"},
            "Camión 6 Toneladas ($60)": {"precio": 60, "foto": "camion 6.jpg"},
        }
        
        camion_select = st.selectbox("Selecciona el tamaño del camión", list(camiones.keys()))
        data_camion = camiones[camion_select]
        
        # Mostrar foto del camión si se selecciona
        if data_camion["foto"] and os.path.exists(data_camion["foto"]):
            st.image(data_camion["foto"], caption=f"Vehículo Referencial: {camion_select}", use_container_width=True)
        elif camion_select != "Seleccionar...":
            st.info("Imagen del vehículo no disponible, pero el servicio está garantizado.")

    st.subheader("2. 📦 Inventario y Materiales")
    with st.container(border=True):
        st.info("Describe brevemente qué llevas o sube fotos.")
        
        # Lista rápida
        c1, c2 = st.columns(2)
        with c1:
            refri = st.checkbox("Refrigeradora")
            cocina = st.checkbox("Cocina")
            lavadora = st.checkbox("Lavadora")
        with c2:
            sala = st.checkbox("Juego de Sala")
            comedor = st.checkbox("Juego de Comedor")
            cama = st.checkbox("Cama(s)")
            
        otros_items = st.text_area("Otros objetos (Cajas, espejos, etc.)", placeholder="Ej: 10 cajas, 1 bicicleta, 2 televisores...")
        
        fotos = st.file_uploader("📸 Sube fotos de tus cosas (Opcional)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        
        st.write("---")
        st.markdown("**Materiales de Embalaje**")
        mc1, mc2 = st.columns(2)
        with mc1:
            cant_cajas = st.number_input("Cajas de Cartón ($1.50 c/u)", min_value=0, step=1)
        with mc2:
            cant_rollos = st.number_input("Rollos de Plástico ($20.00 c/u)", min_value=0, step=1)

with col_der:
    st.subheader("3. 📍 Ruta y Personal")
    with st.container(border=True):
        # Personal
        num_ayudantes = st.slider("Número de Ayudantes ($15 c/u)", 0, 8, 0)
        
        st.write("---")
        # Accesos
        st.markdown("**Pisos / Escaleras**")
        sc1, sc2 = st.columns(2)
        with sc1:
            piso_salida = st.selectbox("Piso Salida", ["PB", "1", "2", "3", "4+"])
            asc_salida = st.checkbox("Ascensor (Salida)")
        with sc2:
            piso_llegada = st.selectbox("Piso Llegada", ["PB", "1", "2", "3", "4+"])
            asc_llegada = st.checkbox("Ascensor (Llegada)")

    # --- CÁLCULOS EN TIEMPO REAL ---
    # Lógica de precios
    p_camion = data_camion["precio"]
    p_personal = num_ayudantes * 15
    p_materiales = (cant_cajas * 1.5) + (cant_rollos * 20)
    
    # Pisos: Si no hay ascensor y es piso > 1, cobra extra
    costo_pisos = 0
    if not asc_salida and piso_salida not in ["PB", "1"]: costo_pisos += 10
    if not asc_llegada and piso_llegada not in ["PB", "1"]: costo_pisos += 10
    
    total = p_camion + p_personal + p_materiales + costo_pisos

    st.write("")
    st.write("")
    
    # --- TARJETA DE TOTAL (ESTILO LIMPIO) ---
    st.markdown(f"""
    <div style="background-color: {COLOR_PRINCIPAL}; color: white; padding: 20px; border-radius: 15px; text-align: center;">
        <h3 style="color:white !important; margin:0;">TOTAL ESTIMADO</h3>
        <h1 style="color:#FFC300 !important; font-size: 50px; margin:0;">${total:.2f}</h1>
        <p style="font-size: 12px; opacity: 0.8;">Incluye transporte y servicios seleccionados</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # --- MÉTODO DE PAGO Y CONFIRMACIÓN ---
    st.markdown("#### ✅ Finalizar")
    metodo_pago = st.selectbox("Forma de Pago", ["Efectivo", "Transferencia Bancaria", "Deuna!"])
    confirmacion = st.checkbox("Entiendo que el precio final depende del inventario real.")

    # Construcción de textos para reporte
    inv_str = f"Refri: {'Sí' if refri else 'No'}, Cocina: {'Sí' if cocina else 'No'}, Sala: {'Sí' if sala else 'No'}. Extras: {otros_items}"
    ruta_str = f"De {piso_salida} a {piso_llegada}"
    materiales_str = f"{cant_cajas} Cajas, {cant_rollos} Rollos"

    if confirmacion and total > 0:
        # 1. Mensaje WhatsApp
        msg_wa = f"*Hola Mudanza Prime!* 🚚\nQuiero reservar:\n📅 *Fecha:* {fecha}\n🚛 *Vehículo:* {camion_select}\n📦 *Inventario:* {inv_str}\n👷 *Ayudantes:* {num_ayudantes}\n💰 *Total:* ${total:.2f}\n📷 *Fotos:* {'Sí adjuntas' if fotos else 'No'}"
        link_wa = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg_wa)}"
        
        st.markdown(f"""<a href="{link_wa}" target="_blank" class="wa-btn">📲 RESERVAR AHORA</a>""", unsafe_allow_html=True)
        
        # 2. PDF
        st.write("")
        pdf_bytes = generar_pdf_completo(
            {'fecha': fecha, 'camion': camion_select, 'ruta': ruta_str, 'pago': metodo_pago, 'inventario': inv_str, 'personal': num_ayudantes, 'materiales': materiales_str},
            {'camion': p_camion, 'personal': p_personal, 'materiales': p_materiales, 'pisos': costo_pisos},
            total, fotos
        )
        st.download_button("📄 Descargar Cotización PDF", data=pdf_bytes, file_name="Cotizacion_Mudanza.pdf", mime="application/pdf", use_container_width=True)
        
    elif total == 0:
        st.warning("Selecciona un camión para ver el precio.")

# --- 7. SECCIÓN DE RESEÑAS Y CONFIANZA ---
st.divider()
st.subheader("⭐ Lo que dicen nuestros clientes")
c_rev1, c_rev2, c_rev3 = st.columns(3)

with c_rev1:
    st.markdown("""
    <div class="review-box">
        <b>María P.</b> ⭐⭐⭐⭐⭐<br>
        "Llegaron súper puntuales y trataron mis muebles con mucho cuidado. Recomendados."
    </div>
    """, unsafe_allow_html=True)

with c_rev2:
    st.markdown("""
    <div class="review-box">
        <b>Carlos A.</b> ⭐⭐⭐⭐⭐<br>
        "El camión de 3.5 toneladas estaba impecable. El personal muy educado."
    </div>
    """, unsafe_allow_html=True)

with c_rev3:
    st.markdown("""
    <div class="review-box">
        <b>Empresa S.A.</b> ⭐⭐⭐⭐⭐<br>
        "Nos ayudaron con una mudanza de oficina compleja. Todo salió perfecto."
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.caption("© 2025 Mudanza Prime Guayaquil | Todos los derechos reservados.")
