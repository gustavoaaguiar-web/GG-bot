import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="GG-bot Market Test", page_icon="🦅")

USER = st.secrets["IOL_USER"].strip()
PASS = st.secrets["IOL_PASS"].strip()

def get_token():
    url = "https://api.invertironline.com/token"
    payload = f"username={USER}&password={PASS}&grant_type=password"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, data=payload, headers=headers)
    return r.json().get("access_token") if r.status_code == 200 else None

st.title("🦅 GG-bot | Prueba de Mercado")

if "token_simple" not in st.session_state:
    st.session_state["token_simple"] = get_token()

tk = st.session_state.get("token_simple")

if tk:
    st.success("Conectado")
    
    # Intentamos 3 rutas diferentes para ver cuál tiene habilitada tu cuenta
    st.subheader("Buscando Datos de GGAL...")
    
    # Opción A: Título individual (Ruta clásica v1)
    # Formato: /api/titulos/{simbolo}/{mercado}
    # mercados posibles: bcpp (BYMA Pesos), bcba (Viejo Buenos Aires)
    rutas_a_testear = [
        "titulos/GGAL/bcpp",
        "Cotizacion/Acciones/Merval/Argentina",
        "Cotizacion/Paneles/Merval/bcpp"
    ]
    
    headers = {"Authorization": f"Bearer {tk}"}
    
    for ruta in rutas_a_testear:
        with st.expander(f"Probando ruta: {ruta}"):
            res = requests.get(f"https://api.invertironline.com/api/{ruta}", headers=headers)
            if res.status_code == 200:
                data = res.json()
                st.write("✅ ¡ÉXITO! Datos recibidos:")
                st.json(data)
            else:
                st.write(f"❌ Falló (Error {res.status_code})")

else:
    st.error("No hay token. Revisá la clave.")
    if st.button("Reintentar Login"):
        st.session_state.clear()
        st.rerun()
        
