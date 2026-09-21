import streamlit as st
import os
import pandas as pd
import time
from deep_translator import GoogleTranslator

# 1. CONFIGURACIÓN CORPORATIVA GLOBAL
st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Diccionario completo de idiomas disponibles en el mundo
IDIOMAS_DISPONIBLES = {
    "Español": "es",
    "English": "en",
    "Português": "pt",
    "Français": "fr",
    "Deutsch": "de",
    "中文 (Chino)": "zh-CN",
    "日本語 (Japonés)": "ja",
    "Italiano": "it",
    "Русский (Ruso)": "ru",
    "العربية (Árabe)": "ar"
}

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

# Estado para controlar el idioma activo mediante botones o selector
if "idioma_codigo" not in st.session_state:
    st.session_state["idioma_codigo"] = "es"
if "idioma_nombre" not in st.session_state:
    st.session_state["idioma_nombre"] = "Español"

# 2. INYECCIÓN DE ESTILOS PREMIUM CORPORATIVOS
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

# Función Máquina para Traducir Texto Dinámicamente en Pantalla
def T(texto):
    if st.session_state["idioma_codigo"] == "es":
        return texto
    try:
        return GoogleTranslator(source='es', target=st.session_state["idioma_codigo"]).translate(texto)
    except Exception:
        return texto

# PANEL DE CONTROL DE ENTRADA: BOTONES DE IDIOMAS CLAVE (MUNDIAL/INDUSTRIA)
st.write("🌍 **Quick Access / Idiomas Clave de la Industria:**")
col_lang1, col_lang2, col_lang3, col_lang4 = st.columns(4)
with col_lang1:
    if st.button("🇺🇸 English (US Core)"):
        st.session_state["idioma_codigo"] = "en"
        st.session_state["idioma_nombre"] = "English"
        st.rerun()
with col_lang2:
    if st.button("🇪🇸 Español (Global)"):
        st.session_state["idioma_codigo"] = "es"
        st.session_state["idioma_nombre"] = "Español"
        st.rerun()
with col_lang3:
    if st.button("🇧🇷 Português (BR)"):
        st.session_state["idioma_codigo"] = "pt"
        st.session_state["idioma_nombre"] = "Português"
        st.rerun()
with col_lang4:
    if st.button("🇨🇳 中文 (China Tech)"):
        st.session_state["idioma_codigo"] = "zh-CN"
        st.session_state["idioma_nombre"] = "中文 (Chino)"
        st.rerun()

# ENCABEZADO CORPORATIVO DINÁMICO
st.markdown(f"""
<div class="brand-container">
    <h1 class="brand-title">⚡ T&B Global</h1>
    <p class="brand-subtitle">{T("QUANTUM ENTERPRISE OPERATING SYSTEM")}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"### 📊 {T('Consola de Comando de Servicios Integrados')}")

# Selector secundario en barra lateral para el RESTO del mundo
with st.sidebar:
    st.markdown(f"### 🌐 {T('Traductor Avanzado')}")
    # Enlazar el selector al estado global
    lista_nombres = list(IDIOMAS_DISPONIBLES.keys())
    indice_actual = lista_nombres.index(st.session_state["idioma_nombre"]) if st.session_state["idioma_nombre"] in lista_nombres else 0
    
    idioma_avanzado = st.selectbox(T("Todos los Idiomas:"), lista_nombres, index=indice_actual)
    if IDIOMAS_DISPONIBLES[idioma_avanzado] != st.session_state["idioma_codigo"]:
        st.session_state["idioma_codigo"] = IDIOMAS_DISPONIBLES[idioma_avanzado]
        st.session_state["idioma_nombre"] = idioma_avanzado
        st.rerun()

# 3. BARRA LATERAL DE CONTROL DE ACCESO
if st.session_state["usuario_activo"] is None:
    st.warning(T("🔒 El sistema operativo se encuentra bloqueado. Inicie sesión en la barra lateral."))
    with st.sidebar:
        st.markdown(f"### 🔐 {T('Acceso Centralizado')}")
        u = st.text_input(f"{T('ID de Usuario Operador')}:")
        p = st.text_input(f"{T('PIN de Seguridad (4 dígitos)')}:", type="password", max_chars=4)
        if st.button(T("Validar Credenciales")):
            if u and p:
                st.session_state["usuario_activo"] = u
                st.rerun()
else:
    with st.sidebar:
        st.success(f"{T('Operador en Línea')}: {st.session_state['usuario_activo']}")
        if st.button(T("🔒 Cerrar Sesión")):
            st.session_state["usuario_activo"] = None
            st.rerun()

    # 4. TELEMETRÍA Y DISTRIBUCIÓN GEOGRÁFICA
    st.markdown(f"#### 🌐 {T('Área 1: Distribución Geográfica y Telemetría')}")
    st.map(st.session_state["nodos_locales"], zoom=1, use_container_width=True)
    
    st.write(f"⚙️ **{T('Controles de Enfoque de Telemetría')}:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(T("📍 Centrar en América del Norte")):
            st.toast(T("Enfocando telemetría en US Core Nodos..."), icon="🌎")
    with col2:
        if st.button("📍 Centrar en Región Europea"):
            st.toast(T("Enfocando telemetría en Euro Link..."), icon="🇪🇺")
    with col3:
        if st.button(T("📍 Centrar en Servidores de Asia")):
            st.toast(T("Enfocando telemetría en Asia Core..."), icon="🇯🇵")

    # 5. FORMULARIO PARA REGISTRAR NUEVOS SERVIDORES
    st.markdown("---")
    with st.expander(f"➕ {T('Abrir Consola para Registrar Nuevo Servidor/Canal')}", expanded=False):
        with st.form("nuevo_nodo_form"):
            n_lat = st.number_input(f"{T('Latitud Geográfica')}:", value=0.0, format="%.4f")
            n_lon = st.number_input(f"{T('Longitud Geográfica')}:", value=0.0, format="%.4f")
            n_name = st.text_input(f"{T('Nombre identificador del Canal o Servidor')}:")
            btn_nodo = st.form_submit_button(T("🚀 EJECUTAR: Aprovisionar y Guardar"))
            
            if btn_nodo:
                if n_name.strip() != "":
                    nuevo_registro = pd.DataFrame([{"lat": n_lat, "lon": n_lon, "nombre_nodo": n_name}])
                    st.session_state["nodos_locales"] = pd.concat([st.session_state["nodos_locales"], nuevo_registro], ignore_index=True)
                    
                    nuevo_log = pd.DataFrame([{"Fecha/Hora": time.strftime("%Y-%m-%d %H:%M:%S"), "Operador": st.session_state["usuario_activo"], "Acción Ejecutada": f"Inyectó nodo: {n_name}"}])
                    st.session_state["bitacora_logs"] = pd.concat([nuevo_log, st.session_state["bitacora_logs"]], ignore_index=True)
                    
                    st.success(T(f"Servidor '{n_name}' registrado en memoria cloud con éxito."))
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(T("El nombre del identificador no puede estar vacío."))

    # 6. ENFOQUE DE INTELIGENCIA VIRTUAL
    st.markdown("---")
    st.markdown(f"#### 🤖 {T('Área 2: Módulo de Enfoque de Inteligencia Virtual')}")
    enfoque_ia = st.radio(
        T("Seleccione el área de análisis que desea que ejecute el sistema operativo principal:"),
        [T("Análisis de Telemetría Global"), T("Monitoreo de Logs de Seguridad"), T("Optimización de Tráfico de Nodos")]
    )
    st.info(f"{T('Módulo activo seleccionado actualmente')}: **{enfoque_ia}**")

    # 7. MONITOR DE CARGA Y TRÁFICO CUÁNTICO
    st.markdown("---")
    with st.expander(f"📈 {T('Visualizar Monitor de Carga y Tráfico Cuántico')}", expanded=True):
        st.write(f"📡 **{T('Flujo de paquetes telemetritos entre nodos activos')}:**")
        total_nodos = len(st.session_state["nodos_locales"])
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            st.metric(label=T("Servidores Conectados"), value=f"{total_nodos} / 12")
        with col_t2:
            st.metric(label=T("Ancho de Banda Asignado"), value=f"{total_nodos * 45} Gbps", delta="+15%")
        with col_t3:
            st.metric(label=T("Latencia Global Media"), value="18 ms", delta="-4 ms")
        
        valores_peticiones = [120, 240, 310]
        while len(valores_peticiones) < total_nodos:
            valores_peticiones.append(150)
            
        chart_data = pd.DataFrame({
            T('Nodos Operativos'): st.session_state["nodos_locales"]["nombre_nodo"],
            T('Peticiones/Min'): valores_peticiones[:total_nodos]
        })
        st.bar_chart(chart_data, x=T('Nodos Operativos'), y=T('Peticiones/Min'))

    # 8. PANEL DE AUDITORÍA HISTÓRICA CON BOTÓN DE DESCARGA
    st.markdown("---")
    st.markdown(f"#### 📑 {T('Área 3: Registro Histórico y Logs de Auditoría Institucional')}")
    
    df_logs_vista = st.session_state["bitacora_logs"].copy()
    df_logs_vista.columns = [T("Fecha/Hora"), T("Operador"), T("Acción Ejecutada")]
    st.dataframe(df_logs_vista, use_container_width=True)
    
