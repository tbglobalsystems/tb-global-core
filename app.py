import streamlit as st
import os
import psycopg2
import pandas as pd

# 1. CONFIGURACIÓN CORPORATIVA
st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. DISEÑO PREMIUM
st.markdown("""
<style>
    .brand-container {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #1e293b;
        border-bottom: 4px solid #0284c7;
        margin-bottom: 25px;
        text-align: center;
    }
    .brand-title {
        font-size: 40px !important;
        font-weight: 800 !important;
        color: #38bdf8 !important;
        margin: 0 !important;
    }
    .brand-subtitle {
        font-size: 13px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        letter-spacing: 5px !important;
    }
</style>
""", unsafe_allow_html=True)

if "usuario_activo" not in st.session_state:
    st.session_state["usuario_activo"] = None

st.markdown("""
<div class="brand-container">
    <h1 class="brand-title">⚡ T&B Global</h1>
    <p class="brand-subtitle">QUANTUM ENTERPRISE OPERATING SYSTEM</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Consola de Comando de Servicios Integrados")

# 3. ACCESO CENTRALIZADO
if st.session_state["usuario_activo"] is None:
    st.warning("🔒 El sistema operativo se encuentra bloqueado. Inicie sesión en la barra lateral.")
    with st.sidebar:
        st.markdown("### 🔐 Acceso Centralizado")
        u = st.text_input("ID de Usuario Operador:")
        p = st.text_input("PIN de Seguridad (4 dígitos):", type="password", max_chars=4)
        if st.button("Validar Credenciales"):
            if u and p:
                st.session_state["usuario_activo"] = u
                st.rerun()
else:
    with st.sidebar:
        st.success(f"Operador en Línea: {st.session_state['usuario_activo']}")
        if st.button("🔒 Cerrar Sesión"):
            st.session_state["usuario_activo"] = None
            st.rerun()

    # 4. TELEMETRÍA Y MAPA Y BOTONES
    st.markdown("#### 🌐 Área 1: Distribución Geográfica y Telemetría")
    
    df_nodos = pd.DataFrame([
        {"lat": 40.7128, "lon": -74.0060, "nombre_nodo": "Nodo Central US"},
        {"lat": 34.0522, "lon": -118.2437, "nombre_nodo": "Nodo Pacifico US"},
        {"lat": 51.5074, "lon": -0.1278, "nombre_nodo": "Nodo Euro Core"}
    ])
    st.map(df_nodos, zoom=1, use_container_width=True)
    
    st.write("⚙️ **Controles de Enfoque:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📍 América del Norte"):
            st.toast("Enfocando US Core...", icon="🌎")
    with col2:
        if st.button("📍 Región Europea"):
            st.toast("Enfocando Euro Link...", icon="🇪🇺")
    with col3:
        if st.button("📍 Servidores de Asia"):
            st.toast("Enfocando Asia Core...", icon="🇯🇵")

    # 5. ENFOQUE DE INTELIGENCIA VIRTUAL
    st.markdown("---")
    st.markdown("#### 🤖 Área 2: Módulo de Enfoque de Inteligencia Virtual")
    enfoque_ia = st.radio(
        "Seleccione el área de análisis:",
        ["Análisis de Telemetría Global", "Monitoreo de Logs de Seguridad", "Optimización de Tráfico de Nodos"]
    )
    st.info(f"Módulo activo: **{enfoque_ia}**")
