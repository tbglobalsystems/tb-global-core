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
html_mundo_3d = """
    <div style="display: flex; justify-content: center; align-items: center; background: #030407; width: 100%; border-radius: 12px; overflow: hidden; padding: 10px 0;">
    <canvas id="canvasTelecom" width="380" height="380" style="background: transparent;"></canvas>
    <script>
        const canvas = document.getElementById('canvasTelecom');
        const ctx = canvas.getContext('2d');
        let rotacion = 0; let tiempo = 0;

        // Coordenadas fijas para simular bases receptoras en la Tierra
        const antenasMundiales = [
            {x: -40, y: -30}, {x: 50, y: -20},
            {x: -10, y: 40}, {x: 45, y: 35}
        ];

        function renderSistema() {
            ctx.clearRect(0, 0, 380, 380);
            ctx.save();
            ctx.translate(190, 190); // Centrar el dibujo en el canvas
            tiempo += 0.03;
            rotacion += 0.004;

            // 1. BRILLO ATMOSFÉRICO DE SEGURIDAD (Glow Neón)
            let gradAtmosfera = ctx.createRadialGradient(0, 0, 95, 0, 0, 140);
            gradAtmosfera.addColorStop(0, 'rgba(2, 132, 199, 0.3)');
            gradAtmosfera.addColorStop(0.6, 'rgba(2, 132, 199, 0.08)');
            gradAtmosfera.addColorStop(1, 'rgba(3, 4, 7, 0)');
            ctx.fillStyle = gradAtmosfera;
            ctx.beginPath(); ctx.arc(0, 0, 140, 0, Math.PI * 2); ctx.fill();

            // 2. CUERPO DEL OCÉANO PROFUNDO (Efecto Esférico)
            let gradOceano = ctx.createRadialGradient(-30, -30, 10, 0, 0, 105);
            gradOceano.addColorStop(0, '#0369a1');
            gradOceano.addColorStop(0.5, '#0f172a');
            gradOceano.addColorStop(1, '#020617');
            ctx.fillStyle = gradOceano;
            ctx.beginPath(); ctx.arc(0, 0, 105, 0, Math.PI * 2); ctx.fill();

            // 3. CONTINENTES EN ROTACIÓN CONTINUA (Relieve Geográfico)
            ctx.save();
            ctx.beginPath(); ctx.arc(0, 0, 105, 0, Math.PI * 2); ctx.clip(); // Limitar la tierra al círculo del planeta
            ctx.rotate(rotacion);
            ctx.fillStyle = 'rgba(16, 185, 129, 0.75)'; // Verde Esmeralda Corporativo
            
            // Dibujamos bloques continentales detallados
            const tierras = [
                [-50, -40, 35], [40, -50, 40], [-30, 40, 45], , [-70, 0, 20], [10, -10, 30]
            ];
            tierras.forEach(t => {
                ctx.beginPath(); ctx.arc(t[0], t[1], t[2], 0, Math.PI * 2); ctx.fill();
            });
            ctx.restore();

            // 4. CAPA DE SOMBRA MAPA REALISTA (Simulación 3D de Esfera)
            let gradSombra = ctx.createRadialGradient(20, 20, 70, 0, 0, 105);
            gradSombra.addColorStop(0, 'rgba(0,0,0,0)');
            gradSombra.addColorStop(0.8, 'rgba(2, 6, 23, 0.4)');
            gradSombra.addColorStop(1, 'rgba(2, 6, 23, 0.95)');
            ctx.fillStyle = gradSombra;
            ctx.beginPath(); ctx.arc(0, 0, 105, 0, Math.PI * 2); ctx.fill();

            // 5. SATÉLITE QUANTUM ALFA (Órbita externa con paneles solares)
            let orbitaA = tiempo * 0.4;
            let satAX = 145 * Math.cos(orbitaA);
            let satAY = 45 * Math.sin(orbitaA);
            ctx.save();
            ctx.rotate(Math.PI / 6); // Órbita inclinada
            ctx.fillStyle = '#f8fafc';
            ctx.beginPath(); ctx.arc(satAX, satAY, 4, 0, Math.PI * 2); ctx.fill(); // Núcleo
            ctx.fillStyle = '#0284c7'; // Paneles solares cian
            ctx.fillRect(satAX - 11, satAY - 1.5, 6, 3);
            ctx.fillRect(satAX + 5, satAY - 1.5, 6, 3);

            // Emisión de pulsos láser directo al núcleo terrestre
            if (Math.sin(tiempo * 2.5) > 0) {
                ctx.strokeStyle = 'rgba(56, 189, 248, 0.6)';
                ctx.lineWidth = 1;
                ctx.beginPath(); ctx.moveTo(satAX, satAY); ctx.lineTo(0, 0); ctx.stroke();
            }
            ctx.restore();

            // 6. SATÉLITE QUANTUM BETA Y ENLACE DE RED CON ANTENAS
            let orbitaB = -tiempo * 0.3;
            let satBX = 155 * Math.cos(orbitaB);
            let satBY = 35 * Math.sin(orbitaB);
            ctx.save();
            ctx.rotate(-Math.PI / 8); // Órbita inversa inclinada
            ctx.fillStyle = '#f1f5f9';
            ctx.beginPath(); ctx.arc(satBX, satBY, 4, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#10b981'; // Paneles solares verdes
            ctx.fillRect(satBX - 10, satBY - 1, 5, 2);
            ctx.fillRect(satBX + 5, satBY - 1, 5, 2);

            // Transmisión inalámbrica de señales dinámicas a puntos terrestres
            antenasMundiales.forEach(ant => {
                if (Math.sin(tiempo + ant.x) > 0.1) {
                    ctx.strokeStyle = 'rgba(16, 185, 129, 0.45)';
                    ctx.lineWidth = 1.2;
                    ctx.beginPath(); ctx.moveTo(satBX, satBY); ctx.lineTo(ant.x, ant.y); ctx.stroke();
                    
                    ctx.fillStyle = '#ffffff';
                    ctx.beginPath(); ctx.arc(ant.x, ant.y, 2.5, 0, Math.PI * 2); ctx.fill();
                }
            });
            ctx.restore();

            ctx.restore();
            requestAnimationFrame(renderSistema);
        }
        renderSistema();
    </script>
    </div>
    """ 
