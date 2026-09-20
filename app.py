import streamlit as st
import os
import sqlite3
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

# Estilos visuales
st.markdown("""
<style>
    .main { background-color: #030407; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    .logo-header {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        padding: 25px; border-radius: 8px; border: 1px solid #1e293b;
        border-bottom: 4px solid #0284c7; margin-bottom: 20px;
        text-align: center;
    }
    .logo-text { font-size: 38px; font-weight: 800; color: #ffffff; letter-spacing: 1px; margin: 0; }
    .logo-sub { font-size: 14px; color: #0284c7; font-weight: 600; letter-spacing: 4px; margin: 5px 0 0 0; }
</style>
""", unsafe_allow_html=True)

if "auth_rol" not in st.session_state: st.session_state["auth_rol"] = None
if "usuario_activo" not in st.session_state: st.session_state["usuario_activo"] = None

# 2. CONEXIÓN A LA BASE DE DATOS
def inicializar_base_datos():
    url_db = os.environ.get("DATABASE_URL")
    if url_db:
        try:
            conn = psycopg2.connect(url_db)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios_sistema (
                    id SERIAL PRIMARY KEY,
                    usuario VARCHAR(50) UNIQUE NOT NULL,
                    pin_hash VARCHAR(64) NOT NULL,
                    rol VARCHAR(30) NOT NULL
                );
            """)
            conn.commit()
            cursor.close()
            conn.close()
            return "PostgreSQL Conectado"
        except Exception as e:
            return f"Error Postgres: {e}"
    return "Modo Local"

estado_infraestructura = inicializar_base_datos()

# 3. BARRA LATERAL
with st.sidebar:
    st.markdown("<h2 style='color:#0284c7;'>⚡ Panel OS</h2>", unsafe_allow_html=True)
    st.caption(f"Infraestructura: {estado_infraestructura}")

# 4. ENCABEZADO
st.markdown("""
<div class='logo-header'>
    <h1 class='logo-text'>⚡ T&B Global</h1>
    <p class='logo-sub'>QUANTUM ENTERPRISE OPERATING SYSTEM</p>
</div>
""", unsafe_allow_html=True)

tab_portal, tab_acceso, tab_consola = st.tabs(["🌐 Portal de Red Global", "🔐 Acceso Centralizado", "📊 Consola de Comando"])

# PESTAÑA 1: PORTAL DE RED GLOBAL
with tab_portal:
    coordenadas_datos = {
        'lat': [40.7128, 34.0522, 51.5074, 35.6762, -22.9068, -33.8688, 19.4326, 48.8566],
        'lon': [-74.0060, -118.2437, -0.1278, 139.6503, -43.1729, 151.2093, -99.1332, 2.3522]
    }
    st.map(pd.DataFrame(coordenadas_datos), zoom=1, use_container_width=True)

# PESTAÑA 2: ACCESO CENTRALIZADO
with tab_acceso:
    st.markdown("### 🔐 Autenticación de Operadores")
    if st.session_state["auth_rol"] is None:
        with st.form("formulario_acceso"):
            input_usuario = st.text_input("ID de Usuario Corporativo:")
            input_pin = st.text_input("PIN de Seguridad (4 dígitos):", type="password", max_chars=4)
            boton_login = st.form_submit_button("Validar Credenciales")
            
            if boton_login:
                hash_verificar = hashlib.sha256(input_pin.encode()).hexdigest()
                url_db = os.environ.get("DATABASE_URL")
                if url_db:
                    try:
                        conn = psycopg2.connect(url_db)
                        cursor = conn.cursor()
                        cursor.execute("SELECT rol FROM usuarios_sistema WHERE usuario=%s AND pin_hash=%s;", (input_usuario, hash_verificar))
                        resultado = cursor.fetchone()
                        if resultado:
                            st.session_state["auth_rol"] = resultado[0]
                            st.session_state["usuario_activo"] = input_usuario
                            st.success("Acceso Concedido")
                            st.rerun()
                        else:
                            st.error("PIN o usuario incorrectos.")
                        cursor.close()
                        conn.close()
                    except Exception as err:
                        st.error(f"Fallo de conexión: {err}")
    else:
        st.info(f"Sesión activa: **{st.session_state['usuario_activo']}**")
        if st.button("Cerrar Sesión"):
            st.session_state["auth_rol"] = None
            st.session_state["usuario_activo"] = None
            st.rerun()

# PESTAÑA 3: CONSOLA DE COMANDO (REGISTRO DIRECTO SIN CONDICIONALES COMPLEJOS)
with tab_consola:
    st.markdown("### 📊 Consola de Comando de Infraestructura")
    
    st.markdown("### 🛰️ Registro Directo de Operadores en PostgreSQL Cloud")
    with st.form("crear_usuario_nuevo"):
        nuevo_user = st.text_input("ID de Usuario Nuevo:")
        nuevo_pin = st.text_input("PIN de Seguridad Nuevo (4 dígitos):", type="password", max_chars=4)
        nuevo_rol = st.selectbox("Asignar Rol:", ["Administrador Industrial", "Operador", "Auditor"])
        boton_crear = st.form_submit_button("Registrar Credenciales")
        
        if boton_crear:
            if len(nuevo_pin) == 4 and nuevo_user != "":
                nuevo_hash = hashlib.sha256(nuevo_pin.encode()).hexdigest()
                url_db = os.environ.get("DATABASE_URL")
                if url_db:
                    try:
                        conn = psycopg2.connect(url_db)
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO usuarios_sistema (usuario, pin_hash, rol) VALUES (%s, %s, %s) ON CONFLICT (usuario) DO NOTHING;",
                            (nuevo_user, nuevo_hash, nuevo_rol)
                        )
                        conn.commit()
                        cursor.close()
                        conn.close()
                        st.success(f"Usuario '{nuevo_user}' registrado con éxito en Railway. Ya puedes iniciar sesión.")
                    except Exception as ex:
                        st.error(f"Error base de datos: {ex}")
