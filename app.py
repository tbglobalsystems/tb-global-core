import streamlit as st
import pandas as pd
import time

# 1. CONFIGURACIÓN CORPORATIVA GLOBAL
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
        "lock": "🔒 El sistema operativo se encuentra bloqueado. Inicie sesión en la barra lateral.",
        "user": "ID de Usuario Operador",
        "pin": "PIN de Seguridad (4 dígitos)",
        "area1": "🌐 Área 1: Distribución Geográfica y Telemetría",
        "focus": "Controles de Enfoque de Telemetría:",
        "us": "📍 América del Norte",
        "eu": "📍 Región Europea",
        "as": "📍 Servidores de Asia",
        "t_us": "Enfocando telemetría en US Core Nodos...",
        "t_eu": "Enfocando telemetría en Euro Link...",
        "t_as": "Enfocando telemetría en Asia Core...",
        "monitor": "📈 Visualizar Monitor de Carga y Tráfico Cuántico",
        "flow": "📡 Flujo de paquetes telemetritos entre nodos activos:",
        "m1": "Servidores Conectados",
        "m2": "Ancho de Banda Asignado",
        "m3": "Latencia Global Media",
        "area3": "📑 Área 3: Registro Histórico y Logs de Auditoría Institucional"
    },
    "en": {
        "title": "QUANTUM ENTERPRISE OPERATING SYSTEM",
        "lock": "🔒 The operating system is locked. Please sign in via the sidebar.",
        "user": "Operator User ID",
        "pin": "Security PIN (4 digits)",
        "area1": "🌐 Area 1: Geographic Distribution and Telemetry",
        "focus": "Telemetry Focus Controls:",
        "us": "📍 North America",
        "eu": "📍 European Region",
        "as": "📍 Asia Servers",
        "t_us": "Focusing telemetry on US Core Nodes...",
        "t_eu": "Focusing telemetry on Euro Link...",
        "t_as": "Focusing telemetry on Asia Core...",
        "monitor": "📈 View Load Monitor and Quantum Traffic",
        "flow": "📡 Telemetry packet flow between active nodes:",
        "m1": "Connected Servers",
        "m2": "Allocated Bandwidth",
        "m3": "Average Global Latency",
        "area3": "📑 Area 3: Historical Record and Institutional Audit Logs"
    }
}

if "lang" not in st.session_state:
    st.session_state["lang"] = "es"
if "usuario_activo" not in st.session_state:
    st.session_state["usuario_activo"] = None

L = IDIOMAS[st.session_state["lang"]]

# BOTONES DE ACCESO RÁPIDO DE IDIOMAS
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

# ENCABEZADO CORPORATIVO
st.markdown(f"""
<div style="background: linear-gradient(135deg, #0f172a 0%, #020617 100%); padding: 30px; border-radius: 12px; border: 1px solid #1e293b; border-bottom: 4px solid #0284c7; text-align: center; margin-bottom: 25px;">
    <h1 style="font-size: 40px; font-weight: 800; color: #38bdf8; margin: 0;">⚡ T&B Global</h1>
    <p style="font-size: 13px; color: #ffffff; font-weight: 600; letter-spacing: 5px; margin-top: 8px;">{L['title']}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Consola de Comando de Servicios Integrados")

# CONTROL DE ACCESO
if st.session_state["usuario_activo"] is None:
    st.warning(L["lock"])
    with st.sidebar:
        st.markdown("### 🔐 Acceso Centralizado")
        u = st.text_input(f"{L['user']}:")
        p = st.text_input(f"{L['pin']}:", type="password", max_chars=4)
        if st.button("Validar Credenciales"):
            if u and p:
                st.session_state["usuario_activo"] = u
                st.rerun()
else:
    with st.sidebar:
        st.success(f"Operador: {st.session_state['usuario_activo']}")
        if st.button("🔒 Cerrar Sesión"):
            st.session_state["usuario_activo"] = None
            st.rerun()

    # ÁREA 1: TELEMETRÍA Y MAPA
    st.markdown(f"#### {L['area1']}")
    df_nodos = pd.DataFrame([
        {"lat": 40.7128, "lon": -74.0060, "nombre_nodo": "Nodo Central US"},
        {"lat": 34.0522, "lon": -118.2437, "nombre_nodo": "Nodo Pacifico US"},
        {"lat": 51.5074, "lon": -0.1278, "nombre_nodo": "Nodo Euro Core"}
    ])
    st.map(df_nodos, zoom=1, use_container_width=True)
    
    # CONTROLES DE ENFOQUE DEL MAPA
    st.write(f"⚙️ **{L['focus']}**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(L["us"]):
            st.toast(L["t_us"], icon="🌎")
    with col2:
        if st.button(L["eu"]):
            st.toast(L["t_eu"], icon="🇪🇺")
    with col3:
        if st.button(L["as"]):
            st.toast(L["t_as"], icon="🇯🇵")

    # MONITOR DE TRÁFICO CUÁNTICO
    st.markdown("---")
    with st.expander(L["monitor"], expanded=True):
        st.write(L["flow"])
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            st.metric(label=L["m1"], value="3 / 12")
        with col_t2:
            st.metric(label=L["m2"], value="135 Gbps", delta="+15%")
        with col_t3:
            st.metric(label=T("m3") if "T" in globals() else "Latencia", value="18 ms", delta="-4 ms")

    # ÁREA 3: AUDITORÍA
    st.markdown("---")
    st.markdown(f"#### {L['area3']}")
    df_logs = pd.DataFrame([
        {"Fecha/Hora": time.strftime("%Y-%m-%d %H:%M:%S"), "Operador": st.session_state["usuario_activo"], "Acción": "Acceso e infraestructura validados con éxito."}
    ])
    st.dataframe(df_logs, use_container_width=True)
