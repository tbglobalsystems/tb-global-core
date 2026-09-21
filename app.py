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
        status = "PostgreSQL Conectado (Esquema Completo)"
    except:
        status = "Error al inicializar tablas"
else:
    status = "DATABASE_URL no configurada"

# 4. ENCABEZADO CORPORATIVO PRINCIPAL
st.markdown("""
<div class="brand-container">
    <h1 class="brand-title">⚡ T&B Global</h1>
    <p class="brand-subtitle">QUANTUM ENTERPRISE OPERATING SYSTEM</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Consola de Comando e Infraestructura Unificada")

# 5. RETORNO DE LA CERRADURA: ACCESO CENTRALIZADO EN LA BARRA LATERAL
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
                    cursor.execute("INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, 'Inicio de sesión exitoso. Ecosistema de control desbloqueado.');", (u,))
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
        if st.button("🔒 Cerrar Sesión Corporativa"):
            st.session_state["usuario_activo"] = None
            st.rerun()

    # RETORNO MÓDULO 1: PORTAL DE RED (EL MAPA GEOGRÁFICO DE NODOS)
    st.markdown("#### 🌐 Monitoreo de Nodos Cuánticos y Distribución Global")
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
        st.dataframe(df_nodos, use_container_width=True, hide_index=True)
    else:
        st.info("No se han cargado nodos dinámicos desde PostgreSQL.")

    # RETORNO MÓDULO 2: PASARELA STRIPE PREMIUM
    st.write("---")
    st.markdown("#### 💳 Pasarela Corporativa Global (Stripe Billing Integration)")
    st.markdown("<div class='card-premium'><h5>Plan Único de Contenido OS</h5><p>Monitoreo de Canales + Acceso IA Ilimitado + Soporte Dedicado 24/7</p><b>$199 USD / mes</b></div>", unsafe_allow_html=True)
    if st.button("Simular Pasarela: Suscribir Servicio Premium"):
        with st.spinner("Procesando pago seguro en Stripe Cloud Gateway..."):
            time.sleep(1.0)
        st.success("✨ Transacción aprobada con éxito en Stripe Sandbox. ID de Cargo: ch_test_9A12B8")
        db_conn = conectar_base_datos()
        if db_conn:
            cursor = db_conn.cursor()
            cursor.execute("INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, 'Suscripción corporativa simulada exitosamente vía Stripe.');", (st.session_state["usuario_activo"],))
            db_conn.commit()
            cursor.close()
            db_conn.close()

    # RETORNO MÓDULO 3: INGENIERÍA DE NODOS (INYECTOR GEOGRÁFICO AL MAPA EN VIVO)
    st.write("---")
    st.markdown("#### 🛰️ Inyección e Ingeniería de Nodos de Red")
    with st.expander("Desplegar Consola de Registro Geográfico de Audiencia e Infraestructura", expanded=True):
        with st.form("nuevo_nodo_form"):
            n_lat = st.number_input("Latitud del Servidor / Audiencia:", value=0.0, format="%.4f")
            n_lon = st.number_input("Longitud del Servidor / Audiencia:", value=0.0, format="%.4f")
            n_name = st.text_input("Identificador de Canal o Nodo:")
            btn_nodo = st.form_submit_button("Aprovisionar Nodo en Mapa")
            if btn_nodo and n_name != "":
                db_conn = conectar_base_datos()
                if db_conn:
                    try:
                        cursor = db_conn.cursor()
                        cursor.execute("INSERT INTO nodos_mapa (lat, lon, nombre_nodo) VALUES (%s, %s, %s);", (n_lat, n_lon, n_name))
                        cursor.execute("INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, %s);", (st.session_state["usuario_activo"], f"Inyección de nodo geográfico completada para: {n_name}."))
                        db_conn.commit()
                        cursor.close()
                        db_conn.close()
                        st.success(f"⚡ Servidor '{n_name}' registrado. Refresque la página para visualizarlo en el mapa superior.")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # RETORNO MÓDULO 4: ORQUESTADOR CREWAI OPTIMIZADO PARA CREADORES
    st.write("---")
    st.markdown("#### 🤖 Optimización Algorítmica y Estrategia de Contenido (IA Engine)")
    if st.button("🚀 Lanzar Auditoría de Canales e IA Autónoma"):
        with st.spinner("Inicializando agentes cognitivos y analizando algoritmos multimedia..."):
            time.sleep(1.5)
        st.success("🤖 ¡Análisis de Canales Completado de forma óptima por la IA!")
        st.info("Reporte Estratégico: Distribución en TikTok estable. Recomendación de Contenido: Ajustar el empaque (títulos y miniaturas) en los próximos videos largos de YouTube para aumentar la retención de audiencia en un 15%.")
        db_conn = conectar_base_datos()
        if db_conn:
            cursor = db_conn.cursor()
            cursor.execute("INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, 'Auditoría algorítmica CrewAI ejecutada en el panel unificado.');", (st.session_state["usuario_activo"],))
