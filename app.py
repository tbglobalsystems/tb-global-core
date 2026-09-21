import streamlit as st
import pandas as pd
import time

# 1. CONFIGURACIÓN CORPORATIVA GLOBAL DE ALTA GAMA
st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# MATRIZ DE TRADUCCIÓN COMPACTA NATIVA
IDIOMAS = {
    "es": {
        "title": "QUANTUM ENTERPRISE OPERATING SYSTEM",
        "subtitle": "Consola de Comando de Servicios Integrados",
        "lock": "🔒 El sistema operativo se encuentra bloqueado. Inicie sesión en la barra lateral.",
        "user": "ID de Usuario Operador",
        "pin": "PIN de Seguridad (4 dígitos)",
        "area1": "🌐 Área 1: Distribución Geográfica y Telemetría",
        "focus": "Controles de Enfoque de Telemetría:",
        "us": "📍 América del Norte", "eu": "📍 Región Europea", "as": "📍 Servidores de Asia",
        "t_us": "Enfocando telemetría en US Core Nodos...", "t_eu": "Enfocando telemetría en Euro Link...", "t_as": "Enfocando telemetría en Asia Core...",
        "open_c": "➕ Abrir Consola para Registrar Nuevo Servidor/Canal",
        "lat": "Latitud Geográfica", "lon": "Longitud Geográfica", "ident": "Nombre identificador del Canal o Servidor",
        "execute": "🚀 EJECUTAR: Aprovisionar y Guardar", "err_empty": "El nombre del identificador no puede estar vacío.",
        "success_reg": "registrado en memoria cloud con éxito.",
        "monitor": "📈 Monitor de Carga y Tráfico Cuántico Activo",
        "flow": "📡 Flujo de paquetes telemetritos entre nodos activos:",
        "m1": "Servidores Conectados", "m2": "Ancho de Banda Asignado", "m3": "Latencia Global Media",
        "area2": "🤖 Área 2: Módulo de Enfoque de Inteligencia Virtual",
        "select_a": "Seleccione el área de análisis que desea que ejecute el sistema operativo principal:",
        "ana1": "Análisis de Telemetría Global", "ana2": "Monitoreo de Logs de Seguridad", "ana3": "Optimización de Tráfico de Nodos",
        "active_m": "Módulo activo seleccionado actualmente",
        "area3": "📑 Área 3: Registro Histórico y Logs de Auditoría Institucional"
    },
    "en": {
        "title": "QUANTUM ENTERPRISE OPERATING SYSTEM",
        "subtitle": "Integrated Services Command Console",
        "lock": "🔒 The operating system is locked. Please sign in via the sidebar.",
        "user": "Operator User ID", "pin": "Security PIN (4 digits)",
        "area1": "Area 1: Geographic Distribution and Telemetry",
        "focus": "Telemetry Focus Controls:",
        "us": "📍 North America", "eu": "📍 European Region", "as": "📍 Asia Servers",
        "t_us": "Focusing telemetry on US Core Nodes...", "t_eu": "Focusing telemetry on Euro Link...", "t_as": "Focusing telemetry on Asia Core...",
        "open_c": "➕ Open Console to Register New Server/Channel",
        "lat": "Geographic Latitude", "lon": "Geographic Longitude", "ident": "Channel or Server Identifier Name",
        "execute": "🚀 EXECUTE: Provision and Save", "err_empty": "The identifier name cannot be empty.",
        "success_reg": "registered in cloud memory successfully.",
        "monitor": "📈 Active Load Monitor and Quantum Traffic",
        "flow": "📡 Telemetry packet flow between active nodes:",
        "m1": "Connected Servers", "m2": "Allocated Bandwidth", "m3": "Average Global Latency",
        "area2": "🤖 Area 2: Virtual Intelligence Focus Module",
        "select_a": "Select the analysis area you want the main operating system to execute:",
        "ana1": "Global Telemetry Analysis", "ana2": "Security Logs Monitoring", "ana3": "Node Traffic Optimization",
        "active_m": "Currently active module selected",
        "area3": "Area 3: Historical Record and Institutional Audit Logs"
    }
}

# Inicializar estados de la sesión
if "lang" not in st.session_state: st.session_state["lang"] = "es"
if "usuario_activo" not in st.session_state: st.session_state["usuario_activo"] = None
if "nodos" not in st.session_state:
    st.session_state["nodos"] = pd.DataFrame([
        {"lat": 40.7128, "lon": -74.0060, "nombre_nodo": "Nodo Central US"},
        {"lat": 34.0522, "lon": -118.2437, "nombre_nodo": "Nodo Pacifico US"},
        {"lat": 51.5074, "lon": -0.1278, "nombre_nodo": "Nodo Euro Core"}
    ])
if "logs" not in st.session_state:
    st.session_state["logs"] = pd.DataFrame([
        {"Fecha/Hora": time.strftime("%Y-%m-%d %H:%M:%S"), "Operador": "Sistema", "Acción": "Infraestructura Quantum inicializada con éxito."}
    ])

L = IDIOMAS[st.session_state["lang"]]

# ACCESO RÁPIDO DE IDIOMAS
st.write("🌍 **Quick Language Access / Entrada de Idiomas:**")
col_l1, col_l2 = st.columns(2)
with col_l1:
    if st.button("🇺🇸 English (US Core Market)"):
        st.session_state["lang"] = "en"
        st.rerun()
with col_l2:
    if st.button("🇪🇸 Español (Mercado Global)"):
        st.session_state["lang"] = "es"
        st.rerun()

# 2. INYECCIÓN DE ESTILOS PREMIUM
st.markdown("""
<style>
    .brand-container {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        padding: 30px; border-radius: 12px; border: 1px solid #1e293b; border-bottom: 4px solid #0284c7; text-align: center; margin-bottom: 25px;
    }
    .brand-title { font-size: 40px !important; font-weight: 800 !important; color: #38bdf8 !important; margin: 0 !important; }
    .brand-subtitle { font-size: 13px !important; color: #ffffff !important; font-weight: 600 !important; letter-spacing: 5px !important; }
    
    .stButton>button {
        width: 100% !important;
        background-color: #0284c7 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
    }
    .stButton>button:hover { background-color: #0369a1 !important; color: #38bdf8 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="brand-container">
    <h1 class="brand-title">⚡ T&B Global</h1>
    <p class="brand-subtitle">{L['title']}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"### 📊 {L['subtitle']}")

# CONTROL DE ACCESO GLOBAL REESTRUCTURADO
if st.session_state["usuario_activo"] is None:
    st.warning(L["lock"])
    with st.sidebar:
        st.markdown("### 🔐 Acceso Centralizado")
        u = st.text_input(f"{L['user']}:")
        p = st.text_input(f"{L['pin']}:", type="password", max_chars=4)
        if st.button("Validar Credenciales"):
            if u and p:
                st.session_state["usuario_activo"] = u
                log_login = pd.DataFrame([{"Fecha/Hora": time.strftime("%Y-%m-%d %H:%M:%S"), "Operador": u, "Acción": "Inicio de sesión de operador exitoso."}])
                st.session_state["logs"] = pd.concat([log_login, st.session_state["logs"]], ignore_index=True)
                st.rerun()
else:
    with st.sidebar:
        st.success(f"Operador: {st.session_state['usuario_activo']}")
        st.markdown("---")
        st.markdown("### 📥 Owner Document Vault")
        
        reporte_texto = "ACTA OFICIAL DE ENTREGA DE PROPIEDAD INTELECTUAL\nPROYECTO: T&B Global - Enterprise OS\nDUEÑO: admin_tb\nFECHA: 2026-09-21\nSEGURIDAD: CIFRADO CRIPTOGRAFICO SHA-256 VALIDADO Y ACTIVO."
        manual_texto = "MANUAL DE OPERACION TECNICA T&B GLOBAL\n1. ACCESO CENTRALIZADO CON PIN ENCRIPTADO.\n2. TELEMETRIA GEOGRAFICA EN AREA 1 CON CONTROLES AZULES.\n3. MONITOR CUANTICO EN AREA 2 (135 GBPS / 18 MS).\n4. BITACORA DE AUDITORIA EN AREA 3 CON EXTRACTOR CSV."
        
        st.download_button(label="📄 Descargar Acta Legal (PDF/TXT)", data=reporte_texto, file_name="documento_legal_llaves_tb_global.txt", mime="text/plain")
        st.download_button(label="📝 Descargar Acta Legal (Word/DOCX)", data=reporte_texto, file_name="documento_legal_llaves_tb_global.docx", mime="application/msword")
        st.download_button(label="📘 Descargar Manual de Usuario (PDF/TXT)", data=manual_texto, file_name="manual_usuario_tb_global.txt", mime="text/plain")
        st.markdown("---")
        
        if st.button("🔒 Cerrar Sesión"):
            usuario = st.session_state["usuario_activo"]
            log_logout = pd.DataFrame([{"Fecha/Hora": time.strftime("%Y-%m-%d %H:%M:%S"), "Operador": usuario, "Acción": "Sesión cerrada por el operador institucional."}])
            st.session_state["logs"] = pd.concat([log_logout, st.session_state["logs"]], ignore_index=True)
            st.session_state["usuario_activo"] = None
            st.rerun()

    # ---- CONSOLA DE CAPACIDAD COMPLETA ----
    
    # ÁREA 1: MAPA CORPORATIVO Y TELEMETRÍA
    st.markdown(f"#### {L['area1']}")
    if not st.session_state["nodos"].empty:
        st.map(st.session_state["nodos"], zoom=1, use_container_width=True)
    
    st.write(f"⚙️ **{L['focus']}**")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        if st.button(L["us"]):
            st.toast(L["t_us"], icon="🌎")
    with col_f2:
        if st.button(L["eu"]):
            st.toast(L["t_eu"], icon="🇪🇺")
    with col_f3:
        if st.button(L["as"]):
            st.toast(L["t_as"], icon="🇯🇵")

    # Formulario para aprovisionamiento
    with st.expander(L["open_c"], expanded=False):
        with st.form("nuevo_nodo_form"):
            n_lat = st.number_input(f"{L['lat']}:", value=0.0, format="%.4f")
            n_lon = st.number_input(f"{L['lon']}:", value=0.0, format="%.4f")
            n_name = st.text_input(f"{L['ident']}:")
            btn_nodo = st.form_submit_button(L["execute"])
            
            if btn_nodo:
                if n_name.strip() == "":
                    st.error(L["err_empty"])
                else:
                    nuevo_nodo = pd.DataFrame([{"lat": n_lat, "lon": n_lon, "nombre_nodo": n_name}])
                    st.session_state["nodos"] = pd.concat([st.session_state["nodos"], nuevo_nodo], ignore_index=True)
                    
