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
        "pin": "PIN de Seguridad (4 dígitos)"
    },
    "en": {
        "title": "QUANTUM ENTERPRISE OPERATING SYSTEM",
        "lock": "🔒 The operating system is locked. Please sign in via the sidebar.",
        "user": "Operator User ID",
        "pin": "Security PIN (4 digits)"
    }
}

if "lang" not in st.session_state:
    st.session_state["lang"] = "es"
if "usuario_activo" not in st.session_state:
    st.session_state["usuario_activo"] = None

# BOTONES DE ACCESO RÁPIDO DE IDIOMAS (SIEMPRE VISIBLES)
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
    <p style="font-size: 13px; color: #ffffff; font-weight: 600; letter-spacing: 5px; margin-top: 8px;">{IDIOMAS[st.session_state['lang']]['title']}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Consola de Comando de Servicios Integrados")

# CONTROL DE ACCESO
if st.session_state["usuario_activo"] is None:
    st.warning(IDIOMAS[st.session_state["lang"]]["lock"])
    with st.sidebar:
        st.markdown("### 🔐 Acceso Centralizado")
        u = st.text_input(f"{IDIOMAS[st.session_state['lang']]['user']}:")
        p = st.text_input(f"{IDIOMAS[st.session_state['lang']]['pin']}:", type="password", max_chars=4)
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

    # ÁREA 1: TELEMETRÍA ESTABLE
    st.markdown("#### 🌐 Área 1: Distribución Geográfica y Telemetría")
    df_nodos = pd.DataFrame([
        {"lat": 40.7128, "lon": -74.0060, "nombre_nodo": "Nodo Central US"},
        {"lat": 34.0522, "lon": -118.2437, "nombre_nodo": "Nodo Pacifico US"},
        {"lat": 51.5074, "lon": -0.1278, "nombre_nodo": "Nodo Euro Core"}
    ])
    st.map(df_nodos, zoom=1, use_container_width=True)
