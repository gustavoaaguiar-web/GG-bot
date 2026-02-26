import streamlit as st
import requests

st.set_page_config(page_title="GG-bot | IOL v2", page_icon="🦅")

# --- CONEXIÓN ---
USER = st.secrets["IOL_USER"]
PASS = st.secrets["IOL_PASS"]

def get_token():
    url = "https://api.invertironline.com/token"
    payload = f"username={USER}&password={PASS}&grant_type=password"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, data=payload, headers=headers)
    return r.json().get("access_token") if r.status_code == 200 else None

st.title("🦅 GG-bot | Mercado v2")

token = get_token()

if token:
    headers = {"Authorization": f"Bearer {token}"}
    
    # Endpoint v2 para cotización de un título específico
    # Mercado: bcpp (Bolsa de Comercio de Bs As)
    symbol = "GGAL"
    url_quote = f"https://api.invertironline.com/api/v2/Titulos/Cotizacion/Instrumentos/ bcpp/{symbol}/Puntas"
    
    if st.button(f"🔍 Consultar Puntas de {symbol}"):
        try:
            res = requests.get(url_quote, headers=headers)
            if res.status_code == 200:
                data = res.json()
                
                st.subheader(f"📊 {symbol} en Tiempo Real")
                
                # Mostramos las puntas (Compra y Venta)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Mejor Compra", f"$ {data.get('puntaCompradora', 0)}")
                with col2:
                    st.metric("Mejor Venta", f"$ {data.get('puntaVendedora', 0)}")
                
                with st.expander("Ver JSON completo de respuesta"):
                    st.json(data)
            else:
                st.error(f"Error al consultar: {res.status_code}")
                st.write(res.text)
        except Exception as e:
            st.error(f"Error técnico: {e}")
else:
    st.error("No se pudo conectar. Revisá Secrets.")
