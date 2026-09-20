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

# 2. INYECCIÓN DE ESTILOS GLOBALES DE ALTA CALIDAD
st.html("""
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
</style>
""")

# Inicialización de variables de sesión
if "auth_rol" not in st.session_state:
    st.session_state["auth_rol"] = None
if "usuario_activo" not in st.session_state:
    st.session_state["usuario_activo"] = None

# 3. CONEXIÓN A BASE DE DATOS
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
        conn.commit()
        cursor.close()
        conn.close()
        estado_infraestructura = "PostgreSQL Conectado (Esquema Completo)"
    except:
        estado_infraestructura = "Error al inicializar tablas"
else:
    estado_infraestructura = "DATABASE_URL no configurada"

# 4. BARRA LATERAL
with st.sidebar:
    st.markdown("<h2 style='color:#0284c7;'>⚡ Panel OS</h2>", unsafe_allow_html=True)
    st.caption(f"Infraestructura: {estado_infraestructura}")
    if st.session_state["usuario_activo"]:
        st.success(f"Operador: {st.session_state['usuario_activo']}")

# 5. ENCABEZADO CORPORATIVO (AZUL Y BLANCO)
st.markdown("""
<div class="brand-container">
    <h1 class="brand-title">⚡ T&B Global</h1>
    <p class="brand-subtitle">QUANTUM ENTERPRISE OPERATING SYSTEM</p>
</div>
""", unsafe_allow_html=True)

# Definición limpia de pestañas
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
    st.markdown("### 🔐 Autenticación de Operadores")
    
    if st.session_state["auth_rol"] is None:
        with st.form("formulario_acceso"):
            input_usuario = st.text_input("ID de Usuario:")
            input_pin = st.text_input("PIN (4 dígitos):", type="password", max_chars=4)
            boton_login = st.form_submit_button("Validar Credenciales")
            
            if boton_login:
                hash_verificar = hashlib.sha256(input_pin.encode()).hexdigest()
                db_conn = conectar_base_datos()
                if db_conn:
                    try:
                        cursor = db_conn.cursor()
                        cursor.execute("SELECT rol FROM usuarios_sistema WHERE usuario=%s AND pin_hash=%s;", (input_usuario, hash_verificar))
                        resultado = cursor.fetchone()
                        
                        if resultado:
                            st.session_state["auth_rol"] = str(resultado[0])
                            st.session_state["usuario_activo"] = input_usuario
                            cursor.execute("INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, %s);", (input_usuario, "Inicio de sesión centralizado exitoso."))
                            db_conn.commit()
                            cursor.close()
                            db_conn.close()
                            st.success("Acceso Concedido")
                            st.rerun()
                        else:
                            st.error("PIN o usuario incorrectos.")
                            cursor.close()
                            db_conn.close()
                    except Exception as err:
                        st.error(f"Fallo en consulta: {err}")
                else:
                    st.error("No se pudo conectar a la base de datos.")
    else:
        st.info(f"Sesión activa: {st.session_state['usuario_activo']}")
        if st.button("Cerrar Sesión"):
            db_conn = conectar_base_datos()
            if db_conn:
                try:
                    cursor = db_conn.cursor()
                    cursor.execute("INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, %s);", (st.session_state["usuario_activo"], "Cierre de sesión voluntario."))
                    db_conn.commit()
                    cursor.close()
                    db_conn.close()
                except:
                    pass
            st.session_state["auth_rol"] = None
            st.session_state["usuario_activo"] = None
            st.rerun()

# PESTAÑA 3: CONSOLA DE COMANDO
with tab_consola:
    st.markdown("### 📊 Consola de Comando de Infraestructura")
    
    if st.session_state["auth_rol"] is not None:
        st.success(f"Autorización Operativa Nivel: {st.session_state['auth_rol']}")
        st.markdown("#### 🤖 Orquestación de Agentes Inteligentes (CrewAI Core)")
        st.write("Ejecute flujos de auditoría automatizados en la nube.")
        
        if st.button("🚀 Lanzar Crew: Auditoría de Nodos Globales"):
            with st.spinner("Inicializando agentes de CrewAI y cargando modelos lingüísticos..."):
                try:
                    from crewai import Agent, Task, Crew
                    
                    auditor = Agent(
                        role='Auditor de Sistemas Cloud',
                        goal='Analizar anomalías en la telemetría de la infraestructura',
                        backstory='Experto en ciberseguridad industrial y bases de datos relacionales.',
                        verbose=False,
                        allow_delegation=False
                    )
                    
                    tarea_auditoria = Task(
                        description='Revisar el estado reportado e identificar puntos críticos en los servidores.',
                        expected_output='Un breve resumen ejecutivo con 3 recomendaciones de seguridad.',
                        agent=auditor
                    )
                    
                    crew = Crew(agents=[auditor], tasks=[tarea_auditoria], verbose=False)
                    resultado_crew = crew.kickoff()
                    
                    st.success("✨ ¡Misión de CrewAI Completada!")
                    st.markdown(f"**Resultado del Análisis:**\n\n{resultado_crew}")
                    
                    db_conn = conectar_base_datos()
                    if db_conn:
                        cursor = db_conn.cursor()
                        cursor.execute("INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, %s);", (st.session_state["usuario_activo"], f"Auditoría CrewAI completada. Reporte: {str(resultado_crew)[:100]}..."))
                        db_conn.commit()
                        cursor.close()
                        db_conn.close()
                except Exception as e:
                    st.error(f"Error al ejecutar CrewAI: {e}")
        
        st.write("---")
        st.markdown("#### 📜 Registro General de Logs de Auditoría (PostgreSQL)")
        db_conn = conectar_base_datos()
        if db_conn:
            try:
                query_logs = "SELECT usuario_operador AS \"Operador\", accion_ejecutada AS \"Acción Realizada\", fecha_registro AS \"Estampa de Tiempo\" FROM logs_auditoria ORDER BY fecha_registro DESC LIMIT 10;"
                df_logs = pd.read_sql_query(query_logs, db_conn)
                db_conn.close()
                if not df_logs.empty:
                    st.dataframe(df_logs, use_container_width=True, hide_index=True)
                else:
                    st.info("No hay eventos registrados en los logs de infraestructura cloud.")
            except Exception as e:
                st.error(f"Error al leer logs: {e}")
                
        st.write("---")
        st.write("### Telemetría de Módulos Base")
        datos_operaciones = pd.DataFrame({
            "Módulo": ["Criptografía Core", "Base Datos Postgres", "Auditoría Engine"],
            "Estado": ["Operando", "Conectado", "Activo (Capturando)"]
        })
        st.table(datos_operaciones)
        
    else:
        st.warning("⚠️ Modo Sandbox Activo: Inicie sesión para ver la consola empresarial.")
