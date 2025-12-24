import streamlit as st
import datetime
import urllib.parse
from fpdf import FPDF
import os
import tempfile
import base64

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Mudanza Prime", page_icon="🚚", layout="wide")
NUMERO_WHATSAPP = "593998994518"

# --- 2. LISTA NEGRA DE ZONAS (SEGURIDAD) ---
# Puedes agregar más zonas aquí según tu experiencia
ZONAS_ROJAS = [
    "trinitaria", "guasmo", "malvinas", "socio vivienda", "entrada de la 8", 
    "monte sinai", "monte sinaí", "bastion", "bastión", "flor de bastion", 
    "prosperina", "suburbio", "cisne", "mascotas", "el fortin", "fortín"
]

def validar_zona_segura(texto):
    """Devuelve False si la zona es peligrosa"""
    if not texto: return True
    texto_lower = texto.lower()
    for zona in ZONAS_ROJAS:
        if zona in texto_lower:
            return False
    return True

# --- 3. FUNCIONES UTILITARIAS ---
def clean_text(text):
    if not isinstance(text, str): text = str(text)
    replacements = {
        '€': 'EUR', '’': "'", '–': "-", '—': "-", 'ñ': 'n', 'Ñ': 'N',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        '⚠️': '', '🚨': '', '⛔': ''
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode('latin-1', 'ignore').decode('latin-1')

# --- 4. CLASE PDF ---
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
        self.cell(0, 10, clean_text('Mudanza Prime Guayaquil'), 0, 0, 'C')

def generar_pdf_completo(datos, desglose, total, imagenes):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Datos
    pdf.set_fill_color(240, 240, 240)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, clean_text(f"Fecha Emisión: {datetime.date.today()}"), ln=1, fill=True)
    pdf.ln(5)
    
    pdf.cell(0, 7, clean_text(f"Fecha Servicio: {datos['fecha']}"), ln=1)
    pdf.cell(0, 7, clean_text(f"Ruta: {datos['ruta']}"), ln=1)
    pdf.cell(0, 7, clean_text(f"Vehículo: {datos['camion']}"), ln=1)
    pdf.ln(5)
    
    # Inventario
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "Detalle de Carga:", ln=1)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, clean_text(datos['inventario']))
    pdf.ln(5)

    # Costos
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(140, 8, "Concepto", 1)
    pdf.cell(40, 8, "Valor", 1, 1, 'C')
    
    pdf.set_font("Arial", size=11)
    pdf.cell(140, 8, clean_text(f"Transporte Base"), 1)
    pdf.cell(40, 8, f"${desglose['camion']:.2f}", 1, 1, 'R')
    pdf.cell(140, 8, clean_text(f"Personal ({datos['personal']} ayudantes)"), 1)
    pdf.cell(40, 8, f"${desglose['personal']:.2f}", 1, 1, 'R')
    pdf.cell(140, 8, clean_text(f"Accesos/Pisos"), 1)
    pdf.cell(40, 8, f"${desglose['pisos']:.2f}", 1, 1, 'R')
    pdf.cell(140, 8, clean_text(f"Materiales"), 1)
    pdf.cell(40, 8, f"${desglose['materiales']:.2f}", 1, 1, 'R')
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(46, 0, 78)
    pdf.cell(140, 12, "TOTAL ESTIMADO", 1)
    pdf.cell(40, 12, f"${total:.2f}", 1, 1, 'R')

    if imagenes:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(0,0,0)
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

# --- 5. ESTILOS ---
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
    
    /* Estilo Alerta Roja */
    .alerta-zona {
        background-color: #FFEBEE; border: 2px solid #D32F2F; color: #D32F2F; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 6. UI ---
col_logo, col_header = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"): st.image("logo.png", width=120)
    else: st.header("🚚")
with col_header:
    st.title("Mudanza Prime")
    st.markdown("**Cotizador Seguro & Profesional** | Guayaquil")
st.divider()

# --- SECCIÓN 0: RUTA Y SEGURIDAD (NUEVO) ---
st.subheader("📍 Ruta del Servicio")
st.info("Ingresa el nombre del sector o ciudadela (Ej: Urdesa, Los Ceibos, Alborada).")

col_ruta1, col_ruta2 = st.columns(2)
with col_ruta1:
    origen = st.text_input("¿Desde dónde salimos? (Sector)", placeholder="Ej: Puerto Azul")
with col_ruta2:
    destino = st.text_input("¿Hacia dónde vamos? (Sector)", placeholder="Ej: La Joya")

# VALIDACIÓN DE SEGURIDAD
es_seguro_origen = validar_zona_segura(origen)
es_seguro_destino = validar_zona_segura(destino)
bloqueo_seguridad = False

if not es_seguro_origen or not es_seguro_destino:
    bloqueo_seguridad = True
    st.markdown("""
        <div class="alerta-zona">
            ⛔ ZONA FUERA DE COBERTURA ESTÁNDAR<br>
            <span style="font-size:14px; font-weight:normal;">
            Por motivos operativos y de seguridad, no realizamos cotizaciones automáticas para el sector ingresado.
            Por favor, contáctanos directamente para evaluar el servicio.
            </span>
        </div>
    """, unsafe_allow_html=True)
    lnk = f"https://wa.me/{NUMERO_WHATSAPP}?text=Hola, quiero consultar una mudanza especial para el sector de {origen} a {destino}."
    st.markdown(f"""<a href="{lnk}" target="_blank" class="wa-btn">💬 CONSULTAR POR WHATSAPP</a>""", unsafe_allow_html=True)

# --- SI LA RUTA ES SEGURA, MOSTRAMOS EL RESTO ---
if not bloqueo_seguridad:
    
    col_izq, col_der = st.columns([1.5, 1], gap="medium")
    puntos_carga = 0 

    with col_izq:
        st.subheader("1. 🚛 Vehículo")
        fecha = st.date_input("Fecha", datetime.date.today(), min_value=datetime.date.today())
        
        camiones = {
            "Seleccionar...": {"precio": 0, "foto": None},
            "Camión 2.5 Ton ($40)": {"precio": 40, "foto": "camion 2.5.jfif"},
            "Camión 3.5 Ton ($50)": {"precio": 50, "foto": "camion 3.5.webp"},
            "Camión 6 Ton ($60)": {"precio": 60, "foto": "camion 6.jpg"},
        }
        camion_select = st.selectbox("Elige Camión", list(camiones.keys()))
        data_camion = camiones[camion_select]
        if data_camion["foto"] and os.path.exists(data_camion["foto"]):
            st.image(data_camion["foto"], caption=f"Unidad: {camion_select}", use_container_width=True)

        st.subheader("2. 📦 Inventario Detallado")
        
        with st.expander("📝 CLIC AQUÍ PARA LLENAR INVENTARIO", expanded=True):
            lista_objetos = []
            
            # DORMITORIO
            st.markdown("##### 🛏️ Dormitorios")
            c1, c2 = st.columns(2)
            with c1:
                camas_std = st.number_input("Camas 1.5 / 2 Plazas", 0, 10, 0)
                if camas_std: puntos_carga += (camas_std * 5); lista_objetos.append(f"{camas_std} Camas Std")
            with c2:
                camas_king = st.number_input("Camas Queen / King", 0, 5, 0)
                if camas_king: puntos_carga += (camas_king * 10); lista_objetos.append(f"{camas_king} Camas KING/Queen")

            # LÍNEA BLANCA
            st.write("---")
            st.markdown("##### ❄️ Línea Blanca")
            lb1, lb2 = st.columns(2)
            with lb1:
                tipo_refri = st.selectbox("Refri", ["Ninguna", "Pequeña/Mediana", "Grande (2 Puertas)", "Industrial"])
                if tipo_refri == "Pequeña/Mediana": puntos_carga += 5; lista_objetos.append("Refri Mediana")
                if tipo_refri == "Grande (2 Puertas)": puntos_carga += 12; lista_objetos.append("Refri Side-by-Side")
            with lb2:
                lavadora = st.checkbox("Lavadora")
                if lavadora: puntos_carga += 4; lista_objetos.append("Lavadora")

            # COMEDOR
            st.write("---")
            st.markdown("##### 🍽️ Comedor")
            cm1, cm2 = st.columns(2)
            with cm1:
                material_mesa = st.selectbox("Mesa", ["Sin Mesa", "Madera", "Vidrio (Delicado)", "Mármol (Pesado)"])
                if material_mesa == "Madera": puntos_carga += 6; lista_objetos.append("Mesa Madera")
                if material_mesa == "Vidrio (Delicado)": puntos_carga += 8; lista_objetos.append("Mesa Vidrio (Delicada)")
                if material_mesa == "Mármol (Pesado)": puntos_carga += 15; lista_objetos.append("Mesa MÁRMOL (Pesada)")
            with cm2:
                sillas = st.number_input("Sillas", 0, 20, 0)
                if sillas: puntos_carga += (sillas * 0.5); lista_objetos.append(f"{sillas} Sillas")

            # SALA
            st.write("---")
            st.markdown("##### 🛋️ Sala")
            sl1, sl2 = st.columns(2)
            with sl1:
                sala_l = st.checkbox("Mueble en L")
                if sala_l: puntos_carga += 10; lista_objetos.append("Sala en L")
            with sl2:
                sofas = st.number_input("Sofás Individuales", 0, 5, 0)
                if sofas: puntos_carga += (sofas * 4); lista_objetos.append(f"{sofas} Sofás")

        otros = st.text_area("Cajas y Otros", placeholder="Ej: 20 cajas, 1 piano...")
        if otros: puntos_carga += 5; lista_objetos.append(f"Extras: {otros}")
        
        fotos = st.file_uploader("Fotos (Opcional)", accept_multiple_files=True, type=['jpg', 'png', 'jpeg'])
        inv_txt = ", ".join(lista_objetos) if lista_objetos else "Básico"

        # ALERTAS
        st.write("")
        if "Mármol" in inv_txt or "King" in inv_txt or "Grande" in inv_txt:
            st.warning("⚠️ Llevas objetos pesados. Recomendamos mínimo 2-3 ayudantes.")
        if puntos_carga > 40 and "6 Ton" not in camion_select:
            st.error("🚨 Alerta: Mucha carga para camión pequeño. Sugerimos 6 Toneladas.")

    with col_der:
        st.subheader("3. 👷 Costos")
        
        st.markdown("**Ayudantes ($15 c/u)**")
        num_ayudantes = st.slider("Cant.", 0, 8, 0, label_visibility="collapsed")
        st.caption(f"Seleccionado: {num_ayudantes}")
        
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

        # CÁLCULOS
        p_camion = data_camion["precio"]
        p_personal = num_ayudantes * 15
        p_materiales = (cant_cajas * 1.5) + (cant_rollos * 20)
        
        costo_pisos = 0
        if not asc_salida and piso_salida not in ["PB", "1"]: costo_pisos += 10
        if not asc_llegada and piso_llegada not in ["PB", "1"]: costo_pisos += 10
        
        total = p_camion + p_personal + p_materiales + costo_pisos
        
        # PRECIO
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
        
        ruta_completa = f"{origen} -> {destino}"
        
        if confirmar and total > 0:
            msg = f"*MUDANZA* 🚚\n📍 {ruta_completa}\n📅 {fecha}\n🚛 {camion_select}\n💰 ${total:.2f}\n📦 {inv_txt}"
            lnk = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
            st.markdown(f"""<a href="{lnk}" target="_blank" class="wa-btn">📲 RESERVAR WHATSAPP</a>""", unsafe_allow_html=True)
            
            st.write("")
            try:
                pdf_bytes = generar_pdf_completo(
                    {'fecha': fecha, 'camion': camion_select, 'ruta': ruta_completa, 'pago': pago, 'inventario': inv_txt, 'personal': num_ayudantes, 'materiales': f"{cant_cajas} Cajas, {cant_rollos} Rollos"},
                    {'camion': p_camion, 'personal': p_personal, 'materiales': p_materiales, 'pisos': costo_pisos},
                    total, fotos
                )
                st.download_button("📄 Descargar PDF", data=pdf_bytes, file_name="Cotizacion.pdf", mime="application/pdf", use_container_width=True)
            except Exception as e:
                st.error(f"Error PDF: {e}")

st.divider()
st.subheader("⭐ Opiniones")
r1, r2, r3 = st.columns(3)
with r1: st.markdown("""<div class="review-box"><b>María P.</b> ⭐⭐⭐⭐⭐<br>"Excelente servicio en Samborondón."</div>""", unsafe_allow_html=True)
with r2: st.markdown("""<div class="review-box"><b>Carlos G.</b> ⭐⭐⭐⭐⭐<br>"Puntuales y seguros."</div>""", unsafe_allow_html=True)
with r3: st.markdown("""<div class="review-box"><b>Ana L.</b> ⭐⭐⭐⭐⭐<br>"Todo llegó bien."</div>""", unsafe_allow_html=True)
