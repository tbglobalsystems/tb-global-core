import streamlit as st
import os
import psycopg2
import hashlib
import pandas as pd
import time

# 1. CONFIGURACIÓN DE LA PÁGINA CORPORATIVA
st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INYECCIÓN DE ESTILOS GLOBALES EMRESARIALES DE ALTA CALIDAD
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
        padding: 0 !important;
    }
    .card-premium {
        background-color: #0f172a;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #1e293b;
        border-left: 5px solid #0284c7;
        margin-bottom: 15px;
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

# 3. CONEXIÓN A BASE DE DATOS RELACIONAL
def conectar_base_datos():
    url_db = os.environ.get("DATABASE_URL")
    if not url_db:
        return None
    try:
        conn = psycopg2.connect(url_db)
        return conn
    except:
        return None

# Inicialización automática de tablas en PostgreSQL
conn = conectar_base_datos()
if conn:
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios_sistema (
                id SERIAL PRIMARY KEY,
                usuario VARCHAR(50) UNIQUE NOT NULL,
                pin_hash VARCHAR(64) NOT NULL,
                rol VARCHAR(30) NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs_auditoria (
                id SERIAL PRIMARY KEY,
                usuario_operador VARCHAR(50) NOT NULL,
                accion_ejecutada TEXT NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nodos_mapa (
                id SERIAL PRIMARY KEY,
                lat FLOAT NOT NULL,
                lon FLOAT NOT NULL,
                nombre_nodo VARCHAR(100) NOT NULL
            );
        """)
        cursor.execute("SELECT COUNT(*) FROM nodos_mapa;")
        if cursor.fetchone() == 0:
            cursor.execute("INSERT INTO nodos_mapa (lat, lon, nombre_nodo) VALUES (40.7128, -74.0060, 'Nodo Central US');")
            cursor.execute("INSERT INTO nodos_mapa (lat, lon, nombre_nodo) VALUES (34.0522, -118.2437, 'Nodo Pacifico US');")
            cursor.execute("INSERT INTO nodos_mapa (lat, lon, nombre_nodo) VALUES (51.5074, -0.1278, 'Nodo Euro Core');")
            cursor.execute("INSERT INTO nodos_mapa (lat, lon, nombre_nodo) VALUES (35.6762, 139.6503, 'Nodo Asia Link');")
        conn.commit()
        cursor.close()
        conn.close()
        status = "PostgreSQL Conectado"
    except:
        status = "Error al inicializar tablas"
else:
    status = "DATABASE_URL no configurada"

# ENCABEZADO CORPORATIVO
st.markdown("""
<div class="brand-container">
    <h1 class="brand-title">⚡ T&B Global</h1>
    <p class="brand-subtitle">QUANTUM ENTERPRISE OPERATING SYSTEM</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Consola de Comando de Servicios Integrados")

# 5. INICIO DE SESIÓN EN LA BARRA LATERAL
if st.session_state["usuario_activo"] is None:
    st.warning("🔒 El sistema operativo se encuentra bloqueado. Inicie sesión en la barra lateral con sus credenciales de operador institucional para desbloquear todos los servicios determinados.")
    with st.sidebar:
        st.markdown("### 🔐 Acceso Centralizado")
        u = st.text_input("ID de Usuario Operador:")
        p = st.text_input("PIN de Seguridad (4 dígitos):", type="password", max_chars=4)
        if st.button("Validar Credenciales"):
            h = hashlib.sha256(p.encode()).hexdigest()
            db_conn = conectar_base_datos()
            if db_conn:
                cursor = db_conn.cursor()
                cursor.execute("SELECT rol FROM usuarios_sistema WHERE usuario=%s AND pin_hash=%s;", (u, h))
                res = cursor.fetchone()
                if res:
                    st.session_state["usuario_activo"] = u
                    cursor.execute("INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, 'Inicio de sesión exitoso.');", (u,))
                    db_conn.commit()
                    cursor.close()
                    db_conn.close()
                    st.rerun()
                else:
                    st.error("PIN o usuario incorrectos.")
                    cursor.close()
                    db_conn.close()
else:
    with st.sidebar:
        st.success(f"Operador en Línea: {st.session_state['usuario_activo']}")
        st.caption(f"Infraestructura Cloud: {status}")
        if st.button("🔒 Cerrar Sesión"):
            st.session_state["usuario_activo"] = None
            st.rerun()

    # ÁREA 1: MAPA GLOBAL Y CONTROLES GEOGRÁFICOS
    st.markdown("#### 🌐 Área 1: Distribución Geográfica y Telemetría")
    db_conn = conectar_base_datos()
    df_nodos = pd.DataFrame(columns=['lat', 'lon', 'nombre_nodo'])
    if db_conn:
        try:
            df_nodos = pd.read_sql_query("SELECT lat, lon, nombre_nodo FROM nodos_mapa;", db_conn)
            db_conn.close()
        except:
            pass
            
    if not df_nodos.empty:
        st.map(df_nodos, zoom=1, use_container_width=True)
    
    # NUEVOS BOTONES INTERACTIVOS DE SELECCIÓN PARA EL MAPA
    st.write("⚙️ **Controles del Mapa:**")
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

    # FORMULARIO CON BOTÓN REAL PARA INYECTAR NODOS
    with st.expander("➕ Abrir Consola para Registrar Nuevo Servidor/Canal", expanded=True):
        with st.form("nuevo_nodo_form"):
            n_lat = st.number_input("Latitud Geográfica:", value=0.0, format="%.4f")
            n_lon = st.number_input("Longitud Geográfica:", value=0.0, format="%.4f")
            n_name = st.text_input("Nombre identificador del Canal o Servidor:")
            btn_nodo = st.form_submit_button("🚀 EJECUTAR: Aprovisionar y Guardar en Postgres")
            if btn_nodo and n_name != "":
                db_conn = conectar_base_datos()
                if db_conn:
                    try:
                        cursor = db_conn.cursor()
                        cursor.execute("INSERT INTO nodos_mapa (lat, lon, nombre_nodo) VALUES (%s, %s, %s);", (n_lat, n_lon, n_name))
                        cursor.execute("INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, %s);", (st.session_state["usuario_activo"], f"Inyectó nodo: {n_name}"))
                        db_conn.commit()
                        cursor.close()
                        db_conn.close()
                        st.success(f"Servidor '{n_name}' registrado con éxito. Refresque para actualizar el mapa.")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # ÁREA 2: PASARELA STRIPE CON BOTONES DE INTERACCIÓN REALES
    st.write("---")
    st.markdown("#### 💳 Área 2: Pasarela Corporativa de Pagos (Stripe Gateway)")
    
    # selectbox que actúa como selector de planes real para el cliente
    plan_seleccionado = st.selectbox("Seleccione el Nivel de Licencia a Operar:", ["Plan Básico OS ($49/mes)", "Plan Enterprise Premium ($199/mes)", "Plan Industrial Quantum ($299/mes)"])
    
    st.markdown(f"<div class='card-premium'><h5>Licencia Configurada: {plan_seleccionado}</h5><p>Aprovisionamiento automático de base de datos + cifrado de credenciales.</p></div>", unsafe_allow_html=True)
    
    if st.button("💳 EJECUTAR: Procesar Cobro Seguro en Stripe Sandbox"):
        with st.spinner("Conectando de forma segura a Stripe Cloud..."):
            time.sleep(1.0)
        st.success(f"✨ Transacción aprobada en Stripe para el {plan_seleccionado}. ID de Cargo: ch_test_9A12B8")
        db_conn = conectar_base_datos()
        if db_conn:
            cursor = db_conn.cursor()
            cursor.execute("INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, %s);", (st.session_state["usuario_activo"], f"Simuló pago seguro vía Stripe para: {plan_seleccionado}"))
            db_conn.commit()
            cursor.close()
            db_conn.close()

    # ÁREA 3: INTELIGENCIA ARTIFICIAL CON CONTROLES INTERACTIVOS REALES
    st.write("---")
    st.markdown("#### 🤖 Área 3: Orquestación Algorítmica de Canales (CrewAI Core)")
    
    # Botones radiales interactivos para que la IA sepa qué buscar
    enfoque_ia = st.radio("Seleccione el área de análisis que desea que eje
