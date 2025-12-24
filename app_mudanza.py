import streamlit as st
import datetime
import urllib.parse
from fpdf import FPDF
import os
import tempfile
import base64

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Mudanza Prime", page_icon="🚚", layout="wide")

# --- VARIABLES ---
NUMERO_WHATSAPP = "593998994518"

# --- 2. FUNCIONES UTILITARIAS ---
def clean_text(text):
    """Limpia caracteres para PDF"""
    if not isinstance(text, str): text = str(text)
    replacements = {
        '€': 'EUR', '’': "'", '–': "-", '—': "-",
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U', '⚠️': ''
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode('latin-1', 'ignore').decode('latin-1')

# --- 3. CLASE PDF ---
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
        self.cell(0, 5, clean_text('Cotización Inteligente'), 0, 1, 'C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, clean_text('Mudanza Prime Guayaquil - Expertos en Logística'), 0, 0, 'C')

def generar_pdf_completo(datos, desglose, total, imagenes):
    pdf = PDF()
    
    # --- PÁGINA 1: COTIZACIÓN ---
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Bloque Gris
    pdf.set_fill_color(240, 240, 240)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, clean_text(f"Fecha Emisión: {datetime.date.today()}"), ln=1, fill=True)
    pdf.ln(5)
    
    # Datos
    pdf.cell(0, 7, clean_text(f"Fecha Servicio: {datos['fecha']}"), ln=1)
    pdf.cell(0, 7, clean_text(f"Vehículo: {datos['camion']}"), ln=1)
    pdf.cell(0, 7, clean_text(f"Ruta: {datos['ruta']}"), ln=1)
    pdf.cell(0, 7, clean_text(f"Pago: {datos['pago']}"), ln=1)
    pdf.ln(5)
    
    # Inventario
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "Inventario Declarado:", ln=1)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, clean_text(datos['inventario']))
    pdf.ln(5)

    # Costos
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(140, 8, "Detalle", 1)
    pdf.cell(40, 8, "Valor", 1, 1, 'C')
    
    pdf.set_font("Arial", size=11)
    pdf.cell(140, 8, clean_text(f"Transporte Base"), 1)
    pdf.cell(40, 8, f"${desglose['camion']:.2f}", 1, 1, 'R')
    pdf.cell(140, 8, clean_text(f"Personal ({datos['personal']} ayudantes)"), 1)
    pdf.cell(40, 8, f"${desglose['personal']:.2f}", 1, 1, 'R')
    pdf.cell(140, 8, clean_text(f"Accesos y Pisos"), 1)
    pdf.cell(40, 8, f"${desglose['pisos']:.2f}", 1, 1, 'R')
    pdf.cell(140, 8, clean_text(f"Materiales"), 1)
    pdf.cell(40, 8, f"${desglose['materiales']:.2f}", 1, 1, 'R')
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(46, 0, 78)
    pdf.cell(140, 12, "TOTAL ESTIMADO", 1)
    pdf.cell(40, 12, f"${total:.2f}", 1, 1, 'R')
    
    # --- PÁGINA 2: CHECKLIST DE VALOR (NUEVO) ---
    pdf.add_page()
    pdf.set_text_color(0,0,0)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, clean_text("🎁 TU GUÍA DE MUDANZA PRIME"), 0, 1, 'C')
    pdf.ln(5)
    
    pdf.set_font("Arial", size=11)
    checklist = """
    Para que tu experiencia sea perfecta, te recomendamos:
    
    1. SEMANA PREVIA:
       [ ] Consigue cajas medianas (son mas faciles de cargar).
       [ ] Separa lo que NO vas a llevar (dona o vende).
       [ ] Etiqueta cada caja con el nombre de la habitacion destino.
    
    2. EL DIA ANTERIOR:
       [ ] Descongela la refrigeradora 24 horas antes.
       [ ] Guarda joyas, dinero y documentos importantes en tu bolso personal.
       [ ] Desconecta lavadora y secadora.
    
    3. EL DIA DE LA MUDANZA:
       [ ] Reserva parqueo para el camion (al menos 10 metros).
       [ ] Ten a la mano llaves de la nueva casa.
       [ ] ¡Relajate! Nosotros nos encargamos del peso pesado.
    """
    pdf.multi_cell(0, 7, clean_text(checklist))

    # Fotos
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

# --- 4. CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .wa-btn {
        display: block; width: 100%; background-color: #25D366; color: white !important;
        text-align: center; padding: 15px; border-radius: 10px; font-weight: bold; font-size: 20px;
        margin-top: 10px; text-decoration: none; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .wa-btn:hover { background-color: #128C7E; transform: scale(1.02); }
    h1, h2, h3 { color: #8A2BE2 !important; } 
    @media (prefers-color-scheme: dark) { h1, h2, h3 { color: #D8B4FE !important; } }
    .review-box {
        background-color: #FFFDE7; color: black; padding: 15px; border-radius: 10px;
        border-left: 5px solid #FFC300; font-size: 14px; margin-bottom: 10px;
    }
    @media (prefers-color-scheme: dark) { .review-box { background-color: #262730; color: white; } }
    </style>
""", unsafe_allow_html=True)

# --- 5. ENCABEZADO ---
col_logo, col_header = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"): st.image("logo.png", width=120)
    else: st.header("🚚")
with col_header:
    st.title("Mudanza Prime")
    st.markdown("**Cotizador Inteligente** | Guayaquil")
st.divider()

# --- 6. LOGICA ---
col_izq, col_der = st.columns([1.5, 1], gap="medium")

# Variables para lógica de recomendación
puntos_carga = 0 

with col_izq:
    st.subheader("1. 🚛 Vehículo")
    fecha = st.date_input("Fecha", datetime.date.today(), min_value=datetime.date.today())
    
    camiones = {
        "Seleccionar...": {"precio": 0, "capacidad": 0, "foto": None},
        "Camión 2.5 Toneladas ($40)": {"precio": 40, "capacidad": 20, "foto": "camion 2.5.jfif"},
        "Camión 3.5 Toneladas ($50)": {"precio": 50, "capacidad": 40, "foto": "camion 3.5.webp"},
        "Camión 6 Toneladas ($60)": {"precio": 60, "capacidad": 70, "foto": "camion 6.jpg"},
    }
    camion_select = st.selectbox("Elige Camión", list(camiones.keys()))
    data_camion = camiones[camion_select]
    if data_camion["foto"] and os.path.exists(data_camion["foto"]):
        st.image(data_camion["foto"], caption=f"Unidad: {camion_select}", use_container_width=True)

    st.subheader("2. 📦 Inventario (Suma Puntos)")
    with st.expander("📝 Desglosar Inventario", expanded=True):
        lista_objetos = []
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown("**❄️ Cocina**")
            refri = st.selectbox("Refri", ["No", "Pequeña", "Grande"])
            if refri == "Pequeña": puntos_carga += 4; lista_objetos.append("Refri Peq.")
            if refri == "Grande": puntos_carga += 8; lista_objetos.append("Refri Grande")
            
            cocina = st.number_input("Cocina", 0, 5, 0)
            if cocina: puntos_carga += (cocina * 3); lista_objetos.append(f"{cocina} Cocina")
            
            lavadora = st.number_input("Lavadora", 0, 5, 0)
            if lavadora: puntos_carga += (lavadora * 3); lista_objetos.append(f"{lavadora} Lavadora")

        with c2:
            st.markdown("**🛋️ Sala**")
            sala = st.number_input("Juego Sala", 0, 5, 0)
            if sala: puntos_carga += (sala * 10); lista_objetos.append(f"{sala} Juego Sala")
            
            tv = st.number_input("TVs", 0, 5, 0)
            if tv: puntos_carga += (tv * 1); lista_objetos.append(f"{tv} TVs")
            
        with c3:
            st.markdown("**🍽️ Comedor**")
            sillas = st.number_input("Sillas", 0, 12, 0)
            if sillas: puntos_carga += (sillas * 0.5); lista_objetos.append(f"{sillas} Sillas")
            mesa = st.checkbox("Mesa Comedor")
            if mesa: puntos_carga += 5; lista_objetos.append("Mesa Comedor")
            
        with c4:
            st.markdown("**🛏️ Cuartos**")
            camas = st.number_input("Camas", 0, 10, 0)
            if camas: puntos_carga += (camas * 8); lista_objetos.append(f"{camas} Camas")
            
            aires = st.number_input("Aires", 0, 10, 0)
            if aires: puntos_carga += (aires * 1); lista_objetos.append(f"{aires} Aires")

    otros = st.text_area("Cajas / Otros", placeholder="Ej: 15 cajas, bicicleta...")
    if others := otros.strip():
        # Estimación simple: 1 punto por cada 10 caracteres de texto (heurística)
        puntos_carga += len(others) / 10 
        lista_objetos.append(f"Extras: {others}")
        
    fotos = st.file_uploader("Fotos (Opcional)", accept_multiple_files=True, type=['jpg', 'png', 'jpeg'])
    inv_txt = ", ".join(lista_objetos) if lista_objetos else "Básico"

    # --- LÓGICA DE RECOMENDACIÓN INTELIGENTE ---
    st.write("")
    if puntos_carga > 0:
        if puntos_carga > 45 and "6 Toneladas" not in camion_select:
            st.warning("⚠️ **Sugerencia:** Tienes mucha carga. Te recomendamos el **Camión de 6 Toneladas** para que todo entre seguro.")
        elif puntos_carga > 25 and "3.5 Toneladas" not in camion_select and "6 Toneladas" not in camion_select:
            st.info("ℹ️ **Consejo:** Para esa cantidad de muebles, el **Camión de 3.5 Toneladas** es el ideal.")

with col_der:
    st.subheader("3. 👷 Costos")
    
    st.markdown("**Ayudantes ($15 c/u)**")
    st.caption("Incluye herramientas básicas para desarmado simple.")
    num_ayudantes = st.slider("Cant.", 0, 8, 0, label_visibility="collapsed")
    st.write(f"Seleccionado: {num_ayudantes}")
    
    st.write("---")
    st.markdown("**Accesos**")
    c_sal, c_lleg = st.columns(2)
    with c_sal:
        piso_salida = st.selectbox("Salida", ["PB", "1", "2", "3", "4+"])
        asc_salida = st.checkbox("Asc. (S)")
    with c_lleg:
        piso_llegada = st.selectbox("Llegada", ["PB", "1", "2", "3", "4+"])
        asc_llegada = st.checkbox("Asc. (Ll)")
        
    st.write("---")
    st.markdown("**Materiales**")
    c_m1, c_m2 = st.columns(2)
    with c_m1: cant_cajas = st.number_input("Cajas $1.5", 0)
    with c_m2: cant_rollos = st.number_input("Rollos $20", 0)

    # --- CÁLCULOS ---
    p_camion = data_camion["precio"]
    p_personal = num_ayudantes * 15
    p_materiales = (cant_cajas * 1.5) + (cant_rollos * 20)
    
    costo_pisos = 0
    if not asc_salida and piso_salida not in ["PB", "1"]: costo_pisos += 10
    if not asc_llegada and piso_llegada not in ["PB", "1"]: costo_pisos += 10
    
    total = p_camion + p_personal + p_materiales + costo_pisos
    
    # --- TARJETA PRECIO ---
    st.write("")
    st.markdown(f"""
    <div style="
        background-color: #FFC300; padding: 20px; border-radius: 12px; text-align: center; border: 2px solid #2E004E;">
        <div style="color: #2E004E !important; font-size: 20px; font-weight: bold;">TOTAL ESTIMADO</div>
        <div style="color: #2E004E !important; font-size: 55px; font-weight: 900; line-height: 1;">${total:.2f}</div>
        <div style="color: #2E004E !important; font-size: 14px;">Referencial</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    pago = st.selectbox("Pago", ["Efectivo", "Transferencia", "Deuna!"])
    confirmar = st.checkbox("Acepto que el valor es referencial.")
    
    ruta_txt = f"De {piso_salida} a {piso_llegada}"
    mat_txt = f"{cant_cajas} Cajas, {cant_rollos} Rollos"
    
    if confirmar and total > 0:
        msg = f"*SOLICITUD MUDANZA* 🚚\n📅 {fecha}\n🚛 {camion_select}\n💰 ${total:.2f}\n📦 {inv_txt}"
        lnk = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
        st.markdown(f"""<a href="{lnk}" target="_blank" class="wa-btn">📲 RESERVAR WHATSAPP</a>""", unsafe_allow_html=True)
        
        st.write("")
        try:
            pdf_bytes = generar_pdf_completo(
                {'fecha': fecha, 'camion': camion_select, 'ruta': ruta_txt, 'pago': pago, 'inventario': inv_txt, 'personal': num_ayudantes, 'materiales': mat_txt},
                {'camion': p_camion, 'personal': p_personal, 'materiales': p_materiales, 'pisos': costo_pisos},
                total, fotos
            )
            st.download_button("📄 Bajar Cotización + Checklist", data=pdf_bytes, file_name="Cotizacion_Mudanza.pdf", mime="application/pdf", use_container_width=True)
        except Exception as e:
            st.error(f"Error PDF: {e}")

st.divider()
st.subheader("⭐ Opiniones")
r1, r2, r3 = st.columns(3)
with r1: st.markdown("""<div class="review-box"><b>María P.</b> ⭐⭐⭐⭐⭐<br>"Excelente servicio."</div>""", unsafe_allow_html=True)
with r2: st.markdown("""<div class="review-box"><b>Carlos G.</b> ⭐⭐⭐⭐⭐<br>"Puntuales y rápidos."</div>""", unsafe_allow_html=True)
with r3: st.markdown("""<div class="review-box"><b>Ana L.</b> ⭐⭐⭐⭐⭐<br>"Recomendados."</div>""", unsafe_allow_html=True)
