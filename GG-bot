import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="GG-bot v1.0", page_icon="🦅", layout="wide")

# Estilo CSS para mejorar la visibilidad
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE CONEXIÓN ---
def get_iol_token():
    url = "https://api.invertironline.com/token"
    # Formato obligatorio para v1
    payload = {
        'username': st.secrets["IOL_USER"],
        'password': st.secrets["IOL_PASS"],
        'grant_type': 'password'
    }
    try:
        # En v1 enviamos como data (form-urlencoded)
        r = requests.post(url, data=payload, timeout=10)
        if r.status_code == 200:
            return r.json().get("access_token")
        return None
    except:
        return None

def fetch_v1(token, endpoint):
    url = f"https://api.invertironline.com/api/{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        return None

# --- APP ---
st.title("🦅 GG-bot | Control de Activos")

# Gestionar Token en sesión para no saturar a IOL
if "token" not in st.session_state:
    with st.spinner("Autenticando..."):
        token = get_iol_token()
        if token:
            st.session_state["token"] = token
            st.toast("Conexión exitosa", icon="✅")
        else:
            st.error("Error de autenticación. Revisá tus Secrets.")

if "token" in st.session_state:
    tk = st.session_state["token"]

    # --- SECCIÓN 1: CUENTA ---
    st.subheader("💰 Resumen de Cuenta")
    data_cuenta = fetch_v1(tk, "estadocuenta")
    
    if data_cuenta:
        cuentas = data_cuenta.get('cuentas', [])
        cols = st.columns(len(cuentas) if cuentas else 1)
        for i, c in enumerate(cuentas):
            with cols[i]:
                st.metric(
                    label=f"Disponible {c.get('moneda')}", 
                    value=f"{c.get('moneda', '$')} {c.get('disponibleOperar', 0):,.2f}"
                )
    
    st.divider()

    # --- SECCIÓN 2: MONITOR ---
    st.subheader("📈 Cotizaciones Líderes (Panel Merval)")
    # Endpoint v1: Cotizacion/Paneles/Merval/bcpp
    panel = fetch_v1(tk, "Cotizacion/Paneles/Merval/bcpp")

    if panel:
        df = pd.DataFrame(panel)
        if not df.empty:
            # Lista de tickers que te interesan
            interes = ["GGAL", "YPFD", "PAMP", "ALUA", "EDN", "CEPU"]
            df_filtro = df[df['simbolo'].isin(interes)].copy()
            
            # Formateo de columnas
            df_view = df_filtro[['simbolo', 'ultimoPrecio', 'variacionPorcentual', 'puntaCompra', 'puntaVenta']]
            df_view.columns = ['Ticker', 'Precio', 'Var %', 'Compra', 'Venta']
            
            # Aplicar color a la variación
            def color_variacion(val):
                color = 'green' if val > 0 else 'red' if val < 0 else 'black'
                return f'color: {color}; font-weight: bold'

            st.table(df_view.style.applymap(color_variacion, subset=['Var %']))
        else:
            st.info("No hay datos disponibles en este momento.")

# --- BOTONERA ---
st.sidebar.title("Configuración")
if st.sidebar.button("🔄 Forzar Actualización"):
    st.session_state.clear()
    st.rerun()

st.sidebar.info(f"Último refresh: {datetime.now().strftime('%H:%M:%S')}")
