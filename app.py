import streamlit as st
import os
import psycopg2
import hashlib
import pandas as pd
import time

st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .brand-title {
        font-size: 40px !important;
        font-weight: 800 !important;
        color: #38bdf8 !important;
        letter-spacing: 2px !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    .brand-subtitle {
        font-size: 13px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        letter-spacing: 5px !important;
        margin-top: 8px !important;
        margin-bottom: 0 !important;
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

    st.markdown("#### 🌐 Área 1: Distribución Geográfica y Telemetría")
    df_nodos = pd.DataFrame([
        {"lat": 40.7128, "lon": -74.0060, "nombre_nodo": "Nodo Central US"},
        {"lat": 34.0522, "lon": -118.2437, "nombre_nodo": "Nodo Pacifico US"},
        {"lat": 51.5074, "lon": -0.1278, "nombre_nodo": "Nodo Euro Core"}
    ])
    st.map(df_nodos, zoom=1, use_container_width=True)
    st.info("Módulo de infraestructura en línea ejecutándose de forma correcta.")
