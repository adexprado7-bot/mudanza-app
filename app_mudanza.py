import streamlit as st
import datetime
import urllib.parse
from fpdf import FPDF
import os
import tempfile
import base64

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Mudanza Prime", page_icon="🚚", layout="wide")

# --- VARIABLES GLOBALES ---
NUMERO_WHATSAPP = "593998994518"
COLOR_PRINCIPAL = "#2E004E" # Morado oscuro
COLOR_SECUNDARIO = "#FFC300" # Amarillo intenso

# --- 2. FUNCIONES UTILITARIAS ---
def clean_text(text):
    """Limpia caracteres especiales para evitar errores en el PDF"""
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        '€': 'EUR', '’': "'", '–': "-", '—': "-",
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', '📷': '', '🚚': '', '📦': '', '📅': ''
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode('latin-1', 'ignore').decode('latin-1')

# --- 3. CLASE PARA PDF ---
class PDF(FPDF):
    def header(self):
        if os.path.exists("logo.png"):
            try: self.image('logo.png', x=10, y=8, w=30)
            except: pass
        self.set_font('Arial', 'B', 16)
        self.set_text_color(46, 0, 78) 
        self.cell(0, 10, clean_text('MUDANZA PRIME'), 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, clean_text('Cotización de Servicio'), 0, 1, 'C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, clean_text('Página %s - Mudanza Prime Guayaquil' % self.page_no()), 0, 0, 'C')

def generar_pdf_completo(datos, desglose, total, imagenes):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Bloque de Fecha y Cliente
    pdf.set_fill_color(245, 245, 245)
    pdf.cell(0, 10, clean_text(f"Fecha Emisión: {datetime.date.today()}"), ln=1, fill=True)
    pdf.ln(5)
    
    pdf.cell(0, 7, clean_text(f"Fecha Servicio: {datos['fecha']}"), ln=1)
    pdf.cell(0, 7, clean_text(f"Vehículo: {datos['camion']}"), ln=1)
    pdf.cell(0, 7, clean_text(f"Ruta: {datos['ruta']}"), ln=1)
    pdf.cell(0, 7, clean_text(f"Pago: {datos['pago']}"), ln=1)
    pdf.ln(5)
    
    # Inventario
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "Resumen de Carga:", ln=1)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, clean_text(datos['inventario']))
    pdf.ln(5)

    # Tabla de Costos
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(140, 8, "Descripción", 1)
    pdf.cell(40, 8, "Valor", 1, 1, 'C')
    
    pdf.set_font("Arial", size=11)
    pdf.cell(140, 8, clean_text(f"Transporte Base"), 1)
    pdf.cell(40, 8, f"${desglose['camion']:.2f}", 1, 1, 'R')
    
    pdf.cell(140, 8, clean_text(f"Personal ({datos['personal']} ayudantes)"), 1)
    pdf.cell(40, 8, f"${desglose['personal']:.2f}", 1, 1, 'R')
    
    pdf.cell(140, 8, clean_text(f"Accesos y Pisos"), 1)
    pdf.cell(40, 8, f"${desglose['pisos']:.2f}", 1, 1, 'R')
    
    pdf.cell(140, 8, clean_text(f"Materiales ({datos['materiales']})"), 1)
    pdf.cell(40, 8, f"${desglose['materiales']:.2f}", 1, 1, 'R')
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(46, 0, 78)
    pdf.cell(140, 12, "TOTAL A PAGAR", 1)
    pdf.cell(40, 12, f"${total:.2f}", 1, 1, 'R')

    # Fotos Adjuntas
    if imagenes:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Fotos Adjuntas:", ln=1)
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

# --- 4. CSS VISIBLE (FIX FANTASMA) ---
st.markdown("""
    <style>
    /* Ocultar menú default */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Contenedores */
    .stExpander, div[data-testid="stForm"] {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 10px;
    }
    
    /* Botón de WhatsApp */
    .wa-btn {
        display: block; width: 100%; background-color: #25D366; color: white !important;
        text-align: center; padding: 15px; border-radius: 10px; text-decoration: none;
        font-weight: bold; font-size: 20px; margin-top: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .wa-btn:hover { background-color: #128C7E; }
    
    /* Títulos Morados */
    h1, h2, h3 { color: #2E004E !important; }
    
    /* Reseñas */
    .review-box {
        background-color: #FFFDE7; padding: 15px; border-radius: 10px;
        border-left: 5px solid #FFC300; font-size: 14px; color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGO Y TÍTULO ---
col_logo, col_header = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    else:
        st.header("🚚")

with col_header:
    st.title("Mudanza Prime")
    st.markdown("**Cotizador Profesional** | Guayaquil, Ecuador")

st.divider()

# --- 6. CUERPO PRINCIPAL ---
col_izq, col_der = st.columns([1.5, 1], gap="medium")

with col_izq:
    st.subheader("1. 🚛 Selecciona tu Vehículo")
    with st.container(border=True):
        fecha = st.date_input("Fecha de Mudanza", datetime.date.today(), min_value=datetime.date.today())
        
        # DEFINICIÓN DE CAMIONES
        camiones = {
            "Seleccionar...": {"precio": 0, "foto": None},
            "Camión 2.5 Toneladas ($40)": {"precio": 40, "foto": "camion 2.5.jfif"},
            "Camión 3.5 Toneladas ($50)": {"precio": 50, "foto": "camion 3.5.webp"},
            "Camión 6 Toneladas ($60)": {"precio": 60, "foto": "camion 6.jpg"},
        }
        
        camion_select = st.selectbox("Tamaño del Camión", list(camiones.keys()))
        data_camion = camiones[camion_select]
        
        # Mostrar foto
        if data_camion["foto"] and os.path.exists(data_camion["foto"]):
            st.image(data_camion["foto"], caption=f"Unidad: {camion_select}", use_container_width=True)

    st.subheader("2. 📦 Detalle de Inventario")
    with st.container(border=True):
        lista_objetos = []
        
        # --- AQUÍ RECUPERAMOS EL DISEÑO DETALLADO ---
        with st.expander("📝 Clic aquí para desglosar tus cosas", expanded=True):
            col_inv_1, col_inv_2, col_inv_3, col_inv_4 = st.columns(4)
            
            with col_inv_1:
                st.markdown("##### ❄️ Cocina")
                tipo_refri = st.selectbox("Refrigeradora", ["Ninguna", "Normal", "Side by Side (Grande)"])
                if tipo_refri != "Ninguna": lista_objetos.append(f"Refri {tipo_refri}")
                cocina = st.number_input("Cocina", 0, 5, 0)
                if cocina: lista_objetos.append(f"{cocina} Cocina")
                lavadora = st.number_input("Lavadora", 0, 5, 0)
                if lavadora: lista_objetos.append(f"{lavadora} Lavadora")
                
            with col_inv_2:
                st.markdown("##### 🛋️ Sala")
                muebles_sala = st.number_input("Juego Sala", 0, 5, 0)
                if muebles_sala: lista_objetos.append(f"{muebles_sala} Juego Sala")
                mesa_centro = st.number_input("Mesa Centro", 0, 5, 0)
                if mesa_centro: lista_objetos.append(f"{mesa_centro} Mesa Centro")
                tv = st.number_input("Televisores", 0, 5, 0)
                if tv: lista_objetos.append(f"{tv} TVs")

            with col_inv_3:
                st.markdown("##### 🍽️ Comedor")
                mesa_comedor = st.checkbox("Mesa Comedor")
                sillas = st.number_input("Sillas", 0, 12, 0)
                if mesa_comedor: lista_objetos.append(f"Mesa Comedor + {sillas} Sillas")
                elif sillas: lista_objetos.append(f"{sillas} Sillas sueltas")
                bufetera = st.number_input("Bufetera", 0, 5, 0)
                if bufetera: lista_objetos.append(f"{bufetera} Bufetera")

            with col_inv_4:
                st.markdown("##### 🛏️ Dormitorio")
                camas = st.number_input("Camas", 0, 10, 0)
                if camas: lista_objetos.append(f"{camas} Camas")
                veladores = st.number_input("Veladores", 0, 10, 0)
                if veladores: lista_objetos.append(f"{veladores} Veladores")
                comodas = st.number_input("Cómodas", 0, 5, 0)
                if comodas: lista_objetos.append(f"{comodas} Cómodas")

        st.write("---")
        otros = st.text_area("Otros objetos / Cajas Varias", placeholder="Ej: 10 cajas de libros, 1 espejo grande...")
        if others := otros.strip():
            lista_objetos.append(f"Extras: {others}")
            
        fotos = st.file_uploader("📸 Sube fotos de objetos delicados", accept_multiple_files=True, type=['jpg', 'png', 'jpeg'])

        # Generar texto final del inventario
        inv_txt = ", ".join(lista_objetos) if lista_objetos else "Inventario Básico"

with col_der:
    st.subheader("3. 👷 Servicios y Costos")
    with st.container(border=True):
        st.markdown("##### Personal de Carga")
        num_ayudantes = st.slider("Ayudantes ($15 c/u)", 0, 8, 0)
        
        st.markdown("##### Accesos (Pisos)")
        c_sal, c_lleg = st.columns(2)
        with c_sal:
            piso_salida = st.selectbox("Salida", ["PB", "1", "2", "3", "4+"])
            asc_salida = st.checkbox("Ascensor (S)")
        with c_lleg:
            piso_llegada = st.selectbox("Llegada", ["PB", "1", "2", "3", "4+"])
            asc_llegada = st.checkbox("Ascensor (Ll)")
            
        st.markdown("##### Materiales")
        c_mat1, c_mat2 = st.columns(2)
        with c_mat1:
            cant_cajas = st.number_input("Cajas ($1.50)", min_value=0)
        with c_mat2:
            cant_rollos = st.number_input("Rollos ($20)", min_value=0)

    # --- LÓGICA DE PRECIOS ---
    p_camion = data_camion["precio"]
    p_personal = num_ayudantes * 15
    p_materiales = (cant_cajas * 1.5) + (cant_rollos * 20)
    
    costo_pisos = 0
    if not asc_salida and piso_salida not in ["PB", "1"]: costo_pisos += 10
    if not asc_llegada and piso_llegada not in ["PB", "1"]: costo_pisos += 10
    
    total = p_camion + p_personal + p_materiales + costo_pisos
    
    # --- TARJETA DE TOTAL (Amarillo Visible) ---
    st.write("")
    
    st.markdown(f"""
    <div style="
        background-color: #FFC300; 
        color: #2E004E; 
        padding: 25px; 
        border-radius: 15px; 
        text-align: center; 
        border: 2px solid #2E004E;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        <h3 style="color: #2E004E !important; margin:0; font-weight:bold;">TOTAL ESTIMADO</h3>
        <h1 style="color: #2E004E !important; font-size: 55px; margin:0; font-weight:900;">${total:.2f}</h1>
        <p style="color: #2E004E; margin:0; font-size: 14px; font-weight:500;">Sujeto a confirmación final</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.markdown("##### Finalizar Reserva")
    pago = st.selectbox("Método de Pago", ["Efectivo", "Transferencia", "Deuna!"])
    confirmar = st.checkbox("Acepto que el valor es referencial.")
    
    ruta_txt = f"De {piso_salida} a {piso_llegada}"
    mat_txt = f"{cant_cajas} Cajas, {cant_rollos} Rollos"
    
    if confirmar and total > 0:
        # Botón WhatsApp
        msg = f"*SOLICITUD DE MUDANZA* 🚚\n📅 {fecha}\n🚛 {camion_select}\n💰 Total: ${total:.2f}\n📦 {inv_txt}"
        lnk = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
        st.markdown(f"""<a href="{lnk}" target="_blank" class="wa-btn">📲 RESERVAR POR WHATSAPP</a>""", unsafe_allow_html=True)
        
        # Botón PDF
        st.write("")
        try:
            pdf_bytes = generar_pdf_completo(
                {'fecha': fecha, 'camion': camion_select, 'ruta': ruta_txt, 'pago': pago, 'inventario': inv_txt, 'personal': num_ayudantes, 'materiales': mat_txt},
                {'camion': p_camion, 'personal': p_personal, 'materiales': p_materiales, 'pisos': costo_pisos},
                total, fotos
            )
            st.download_button("📄 Descargar Cotización PDF", data=pdf_bytes, file_name="Cotizacion.pdf", mime="application/pdf", use_container_width=True)
        except Exception as e:
            st.error(f"Error al generar PDF: {e}")

# --- 7. SECCIÓN DE RESEÑAS ---
st.divider()
st.subheader("⭐ Opiniones de Clientes")
r1, r2, r3 = st.columns(3)

with r1:
    st.markdown("""<div class="review-box"><b>María P.</b> ⭐⭐⭐⭐⭐<br>"Excelente servicio, muy cuidadosos con mi refrigeradora."</div>""", unsafe_allow_html=True)
with r2:
    st.markdown("""<div class="review-box"><b>Carlos G.</b> ⭐⭐⭐⭐⭐<br>"El camión llegó puntual. Recomendados 100% en Guayaquil."</div>""", unsafe_allow_html=True)
with r3:
    st.markdown("""<div class="review-box"><b>Ana L.</b> ⭐⭐⭐⭐⭐<br>"Me ayudaron a embalar todo. El personal muy amable."</div>""", unsafe_allow_html=True)
