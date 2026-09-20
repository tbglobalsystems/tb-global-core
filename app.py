st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #030407; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    .logo-header {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        padding: 30px; border-radius: 8px; border: 1px solid #1e293b;
        border-bottom: 4px solid #0284c7; margin-bottom: 25px;
        text-align: center;
    }
    .logo-text { font-size: 42px; font-weight: 800; color: #ffffff; letter-spacing: 1px; margin: 0; }
    .logo-sub { font-size: 16px; color: #0284c7; font-weight: 600; letter-spacing: 4px; margin: 5px 0 0 0; }
</style>
""", unsafe_allow_html=True)

if "auth_rol" not in st.session_state: st.session_state["auth_rol"] = None
if "user_token" not in st.session_state: st.session_state["user_token"] = None
if "raw_pin" not in st.session_state: st.session_state["raw_pin"] = None
if "abrir_chat_soporte" not in st.session_state: st.session_state["abrir_chat_soporte"] = False

# Logo Corporativo
st.markdown("""
<div class='logo-header'>
    <h1 class='logo-text'>⚡ T&B Global</h1>
    <p class='logo-sub'>QUANTUM ENTERPRISE OPERATING SYSTEM</p>
</div>
""", unsafe_allow_html=True)

# LECTURA DEL ARCHIVO LOCAL (MÁXIMA SEGURIDAD CONTRA EL BLOQUEO DE SAFARI)
try:
    with open("mundo.html", "r", encoding="utf-8") as f:
        codigo_mundo = f.read()
    st.components.v1.html(codigo_mundo, height=410)
except Exception as e:
    st.error(f"Error cargando los sistemas de telecomunicaciones: {e}")
