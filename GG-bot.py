import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="GG-bot | Oficial", page_icon="🦅", layout="wide")

# Estilo para que se vea impecable
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE DATOS ---
def get_token():
    url = "https://api.invertironline.com/token"
    payload = {
        'username': st.secrets["IOL_USER"],
        'password': st.secrets["IOL_PASS"],
        'grant_type': 'password'
    }
    try:
        r = requests.post(url, data=payload, timeout=10)
        if r.status_code == 200:
            return r.json().get("access_token")
        return None
    except:
        return None

def fetch_data(token, endpoint):
    url = f"https://api.invertironline.com/api/{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        return None

# --- APP PRINCIPAL ---
st.title("🦅 GG-bot | Monitor de Control")
st.caption(f"Conectado como: {st.secrets['IOL_USER']}")

if "token" not in st.session_state:
    with st.spinner("Autenticando..."):
        token = get_token()
        if token:
            st.session_state["token"] = token
        else:
            st.error("Error de conexión. Revisá tus credenciales.")

if "token" in st.session_state:
    tk = st.session_state["token"]

    # --- SALDOS (Basado en tu captura exitosa) ---
    st.subheader("💰 Resumen de Billetera")
    data_cuenta = fetch_data(tk, "estadocuenta")
    
    if data_cuenta:
        cuentas = data_cuenta.get('cuentas', [])
        cols = st.columns(len(cuentas) if cuentas else 1)
        for i, c in enumerate(cuentas):
            with cols[i]:
                # Usamos los nombres exactos que vimos en tu JSON ('moneda' y 'disponible')
                moneda = c.get('moneda', 'ARS').replace('_', ' ')
                st.metric(label=f"Disponible {moneda}", value=f"$ {c.get('disponible', 0):,.2f}")
    
    st.divider()

    # --- MONITOR DE MERCADO ---
    st.subheader("📈 Cotizaciones Destacadas")
    # Usamos el panel Merval que es el más estable en v1
    panel = fetch_data(tk, "Cotizacion/Paneles/Merval/bcpp")

    if panel:
        df = pd.DataFrame(panel)
        if not df.empty:
            # Lista de tickers que te interesan
            tickers = ["GGAL", "YPFD", "PAMP", "ALUA", "EDN"]
            df_filtro = df[df['simbolo'].isin(tickers)].copy()
            
            # Limpieza de tabla
            df_view = df_filtro[['simbolo', 'ultimoPrecio', 'variacionPorcentual']]
            df_view.columns = ['Activo', 'Último Precio', 'Var %']
            
            # Mostrar tabla
            st.dataframe(df_view.set_index('Activo'), use_container_width=True)
        else:
            st.info("Buscando cotizaciones...")

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1155/1155253.png", width=100)
    st.title("Opciones")
    if st.button("🔄 Actualizar Todo"):
        st.session_state.clear()
        st.rerun()
    st.write(f"Último refresh: {datetime.now().strftime('%H:%M:%S')}")

