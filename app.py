import streamlit as st
import plotly.graph_objects as go
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

# =======================================================================
# MODELADO DEL MUNDO TERRÁQUEO Y RED DE SATÉLITES (NATIVO EN PYTHON)
# =======================================================================

# Creación geométrica de la esfera terrestre (Red de malla matemática cuántica)
phi = np.linspace(0, 2 * np.pi, 40)
theta = np.linspace(0, np.pi, 40)
phi, theta = np.meshgrid(phi, theta)

x = 100 * np.sin(theta) * np.cos(phi)
y = 100 * np.sin(theta) * np.sin(phi)
z = 100 * np.cos(theta)

fig = go.Figure()

# Dibujar la superficie del planeta con estética de red digital de telecomunicaciones
fig.add_trace(go.Surface(
    x=x, y=y, z=z,
    colorscale=[[0, '#0f172a'], [0.5, '#1d4ed8'], [1, '#10b981']],
    showscale=False,
    opacity=0.85,
    hoverinfo='none'
))

# Coordenadas tridimensionales de las Órbitas de los Satélites
t = np.linspace(0, 2 * np.pi, 100)
# Satélite Alfa
sat_a_x = 140 * np.cos(t)
sat_a_y = 140 * np.sin(t)
sat_a_z = np.zeros_like(t)

# Satélite Beta (Órbita Inclinada)
sat_b_x = 150 * np.cos(t)
sat_b_y = 150 * np.sin(t) * Math.cos(np.pi/4) if 'Math' not in locals() else 150 * np.sin(t) * np.cos(np.pi/4)
sat_b_z = 150 * np.sin(t) * np.sin(np.pi/4)

# Dibujar líneas de órbita en el espacio tridimensional
fig.add_trace(go.Scatter3d(x=sat_a_x, y=sat_a_y, z=sat_a_z, mode='lines', line=dict(color='#00ffcc', width=2), name='Órbita Alfa'))
fig.add_trace(go.Scatter3d(x=sat_b_x, y=sat_b_y, z=sat_b_z, mode='lines', line=dict(color='#10b981', width=2), name='Órbita Beta'))

# Ubicación actual de los satélites (Puntos brillantes emisores)
fig.add_trace(go.Scatter3d(x=[sat_a_x[30]], y=[sat_a_y[30]], z=[sat_a_z[30]], mode='markers', marker=dict(size=8, color='#ffffff', symbol='diamond'), name='Satélite Alfa'))
fig.add_trace(go.Scatter3d(x=[sat_b_x[60]], y=[sat_b_y[60]], z=[sat_b_z[60]], mode='markers', marker=dict(size=8, color='#ffffff', symbol='diamond'), name='Satélite Beta'))

# Simulación de ráfagas de señales cuánticas directas hacia el planeta (Líneas de transmisión)
fig.add_trace(go.Scatter3d(x=[sat_a_x[30], 0], y=[sat_a_y[30], 0], z=[sat_a_z[30], 0], mode='lines', line=dict(color='#00ffcc', width=3, dash='dash'), name='Señal Cuántica'))
fig.add_trace(go.Scatter3d(x=[sat_b_x[60], 10], y=[sat_b_y[60], -20], z=[sat_b_z[60], 40], mode='lines', line=dict(color='#10b981', width=3, dash='dash'), name='Enlace Global'))

# Configuración del escenario espacial (Fondo oscuro, sin ejes molestos)
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        backgroundcolor='#030407'
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor='#030407',
    showlegend=False,
    height=450
)

# Renderizado directo en Streamlit certificado para funcionar en tablets
st.plotly_chart(fig, use_container_width=True)
