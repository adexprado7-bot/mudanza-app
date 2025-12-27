import streamlit as st
import datetime
import urllib.parse
from fpdf import FPDF
import os
import tempfile
import base64

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Mudanzas Acom", page_icon="🚛", layout="wide")
NUMERO_WHATSAPP = "593998994518"

# --- 2. ZONAS Y SEGURIDAD ---
ZONAS_ROJAS = [
    "trinitaria", "guasmo", "malvinas", "socio vivienda", "entrada de la 8", 
    "monte sinai", "monte sinaí", "bastion", "bastión", "flor de bastion", 
    "prosperina", "suburbio", "cisne", "mascotas", "el fortin", "fortín"
]

def validar_zona_segura(texto):
    if not texto: return True
    texto_lower = texto.lower()
    for zona in ZONAS_ROJAS:
        if zona in texto_lower: return False
    return True

# --- 3. UTILIDADES ---
def clean_text(text):
    if not isinstance(text, str): text = str(text)
    replacements = {
        '€': 'EUR', '’': "'", '–': "-", '—': "-", 'ñ': 'n', 'Ñ': 'N',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        '⚠️': '', '🚨': '', '⛔': '', '📍': '', '📹': '', '🛡️': '', '💡': ''
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode('latin-1', 'ignore').decode('latin-1')

# --- 4. CLASE PDF (REBRANDING) ---
class PDF(FPDF):
    def header(self):
        if os.path.exists("logo.png"):
            try: self.image('logo.png', x=10, y=8, w=30)
            except: pass
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 68, 129) # Azul Corporativo
        self.cell(0, 10, clean_text('MUDANZAS ACOM'), 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, clean_text('Alianza Estratégica & Logística'), 0, 1, 'C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, clean_text('Mudanzas Acom - Servicio Garantizado'), 0, 0, 'C')

def generar_pdf_completo(datos, desglose, total, imagenes, tiene_video):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Encabezado (Gris muy suave)
    pdf.set_fill_color(245, 245, 245)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, clean_text(f"Fecha Emisión: {datetime.date.today()}"), ln=1, fill=True)
    pdf.ln(5)
    
    # Datos Generales
    pdf.cell(0, 7, clean_text(f"Fecha Servicio: {datos['fecha']}"), ln=1)
    pdf.cell(0, 7, clean_text(f"Hora Solicitada: {datos['horario']}"), ln=1)
    pdf.cell(0, 7, clean_text(f"Vehículo: {datos['camion']}"), ln=1)
    
    pdf.set_font("Arial", 'B', 11)
    pdf.ln(2)
    pdf.cell(0, 7, "Detalle de Ruta:", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, clean_text(datos['ruta']))
    pdf.ln(5)
    
    # Inventario
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "Carga Declarada:", ln=1)
    pdf.set_font("Arial", size=10)
    
    texto_inv = datos['inventario']
    if tiene_video:
        texto_inv += "\n[!] EL CLIENTE ADJUNTÓ VIDEO DE REFERENCIA."
        
    pdf.multi_cell(0, 5, clean_text(texto_inv))
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
    
    if desglose['parada_extra'] > 0:
        pdf.cell(140, 8, clean_text(f"Parada Adicional"), 1)
        pdf.cell(40, 8, f"${desglose['parada_extra']:.2f}", 1, 1, 'R')
        
    if desglose['seguro'] > 0:
        pdf.cell(140, 8, clean_text(f"Seguro de Carga (Protección)"), 1)
        pdf.cell(40, 8, f"${desglose['seguro']:.2f}", 1, 1, 'R')

    pdf.cell(140, 8, clean_text(f"Accesos/Pisos"), 1)
    pdf.cell(40, 8, f"${desglose['pisos']:.2f}", 1, 1, 'R')
    pdf.cell(140, 8, clean_text(f"Materiales"), 1)
    pdf.cell(40, 8, f"${desglose['materiales']:.2f}", 1, 1, 'R')
    
    pdf.set_font("Arial", 'B', 14)
    # Azul para el total en PDF
    pdf.set_text_color(0, 68, 129)
    pdf.cell(140, 12, "TOTAL ESTIMADO", 1)
    pdf.cell(40, 12, f"${total:.2f}", 1, 1, 'R')

    # Fotos
    if imagenes:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(0,0,0)
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

# --- 5. ESTILOS AZUL Y BLANCO ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Botón WhatsApp: Un verde más profesional que combine con azul */
    .wa-btn {
        display: block; width: 100%; 
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: white !important;
        text-align: center; padding: 15px; border-radius: 8px; 
        font-weight: bold; font-size: 20px; 
        margin-top: 5px; text-decoration: none; 
        box-shadow: 0 4px 10px rgba(37, 211, 102, 0.2);
        transition: transform 0.2s;
    }
    .wa-btn:hover { transform: translateY(-2px); }
    
    /* Títulos en Azul Corporativo Acom */
    h1, h2, h3 { color: #004481 !important; } 
    
    /* Modo Oscuro: Títulos en Azul Claro */
    @media (prefers-color-scheme: dark) { h1, h2, h3 { color: #64B5F6 !important; } }
    
    /* Cajas de Reseñas: Blanco con borde azul */
    .review-box {
        background-color: #F5F9FC; color: #333; 
        padding: 15px; border-radius: 8px;
        border-left: 5px solid #004481; 
        font-size: 14px; margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    @media (prefers-color-scheme: dark) { 
        .review-box { background-color: #1E293B; color: white; border-left: 5px solid #64B5F6; } 
    }
    
    .alerta-zona {
        background-color: #FFEBEE; border: 1px solid #D32F2F; color: #D32F2F; 
        padding: 15px; border-radius: 8px; font-weight: bold; 
        text-align: center; margin-bottom: 20px;
    }
    .instruccion-adjunto {
        background-color: #E3F2FD; color: #004481; padding: 10px; 
        border-radius: 8px; text-align: center; font-size: 14px; 
        margin-bottom: 5px; border: 1px dashed #004481;
    }
    .caja-sugerencia {
        background-color: #F0F4C3; color: #33691E; padding: 10px; border-radius: 8px; 
        border-left: 5px solid #8BC34A; font-size: 14px; margin-bottom: 10px;
    }
    
    /* Estilo para los inputs */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        border-color: #E0E0E0;
    }
    </style>
""", unsafe_allow_html=True)

# --- 6. UI PRINCIPAL ---
col_logo, col_header = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"): st.image("logo.png", width=120)
    else: st.header("🚛")
with col_header:
    st.title("Mudanzas Acom")
    st.markdown("**Calidad, Confianza y Seguridad** | Socio Estratégico")
st.divider()

# --- RUTA ---
st.subheader("📍 Ruta del Servicio")
col_ruta1, col_ruta2 = st.columns(2)
with col_ruta1: origen = st.text_input("¿Desde dónde salimos?", placeholder="Ej: Ceibos")
with col_ruta2: destino = st.text_input("¿Hacia dónde vamos?", placeholder="Ej: Vía a la Costa")

parada_extra = st.checkbox("➕ Agregar parada extra (+$15.00)")
texto_parada = ""
costo_parada = 0
if parada_extra:
    texto_parada = st.text_input("Dirección de la parada extra:", placeholder="Ej: Dejar cama en Urdesa")
    costo_parada = 15.00

# VALIDACIÓN
bloqueo = False
if not (validar_zona_segura(origen) and validar_zona_segura(destino) and validar_zona_segura(texto_parada)):
    bloqueo = True
    st.markdown("""<div class="alerta-zona">⛔ ZONA FUERA DE COBERTURA ESTÁNDAR. CONTÁCTANOS POR WHATSAPP.</div>""", unsafe_allow_html=True)
    lnk = f"https://wa.me/{NUMERO_WHATSAPP}?text=Consulta especial por zona de riesgo."
    st.markdown(f"""<a href="{lnk}" target="_blank" class="wa-btn">💬 CONSULTAR MANUALMENTE</a>""", unsafe_allow_html=True)

if not bloqueo:
    col_izq, col_der = st.columns([1.5, 1], gap="medium")
    puntos_carga = 0 
    cajas_estimadas = 0 

    with col_izq:
        st.subheader("1. 🚛 Vehículo y Horario")
        col_fecha, col_hora = st.columns(2)
        with col_fecha:
            fecha = st.date_input("Fecha", datetime.date.today(), min_value=datetime.date.today())
        with col_hora:
            horas = [
                "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
                "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"
            ]
            hora_inicio = st.selectbox("Hora de Inicio Preferida", horas)
            st.caption("ℹ️ Consultaremos disponibilidad al recibir tu pedido.")

        camiones = {
            "Seleccionar...": {"precio": 0, "foto": None},
            "Furgoneta (Pequeña) - $30": {"precio": 30, "foto": "furgoneta.jpg"},
            "Camión 2.5 Ton ($40)": {"precio": 40, "foto": "camion 2.5.jfif"},
            "Camión 3.5 Ton ($50)": {"precio": 50, "foto": "camion 3.5.webp"},
            "Camión 6 Ton ($60)": {"precio": 60, "foto": "camion 6.jpg"},
        }
        camion_select = st.selectbox("Elige Vehículo", list(camiones.keys()))
        data_camion = camiones[camion_select]
        if data_camion["foto"] and os.path.exists(data_camion["foto"]):
            st.image(data_camion["foto"], caption=f"Unidad: {camion_select}", use_container_width=True)

        st.subheader("2. 📦 Inventario & Video")
        with st.expander("📝 LISTA DE OBJETOS", expanded=True):
            lista_objetos = []
            
            st.markdown("##### 🛏️ Dormitorios")
            c1, c2 = st.columns(2)
            with c1:
                camas_std = st.number_input("Camas 1.5 / 2 Plazas", 0, 10, 0)
                if camas_std: 
                    puntos_carga += (camas_std * 5)
                    cajas_estimadas += (camas_std * 2) 
                    lista_objetos.append(f"{camas_std} Camas Std")
            with c2:
                camas_king = st.number_input("Camas Queen / King", 0, 5, 0)
                if camas_king: 
                    puntos_carga += (camas_king * 10)
                    cajas_estimadas += (camas_king * 3)
                    lista_objetos.append(f"{camas_king} Camas KING")

            st.write("---")
            st.markdown("##### 🍽️ Comedor")
            cm1, cm2 = st.columns(2)
            with cm1:
                mat_mesa = st.selectbox("Mesa", ["Sin Mesa", "Madera", "Vidrio", "Mármol"])
                if mat_mesa != "Sin Mesa": 
                    pts = 15 if "Mármol" in mat_mesa else (8 if "Vidrio" in mat_mesa else 6)
                    puntos_carga += pts
                    cajas_estimadas += 2 
                    lista_objetos.append(f"Mesa {mat_mesa}")
            with cm2:
                sillas = st.number_input("Sillas", 0, 20, 0)
                if sillas: puntos_carga += (sillas * 0.5); lista_objetos.append(f"{sillas} Sillas")

            st.write("---")
            lb1, lb2 = st.columns(2)
            with lb1:
                st.markdown("##### ❄️ Línea Blanca")
                refri = st.selectbox("Refri", ["No", "Normal", "Side-by-Side"])
                if refri != "No": 
                    pts = 12 if "Side" in refri else 5
                    puntos_carga += pts; lista_objetos.append(f"Refri {refri}")
                
                cocina_item = st.checkbox("Cocina (Estufa)")
                if cocina_item:
                    cajas_estimadas += 4 
                    lista_objetos.append("Cocina")
                    
            with lb2:
                st.markdown("##### 🛋️ Sala")
                sala = st.checkbox("Juego de Sala")
                if sala: 
                    puntos_carga += 10
                    cajas_estimadas += 2 
                    lista_objetos.append("Juego Sala")

        otros = st.text_area("Cajas / Otros", placeholder="Ej: Libros, Ropa, Juguetes...")
        if otros: puntos_carga += 5; lista_objetos.append(f"Extras: {otros}")
        
        if cajas_estimadas > 0: cajas_estimadas += 2 

        st.write("---")
        st.markdown("##### 📹 Subir Evidencia")
        video_file = st.file_uploader("Video (MP4/MOV) - Max 30seg", type=['mp4', 'mov', 'avi'])
        fotos = st.file_uploader("Fotos (JPG/PNG)", accept_multiple_files=True, type=['jpg', 'png'])
        
        tiene_video = video_file is not None
        inv_txt = ", ".join(lista_objetos) if lista_objetos else "Básico"

        if puntos_carga > 40 and "6 Ton" not in camion_select:
            st.error("🚨 Alerta: Mucha carga. Sugerimos Camión 6 Toneladas.")

    with col_der:
        st.subheader("3. 👷 Costos")
        num_ayudantes = st.slider("Ayudantes ($15 c/u)", 0, 8, 0)
        
        st.write("---")
        st.markdown("**Accesos**")
        c_sal, c_lleg = st.columns(2)
        with c_sal:
            piso_sal = st.selectbox("Salida", ["PB", "1", "2", "3", "4+"])
            asc_sal = st.checkbox("Asc. (S)")
        with c_lleg:
            piso_lleg = st.selectbox("Llegada", ["PB", "1", "2", "3", "4+"])
            asc_lleg = st.checkbox("Asc. (Ll)")
            
        st.write("---")
        st.markdown("**Materiales**")
        
        if cajas_estimadas > 5:
            st.markdown(f"""
            <div class="caja-sugerencia">
                💡 <b>Sugerencia:</b> Estimamos que necesitarás <b>{cajas_estimadas} cajas</b>.
            </div>
            """, unsafe_allow_html=True)
        
        c_m1, c_m2 = st.columns(2)
        with c_m1: c_cajas = st.number_input("Cajas $1.5", 0)
        with c_m2: c_rollos = st.number_input("Rollos $20", 0)

        st.write("---")
        seguro = st.checkbox("🛡️ Proteger carga (Seguro +$8.00)")
        costo_seguro = 8.00 if seguro else 0

        # CÁLCULOS
        p_camion = data_camion["precio"]
        p_personal = num_ayudantes * 15
        p_mat = (c_cajas * 1.5) + (c_rollos * 20)
        
        p_pisos = 0
        if not asc_sal and piso_sal not in ["PB", "1"]: p_pisos += 10
        if not asc_lleg and piso_lleg not in ["PB", "1"]: p_pisos += 10
        
        total = p_camion + p_personal + p_mat + p_pisos + costo_parada + costo_seguro
        
        # TARJETA TOTAL EN AZUL Y BLANCO
        st.write("")
        st.markdown(f"""
        <div style="background-color: #004481; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(0, 68, 129, 0.3);">
            <div style="color: white !important; font-size: 20px; font-weight: bold; opacity: 0.9;">TOTAL ESTIMADO</div>
            <div style="color: white !important; font-size: 55px; font-weight: 900; line-height: 1.1;">${total:.2f}</div>
            <div style="color: white !important; font-size: 14px; opacity: 0.8; margin-top: 5px;">Mudanzas Acom Garantía</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        pago = st.selectbox("Pago", ["Efectivo", "Transferencia", "Deuna!"])
        confirmar = st.checkbox("Acepto términos.")
        
        ruta_final = f"{origen} -> {destino}"
        if parada_extra: ruta_final += f" (Parada: {texto_parada})"
        
        if confirmar and total > 0:
            txt_vid = "📹 ¡TENGO VIDEO!" if tiene_video else "No"
            txt_seguro = "🛡️ CON SEGURO" if seguro else "Sin seguro"
            
            msg = f"*PEDIDO ACOM* 🚚\n📍 {ruta_final}\n📅 {fecha} ({hora_inicio})\n🚛 {camion_select}\n💰 ${total:.2f}\n📦 {inv_txt}\n{txt_vid}\n{txt_seguro}"
            lnk = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
            
            if tiene_video or fotos:
                st.markdown("""<div class="instruccion-adjunto">👆 <b>¡RECUERDA!</b> Adjunta tu <b>VIDEO/PDF</b> en WhatsApp.</div>""", unsafe_allow_html=True)
            
            st.markdown(f"""<a href="{lnk}" target="_blank" class="wa-btn">📲 CONFIRMAR EN WHATSAPP</a>""", unsafe_allow_html=True)
            
            st.write("")
            try:
                pdf_bytes = generar_pdf_completo(
                    {'fecha': fecha, 'horario': hora_inicio, 'camion': camion_select, 'ruta': ruta_final, 'pago': pago, 'inventario': inv_txt, 'personal': num_ayudantes},
                    {'camion': p_camion, 'personal': p_personal, 'materiales': p_mat, 'pisos': p_pisos, 'parada_extra': costo_parada, 'seguro': costo_seguro},
                    total, fotos, tiene_video
                )
                st.download_button("📄 Bajar PDF Acom", data=pdf_bytes, file_name="Cotizacion_Acom.pdf", mime="application/pdf", use_container_width=True)
            except Exception as e:
                st.error(f"Error PDF: {e}")

st.divider()
st.subheader("⭐ Experiencias Acom")
r1, r2, r3 = st.columns(3)
with r1: st.markdown("""<div class="review-box"><b>María P.</b> ⭐⭐⭐⭐⭐<br>"Excelente servicio y seriedad."</div>""", unsafe_allow_html=True)
with r2: st.markdown("""<div class="review-box"><b>Carlos G.</b> ⭐⭐⭐⭐⭐<br>"Llegaron a la hora exacta. Muy formales."</div>""", unsafe_allow_html=True)
with r3: st.markdown("""<div class="review-box"><b>Ana L.</b> ⭐⭐⭐⭐⭐<br>"Me sentí segura con el servicio."</div>""", unsafe_allow_html=True)
