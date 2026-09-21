cat << 'EOF' > app.py
import streamlit as st
import os
import psycopg2
import hashlib
import pandas as pd
import time

st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

if "nodos_locales" not in st.session_state:
    st.session_state["nodos_locales"] = pd.DataFrame([
        {"lat": 40.7128, "lon": -74.0060, "nombre_nodo": "Nodo Central US (Modo Seguro)"},
        {"lat": 34.0522, "lon": -118.2437, "nombre_nodo": "Nodo Pacifico US (Modo Seguro)"},
        {"lat": 51.5074, "lon": -0.1278, "nombre_nodo": "Nodo Euro Core (Modo Seguro)"}
    ])

def conectar_base_datos():
    url_db = os.environ.get("DATABASE_URL")
    if not url_db:
        return None
    try:
        conn = psycopg2.connect(url_db, connect_timeout=3)
        return conn
    except Exception:
        return None

db_disponible = False
status = "DATABASE_URL no configurada (Ejecutando en Modo Local Seguro)"

conn = conectar_base_datos()
if conn:
    try:
        with conn.cursor() as cursor:
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
            conn.commit()
        status = "PostgreSQL Conectado Activo"
        db_disponible = True
    except Exception as e:
        status = f"Modo Contingencia (Error DB: {str(e)})"
    finally:
        conn.close()

st.markdown("""
<div class="brand-container">
    <h1 class="brand-title">⚡ T&B Global</h1>
    <p class="brand-subtitle">QUANTUM ENTERPRISE OPERATING SYSTEM</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Consola de Comando de Servicios Integrados")

if st.session_state["usuario_activo"] is None:
    st.warning("🔒 El sistema operativo se encuentra bloqueado. Inicie sesión en la barra lateral con sus credenciales de operador institucional para desbloquear todos los servicios determinados.")
    with st.sidebar:
        st.markdown("### 🔐 Acceso Centralizado")
        u = st.text_input("ID de Usuario Operador:")
        p = st.text_input("PIN de Seguridad (4 dígitos):", type="password", max_chars=4)
        
        if not db_disponible:
            st.info("💡 Modo seguro activo: ingrese cualquier usuario/PIN para pruebas locales.")
            
        if st.button("Validar Credenciales"):
            if u and p:
                if db_disponible:
                    h = hashlib.sha256(p.encode()).hexdigest()
                    db_conn = conectar_base_datos()
                    if db_conn:
                        try:
                            with db_conn.cursor() as cursor:
                                cursor.execute("SELECT rol FROM usuarios_sistema WHERE usuario=%s AND pin_hash=%s;", (u, h))
                                res = cursor.fetchone()
                                if res:
                                    st.session_state["usuario_activo"] = u
                                    cursor.execute("INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, 'Inicio de sesión exitoso.');", (u,))
                                    db_conn.commit()
                                    st.rerun()
                                else:
                                    st.error("PIN o usuario incorrectos.")
                        except Exception as e:
                            st.error(f"Error de consulta: {str(e)}")
                        finally:
                            db_conn.close()
                else:
                    st.session_state["usuario_activo"] = u
                    st.rerun()
            else:
                st.error("Por favor, rellene todos los campos.")
else:
    with st.sidebar:
        st.success(f"Operador en Línea: {st.session_state['usuario_activo']}")
        st.caption(f"Infraestructura Cloud: {status}")
        if st.button("🔒 Cerrar Sesión"):
            st.session_state["usuario_activo"] = None
            st.rerun()

    st.markdown("#### 🌐 Área 1: Distribución Geográfica y Telemetría")
    df_nodos = pd.DataFrame(columns=['lat', 'lon', 'nombre_nodo'])
    
    if db_disponible:
        db_conn = conectar_base_datos()
        if db_conn:
            try:
                df_nodos = pd.read_sql_query("SELECT lat, lon, nombre_nodo FROM nodos_mapa;", db_conn)
            except Exception:
                df_nodos = st.session_state["nodos_locales"]
            finally:
                db_conn.close()
    else:
        df_nodos = st.session_state["nodos_locales"]
            
    if not df_nodos.empty:
        st.map(df_nodos, zoom=1, use_container_width=True)
    else:
        st.info("No hay nodos configurados en el mapa.")
    
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

    with st.expander("➕ Abrir Consola para Registrar Nuevo Servidor/Canal", expanded=True):
        with st.form("nuevo_nodo_form"):
            n_lat = st.number_input("Latitud Geográfica:", value=0.0, format="%.4f")
            n_lon = st.number_input("Longitud Geográfica:", value=0.0, format="%.4f")
            n_name = st.text_input("Nombre identificador del Canal o Servidor:")
            btn_nodo = st.form_submit_button("🚀 EJECUTAR: Aprovisionar y Guardar")
            
            if btn_nodo:
                if n_name.strip() != "":
                    if db_disponible:
                        db_conn = conectar_base_datos()
                        if db_conn:
                            try:
                                with db_conn.cursor() as cursor:
                                    cursor.execute("INSERT INTO nodos_mapa (lat, lon, nombre_nodo) VALUES (%s, %s, %s);", (n_lat, n_lon, n_name))
                                    cursor.execute("INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, %s);", (st.session_state["usuario_activo"], f"Inyectó nodo: {n_name}"))
                                    db_conn.commit()
                                st.success(f"Servidor '{n_name}' registrado en Postgres exitosamente.")
                                time.sleep(0.5)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error al guardar en base de datos: {str(e)}")
                            finally:
                                db_conn.close()
                    else:
                        nuevo_registro = pd.DataFrame([{"lat": n_lat, "lon": n_lon, "nombre_nodo": f"{n_name} (Local)"}])
                        st.session_state["nodos_locales"] = pd.concat([st.session_state["nodos_locales"], nuevo_registro], ignore_index=True)
                        st.success(f"Servidor '{n_name}' guardado en memoria de sesión.")
