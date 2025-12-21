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
NUMERO_WHATSAPP = "593998994518"

# --- FUNCIÓN PARA LIMPIAR TEXTO (ADIÓS ERROR UNICODE) ---
def clean_text(text):
    # Esta función elimina emojis y caracteres raros para que el PDF no falle
    return text.encode('latin-1', 'ignore').decode('latin-1')

# --- CLASE PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 20)
        self.set_text_color(46, 0, 78) 
        self.cell(0, 10, clean_text('MUDANZA PRIME'), 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, clean_text('Detalle de Solicitud de Servicio'), 0, 1, 'C')
        self.ln(10)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, clean_text('Mudanza Prime - Guayaquil | Cotizacion sujeta a disponibilidad'), 0, 0, 'C')

def generar_pdf(fecha, camion, personal, materiales, accesos_txt, inventario_txt, total, desglose):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Fecha Emisión
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, txt=clean_text(f"Fecha Emision: {datetime.date.today()}"), ln=1, fill=True)
    pdf.ln(5)
    
    # Detalles Generales (Usamos clean_text para quitar emojis)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, txt=clean_text(f"Fecha Solicitada: {fecha}"), ln=1)
    # Quitamos el precio del nombre del camión para el PDF para que se vea limpio
    nombre_camion_limpio = camion.split("-")[0] 
    pdf.cell(0, 10, txt=clean_text(f"Vehiculo: {nombre_camion_limpio}"), ln=1)
    pdf.cell(0, 10, txt=clean_text(f"Accesos: {accesos_txt}"), ln=1)
    
    if len(inventario_txt) > 5:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 8, clean_text("Inventario Declarado:"), ln=1)
        pdf.set_font("Arial", size=9)
        pdf.multi_cell(0, 6, txt=clean_text(inventario_txt))
        pdf.ln(5)
        
    # Tabla de Valores
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(140, 10, clean_text("Descripcion"), 1)
    pdf.cell(50, 10, clean_text("Valor"), 1, 1, 'C')
    
    pdf.set_font("Arial", size=12)
    pdf.cell(140, 10, clean_text(f"Transporte Base ({nombre_camion_limpio})"), 1)
    pdf.cell(50, 10, f"${desglose['camion']:.2f}", 1, 1, 'R')
    
    pdf.cell(140, 10, clean_text(f"Personal ({personal} ayudantes)"), 1)
    pdf.cell(50, 10, f"${desglose['personal']:.2f}", 1, 1, 'R')
    
    pdf.cell(140, 10, clean_text("Recargo Pisos/Escaleras"), 1)
    pdf.cell(50, 10, f"${desglose['pisos']:.2f}", 1, 1, 'R')
    
    pdf.cell(140, 10, clean_text(f"Materiales ({materiales})"), 1)
    pdf.cell(50, 10, f"${desglose['materiales']:.2f}", 1, 1, 'R')
    
    pdf.cell(140, 10, clean_text("Tarifa Ciudad"), 1)
    pdf.cell(50, 10, "$0.00", 1, 1, 'R')
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(46, 0, 78)
    pdf.cell(140, 15, clean_text("TOTAL ESTIMADO"), 1)
    pdf.cell(50, 15, f"${total:.2f}", 1, 1, 'R')
    
    # Métodos de Pago en el PDF
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, clean_text("FORMAS DE PAGO ACEPTADAS:"), 0, 1, 'L')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 6, clean_text("- Efectivo"), 0, 1, 'L')
    pdf.cell(0, 6, clean_text("- Transferencia Bancaria (Pichincha / Guayaquil)"), 0, 1, 'L')
    pdf.cell(0, 6, clean_text("- Deuna!"), 0, 1, 'L')
    
    return pdf.output(dest='S').encode('latin-1', 'ignore') # 'ignore' evita que explote si queda algún caracter raro

# --- CSS BLINDADO ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    .stApp {{ background-color: {FONDO_APP}; font-family: 'Montserrat', sans-serif; }}
    h1, h2, h3, h4, h5, p, span, div, label, li {{ color: {COLOR_TEXTO} !important; }}
    
    /* SOLUCIÓN CAJAS NEGRAS */
    div[data-baseweb="input"], div[data-baseweb="base-input"], div[data-baseweb="select"] {{
        background-color: white !important;
        border: 1px solid #ccc !important;
        color: black !important;
    }}
    .stNumberInput input {{ background-color: white !important; color: black !important; }}
    input {{ color: black !important; caret-color: black !important; }}
    
    /* DROPDOWNS */
    ul[data-testid="stSelectboxVirtualDropdown"] {{ background-color: white !important; }}
    li[role="option"] {{ background-color: white !important; color: black !important; }}
    li[role="option"]:hover {{ background-color: {COLOR_AMARILLO} !important; color: black !important; }}
    
    /* ESTILO TIPs Y RESEÑAS */
    .tip-box {{ padding: 10px; border-bottom: 1px solid #eee; font-size: 14px; }}
    .review-card {{ background-color: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid {COLOR_AMARILLO}; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
    
    .control-panel {{ background-color: {COLOR_CARD_BG}; padding: 20px; border-radius: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px; }}
    .slogan-box {{ background-color: white; padding: 10px 20px; border-radius: 10px; border-left: 5px solid {COLOR_MORADO}; font-style: italic; color: #555 !important; margin-top: 5px; }}
    
    .hero-card {{ border-radius: 20px; padding: 25px; color: white; height: 160px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 10px 25px rgba(0,0,0,0.08); transition: transform 0.2s; }}
    .hero-card:hover {{ transform: translateY(-5px); }}
    .card-purple {{ background: linear-gradient(135deg, {COLOR_MORADO} 0%, #4a148c 100%); }}
    .card-purple div {{ color: white !important; }}
    .card-yellow {{ background: linear-gradient(135deg, {COLOR_AMARILLO} 0%, #ffca28 100%); }}
    .card-yellow div {{ color: {COLOR_MORADO} !important; }}
    .card-label {{ font-size: 12px; font-weight: 700; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; }}
    .card-amount {{ font-size: 32px; font-weight: 800; margin-top: 5px; }}

    .action-btn {{ background-color: {COLOR_CARD_BG}; border-radius: 16px; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.02); transition: all 0.2s; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; border: 1px solid rgba(0,0,0,0.05); text-decoration: none; }}
    .action-btn:hover {{ transform: scale(1.03); border-color: {COLOR_AMARILLO}; }}
    .icon-box {{ width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; margin-bottom: 10px; }}
    .bg-green {{ background-color: #E8F5E9; }}
    .bg-blue {{ background-color: #E3F2FD; }}
    .bg-yellow {{ background-color: #FFF8E1; }}
    .bg-purple {{ background-color: #F3E5F5; }}
    .action-text {{ font-size: 13px; font-weight: 700; color: #374151; }}
    
    .stDownloadButton > button {{ background-color: white !important; color: {COLOR_MORADO} !important; border: 1px solid {COLOR_MORADO} !important; border-radius: 8px !important; padding: 5px 15px !important; }}
    .stDownloadButton > button:hover {{ background-color: {COLOR_MORADO} !important; color: white !important; }}

    header {{ visibility: hidden; }} footer {{ visibility: hidden; }}
    </style>
""", unsafe_allow_html=True)

# --- CABECERA ---
col_logo, col_titulo = st.columns([1, 6])
with col_logo:
    try: st.image("logo.jpg", width=110)
    except: st.markdown("# 🚚")
with col_titulo:
    st.markdown(f"<h1 style='margin-bottom:0; color:{COLOR_MORADO} !important;'>MUDANZA PRIME</h1>", unsafe_allow_html=True)
    st.markdown(f"""<div class="slogan-box">"Movemos lo que más quieres."</div>""", unsafe_allow_html=True)

# --- PANEL DE CONFIGURACIÓN ---
st.markdown(f"<div class='control-panel'>", unsafe_allow_html=True)
st.markdown("### ⚙️ Configura tu Servicio")

c1, c2, c3, c4 = st.columns(4) 
with c1:
    st.markdown("**1. Fecha y Vehículo**")
    fecha_seleccionada = st.date_input("📅 Fecha", datetime.date.today())
    vehiculos = {
        "👉 Seleccione un Vehículo": {"precio": 0, "img": "❓"},
        "Furgoneta (Pequeña) - $30": {"precio": 30, "img": "🚐"},
        "Camión 2 Toneladas - $40": {"precio": 40, "img": "🚛"},
        "Camión 3.5 Toneladas - $50": {"precio": 50, "img": "🚚"},
        "Camión 6 Toneladas - $60": {"precio": 60, "img": "🚛🚛"}
    }
    seleccion = st.selectbox("🚛 Camión", list(vehiculos.keys()))
    dato_camion = vehiculos[seleccion]

with c2:
    st.markdown("**2. Personal**")
    personal = st.slider("👷 Ayudantes", 0, 10, 0)
    st.caption("Tarifa: $15 c/u")

with c3:
    st.markdown("**3. Pisos / Accesos**")
    st.caption("Escaleras: $10 extra cada 2 pisos")
    col_salida, col_llegada = st.columns(2)
    with col_salida:
        piso_salida = st.selectbox("Salida", ["PB", "1", "2", "3", "4", "5+"], key="piso_sal")
        asc_salida = st.checkbox("Ascensor S.")
    with col_llegada:
        piso_llegada = st.selectbox("Llegada", ["PB", "1", "2", "3", "4", "5+"], key="piso_lleg")
        asc_llegada = st.checkbox("Ascensor Ll.")

with c4:
    st.markdown("**4. Materiales**")
    cajas = st.number_input("📦 Cajas ($1.50 c/u)", 0, 100, 0) 
    rollos = st.number_input("🗞️ Rollos ($20.00 c/u)", 0, 20, 0) 

st.markdown("</div>", unsafe_allow_html=True)

# --- INVENTARIO ---
lista_objetos = []
with st.expander("📝 LISTA DE INVENTARIO (Clic para desplegar)", expanded=False):
    col_inv_1, col_inv_2, col_inv_3, col_inv_4 = st.columns(4)
    with col_inv_1:
        st.markdown("##### ❄️ Línea Blanca")
        tipo_refri = st.selectbox("Tipo de Refri", ["Ninguna", "Normal", "Side by Side (Grande)"])
        if tipo_refri != "Ninguna": lista_objetos.append(f"Refri {tipo_refri}")
        cocina = st.number_input("Cocina", 0, 5, 0, key="inv_cocina")
        lavadora = st.number_input("Lavadora", 0, 5, 0, key="inv_lavadora")
        secadora = st.number_input("Secadora", 0, 5, 0, key="inv_secadora")
        if cocina: lista_objetos.append(f"{cocina} Cocina")
        if lavadora: lista_objetos.append(f"{lavadora} Lavadora")
        if secadora: lista_objetos.append(f"{secadora} Secadora")
    with col_inv_2:
        st.markdown("##### 🛋️ Sala")
        mesa_centro = st.number_input("Mesa Centro", 0, 5, 0, key="inv_mesa_centro")
        muebles_sala = st.number_input("Juego Muebles", 0, 10, 0, key="inv_sofas")
        esquinero = st.number_input("Esquinero", 0, 5, 0, key="inv_esquinero")
        if mesa_centro: lista_objetos.append(f"{mesa_centro} Mesa Centro")
        if muebles_sala: lista_objetos.append(f"{muebles_sala} Juegos Sala")
        if esquinero: lista_objetos.append(f"{esquinero} Esquinero")
    with col_inv_3:
        st.markdown("##### 🍽️ Comedor")
        tiene_mesa = st.checkbox("¿Lleva Mesa?")
        if tiene_mesa:
            material_mesa = st.selectbox("Material", ["Madera", "Vidrio", "Mármol"])
            lista_objetos.append(f"Mesa Comedor ({material_mesa})")
        sillas = st.number_input("Sillas", 0, 12, 0, key="inv_sillas")
        bufetera = st.number_input("Bufetera", 0, 5, 0, key="inv_bufetera")
        if sillas: lista_objetos.append(f"{sillas} Sillas")
        if bufetera: lista_objetos.append(f"{bufetera} Bufetera")
    with col_inv_4:
        st.markdown("##### 🛏️ Dormitorios")
        camas = st.number_input("Camas", 0, 10, 0, key="inv_camas")
        veladores = st.number_input("Veladores", 0, 10, 0, key="inv_veladores")
        comodas = st.number_input("Cómodas", 0, 5, 0, key="inv_comodas")
        if camas: lista_objetos.append(f"{camas} Camas")
        if veladores: lista_objetos.append(f"{veladores} Veladores")
        if comodas: lista_objetos.append(f"{comodas} Cómodas")

inventario_final = ", ".join(lista_objetos) if lista_objetos else "No especificado"

# --- CÁLCULOS ---
def calcular_recargo_piso(piso, ascensor):
    if ascensor or piso in ["PB", "1"]: return 0
    if piso in ["2", "3"]: return 10
    if piso in ["4", "5+"]: return 20
    return 0

if dato_camion["precio"] == 0:
    precio_pisos = 0
else:
    recargo_salida = calcular_recargo_piso(piso_salida, asc_salida)
    recargo_llegada = calcular_recargo_piso(piso_llegada, asc_llegada)
    precio_pisos = recargo_salida + recargo_llegada

precio_camion = dato_camion["precio"]
precio_personal = personal * 15
precio_materiales = (cajas * 1.5) + (rollos * 20)
total = precio_camion + precio_personal + precio_materiales + precio_pisos

if total == 0:
    titulo_card = "EMPIEZA AQUÍ"
    icono_card = "👆"
    monto_mostrar = "$0.00"
    subtexto_card = "Selecciona un vehículo"
else:
    titulo_card = "VALOR A PAGAR"
    icono_card = "💰"
    monto_mostrar = f"${total:.2f}"
    subtexto_card = "Tarifa Final Ciudad"

txt_salida = f"{piso_salida} ({'Ascensor' if asc_salida else 'Escaleras'})"
txt_llegada = f"{piso_llegada} ({'Ascensor' if asc_llegada else 'Escaleras'})"
accesos_txt = f"De: {txt_salida} -> A: {txt_llegada}"

# --- DASHBOARD ---
st.markdown("### 📊 Tu Cotización")
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"""
    <div class="hero-card card-purple">
        <div><div class="card-label">{titulo_card}</div><div class="card-amount">{monto_mostrar}</div></div>
        <div style="display:flex; justify-content:space-between; align-items:end;"><div style="font-size:12px; opacity:0.8;">{subtexto_card}</div><div style="font-size:24px;">{icono_card}</div></div>
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
ac1, ac2 = st.columns(2)
msg = f"""Hola Mudanza Prime. Solicito Reserva:
🚚 Vehículo: {seleccion}
📅 Fecha: {fecha_str}
🏗️ Accesos: {accesos_txt}
👷 Personal: {personal} ayudantes
📦 Items: {inventario_final}
💰 Total Estimado: ${total:.2f}

Quedo a la espera de su confirmación."""
lnk = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
def btn(i, t, c, l="#"): return f"""<a href="{l}" target="_blank" style="text-decoration:none;"><div class="action-btn"><div class="icon-box {c}">{i}</div><div class="action-text">{t}</div></div></a>"""

with ac1: 
    st.markdown(btn("📲", "CONFIRMAR RESERVA (WhatsApp)", "bg-green", lnk), unsafe_allow_html=True)
    st.markdown("""<div class="success-box">✅ Envía los datos directamente a nuestro sistema.</div>""", unsafe_allow_html=True)
with ac2: 
    col_pdf1, col_pdf2 = st.columns([1, 4])
    with col_pdf1: st.markdown("""<div style="font-size:30px; text-align:center;">📄</div>""", unsafe_allow_html=True)
    with col_pdf2:
         pdf_bytes = generar_pdf(
            fecha=fecha_str,
            camion=seleccion,
            personal=personal,
            materiales=f"{cajas} cajas, {rollos} rollos",
            accesos_txt=accesos_txt,
            inventario_txt=inventario_final,
            total=total,
            desglose={'camion': precio_camion, 'personal': precio_personal, 'materiales': precio_materiales, 'pisos': precio_pisos}
        )
         st.download_button(
            label="Descargar Cotización (PDF)",
            data=pdf_bytes,
            file_name="Cotizacion_Mudanza.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.write("")

# --- DESGLOSE + TIPS + RESEÑAS ---
c_desglose, c_extra = st.columns([3, 2])

with c_desglose:
    # DESGLOSE HTML
    html_desglose = f"""
    <div style="background-color:{COLOR_CARD_BG}; padding:20px; border-radius:15px; box-shadow:0 4px 6px rgba(0,0,0,0.02); margin-bottom: 20px;">
        <h4 style="margin-bottom:20px; color:{COLOR_TEXTO};">🧾 Desglose de Servicios</h4>
        <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
            <span style="color:#666;">🚛 {seleccion}</span><span style="font-weight:bold; color:{COLOR_TEXTO};">${precio_camion:.2f}</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
            <span style="color:#666;">👷 {personal} Cargadores</span><span style="font-weight:bold; color:{COLOR_TEXTO};">${precio_personal:.2f}</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
            <span style="color:#666;">🏢 Accesos / Escaleras</span><span style="font-weight:bold; color:{COLOR_TEXTO};">${precio_pisos:.2f}</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
            <span style="color:#666;">📦 Materiales</span><span style="font-weight:bold; color:{COLOR_TEXTO};">${precio_materiales:.2f}</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
            <span style="color:#666;">📍 Cobertura Ciudad</span><span style="font-weight:bold; color:#2E7D32;">Incluida</span>
        </div>
        <div style="border-top: 1px solid #eee; margin-top:10px; padding-top:10px;">
            <span style="font-weight:bold; color:{COLOR_TEXTO};">💳 Métodos de Pago:</span><br>
            <span style="font-size:14px; color:#666;">💵 Efectivo | 🏦 Transferencia | 📱 Deuna!</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:15px 0; margin-top:10px;">
            <span style="font-weight:bold; font-size:18px; color:{COLOR_MORADO};">TOTAL FINAL</span>
            <span style="font-weight:bold; font-size:18px; color:{COLOR_MORADO};">${total:.2f}</span>
        </div>
    </div>
    """
    st.markdown(html_desglose, unsafe_allow_html=True)

with c_extra:
    # SECCIÓN TIPS
    with st.expander("💡 10 Tips de Mudanza", expanded=False):
        st.markdown("""
        <div class="tip-box">1. 📅 Reserva 3 días antes.</div>
        <div class="tip-box">2. 🧊 Descongela la refri 24h antes.</div>
        <div class="tip-box">3. 🏷️ Etiqueta las cajas por cuarto.</div>
        <div class="tip-box">4. 💼 Joyas y dinero llévalos tú.</div>
        <div class="tip-box">5. 📦 Libros en cajas pequeñas.</div>
        <div class="tip-box">6. 📺 Toma fotos a los cables de TV.</div>
        <div class="tip-box">7. 👗 Usa ropa para proteger vidrio.</div>
        <div class="tip-box">8. 🐕 Cuida a tus mascotas ese día.</div>
        <div class="tip-box">9. 📏 Mide puertas y pasillos.</div>
        <div class="tip-box">10. 🎒 Prepara maleta de primera noche.</div>
        """, unsafe_allow_html=True)

    # SECCIÓN RESEÑAS
    st.markdown("##### ⭐ Opiniones de Clientes")
    st.markdown("""
    <div class="review-card">
        <div style="color:#FFC107;">⭐⭐⭐⭐⭐</div>
        <div style="font-weight:bold; font-size:13px;">María P.</div>
        "Excelente servicio, puntuales y cuidadosos."
    </div>
    <div class="review-card">
        <div style="color:#FFC107;">⭐⭐⭐⭐⭐</div>
        <div style="font-weight:bold; font-size:13px;">Carlos A.</div>
        "Me ayudaron a armar todo super rápido."
    </div>
    """, unsafe_allow_html=True)
    
    # INPUT DE CALIFICACIÓN
    st.write("---")
    st.caption("Déjanos tu opinión:")
    calificacion = st.slider("Puntuación", 1, 5, 5)
    if st.button("Enviar Calificación"):
        st.toast("¡Gracias por tu opinión! ⭐")
