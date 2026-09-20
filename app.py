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

# Inyección de estilos globales de alta calidad para anular el tema nativo de Streamlit
st.html("""
<style>
    /* Estilización del contenedor del logotipo */
    .brand-container {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #1e293b;
        border-bottom: 4px solid #0284c7;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Fuerza el color Azul Corporativo Brillante en el título principal */
    .brand-title {
        font-size: 40px !important;
        font-weight: 800 !important;
        color: #38bdf8 !important;
        letter-spacing: 2px !important;
        margin: 0 !important;
        padding: 0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Fuerza el color Blanco Puro en el subtítulo institucional */
    .brand-subtitle {
        font-size: 13px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        letter-spacing: 5px !important;
        margin-top: 8px !important;
        margin-bottom: 0 !important;
        padding: 0 !important;
        opacity: 0.95 !important;
        font-family: 'Inter', sans-serif !important;
    }
</style>
""")

if "auth_rol" not in st.session_state:
    st.session_state["auth_rol"] = None
if "usuario_activo" not in st.session_state:
    st.session_state["usuario_activo"] = None

# 2. CONEXIÓN A BASE DE DATOS
def inicializar_base_datos():
    url_db = os.environ.get("DATABASE_URL")
    if not url_db:
        return "Falta variable DATABASE_URL"
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

estado_infraestructura = inicializar_base_datos()

# 3. BARRA LATERAL
with st.sidebar:
    st.markdown("<h2 style='color:#0284c7;'>⚡ Panel OS</h2>", unsafe_allow_html=True)
    st.caption(f"Infraestructura: {estado_infraestructura}")
    if st.session_state["usuario_activo"]:
        st.success(f"Operador: {st.session_state['usuario_activo']}")

# 4. ENCABEZADO CORPORATIVO ESTRUCTURADO CON CLASES DE ALTO CONTRASTE
st.markdown("""
<div class="brand-container">
    <h1 class="brand-title">⚡ T&B Global</h1>
    <p class="brand-subtitle">QUANTUM ENTERPRISE OPERATING SYSTEM</p>
</div>
""", unsafe_allow_html=True)

tab_portal, tab_acceso, tab_consola = st.tabs(["🌐 Portal de Red Global", "🔐 Acceso Centralizado", "📊 Consola de Comando"])

# PESTAÑA 1: PORTAL DE RED GLOBAL
with tab_portal:
    st.markdown("### 🌐 Monitoreo de Nodos")
    coordenadas_datos = {
        'lat': [40.7128, 34.0522, 51.5074, 35.6762],
        'lon': [-74.0060, -118.2437, -0.1278, 139.6503]
    }
    st.map(pd.DataFrame(coordenadas_datos), zoom=1, use_container_width=True)

# PESTAÑA 2: ACCESO CENTRALIZADO
with tab_acceso:
    st.markdown("### 🔐 Autenticación")
    if st.session_state["auth_rol"] is None:
        with st.form("formulario_acceso"):
            input_usuario = st.text_input("ID de Usuario:")
            input_pin = st.text_input("PIN (4 dígitos):", type="password", max_chars=4)
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
                        cursor.close()
                        conn.close()
                        if resultado:
                            st.session_state["auth_rol"] = resultado[0]
                            st.session_state["usuario_activo"] = input_usuario
                            st.success("Acceso Concedido")
                            st.rerun()
                        else:
                            st.error("PIN o usuario incorrectos.")
                    except Exception as err:
                        st.error(f"Error: {err}")
    else:
        st.info(f"Sesión activa: {st.session_state['usuario_activo']}")
        if st.button("Cerrar Sesión"):
            st.session_state["auth_rol"] = None
            st.session_state["usuario_activo"] = None
            st.rerun()

# PESTAÑA 3: CONSOLA DE COMANDO
with tab_consola:
    st.markdown("### 📊 Consola de Comando")
    if st.session_state["auth_rol"] is not None:
        st.success(f"Autorización: {st.session_state['auth_rol']}")
        st.write("Telemetría en Tiempo Real")
        datos_operaciones = pd.DataFrame({
            "Módulo": ["Criptografía Core", "Base Datos Postgres"],
            "Estado": ["Operando", "Conectado"]
        })
        st.table(datos_operaciones)
        
    if st.session_state["auth_rol"] is None:
        st.warning("⚠️ Modo Sandbox Activo")
        st.markdown("### 🛰️ Registro de Operadores")
        with st.form("crear_usuario_nuevo"):
            nuevo_user = st.text_input("ID de Usuario Nuevo:")
            nuevo_pin = st.text_input("PIN Nuevo (4 dígitos):", type="password", max_chars=4)
            nuevo_rol = st.selectbox("Rol:", ["Administrador", "Operador", "Auditor"])
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
                            st.success(f"Usuario {nuevo_user} registrado con éxito.")
                        except Exception as err:
                            st.error(f"Error db: {err}")
                else:
                    st.error("Datos inválidos.")
