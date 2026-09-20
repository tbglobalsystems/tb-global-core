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

# =======================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =======================================================================
st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos visuales del sistema
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

# Variables de control del sistema de seguridad
if "auth_rol" not in st.session_state: st.session_state["auth_rol"] = None
if "user_token" not in st.session_state: st.session_state["user_token"] = None
if "raw_pin" not in st.session_state: st.session_state["raw_pin"] = None
if "abrir_chat_soporte" not in st.session_state: st.session_state["abrir_chat_soporte"] = False

# =======================================================================
# ENCABEZADO COMERCIAL (LOGO T&B GLOBAL)
# =======================================================================
st.markdown("""
<div class='logo-header'>
    <h1 class='logo-text'>⚡ T&B Global</h1>
    <p class='logo-sub'>QUANTUM ENTERPRISE OPERATING SYSTEM</p>
</div>
""", unsafe_allow_html=True)

# =======================================================================
# MUNDO TERRÁQUEO CON SATÉLITES EMITIENDO SEÑALES
# =======================================================================
html_mundo_3d = """
<div style="display: flex; justify-content: center; align-items: center; background: #030407; width: 100%; border-radius: 12px; overflow: hidden; padding: 20px 0;">
    <canvas id="canvasTelecom" width="380" height="380" style="background: transparent;"></canvas>
</div>
<script>
    const canvas = document.getElementById('canvasTelecom');
    const ctx = canvas.getContext('2d');
    let rotacion = 0; let tiempo = 0;

    const antenasMundiales = [
        {x: -40, y: -30}, {x: 50, y: -20},
        {x: -10, y: 40}, {x: 45, y: 35}
    ];

    function renderSistema() {
        ctx.clearRect(0, 0, 380, 380);
        ctx.save();
        ctx.translate(190, 190);
        tiempo += 0.03;
        rotacion += 0.004;

        // Atmósfera (Brillo Azul)
        let gradAtmosfera = ctx.createRadialGradient(0, 0, 95, 0, 0, 140);
        gradAtmosfera.addColorStop(0, 'rgba(2, 132, 199, 0.3)');
        gradAtmosfera.addColorStop(0.6, 'rgba(2, 132, 199, 0.08)');
        gradAtmosfera.addColorStop(1, 'rgba(3, 4, 7, 0)');
        ctx.fillStyle = gradAtmosfera; ctx.beginPath(); ctx.arc(0, 0, 140, 0, Math.PI * 2); ctx.fill();

        // Océano Esférico
        let gradOceano = ctx.createRadialGradient(-30, -30, 10, 0, 0, 105);
        gradOceano.addColorStop(0, '#0369a1'); gradOceano.addColorStop(0.5, '#0f172a'); gradOceano.addColorStop(1, '#020617');
        ctx.fillStyle = gradOceano; ctx.beginPath(); ctx.arc(0, 0, 105, 0, Math.PI * 2); ctx.fill();

        // Continentes en movimiento
        ctx.save();
        ctx.beginPath(); ctx.arc(0, 0, 105, 0, Math.PI * 2); ctx.clip();
        ctx.rotate(rotacion);
        ctx.fillStyle = 'rgba(16, 185, 129, 0.75)';
        const tierras = [[-50, -40, 35], [40, -50, 40], [-30, 40, 45], [-70, 0, 20], [10, -10, 30]];
        tierras.forEach(t => { ctx.beginPath(); ctx.arc(t[0], t[1], t[2], 0, Math.PI * 2); ctx.fill(); });
        ctx.restore();

        // Sombra de planeta 3D
        let gradSombra = ctx.createRadialGradient(20, 20, 70, 0, 0, 105);
        gradSombra.addColorStop(0, 'rgba(0,0,0,0)'); gradSombra.addColorStop(0.8, 'rgba(2, 6, 23, 0.4)'); gradSombra.addColorStop(1, 'rgba(2, 6, 23, 0.95)');
        ctx.fillStyle = gradSombra; ctx.beginPath(); ctx.arc(0, 0, 105, 0, Math.PI * 2); ctx.fill();

        // Satélite Alfa (Emisión Central)
        let orbitaA = tiempo * 0.4;
        let satAX = 145 * Math.cos(orbitaA); let satAY = 45 * Math.sin(orbitaA);
        ctx.save(); ctx.rotate(Math.PI / 6);
        ctx.fillStyle = '#f8fafc'; ctx.beginPath(); ctx.arc(satAX, satAY, 4, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#0284c7'; ctx.fillRect(satAX - 11, satAY - 1.5, 6, 3); ctx.fillRect(satAX + 5, satAY - 1.5, 6, 3);
        if (Math.sin(tiempo * 2.5) > 0) {
            ctx.strokeStyle = 'rgba(56, 189, 248, 0.6)'; ctx.lineWidth = 1;
            ctx.beginPath(); ctx.moveTo(satAX, satAY); ctx.lineTo(0, 0); ctx.stroke();
        }
        ctx.restore();

        // Satélite Beta y Antenas Globales
        let orbitaB = -tiempo * 0.3;
        let satBX = 155 * Math.cos(orbitaB); let satBY = 35 * Math.sin(orbitaB);
        ctx.save(); ctx.rotate(-Math.PI / 8);
        ctx.fillStyle = '#f1f5f9'; ctx.beginPath(); ctx.arc(satBX, satBY, 4, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#10b981'; ctx.fillRect(satBX - 10, satBY - 1, 5, 2); ctx.fillRect(satBX + 5, satBY - 1, 5, 2);

        antenasMundiales.forEach(ant => {
            if (Math.sin(tiempo + ant.x) > 0.1) {
                ctx.strokeStyle = 'rgba(16, 185, 129, 0.45)'; ctx.lineWidth = 1.2;
                ctx.beginPath(); ctx.moveTo(satBX, satBY); ctx.lineTo(ant.x, ant.y); ctx.stroke();
                ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(ant.x, ant.y, 2.5, 0, Math.PI * 2); ctx.fill();
            }
        });
        ctx.restore();

        ctx.restore();
        requestAnimationFrame(renderSistema);
    }
    renderSistema();
</script>
"""

