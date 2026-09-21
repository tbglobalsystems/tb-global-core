import streamlit as st
import os
import psycopg2
import pandas as pd
import time

# 1. CONFIGURACIÓN CORPORATIVA DE ALTA GAMA
st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INYECCIÓN DE ESTILOS PREMIUM
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
    .brand-title {
        font-size: 40px !important;
        font-weight: 800 !important;
        color: #38bdf8 !important;
        margin: 0 !important;
    }
    .brand-subtitle {
        font-size: 13px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        letter-spacing: 5px !important;
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

# Inicializar estados de la sesión de forma segura
if "usuario_activo" not in st.session_state:
    st.session_state["usuario_activo"] = None

if "nodos_locales" not in st.session_state:
    st.session_state["nodos_locales"] = pd.DataFrame([
        {"lat": 40.7128, "lon": -74.0060, "nombre_nodo": "Nodo Central US"},
        {"lat": 34.0522, "lon": -118.2437, "nombre_nodo": "Nodo Pacifico US"},
        {"lat": 51.5074, "lon": -0.1278, "nombre_nodo": "Nodo Euro Core"}
    ])

if "bitacora_logs" not in st.session_state:
    st.session_state["bitacora_logs"] = pd.DataFrame([
        {"Fecha/Hora": time.strftime("%Y-%m-%d %H:%M:%S"), "Operador": "Sistema", "Acción Ejecutada": "Infraestructura Quantum inicializada con éxito."}
    ])

st.markdown("""
<div class="brand-container">
    <h1 class="brand-title">⚡ T&B Global</h1>
    <p class="brand-subtitle">QUANTUM ENTERPRISE OPERATING SYSTEM</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Consola de Comando de Servicios Integrados")

# 3. BARRA LATERAL DE CONTROL DE ACCESO
if st.session_state["usuario_activo"] is None:
    st.warning("🔒 El sistema operativo se encuentra bloqueado. Inicie sesión en la barra lateral.")
    with st.sidebar:
        st.markdown("### 🔐 Acceso Centralizado")
        u = st.text_input("ID de Usuario Operador:")
        p = st.text_input("PIN de Seguridad (4 dígitos):", type="password", max_chars=4)
        if st.button("Validar Credenciales"):
            if u and p:
                st.session_state["usuario_activo"] = u
                st.rerun()
else:
    with st.sidebar:
        st.success(f"Operador en Línea: {st.session_state['usuario_activo']}")
        if st.button("🔒 Cerrar Sesión"):
            st.session_state["usuario_activo"] = None
            st.rerun()

    # 4. TELEMETRÍA Y DISTRIBUCIÓN GEOGRÁFICA
    st.markdown("#### 🌐 Área 1: Distribución Geográfica y Telemetría")
    st.map(st.session_state["nodos_locales"], zoom=1, use_container_width=True)
    
    st.write("⚙️ **Controles de Enfoque de Telemetría:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📍 Centrar en América del Norte"):
            st.toast("Enfocando telemetría en US Core Nodos...", icon="🌎")
    with col2:
        if st.button("📍 Centrar en Región Europea"):
            st.toast("Enfocando telemetría en Euro Link...", icon="🇪🇺")
    with col3:
        if st.button("📍 Centrar en Servidores de Asia"):
            st.toast("Enfocando telemetría en Asia Core...", icon="🇯🇵")

    # 5. FORMULARIO PARA REGISTRAR NUEVOS SERVIDORES
    st.markdown("---")
    with st.expander("➕ Abrir Consola para Registrar Nuevo Servidor/Canal", expanded=False):
        with st.form("nuevo_nodo_form"):
            n_lat = st.number_input("Latitud Geográfica:", value=0.0, format="%.4f")
            n_lon = st.number_input("Longitud Geográfica:", value=0.0, format="%.4f")
            n_name = st.text_input("Nombre identificador del Canal o Servidor:")
            btn_nodo = st.form_submit_button("🚀 EJECUTAR: Aprovisionar y Guardar")
            
            if btn_nodo:
                if n_name.strip() != "":
                    # Insertar nuevo nodo al mapa
                    nuevo_registro = pd.DataFrame([{"lat": n_lat, "lon": n_lon, "nombre_nodo": n_name}])
                    st.session_state["nodos_locales"] = pd.concat([st.session_state["nodos_locales"], nuevo_registro], ignore_index=True)
                    
                    # Registrar la acción en la bitácora de auditoría
                    nuevo_log = pd.DataFrame([{"Fecha/Hora": time.strftime("%Y-%m-%d %H:%M:%S"), "Operador": st.session_state["usuario_activo"], "Acción Ejecutada": f"Inyectó nodo: {n_name}"}])
                    st.session_state["bitacora_logs"] = pd.concat([nuevo_log, st.session_state["bitacora_logs"]], ignore_index=True)
                    
                    st.success(f"Servidor '{n_name}' registrado en memoria cloud con éxito.")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("El nombre del identificador no puede estar vacío.")

    # 6. ENFOQUE DE INTELIGENCIA VIRTUAL
    st.markdown("---")
    st.markdown("#### 🤖 Área 2: Módulo de Enfoque de Inteligencia Virtual")
    enfoque_ia = st.radio(
        "Seleccione el área de análisis que desea que ejecute el sistema operativo principal:",
        ["Análisis de Telemetría Global", "Monitoreo de Logs de Seguridad", "Optimización de Tráfico de Nodos"]
    )
    st.info(f"Módulo activo seleccionado actualmente: **{enfoque_ia}**")

    # NUEVO MÓDULO: SIMULACIÓN EN TIEMPO REAL DE TRÁFICO DE DATOS
    with st.expander("📈 Visualizar Monitor de Carga y Tráfico Cuántico", expanded=True):
        st.write("📡 **Flujo de paquetes telemetritos entre nodos activos:**")
        # Generar métricas dinámicas basadas en los nodos inyectados
        total_nodos = len(st.session_state["nodos_locales"])
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            st.metric(label="Servidores Conectados", value=f"{total_nodos} / 12")
        with col_t2:
            st.metric(label="Ancho de Banda Asignado", value=f"{total_nodos * 45} Gbps", delta="+15% optimizado")
        with col_t3:
            st.metric(label="Latencia Global Media", value="18 ms", delta="-4 ms eficiente")
        
        # Simulación de tráfico en gráfico nativo
        chart_data = pd.DataFrame({
            'Nodos Operativos': st.session_state["nodos_locales"]["nombre_nodo"],
            'Peticiones/Min': [120, 240, 310] + [150] * (total_nodos - 3)
        })
        st.bar_chart(chart_data, x='Nodos Operativos', y='Peticiones/Min')

    # 7. PANEL DE AUDITORÍA HISTÓRICA CON BOTÓN DE DESCARGA EXCEL NATIVO
    st.markdown("---")
    st.markdown("#### 📑 Área 3: Registro Histórico y Logs de Auditoría Institucional")
    st.dataframe(st.session_state["bitacora_logs"], use_container_width=True)
    
    # Conversión nativa a CSV para el botón de descarga rápida empresarial
    csv_data = st.session_state["bitacora_logs"].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Exportar Historial de Auditoría Corporativa (CSV)",
        data=csv_data,
        file_name=f"log_auditoria_{time.strftime('%Y%md_%H%M%S')}.csv",
