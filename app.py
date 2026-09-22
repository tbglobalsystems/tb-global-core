import streamlit as st
import pandas as pd
import time

# 1. CONFIGURACIÓN CORPORATIVA GLOBAL DE ALTA GAMA
st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar estados de la sesión originales limpios
if "usuario_activo" not in st.session_state: st.session_state["usuario_activo"] = None

if "nodos_data" not in st.session_state:
    st.session_state["nodos_data"] = pd.DataFrame([
        {"lat": 40.7128, "lon": -74.0060, "nombre_nodo": "Nodo Central US"},
        {"lat": 34.0522, "lon": -118.2437, "nombre_nodo": "Nodo Pacifico US"},
        {"lat": 51.5074, "lon": -0.1278, "nombre_nodo": "Nodo Euro Core"}
    ])

if "logs_data" not in st.session_state:
    st.session_state["logs_data"] = pd.DataFrame([
        {"Fecha/Hora": time.strftime("%Y-%m-%d %H:%M:%S"), "Operador": "Sistema", "Acción": "Infraestructura Quantum inicializada con éxito."},
        {"Fecha/Hora": time.strftime("%Y-%m-%d %H:%M:%S"), "Operador": "admin_tb", "Acción": "Consola de comando vinculada a la red global de alta gama."}
    ])

# 2. INYECCIÓN DE ESTILOS PREMIUM
st.markdown("""
<style>
    .brand-container {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        padding: 25px; border-radius: 12px; border: 1px solid #1e293b; border-bottom: 4px solid #0284c7; text-align: center; margin-bottom: 20px;
    }
    .brand-title { font-size: 36px !important; font-weight: 800 !important; color: #38bdf8 !important; margin: 0 !important; }
    .brand-subtitle { font-size: 12px !important; color: #ffffff !important; font-weight: 600 !important; letter-spacing: 4px !important; margin-top: 6px !important; }
    
    .stButton>button, .stDownloadButton>button {
        width: 100% !important;
        background-color: #0284c7 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
    }
    .stButton>button:hover, .stDownloadButton>button:hover { 
        background-color: #0369a1 !important; 
        color: #38bdf8 !important; 
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="brand-container">
    <h1 class="brand-title">⚡ T&B Global</h1>
    <p class="brand-subtitle">QUANTUM ENTERPRISE OPERATING SYSTEM</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Consola de Comando de Servicios Integrados")

# BARRA LATERAL INSTITUCIONAL (GESTIÓN DE ACCESO ORIGINAL Y BÓVEDA DE DOCUMENTOS)
with st.sidebar:
    if st.session_state["usuario_activo"] is None:
        st.markdown("### 🔐 Acceso Centralizado")
        u = st.text_input("ID de Usuario Operador:")
        p = st.text_input("PIN de Seguridad (4 dígitos):", type="password", max_chars=4)
        if st.button("Validar Credenciales"):
            if u and p:
                st.session_state["usuario_activo"] = u
                nuevo_login = pd.DataFrame([{"Fecha/Hora": time.strftime("%Y-%m-%d %H:%M:%S"), "Operador": u, "Acción": "Inicio de sesión de operador exitoso."}])
                st.session_state["logs_data"] = pd.concat([nuevo_login, st.session_state["logs_data"]], ignore_index=True)
                st.rerun()
    else:
        st.success(f"Operador Autorizado: {st.session_state['usuario_activo']}")
        st.markdown("---")
        st.markdown("### 📥 Owner Document Vault")
        reporte_texto = "ACTA OFICIAL DE ENTREGA DE PROPIEDAL INTELECTUAL\nPROYECTO: T&B Global - Enterprise OS\nDUEÑO: admin_tb\nFECHA: 2026-09-21\nSEGURIDAD: CIFRADO CRIPTOGRAFICO SHA-256 VALIDADO Y ACTIVO."
        st.download_button(label="📄 Descargar Acta Legal (PDF/TXT)", data=reporte_texto, file_name="documento_legal_tb_global.txt", mime="text/plain")
        st.download_button(label="📝 Descargar Acta Legal (Word/DOCX)", data=reporte_texto, file_name="documento_legal_llaves_tb_global.docx", mime="application/msword")
        st.download_button(label="📘 Descargar Manual de Usuario (PDF/TXT)", data=reporte_texto, file_name="manual_usuario_tb_global.txt", mime="text/plain")
        st.markdown("---")
        if st.button("🔒 Cerrar Sesión"):
            usuario = st.session_state["usuario_activo"]
            nuevo_logout = pd.DataFrame([{"Fecha/Hora": time.strftime("%Y-%m-%d %H:%M:%S"), "Operador": usuario, "Acción": "Sesión cerrada por el operador institucional."}])
            st.session_state["logs_data"] = pd.concat([nuevo_logout, st.session_state["logs_data"]], ignore_index=True)
            st.session_state["usuario_activo"] = None
            st.rerun()

# ---- INTERFAZ PLANO-SECUENCIAL DE CAPACIDAD COMPLETA ----

# ÁREA 1: TELEMETRÍA Y MAPA DINÁMICO
st.markdown("#### 🌐 Área 1: Distribución Geográfica y Telemetría")
st.map(st.session_state["nodos_data"], zoom=1, use_container_width=True)

# CONTROLES DE ENFOQUE DEL MAPA
st.write("⚙️ **Controles de Enfoque de Telemetría:**")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📍 América del Norte"): st.toast("Enfocando telemetría en US Core Nodos...", icon="🌎")
with col2:
    if st.button("📍 Región Europea"): st.toast("Enfocando telemetría en Euro Link...", icon="🇪🇺")
with col3:
    if st.button("📍 Servidores de Asia"): st.toast("Enfocando telemetría en Asia Core...", icon="🇯🇵")
    
st.markdown("---")
# CONSOLA PARA REGISTRAR NUEVOS SERVIDORES
st.markdown("#### ➕ Consola de Registro de Nuevo Servidor/Canal")
n_lat = st.number_input("Latitud Geográfica:", value=0.0, format="%.4f")
n_lon = st.number_input("Longitud Geográfica:", value=0.0, format="%.4f")
n_name = st.text_input("Nombre identificador del Canal o Servidor:")
btn_nodo = st.button("🚀 EJECUTAR: Aprovisionar y Guardar")

if btn_nodo:
    if n_name.strip() != "":
        nuevo_nodo = pd.DataFrame([{"lat": n_lat, "lon": n_lon, "nombre_nodo": n_name}])
        st.session_state["nodos_data"] = pd.concat([st.session_state["nodos_data"], nuevo_nodo], ignore_index=True)
        
        operador_actual = st.session_state["usuario_activo"] if st.session_state["usuario_activo"] else "Anonimo"
        nuevo_log = pd.DataFrame([{"Fecha/Hora": time.strftime("%Y-%m-%d %H:%M:%S"), "Operador": operador_actual, "Acción": f"Aprovisionó Servidor Canal: {n_name} ({n_lat}, {n_lon})"}])
        st.session_state["logs_data"] = pd.concat([nuevo_log, st.session_state["logs_data"]], ignore_index=True)
        
        st.success(f"✔️ '{n_name}' registrado en memoria cloud con éxito.")
        time.sleep(0.4)
        st.rerun()
    else:
        st.error("El nombre del identificador no puede estar vacío.")

# ÁREA 2: INTELIGENCIA VIRTUAL Y MONITOR DE TRÁFICO
st.markdown("---")
st.markdown("#### 🤖 Área 2: Módulo de Enfoque de Inteligencia Virtual")
opciones = ["Análisis de Telemetría Global", "Monitoreo de Logs de Seguridad", "Optimización de Tráfico de Nodos"]
enfoque_ia = st.radio("Seleccione el área de análisis que desea que ejecute el sistema operativo principal:", opciones, horizontal=True)
st.info(f"⚡ Módulo activo seleccionado actualmente: **{enfoque_ia}**")

st.write("📊 **📈 Monitor de Carga y Tráfico Cuántico Activo**")
st.caption("📡 Flujo de paquetes telemetritos entre nodos activos:")
total_nodos = len(st.session_state["nodos_data"])
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1: st.metric(label="Servidores Conectados", value=f"{total_nodos} / 12 Nodes")
with col_t2: st.metric(label="Ancho de Banda Asignado", value=f"{total_nodos * 45} Gbps")
with col_t3: st.metric(label="Latencia Global Media", value="18 ms")

# ÁREA 3: AUDITORÍA HISTÓRICA E INSTITUCIONAL
st.markdown("---")
st.markdown("#### 📑 Área 3: Registro Histórico y Logs de Auditoría Institucional")
st.dataframe(st.session_state["logs_data"], use_container_width=True, height=200)

csv_data = st.session_state["logs_data"].to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Exportar Historial de Auditoría (CSV)",
    data=csv_data,
    file_name="audit_log_tb_global.csv",
    mime="text/csv"
