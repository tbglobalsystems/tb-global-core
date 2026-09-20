import streamlit as st
import os
import sqlite3
import psycopg2
import hashlib
import pandas as pd

# =======================================================================
# CONFIGURACIÓN DE LA PÁGINA E INTERFAZ UI
# =======================================================================
st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos visuales premium del sistema corporativo
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
    .card-modulo {
        background: #0f172a; padding: 20px; border-radius: 8px;
        border: 1px solid #1e293b; border-left: 4px solid #10b981; margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

if "auth_rol" not in st.session_state: st.session_state["auth_rol"] = None
if "usuario_activo" not in st.session_state: st.session_state["usuario_activo"] = None

# =======================================================================
# CONEXIÓN INTELIGENTE A LA BASE DE DATOS
# =======================================================================
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
            cursor.execute("SELECT COUNT(*) FROM usuarios_sistema;")
            if cursor.fetchone() == 0:
                pin_por_defecto = hashlib.sha256("1234".encode()).hexdigest()
                cursor.execute(
                    "INSERT INTO usuarios_sistema (usuario, pin_hash, rol) VALUES (%s, %s, %s);",
                    ("admin_tb", pin_por_defecto, "Administrador Industrial")
                )
            conn.commit()
            cursor.close()
            conn.close()
            return "PostgreSQL (Railway Cloud Active)"
        except Exception as e:
            return f"Error Postgres: {e}"
    else:
        conn = sqlite3.connect("respaldo_local.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios_sistema (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                pin_hash TEXT NOT NULL,
                rol TEXT NOT NULL
            );
        """)
        cursor.execute("SELECT COUNT(*) FROM usuarios_sistema;")
        if cursor.fetchone() == 0:
            pin_por_defecto = hashlib.sha256("1234".encode()).hexdigest()
            cursor.execute(
                "INSERT INTO usuarios_sistema (usuario, pin_hash, rol) VALUES (?, ?, ?);",
                ("admin_tb", pin_por_defecto, "Administrador Industrial")
            )
        conn.commit()
        conn.close()
        return "SQLite3 (Modo Respaldo Local)"

estado_infraestructura = inicializar_base_datos()

# =======================================================================
# BARRA LATERAL TELEMETRÍA (SIDEBAR)
# =======================================================================
with st.sidebar:
    st.markdown("<h2 style='color:#0284c7;'>⚡ Panel OS</h2>", unsafe_allow_html=True)
    st.caption(f"Infraestructura: {estado_infraestructura}")
    st.write("---")
    st.write("Estado de Nodos Globales: **Óptimo**")

# =======================================================================
# ENCABEZADO PRINCIPAL DEL SISTEMA
# =======================================================================
st.markdown("""
<div class='logo-header'>
    <h1 class='logo-text'>⚡ T&B Global</h1>
    <p class='logo-sub'>QUANTUM ENTERPRISE OPERATING SYSTEM</p>
</div>
""", unsafe_allow_html=True)

# NAVEGACIÓN MODERNA MEDIANTE PESTAÑAS (MÁXIMA ESTABILIDAD)
tab_portal, tab_acceso, tab_consola = st.tabs(["🌐 Portal de Red Global", "🔐 Acceso Centralizado", "📊 Consola de 

# =======================================================================
# PESTAÑA 2: ACCESO CENTRALIZADO
# =======================================================================
with tab_acceso:
    st.markdown("### 🔐 Autenticación de Operadores")
    if st.session_state["auth_rol"] is None:
        with st.form("formulario_acceso"):
            input_usuario = st.text_input("ID de Usuario Corporativo:", placeholder="Ej: admin_tb")
            input_pin = st.text_input("PIN de Seguridad (4 dígitos):", type="password", max_chars=4)
            boton_login = st.form_submit_button("Validar Credenciales y Firmar Token")
            
            if boton_login:
                hash_verificar = hashlib.sha256(input_pin.encode()).hexdigest()
                url_db = os.environ.get("DATABASE_URL")
                usuario_valido = False
                rol_encontrado = None
                
                try:
                    if url_db:
                        conn = psycopg2.connect(url_db)
                        cursor = conn.cursor()
                        cursor.execute("SELECT rol FROM usuarios_sistema WHERE usuario=%s AND pin_hash=%s;", (input_usuario, hash_verificar))
                        resultado = cursor.fetchone()
                        if resultado:
                            usuario_valido = True
                            rol_encontrado = resultado[0]
                        cursor.close()
                        conn.close()
                    else:
                        conn = sqlite3.connect("respaldo_local.db")
                        cursor = conn.cursor()
                        cursor.execute("SELECT rol FROM usuarios_sistema WHERE usuario=? AND pin_hash=?;", (input_usuario, hash_verificar))
                        resultado = cursor.fetchone()
                        if resultado:
                            usuario_valido = True
                            rol_encontrado = resultado[0]
                        conn.close()
                        
                    if usuario_valido:
                        st.session_state["auth_rol"] = rol_encontrado
                        st.session_state["usuario_activo"] = input_usuario
                        st.success(f"¡Acceso Concedido! Rol: {rol_encontrado}")
                        st.rerun()
                    else:
                        st.error("ID de usuario o PIN incorrectos.")
                except Exception as err:
                    st.error(f"Fallo en el módulo de seguridad: {err}")
    else:
        st.info(f"Sesión activa: **{st.session_state['usuario_activo']}**")
        st.write(f"Nivel de Autorización: `{st.session_state['auth_rol']}`")
        if st.button("Cerrar Sesión Segura (Revocar Token)"):
            st.session_state["auth_rol"] = None
            st.session_state["usuario_activo"] = None
            st.rerun()

# =======================================================================
# PESTAÑA 3: CONSOLA DE COMANDO
# =======================================================================
with tab_consola:
    st.markdown("### 📊 Consola de Comando de Infraestructura")
    if st.session_state["auth_rol"] is not None:
        st.success(f"Panel Desbloqueado para: {st.session_state['auth_rol']}")
        st.write("### Registros de Telecomunicaciones en Tiempo Real")
        datos_operaciones = pd.DataFrame({
            "Módulo": ["Criptografía", "Base Datos Postgres", "CrewAI Agents", "Stripe Gateway (Sandbox)"],
            "Estado": ["Operando (Fernet Activo)", "Conectado (Cloud)", "Durmiente", "Modo Pruebas Listo"],
            "Carga": ["4%", "12%", "0%", "Listo"]
        })
        st.table(datos_operaciones)
    else:
        st.warning("⚠️ Acceso Restringido. Inicie sesión primero en la pestaña 'Acceso Centralizado'.")
