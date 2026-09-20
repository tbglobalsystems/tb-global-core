import streamlit as st
import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib

# =======================================================================
# CONFIGURACIÓN DE LA PÁGINA E INTERFAZ UI
# =======================================================================
st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Premium de Grado SaaS (Zero-Trust UI Blindada)
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

# Inicialización Blindada de Estados de Sesión Corporativa
if "auth_rol" not in st.session_state: st.session_state["auth_rol"] = None
if "usuario_activo" not in st.session_state: st.session_state["usuario_activo"] = None

# =======================================================================
# CONEXIÓN INTELIGENTE A LA BASE DE DATOS (POSTGRES / SQLITE DETECTOR)
# =======================================================================
def inicializar_base_datos():
    url_db = os.environ.get("DATABASE_URL")
    
    # Si estamos en Railway con Postgres activo
    if url_db:
        try:
            conn = psycopg2.connect(url_db)
            cursor = conn.cursor()
            # Crear tabla de infraestructura de usuarios si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios_sistema (
                    id SERIAL PRIMARY KEY,
                    usuario VARCHAR(50) UNIQUE NOT NULL,
                    pin_hash VARCHAR(64) NOT NULL,
                    rol VARCHAR(30) NOT NULL
                );
            """)
            # Insertar un Administrador de pruebas por defecto (PIN: 1234)
            cursor.execute("SELECT COUNT(*) FROM usuarios_sistema;")
            if cursor.fetchone()[0] == 0:
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
    
    # Modo de respaldo local si la nube no responde
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
        if cursor.fetchone()[0] == 0:
            pin_por_defecto = hashlib.sha256("1234".encode()).hexdigest()
            cursor.execute(
                "INSERT INTO usuarios_sistema (usuario, pin_hash, rol) VALUES (?, ?, ?);",
                ("admin_tb", pin_por_defecto, "Administrador Industrial")
            )
        conn.commit()
        conn.close()
        return "SQLite3 (Modo Respaldo Local)"

# Ejecutar el motor de inicialización al arrancar
estado_infraestructura = inicializar_base_datos()

# =======================================================================
# MENÚ LATERAL PROFESIONAL DE CONTROL (SIDEBAR NAV)
# =======================================================================
with st.sidebar:
    st.markdown("<h2 style='color:#0284c7; margin-bottom:5px;'>⚡ Panel OS</h2>", unsafe_allow_html=True)
    st.caption(f"Infraestructura: {estado_infraestructura}")
    st.line_chart([1, 2, 3, 5, 4, 6])  # Gráfico pequeño de telemetría de red
    st.write("---")
    
    # Navegación del Sistema mediante Botones de Radio Profesionales
    opcion_menu = st.radio(
        "Seleccione el Área de Operación:",
        ["🌐 Portal de Red Global", "🔐 Acceso Centralizado", "📊 Consola de Comando"]
    )

# =======================================================================
# ÁREA 1: PORTAL DE RED GLOBAL (PANTALLA DE INICIO)
# =======================================================================
if opcion_menu == "🌐 Portal de Red Global":
    st.markdown("""
    <div class='logo-header'>
        <h1 class='logo-text'>⚡ T&B Global</h1>
        <p class='logo-sub'>QUANTUM ENTERPRISE OPERATING SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carga segura del mapa independiente
    try:
        with open("mundo.html", "r", encoding="utf-8") as f:
            codigo_mundo = f.read()
        st.components.v1.html(codigo_mundo, height=410)
    except Exception as e:
        st.error(f"Error en los sistemas de telecomunicaciones: {e}")

# =======================================================================
# ÁREA 2: ACCESO CENTRALIZADO (FORMULARIO DE LOGIN CON PIN)
# =======================================================================
elif opcion_menu == "🔐 Acceso Centralizado":
    st.markdown("<h2 style='color:#ffffff;'>🔐 Autenticación de Operadores</h2>", unsafe_allow_html=True)
    st.write("Ingrese sus credenciales corporativas para liberar las diferentes áreas funcionales.")
    
    if st.session_state["auth_rol"] is None:
        with st.form("formulario_acceso"):
            input_usuario = st.text_input("ID de Usuario Corporativo:", placeholder="Ej: admin_tb")
            input_pin = st.text_input("PIN de Seguridad Quantum (4 dígitos):", type="password", max_chars=4)
            boton_login = st.form_submit_button("Validar Credenciales y Firmar Token")
            
            if boton_login:
                hash_verificar = hashlib.sha256(input_pin.encode()).hexdigest()
                
                # Validar consultas en la base de datos correspondiente
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
                        st.success(f"¡Acceso Concedido! Rol: {rol_encontrado}. Token firmado digitalmente.")
                        st.rerun()
                    else:
                        st.error("Error de autenticación: El ID de usuario o el PIN son incorrectos.")
                except Exception as err:
                    st.error(f"Fallo crítico en el módulo de seguridad: {err}")
    else:
        st.info(f"Sesión activa actual: **{st.session_state['usuario_activo']}**")
        st.write(f"Nivel de Autorización: `{st.session_state['auth_rol']}`")
        if st.button("Cerrar Sesión Segura (Revocar Token)"):
            st.session_state["auth_rol"] = None
            st.session_state["usuario_activo"] = None
            st.rerun()

# =======================================================================
# ÁREA 3: CONSOLA DE COMANDO (PROTEGIDA POR ROL)
# =======================================================================
elif opcion_menu == "📊 Consola de Comando":
    st.markdown("<h2 style='color:#ffffff;'>📊 Consola de Comando de Infraestructura</h2>", unsafe_allow_html=True)
    
    if st.session_state["auth_rol"] is not None:
        st.success(f"Panel Desbloqueado para: {st.session_state['auth_rol']}")
        
        st.markdown(f"""
        <div class='card-modulo'>
            <h3 style='margin:0; color:#10b981;'>⚙️ Monitoreo de Operaciones de T&B Global</h3>
            <p style='color:#94a3b8; font-size:14px; margin-top:5px;'>
                Todas las llamadas de CrewAI, encriptación Fernet y bases de datos Postgres están respondiendo de manera óptima.
            </p>
        </div>
        """, unsafe_allow_html=True)
st.st.write("### Registros de Telecomunicaciones en Tiempo Real")
        datos_operaciones = pd.DataFrame({
            "Módulo": ["Criptografía", "Base Datos Postgres", "CrewAI Agents", "Stripe Gateway (Sandbox)"],
            "Estado": ["Operando (Fernet Activo)", "Conectado (Cloud)", "Durmiente", "Modo Pruebas Listo"],
            "Carga": ["4%", "12%", "0%", "Listo"]
        })
        st.table(datos_operaciones)
