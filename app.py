import streamlit as st
import os
import pandas as pd
import time

# 1. CONFIGURACIÓN CORPORATIVA GLOBAL DE ALTA GAMA
st.set_page_config(
    page_title="T&B Global - Enterprise OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# INFRAESTRUCTURA DE IDIOMAS DE LA INDUSTRIA (Módulo de Recursos Estructurado)
IDIOMAS_SOPORTADOS = {
    "es": {
        "name": "Español",
        "data": {
            "title": "QUANTUM ENTERPRISE OPERATING SYSTEM",
            "subtitle": "Consola de Comando de Servicios Integrados",
            "lock": "🔒 El sistema operativo se encuentra bloqueado. Inicie sesión en la barra lateral.",
            "access": "Acceso Centralizado",
            "user": "ID de Usuario Operador",
            "pin": "PIN de Seguridad (4 dígitos)",
            "validate": "Validar Credenciales",
            "online": "Operador en Línea",
            "logout": "Cerrar Sesión",
            "area1": "Área 1: Distribución Geográfica y Telemetría",
            "focus": "Controles de Enfoque de Telemetría",
            "us": "Centrar en América del Norte",
            "eu": "Centrar en Región Europea",
            "as": "Centrar en Servidores de Asia",
            "toast_us": "Enfocando telemetría en US Core Nodos...",
            "toast_eu": "Enfocando telemetría en Euro Link...",
            "toast_as": "Enfocando telemetría en Asia Core...",
            "open_console": "Abrir Consola para Registrar Nuevo Servidor/Canal",
            "lat": "Latitud Geográfica",
            "lon": "Longitud Geográfica",
            "ident": "Nombre identificador del Canal o Servidor",
            "execute": "EJECUTAR: Aprovisionar y Guardar",
            "err_empty": "El nombre del identificador no puede estar vacío.",
            "success_reg": "registrado en memoria cloud con éxito.",
            "area2": "Área 2: Módulo de Enfoque de Inteligencia Virtual",
            "select_analysis": "Seleccione el área de análisis que desea que ejecute el sistema operativo principal:",
            "ana1": "Análisis de Telemetría Global",
            "ana2": "Monitoreo de Logs de Seguridad",
            "ana3": "Optimización de Tráfico de Nodos",
            "active_mod": "Módulo activo seleccionado actualmente",
            "monitor": "Visualizar Monitor de Carga y Tráfico Cuántico",
            "flow": "Flujo de paquetes telemetritos entre nodos activos",
            "metric1": "Servidores Conectados",
            "metric2": "Ancho de Banda Asignado",
            "metric3": "Latencia Global Media",
            "chart_x": "Nodos Operativos",
            "chart_y": "Peticiones/Min",
            "area3": "Área 3: Registro Histórico y Logs de Auditoría Institucional",
            "col1": "Fecha/Hora",
            "col2": "Operador",
            "col3": "Acción Ejecutada",
            "export": "Exportar Historial de Auditoría Corporativa (CSV)"
        }
    },
    "en": {
        "name": "English",
        "data": {
            "title": "QUANTUM ENTERPRISE OPERATING SYSTEM",
            "subtitle": "Integrated Services Command Console",
            "lock": "🔒 The operating system is locked. Please sign in via the sidebar.",
            "access": "Centralized Access",
            "user": "Operator User ID",
            "pin": "Security PIN (4 digits)",
            "validate": "Validate Credentials",
            "online": "Operator Online",
            "logout": "Sign Out",
            "area1": "Area 1: Geographic Distribution and Telemetry",
            "focus": "Telemetry Focus Controls",
            "us": "Center on North America",
            "eu": "Center on European Region",
            "as": "Center on Asia Servers",
            "toast_us": "Focusing telemetry on US Core Nodes...",
            "toast_eu": "Focusing telemetry on Euro Link...",
            "toast_as": "Focusing telemetry on Asia Core...",
            "open_console": "Open Console to Register New Server/Channel",
            "lat": "Geographic Latitude",
            "lon": "Geographic Longitude",
            "ident": "Channel or Server Identifier Name",
            "execute": "EXECUTE: Provision and Save",
            "err_empty": "The identifier name cannot be empty.",
            "success_reg": "registered in cloud memory successfully.",
            "area2": "Area 2: Virtual Intelligence Focus Module",
            "select_analysis": "Select the analysis area you want the main operating system to execute:",
            "ana1": "Global Telemetry Analysis",
            "ana2": "Security Logs Monitoring",
            "ana3": "Node Traffic Optimization",
            "active_mod": "Currently active module selected",
            "monitor": "View Load Monitor and Quantum Traffic",
            "flow": "Telemetry packet flow between active nodes",
            "metric1": "Connected Servers",
            "metric2": "Allocated Bandwidth",
            "metric3": "Average Global Latency",
            "chart_x": "Operating Nodes",
            "chart_y": "Requests/Min",
            "area3": "Area 3: Historical Record and Institutional Audit Logs",
            "col1": "Date/Time",
            "col2": "Operator",
            "col3": "Action Executed",
            "export": "Export Corporate Audit History (CSV)"
        }
    },
    "pt": {
        "name": "Português",
        "data": {
            "title": "SISTEMA OPERACIONAL QUANTUM ENTERPRISE",
            "subtitle": "Console de Comando de Serviços Integrados",
            "lock": "🔒 O sistema operacional está bocado. Por favor, faça login na barra lateral.",
            "access": "Acesso Centralizado",
            "user": "ID do Usuário Operador",
            "pin": "PIN de Segurança (4 dígitos)",
            "validate": "Validar Credenciais",
            "online": "Operador Online",
            "logout": "Encerrar Sessão",
            "area1": "Área 1: Distribuição Geográfica e Telemetria",
            "focus": "Controles de Foco de Telemetria",
            "us": "Centrar na América do Norte",
            "eu": "Centrar na Região Europeia",
            "as": "Centrar nos Servidores da Ásia",
            "toast_us": "Focando telemetria nos Nodos US Core...",
            "toast_eu": "Focando telemetria no Euro Link...",
            "toast_as": "Focando telemetria no Asia Core...",
            "open_console": "Abrir Console para Registrar Novo Server/Canal",
            "lat": "Latitude Geográfica",
            "lon": "Longitude Geográfica",
            "ident": "Nome Identificador do Canal ou Servidor",
            "execute": "EXECUTAR: Aprovisionar e Salvar",
            "err_empty": "O nome do identificador não pode estar vazio.",
            "success_reg": "registrado em memória cloud com sucesso.",
            "area2": "Área 2: Módulo de Foco de Inteligência Virtual",
            "select_analysis": "Selecione a área de análise que deseja que o sistema operacional principal execute:",
            "ana1": "Análise de Telemetria Global",
            "ana2": "Monitoramento de Logs de Segurança",
            "ana3": "Otimização de Tráfego de Nodos",
            "active_mod": "Módulo ativo selecionado atualmente",
            "monitor": "Visualizar Monitor de Carga e Tráfego Quântico",
            "flow": "Fluxo de pacotes de telemetria entre nodos ativos",
            "metric1": "Servidores Conectados",
            "metric2": "Largura de Banda Alocada",
            "metric3": "Latência Global Média",
            "chart_x": "Nodos Operativos",
            "chart_y": "Requisições/Min",
            "area3": "Área 3: Registro Histórico e Logs de Auditoria Institucional",
            "col1": "Data/Hora",
            "col2": "Operador",
            "col3": "Ação Executada",
            "export": "Exportar Histórico de Auditoria Corporativa (CSV)"
        }
    },
    "zh-CN": {
        "name": "中文",
        "data": {
            "title": "量子企业操作系统",
            "subtitle": "综合服务命令控制台",
            "lock": "🔒 操作系统已锁定。请在侧边栏登录。",
            "access": "集中访问",
            "user": "操作员用户 ID",
            "pin": "安全 PIN（4 位数字）",
            "validate": "验证凭据",
            "online": "操作员在线",
            "logout": "退出登录",
            "area1": "区域 1：地理分布与遥测",
            "focus": "遥测聚焦控制",
            "us": "聚焦北美",
            "eu": "聚焦欧洲地区",
            "as": "聚焦亚洲服务器",
            "toast_us": "正在将遥测聚焦于美国核心节点...",
            "toast_eu": "正在将遥测聚焦于欧洲链路...",
            "toast_as": "正在将遥测聚焦于亚洲核心...",
            "open_console": "打开控制台以注册新服务器/频道",
            "lat": "地理纬度",
            "lon": "地理经度",
            "ident": "频道或服务器标识符名称",
            "execute": "执行：配置并保存",
            "err_empty": "标识符名称不能为空。",
            "success_reg": "已成功注册到云内存中。",
            "area2": "区域 2：虚拟智能聚焦模块",
            "select_analysis": "选择您希望主操作系统执行的分析区域：",
            "ana1": "全球遥测分析",
            "ana2": "安全日志监控",
            "ana3": "节点流量优化",
            "active_mod": "当前选定的活动模块",
            "monitor": "查看负载监控器与量子流量",
            "flow": "活动节点之间的遥测数据包流",
            "metric1": "已连接的服务器",
            "metric2": "分配的总带宽",
            "metric3": "平均全球延迟",
            "chart_x": "运行中的节点",
            "chart_y": "每分钟请求数",
            "area3": "区域 3：历史记录与机构审计日志",
            "col1": "日期/时间",
            "col2": "操作员",
            "col3": "执行的操作",
            "export": "导出企业审计历史记录 (CSV)"
        }
    }
}

# Inicializar estados de control de idioma nativo
if "lang_code" not in st.session_state:
    st.session_state["lang_code"] = "es"

# Motor de traducción instantáneo sin dependencias externas
def T(key):
    return IDIOMAS_SOPORTADOS.get(st.session_state["lang_code"], {}).get("data", {}).get(key, key)

# Inicializar estados funcionales de la sesión
if "usuario_activo" not in st.session_state:
    st.session_state["usuario_activo"] = None

if "nodos_locales" not in st.session_state:
    st.session_state["nodos_locales"] = pd.DataFrame([
        {"lat": 40.7128, "lon": -74.0060, "nombre_nodo": "Nodo Central US"},
