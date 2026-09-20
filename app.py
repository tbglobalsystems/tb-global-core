import streamlit as st
import pandas as pd
import numpy as np

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos Premium de la Interfaz
st.markdown("""
<style>
    .main { background-color: #030407; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    .logo-header {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        padding: 30px; border-radius: 8px; border: 1px solid #1e293b;
        border-bottom: 4px solid #0284c7; margin-bottom: 25px;
        text-align: center;
    }
    .logo-text { font-size: 42px; font-weight: 800; color: #ffffff; letter-spacing: 1px; margin: 0; }
    .logo-sub { font-size: 16px; color: #0284c7; font-weight: 600; letter-spacing: 4px; margin: 5px 0 0 0; }
</style>
""", unsafe_allow_html=True)

# Inicialización de estados del sistema corporativo
if "auth_rol" not in st.session_state: st.session_state["auth_rol"] = None
if "user_token" not in st.session_state: st.session_state["user_token"] = None
if "raw_pin" not in st.session_state: st.session_state["raw_pin"] = None
if "abrir_chat_soporte" not in st.session_state: st.session_state["abrir_chat_soporte"] = False

# Encabezado Comercial
st.markdown("""
<div class='logo-header'>
    <h1 class='logo-text'>⚡ T&B Global</h1>
    <p class='logo-sub'>QUANTUM ENTERPRISE OPERATING SYSTEM</p>
</div>
""", unsafe_allow_html=True)

st.subheader("🌐 Red de Telecomunicaciones y Enlaces Globales Cuánticos")

# Generación matemática de coordenadas mundiales (Antenas y Satélites fijos)
# Puntos simulados alrededor del mundo
coordenadas_datos = {
    'lat': [40.7128, 34.0522, 51.5074, 35.6762, -22.9068, -33.8688, 19.4326, 48.8566],
    'lon': [-74.0060, -118.2437, -0.1278, 139.6503, -43.1729, 151.2093, -99.1332, 2.3522],
    'Tipo': ['Antena Alfa', 'Satélite Enlace', 'Base Cuántica', 'Estación Delta', 'Antena Omega', 'Satélite Beta', 'Estación Central', 'Enlace Central']
}

df_mapa = pd.DataFrame(coordenadas_datos)

# Renderizado del mapa interactivo global nativo de Streamlit
# Este mapa viene integrado de fábrica y no puede fallar por falta de librerías ni bloquearse en el iPad
st.map(df_mapa, zoom=1, use_container_width=True)

st.dataframe(df_mapa, use_container_width=True)
