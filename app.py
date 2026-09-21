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
    .stButton>button {
        width: 100% !important;
        background-color: #0284c7 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

if "usuario_activo" not in st.session_state:
    st.session_state["usuario_activo"] = None

if "nodos_locales" not in st.session_state:
    st.session_state["nodos_locales"] = pd.DataFrame([
        {"lat": 40.7128, "lon": -74.0060, "nombre_nodo": "Nodo Central US"},
        {"lat": 34.0522, "lon": -118.2437, "nombre_nodo": "Nodo Pacifico US"},
        {"lat": 51.5074, "lon": -0.1278, "nombre_nodo": "Nodo Euro Core"}
    ])

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
    
    # Desplegar mapa con los nodos activos
    st.map(st.session_state["nodos_locales"], zoom=1, use_container_width=True)
    
    # CONTROLES DEL MAPA RECUPERADOS
    st.write("⚙️ **Controles de Enfoque de Telemetría:**")
    col_m1, col_st2, col_m3 = st.columns(3)
    with col_m1:
        if st.button("📍 Centrar en América del Norte"):
            st.toast("Enfocando telemetría en US Core Nodos...", icon="🌎")
    with col_st2:
        if st.button("📍 Centrar en Región Europea"):
            st.toast("Enfocando telemetría en Euro Link...", icon="🇪🇺")
    with col_m3:
        if st.button("📍 Centrar en Servidores de Asia"):
            st.toast("Enfocando telemetría en Asia Core...", icon="🇯🇵")

    # CONSOLA PARA REGISTRAR NUEVOS NODOS RECUPERADA y MODULADA
    st.markdown("---")
    with st.expander("➕ Abrir Consola para Registrar Nuevo Servidor/Canal", expanded=False):
        with st.form("nuevo_nodo_form"):
            n_lat = st.number_input("Latitud Geográfica:", value=0.0, format="%.4f")
            n_lon = st.number_input("Longitud Geográfica:", value=0.0, format="%.4f")
            n_name = st.text_input("Nombre identificador del Canal o Servidor:")
            btn_nodo = st.form_submit_button("🚀 EJECUTAR: Aprovisionar y Guardar")
            
            if btn_nodo:
                if n_name.strip() != "":
                    nuevo_registro = pd.DataFrame([{"lat": n_lat, "lon": n_lon, "nombre_nodo": n_name}])
                    st.session_state["nodos_locales"] = pd.concat([st.session_state["nodos_locales"], nuevo_registro], ignore_index=True)
                    st.success(f"Servidor '{n_name}' registrado en memoria cloud exitosamente.")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("El nombre del identificador no puede estar vacío.")

    # ÁREA DE SELECCIÓN DE ANÁLISIS DE INTELIGENCIA VIRTUAL RECUPERADA
    st.markdown("---")
    st.markdown("#### 🤖 Área 2: Módulo de Enfoque de Inteligencia Virtual")
    enfoque_ia = st.radio(
        "Seleccione el área de análisis que desea que ejecute el sistema operativo principal:",
        ["Análisis de Telemetría Global", "Monitoreo de Logs de Seguridad", "Optimización de Tráfico de Nodos"],
        index=0
    )
    st.info(f"Módulo activo seleccionado actualmente: **{enfoque_ia}**")
