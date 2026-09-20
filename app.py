import streamlit as st
import os
import psycopg2
import hashlib
import pandas as pd
import threading

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de estilos globales de alta calidad
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

if "auth_rol" not in st.session_state:
    st.session_state["auth_rol"] = None
if "usuario_activo" not in st.session_state:
    st.session_state["usuario_activo"] = None
if "crew_ejecutando" not in st.session_state:
    st.session_state["crew_ejecutando"] = False
if "crew_resultado" not in st.session_state:
    st.session_state["crew_resultado"] = None

# 2. CONEXIÓN Y CREACIÓN DE TABLAS
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
        return "PostgreSQL Conectado (Esquema Completo)"
    except Exception as e:
        return f"Error Postgres: {e}"

estado_infraestructura = inicializar_base_datos()

# 3. FUNCIÓN DE BACKEND PARA EJECUTAR CREWAI (SEGURO PARA HILOS)
def ejecutar_flujo_crew(usuario, api_key):
    try:
        os.environ["OPENAI_API_KEY"] = api_key
        from crewai import Agent, Task, Crew
        
        analista = Agent(
            role='Analista de Infraestructura Global',
            goal='Auditar logs operativos e identificar áreas críticas de rendimiento.',
            backstory='Un motor de IA experto en optimización de sistemas en la nube y bases de datos relacionales.',
            verbose=False,
            allow_delegation=False
        )
        
        tarea_analisis = Task(
            description='Analizar el estado de conexión de la red cuántica simulada y proponer mejoras.',
            expected_output='Un resumen ejecutivo en limpio con 3 puntos clave optimizados.',
            agent=analista
        )
        
        instancia_crew = Crew(agents=[analista], tasks=[tarea_analisis], verbose=False)
        salida_texto = instancia_crew.kickoff()
        
        st.session_state["crew_resultado"] = str(salida_texto)
        
        url_db = os.environ.get("DATABASE_URL")
        if url_db:
            conn = psycopg2.connect(url_db)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, %s);",
                (usuario, f"Auditoría CrewAI completada con éxito. Reporte: {str(salida_texto)[:100]}...")
            )
            conn.commit()
            cursor.close()
            conn.close()
            
    except Exception as e:
        st.session_state["crew_resultado"] = f"Error en la ejecución agéntica: {str(e)}"
    finally:
        st.session_state["crew_ejecutando"] = False

# 4. BARRA LATERAL
with st.sidebar:
    st.markdown("<h2 style='color:#0284c7;'>⚡ Panel OS</h2>", unsafe_allow_html=True)
    st.caption(f"Infraestructura: {estado_infraestructura}")
    if st.session_state["usuario_activo"]:
        st.success(f"Operador: {st.session_state['usuario_activo']}")

# 5. ENCABEZADO CORPORATIVO
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
                        
                        if resultado:
                            st.session_state["auth_rol"] = str(resultado[0])
                            st.session_state["usuario_activo"] = input_usuario
                            
                            cursor.execute(
                                "INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, %s);",
                                (input_usuario, "Inicio de sesión centralizado exitoso.")
                            )
                            conn.commit()
                            cursor.close()
                            conn.close()
                            st.success("Acceso Concedido")
                            st.rerun()
                        else:
                            st.error("PIN o usuario incorrectos.")
                            cursor.close()
                            conn.close()
                    except Exception as err:
                        st.error(f"Error: {err}")
    else:
        st.info(f"Sesión activa: {st.session_state['usuario_activo']}")
        if st.button("Cerrar Sesión"):
            url_db = os.environ.get("DATABASE_URL")
            if url_db:
                try:
                    conn = psycopg2.connect(url_db)
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO logs_auditoria (usuario_operador, accion_ejecutada) VALUES (%s, %s);",
                        (st.session_state["usuario_activo"], "Cierre de sesión voluntario.")
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                except Exception:
                    pass
            st.session_state["auth_rol"] = None
            st.session_state["usuario_activo"] = None
            st.rerun()

# PESTAÑA 3: CONSOLA DE COMANDO
with tab_consola:
    st.markdown("### 📊 Consola de Comando")
    
    if st.session_state["auth_rol"] is not None:
        st.success(f"Autorización Operativa Nivel: {st.session_state['auth_rol']}")
        
        st.markdown("#### 🤖 Orquestación de Agentes Inteligentes (CrewAI Core)")
        st.write("Despliegue agentes cognitivos para auditar la telemetría global en segundo plano.")
        
        input_token_ai = st.text_input("Introduzca OpenAI API Key corporativa (sk-...):", type="password")
        
        if st.button("🚀 Lanzar Flujo de CrewAI Autónomo", disabled=st.session_state["crew_ejecutando"]):
            if input_token_ai.startswith("sk-"):
                st.session_state["crew_ejecutando"] = True
                st.session_state["crew_resultado"] = None
                
                hilo_agente = threading.Thread(
                    target=ejecutar_flujo_crew,
                    args=(st.session_state["usuario_activo"], input_token_ai)
                )
                hilo_agente.start()
                st.toast("Ecosistema de agentes CrewAI inicializado en segundo plano.", icon="🤖")
            else:
                st.error("Por favor, ingrese un token válido de OpenAI para aprovisionar los agentes.")
        
        if st.session_state["crew_ejecutando"]:
            st.info("⌛ Los agentes de CrewAI se encuentran procesando la telemetría. Por favor espere...")
        
        if st.session_state["crew_resultado"]:
            st.markdown("##### 📝 Reporte Generado por la IA:")
            st.info(st.session_state["crew_resultado"])
        
        st.write("---")
        # MÓDULO DE LOGS HISTÓRICOS
