import streamlit as st
import requests
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="GG-bot RealTime", page_icon="🦅")

USER = st.secrets["IOL_USER"].strip()
PASS = st.secrets["IOL_PASS"].strip()

def get_token():
    url = "https://api.invertironline.com/token"
    payload = f"username={USER}&password={PASS}&grant_type=password"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, data=payload, headers=headers)
    return r.json().get("access_token") if r.status_code == 200 else None

st.title("🦅 GG-bot | Tiempo Real v1")

if "tk" not in st.session_state:
    st.session_state["tk"] = get_token()

tk = st.session_state["tk"]

if tk:
    # Definimos los activos que querés seguir
    activos = ["GGAL", "YPFD", "PAMP", "ALUA"]
    mercado = "bcpp" # BYMA Pesos
    
    resultados = []
    headers = {"Authorization": f"Bearer {tk}"}

    st.write("### ⏱️ Cotizaciones en Vivo (Sin Delay)")
    
    for activo in activos:
        # Probamos la ruta de título individual
        url = f"https://api.invertironline.com/api/titulos/{activo}/{mercado}/Cotizacion"
        
        r = requests.get(url, headers=headers)
        
        if r.status_code == 200:
            data = r.json()
            resultados.append({
                "Ticker": activo,
                "Último": data.get("ultimoPrecio"),
                "Variación": data.get("variacionPorcentual"),
                "Venta": data.get("puntaVenta", {}).get("precio"),
                "Compra": data.get("puntaCompra", {}).get("precio")
            })
        else:
            st.error(f"Error en {activo}: {r.status_code}")

    if resultados:
        df = pd.DataFrame(resultados)
        st.table(df)
    else:
        st.warning("No se pudieron obtener cotizaciones individuales.")

else:
    st.error("Error de autenticación.")
    
