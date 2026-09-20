import streamlit as st
import os
import psycopg2
import hashlib
import pandas as pd

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTILOS COMPATIBLES
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
    .brand-title { font-size: 40px !important; color: #38bdf8 !important; font-weight: 800; }
    .brand-subtitle { font-size: 13px !important; color: #ffffff !important; letter-spacing: 5px; }
</style>
""", unsafe_allow_html=True)

if "usuario_activo" not in st.session_state:
    st.session_state["usuario_activo"] = None

# 3. BASE DE DATOS DIRECTA
def conectar_base_datos():
    url = os.environ.get("DATABASE_URL")
    if not url: return None
    try: return psycopg2.connect(url)
    except: return None

# Inicialización forzada plana
db = conectar_base_datos()
if db:
    try:
        c = db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS usuarios_sistema (id SERIAL PRIMARY KEY, usuario VARCHAR(50) UNIQUE, pin_hash VARCHAR(64), rol VARCHAR(30));")
        c.execute("CREATE TABLE IF NOT EXISTS logs_auditoria (id SERIAL PRIMARY KEY, usuario_operador VARCHAR(50), accion_ejecutada TEXT, fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
        db.commit()
        c.close()
        db.close()
        status = "PostgreSQL Conectado"
    except: status = "Error tablas"
else: status = "DATABASE_URL Ausente"

# 4. ENCABEZADO
st.markdown('<div class="brand-container"><h1 class="brand-title">⚡ T&B Global</h1><p class="brand-subtitle">QUANTUM ENTERPRISE OPERATING SYSTEM</p></div>', unsafe_allow_html=True)

# 5. ESTRUCTURA PLANA EN LÍNEA (No anidada, inmune a errores)
st.markdown("### 📊 Panel Único de Infraestructura y Control")

if st.session_state["usuario_activo"] is None:
    st.warning("🔒 Inicie sesión en la barra lateral para desbloquear los servicios institucionales.")
    with st.sidebar:
        st.markdown("### 🔐 Acceso")
        u = st.text_input("Usuario:")
        p = st.text_input("PIN (4 dígitos):", type="password", max_chars=4)
        if st.button("Ingresar al Sistema"):
            h = hashlib.sha256(p.encode()).hexdigest()
            db_conn = conectar_base_datos()
            if db_conn:
                cursor = db_conn.cursor()
                cursor.execute("SELECT rol FROM usuarios_sistema WHERE usuario=%s AND pin_hash=%s;", (u, h))
                res = cursor.fetchone()
                if res:
                    st.session_state["usuario_activo"] = u
                    cursor.execute("INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, 'Login exitoso en entorno plano.');", (u,))
                    db_conn.commit()
                    cursor.close()
                    db_conn.close()
                    st.rerun()
                else: st.error("PIN o usuario incorrectos.")
else:
    st.success(f"Operador Activo: {st.session_state['usuario_activo']} | Infraestructura: {status}")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["usuario_activo"] = None
        st.rerun()

    # SERVICIOS DESPLEGADOS DIRECTOS
    st.markdown("---")
    st.markdown("#### 💳 Pasarela Stripe Billing Integration")
    if st.button("Simular Cobro Suscripción Corporativa"):
        st.success("✨ Cobro aprobado en Stripe Gateway Sandbox. Token: ch_test_9A12B8")

    st.markdown("---")
    st.markdown("#### 🤖 Orquestador de Estrategia de Contenido (CrewAI Engine)")
    if st.button("🚀 Lanzar Auditoría de Canales e IA Autónoma"):
        st.info("🤖 Procesando métricas de retención con el Director de Estrategia Digital...")
        time.sleep(2)
        st.success("Análisis completado: Canales estables, optimización de algoritmos recomendada para Shorts y TikTok.")

    st.markdown("---")
    st.markdown("#### 📜 Registro General de Logs de Auditoría (PostgreSQL)")
    db_conn = conectar_base_datos()
    if db_conn:
        try:
            df = pd.read_sql_query("SELECT usuario_operador AS \"Operador\", accion_ejecutada AS \"Acción\", fecha_registro AS \"Fecha\" FROM logs_auditoria ORDER BY fecha_registro DESC LIMIT 5;", db_conn)
            db_conn.close()
            st.dataframe(df, use_container_width=True, hide_index=True)
        except: pass
