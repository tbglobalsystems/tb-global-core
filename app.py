import streamlit as st
import os
import time
import secrets
import hashlib
import sqlite3
import pandas as pd
import mimetypes
import re
from PIL import Image
from cryptography.fernet import Fernet
from crewai import Agent, Task, Crew
import stripe

# =====================================================================
# 🔐 BLUEPRINT INDUSTRIAL TRIPLICADO LEGAL: T&B GLOBAL PLATFORM V500
# =====================================================================
st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Premium de Grado SaaS Internacional (Zero-Trust UI Blindada)
st.markdown("""
    <style>
    .main { background-color: #030407; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    .stButton>button {
        background: linear-gradient(135deg, #0284c7, #0369a1);
        color: white; border: none; border-radius: 6px;
        padding: 12px 28px; font-weight: 700; font-size: 14px;
        transition: all 0.2s ease; box-shadow: 0 4px 12px rgba(2,132,199,0.3);
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(2,132,199,0.5); }
    .logo-header {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        padding: 30px; border-radius: 8px; border: 1px solid #1e293b;
        border-left: 5px solid #0284c7; margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .logo-text { font-size: 32px; font-weight: 800; color: #ffffff; letter-spacing: 1px; margin: 0; }
    .logo-sub { font-size: 14px; color: #0284c7; font-weight: 600; letter-spacing: 2px; margin: 5px 0 0 0; text-transform: uppercase; }
    .vault-banner { background: linear-gradient(135deg, #020617 0%, #0f172a 100%); padding: 24px; border-radius: 8px; border: 1px solid #1e293b; border-left: 4px solid #38bdf8; margin-bottom: 20px; }
    .folder-box { background-color: #0f172a; padding: 15px; border-radius: 6px; border: 1px solid #1e293b; margin-bottom: 10px; }
    .card-premium { background: linear-gradient(135deg, #0f172a 0%, #020617 100%); padding: 24px; border-radius: 8px; border: 1px solid #1e293b; margin-bottom: 20px; }
    .card-finanzas { background: linear-gradient(135deg, #0c1e2f 0%, #030407 100%); padding: 24px; border-radius: 8px; border-left: 4px solid #38bdf8; margin-bottom: 20px; }
    .card-creativo { background: linear-gradient(135deg, #2e1065 0%, #030407 100%); padding: 24px; border-radius: 8px; border-left: 4px solid #c084fc; margin-bottom: 20px; }
    .card-ingenieria { background: linear-gradient(135deg, #1e293b 0%, #030407 100%); padding: 24px; border-radius: 8px; border-left: 4px solid #f59e0b; margin-bottom: 20px; }
    .policy-box { background-color: #0f172a; padding: 20px; border-radius: 6px; border: 1px solid #334155; height: 220px; overflow-y: scroll; margin-bottom: 15px; font-size: 13px; color: #94a3b8; line-height: 1.6; }
    </style>
""", unsafe_allow_html=True)

# ─── CARGA SEGURA DE VARIABLES OCULTAS EN LA NUBE ───
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PRICE_MENSUAL = os.getenv("STRIPE_PRICE_MENSUAL_ID","")
STRIPE_PRICE_ANUAL = os.getenv("STRIPE_PRICE_ANUAL_ID","")

HASH_MAESTRO_PRODUCCION = "d57924d5ff1a052ff39912cd311910efc1fc86a42ec34c11b0bb7a7c8bc7f2e1"
HASH_SOCIO_PRODUCCION = "7ef5927c3da33457a4d5b2c7e09cd4b46c21e05d9fcba128a3bb8b874fa72b4f"

NUCLEO_CRYPT_KEY = os.getenv("SERVER_FERNET_KEY", Fernet.generate_key().decode())
fernet_servidor = Fernet(NUCLEO_CRYPT_KEY.encode())

DATA_DIR = "/data" if os.path.exists("/data") else "."
VAULT_ROOT = os.path.join(DATA_DIR, "secure_vaults")
KYC_DIR = os.path.join(DATA_DIR, "identificaciones_kyc")
MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  
EXTENSIONES_PROHIBIDAS = [".exe", ".bat", ".sh", ".cmd", ".msi", ".vbs", ".scr", ".com", ".php", ".phtml", ".js"]

for d in [VAULT_ROOT, KYC_DIR]:
    if not os.path.exists(d): os.makedirs(d)

def obtener_conexion_db():
    url_postgres = os.getenv("DATABASE_URL")
    if url_postgres:
        import psycopg2
        return psycopg2.connect(url_postgres, timeout=30)
    else:
        return sqlite3.connect(os.path.join(DATA_DIR, "quantum_matrix.db"), timeout=30.0)

def ejecutar_consulta_db(query, params=(), fetch=False, commit=False):
    if os.getenv("DATABASE_URL") is None:
        query = query.replace("%s", "?")
    else:
        query = query.replace("?", "%s")
    conn = obtener_conexion_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        if commit: conn.commit()
        if fetch: return cursor.fetchall()
    except Exception as e:
        st.error(f"Error de consistencia en el clúster de datos protegido: {e}")
    finally:
        conn.close()

def init_production_db():
    ejecutar_consulta_db("""
        CREATE TABLE IF NOT EXISTS usuarios (
            token TEXT PRIMARY KEY, nombre_enc TEXT, apellido_enc TEXT, email_enc TEXT, 
            fecha_nacimiento_enc TEXT, pais_enc TEXT, telefono_enc TEXT, direccion_enc TEXT, 
            pin TEXT, plan TEXT, estado TEXT, tareas_max INTEGER, usadas INTEGER,
            firma_legal TEXT, fecha_firma TEXT, ruta_id_frontal TEXT, ruta_id_reversa TEXT,
            infracciones INTEGER DEFAULT 0
        )
    """, commit=True)
    ejecutar_consulta_db("CREATE TABLE IF NOT EXISTS workspaces (workspace_id TEXT PRIMARY KEY, token_cliente TEXT, nombre TEXT, campo TEXT, descripcion TEXT)", commit=True)
    ejecutar_consulta_db("CREATE TABLE IF NOT EXISTS archivos_vault (archivo_id TEXT PRIMARY KEY, token_cliente TEXT, workspace_id TEXT, filename TEXT, enc_key TEXT)", commit=True)
    ejecutar_consulta_db("CREATE TABLE IF NOT EXISTS trabajadores (worker_token TEXT PRIMARY KEY, nombre TEXT, rol TEXT, estado TEXT)", commit=True)
    ejecutar_consulta_db("CREATE TABLE IF NOT EXISTS tickets (ticket_id TEXT PRIMARY KEY, token_cliente TEXT, inconveniente TEXT, estado TEXT, resolucion_ia TEXT, requiere_humano TEXT)", commit=True)

init_production_db()

def encrypter(texto): 
    primer_paso = hashlib.sha256(texto.encode()).hexdigest()
    return hashlib.sha256((primer_paso + "T&B_SALT_2026").encode()).hexdigest()

def cifrar_dato(texto): return fernet_servidor.encrypt(texto.encode()).decode()
def descifrar_dato(texto_cifrado): return fernet_servidor.decrypt(texto_cifrado.encode()).decode()

def obtener_fernet_key(pin_usuario, user_token):
    hash_base = hashlib.sha256((pin_usuario + user_token + "CAPA_TRIPLICADA").encode()).digest()
    return Fernet(hashlib.sha256(hash_base).hexdigest()[:32].encode('utf-8').zfill(32).replace(b'0', b'A'))

def sanitizar_entrada(texto):
    if not texto: return ""
    texto_limpio = re.sub(r'<[^>]*>', '', texto)
    return re.sub(r'[^a-zA-Z0-9\s@._,-]', '', texto_limpio)

if "auth_rol" not in st.session_state: st.session_state["auth_rol"] = None
if "user_token" not in st.session_state: st.session_state["user_token"] = None
if "raw_pin" not in st.session_state: st.session_state["raw_pin"] = None
if "abrir_chat_soporte" not in st.session_state: st.markdown("""
<div class='logo-header' style='text-align: center; border-left: none; border-bottom: 4px solid #0284c7; padding: 15px;'>
    <h1 class='logo-text' style='font-size: 42px;'>⚡ T&B Global</h1>
    <p class='logo-sub' style='font-size: 16px; letter-spacing: 4px;'>QUANTUM ENTERPRISE OPERATING SYSTEM</p>
</div>
""", unsafe_allow_html=True)

col_izq, col_centro, col_der = st.columns([0.5, 2, 0.5])
with col_centro:
    html_mundo_3d = """
    <div style="display: flex; justify-content: center; align-items: center; background: #030407; width: 100%; border-radius: 12px; overflow: hidden;">
    <script src="https://cloudflare.com"></script>
    <div id="globe3d-container" style="width: 100%; height: 410px; position: relative;"></div>
    <script>
        const container = document.getElementById('globe3d-container');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / 410, 0.1, 1000);
        camera.position.z = 250;
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(container.clientWidth, 410);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);
        
        const ambientLight = new THREE.AmbientLight(0x444444); scene.add(ambientLight);
        const sunLight = new THREE.DirectionalLight(0xffffff, 1.5); sunLight.position.set(5, 3, 5).normalize(); scene.add(sunLight);

        const textureCanvas = document.createElement('canvas'); textureCanvas.width = 2048; textureCanvas.height = 1024;
        const tCtx = textureCanvas.getContext('2d');
        tCtx.fillStyle = '#0b132b'; tCtx.fillRect(0, 0, 2048, 1024);
        tCtx.fillStyle = '#1c7c54';
        for(let i=0; i<400; i++) {
            let x = Math.random() * 2048; let y = 150 + Math.random() * 724; let r = 30 + Math.random() * 100;
            tCtx.beginPath(); tCtx.arc(x, y, r, 0, Math.PI*2); tCtx.fill();
        }

        const earthTexture = new THREE.CanvasTexture(textureCanvas);
        const earthGeo = new THREE.SphereGeometry(75, 64, 64);
        const earthMat = new THREE.MeshStandardMaterial({ map: earthTexture, roughness: 0.6, metalness: 0.1 });
        const earth = new THREE.Mesh(earthGeo, earthMat); scene.add(earth);

        const atmosGeo = new THREE.SphereGeometry(77, 64, 64);
        const atmosMat = new THREE.MeshBasicMaterial({ color: 0x0284c7, transparent: true, opacity: 0.15, blending: THREE.AdditiveBlending, side: THREE.BackSide });
        const atmosphere = new THREE.Mesh(atmosGeo, atmosMat); scene.add(atmosphere);

        const satellites = [];
        function crearSatelite(radio, velocidad, color, inc) {
            const group = new THREE.Group();
            const body = new THREE.Mesh(new THREE.BoxGeometry(3, 3, 4), new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.8 })); group.add(body);
            const panel = new THREE.Mesh(new THREE.BoxGeometry(12, 2, 0.5), new THREE.MeshStandardMaterial({ color: color, emissive: color, emissiveIntensity: 0.4 })); group.add(panel);
            scene.add(group); satellites.push({ mesh: group, radius: radio, angle: Math.random()*10, speed: velocidad, color: color, inc: inc });
        }
        crearSatelite(115, 0.012, 0x00ffcc, Math.PI / 6);
        crearSatelite(135, -0.009, 0x10b981, -Math.PI / 8);

        let lineasSenal = []; let clock = 0;
        function animate() {
            requestAnimationFrame(animate); clock += 0.03; earth.rotation.y += 0.0015;
            lineasSenal.forEach(l => scene.remove(l)); lineasSenal = [];

            satellites.forEach(sat => {
                sat.angle += sat.speed;
                sat.mesh.position.x = sat.radius * Math.cos(sat.angle);
                sat.mesh.position.y = (sat.radius * Math.sin(sat.angle)) * Math.sin(sat.inc);
                sat.mesh.position.z = sat.radius * Math.sin(sat.angle) * Math.cos(sat.inc);
                sat.mesh.lookAt(earth.position);

                if (Math.sin(clock * 2 + sat.radius) > 0.2) {
                    const puntos = [sat.mesh.position.clone(), new THREE.Vector3((Math.random()-0.5)*40, (Math.random()-0.5)*40, (Math.random()-0.5)*40)];
                    const linea = new THREE.Line(new THREE.BufferGeometry().setFromPoints(puntos), new THREE.LineBasicMaterial({ color: sat.color, transparent: true, opacity: 0.5 }));
                    scene.add(linea); lineasSenal.push(linea);
                }
            });
            renderer.render(scene, camera);
        }
        animate();
        window.addEventListener('resize', () => { camera.aspect = container.clientWidth / 410; camera.updateProjectionMatrix(); renderer.setSize(container.clientWidth, 410); });
    </script>
    </div>
    """
    st.components.v1.html(html_mundo_3d, height=410)
