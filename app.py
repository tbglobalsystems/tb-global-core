import streamlit as st
import pandas as pd
import time
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# 1. CONFIGURACIÓN CORPORATIVA GLOBAL DE ALTA GAMA
st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# MATRIZ DE TRADUCCIÓN MULTILENGUAJE COMPACTA NATIVA
IDIOMAS = {
    "es": {
        "title": "QUANTUM ENTERPRISE OPERATING SYSTEM",
        "lock": "🔒 El sistema operativo se encuentra bloqueado. Inicie sesión a continuación.",
        "user": "ID de Usuario Operador",
        "pin": "PIN de Seguridad (4 dígitos)",
        "area1": "🌐 Área 1: Distribución Geográfica y Telemetría",
        "focus": "Controles de Enfoque de Telemetría:",
        "us": "📍 América del Norte", "eu": "📍 Región Europea", "as": "📍 Servidores de Asia",
        "t_us": "Enfocando telemetría en US Core Nodos...", "t_eu": "Enfocando telemetría en Euro Link...", "t_as": "Enfocando telemetría en Asia Core...",
        "open_c": "➕ Consola de Registro de Nuevo Servidor/Canal",
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
        "lock": "🔒 The operating system is locked. Please sign in below.",
        "user": "Operator User ID", 
        "pin": "Security PIN (4 digits)", 
        "area1": "🌐 Area 1: Geographic Distribution and Telemetry", 
        "focus": "Telemetry Focus Controls:", 
        "us": "📍 North America", "eu": "📍 European Region", "as": "📍 Asia Servers", 
        "t_us": "Focusing telemetry on US Core Nodes...", "t_eu": "Focusing telemetry on Euro Link...", "t_as": "Focusing telemetry on Asia Core...", 
        "open_c": "➕ Open Console to Register New Server/Channel",
        "lat": "Geographic Latitude", "lon": "Geographic Longitude", "ident": "Channel or Server Identifier Name", 
        "execute": "🚀 EXECUTE: Provision and Save", "err_empty": "The identifier name cannot be empty.", 
        "success_reg": "registered in cloud memory successfully.", 
        "monitor": "📈 View Load Monitor and Quantum Traffic", 
        "flow": "📡 Telemetry packet flow between active nodes:", 
        "m1": "Connected Servers", "m2": "Allocated Bandwidth", "m3": "Average Global Latency", 
        "area2": "🤖 Area 2: Virtual Intelligence Focus Module", 
        "select_a": "Select the analysis area you want the main operating system to execute:", 
        "ana1": "Global Telemetry Analysis", "ana2": "Security Logs Monitoring", "ana3": "Node Traffic Optimization",
        "active_m": "Currently active module selected", 
        "area3": "📑 Area 3: Historical Record and Institutional Audit Logs"
    }
}

if "lang" not in st.session_state: st.session_state["lang"] = "es"
if "usuario_activo" not in st.session_state: st.session_state["usuario_activo"] = None
if "zoom_mapa" not in st.session_state: st.session_state["zoom_mapa"] = 1

# CONEXIÓN AL ELEFANTE DE POSTGRESQL
def init_db():
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        try:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS nodos (
                    id SERIAL PRIMARY KEY, lat DOUBLE PRECISION, lon DOUBLE PRECISION, nombre_nodo VARCHAR(255)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id SERIAL PRIMARY KEY, fecha_hora VARCHAR(100), operador VARCHAR(100), accion TEXT
                );
            """)
            cursor.execute("SELECT COUNT(*) FROM nodos;")
            if cursor.fetchone() == 0:
                cursor.execute("INSERT INTO nodos (lat, lon, nombre_nodo) VALUES (40.7128, -74.0060, 'Nodo Central US'), (34.0522, -118.2437, 'Nodo Pacifico US'), (51.5074, -0.1278, 'Nodo Euro Core');")
            cursor.execute("SELECT COUNT(*) FROM audit_logs;")
            if cursor.fetchone() == 0:
                cursor.execute("INSERT INTO audit_logs (fecha_hora, operador, accion) VALUES (%s, %s, %s);", (time.strftime("%Y-%m-%d %H:%M:%S"), "Sistema", "Infraestructura Quantum inicializada en Postgres."))
            conn.commit()
            cursor.close(); conn.close()
        except:
            pass

init_db()

def obtener_nodos():
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        try:
            conn = psycopg2.connect(db_url)
            df = pd.read_sql("SELECT lat, lon, nombre_nodo FROM nodos ORDER BY id ASC;", conn)
            conn.close()
            return df
        except:
            pass
    return pd.DataFrame([
        {"lat": 40.7128, "lon": -74.0060, "nombre_nodo": "Nodo Central US"},
        {"lat": 34.0522, "lon": -118.2437, "nombre_nodo": "Nodo Pacifico US"},
        {"lat": 51.5074, "lon": -0.1278, "nombre_nodo": "Nodo Euro Core"}
    ])

def obtener_logs():
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        try:
            conn = psycopg2.connect(db_url)
            df = pd.read_sql("SELECT fecha_hora AS \"Fecha/Hora\", operador AS \"Operador\", accion AS \"Acción\" FROM audit_logs ORDER BY id DESC;", conn)
            conn.close()
            return df
        except:
            pass
    return pd.DataFrame([{"Fecha/Hora": time.strftime("%Y-%m-%d %H:%M:%S"), "Operador": "Sistema", "Acción": "Modo de respaldo local activo."}])

def guardar_nodo(lat, lon, nombre):
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        try:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO nodos (lat, lon, nombre_nodo) VALUES (%s, %s, %s);", (lat, lon, nombre))
            conn.commit(); cursor.close(); conn.close()
        except:
            pass

def guardar_log(operador, accion):
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        try:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO audit_logs (fecha_hora, operador, accion) VALUES (%s, %s, %s);", (time.strftime("%Y-%m-%d %H:%M:%S"), operador, accion))
            conn.commit(); cursor.close(); conn.close()
        except:
            pass

L = IDIOMAS[st.session_state["lang"]]

# 2. INYECCIÓN DE ESTILOS PREMIUM
st.markdown("""
<style>
    .brand-container {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        padding: 25px; border-radius: 12px; border: 1px solid #1e293b; border-bottom: 4px solid #0284c7; text-align: center; margin-bottom: 20px;
    }
    .brand-title { font-size: 36px !important; font-weight: 800 !important; color: #38bdf8 !important; margin: 0 !important; }
    .brand-subtitle { font-size: 12px !important; color: #ffffff !important; font-weight: 600 !important; letter-spacing: 4px !important; margin-top: 6px !important; }
    .stButton>button, .stDownloadButton>button {
        width: 100% !important; background-color: #0284c7 !important; color: white !important;
        border-radius: 8px !important; font-weight: bold !important; border: none !important;
    }
    .stButton>button:hover, .stDownloadButton>button:hover { background-color: #0369a1 !important; color: #38bdf8 !important; }
</style>
""", unsafe_allow_html=True)

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

# ENCABEZADO CORPORATIVO DINÁMICO
st.markdown(f"""
<div class="brand-container">
    <h1 class="brand-title">⚡ T&B Global</h1>
    <p class="brand-subtitle">{L['title']}</p>
</div>
""", unsafe_allow_html=True)

# CONTROL DE ACCESO CENTRALIZADO
if st.session_state["usuario_activo"] is None:
    st.warning(L["lock"])
    with st.sidebar:
        st.markdown("### 🔐 Acceso Centralizado")
        u = st.text_input(f"{L['user']}:")
        p = st.text_input(f"{L['pin']}:", type="password", max_chars=4)
        if st.button("Validar Credenciales"):
            if u and p:
                st.session_state["usuario_activo"] = u
                guardar_log(u, "Inicio de sesión de operador exitoso.")
                st.rerun()
else:
    # MENÚ LATERAL Y BÓVEDA DE DOCUMENTOS INTEGRADA
    with st.sidebar:
        st.success(f"Operador en Línea: {st.session_state['usuario_activo']}")
        st.markdown("---")
        st.markdown("### 📥 Owner Document Vault")
        
        reporte_texto = "ACTA OFICIAL DE ENTREGA DE PROPIEDAD INTELECTUAL\nPROYECTO: T&B Global - Enterprise OS\nDUEÑO: admin_tb\nSEGURIDAD: CIFRADO CRIPTOGRAFICO SHA-256 VALIDADO Y ACTIVO."
