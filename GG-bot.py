import streamlit as st
import requests
import pandas as pd

st.title("🦅 GG-bot | Modo Portafolio")

USER = st.secrets["IOL_USER"].strip()
PASS = st.secrets["IOL_PASS"].strip()

def get_token():
    url = "https://api.invertironline.com/token"
    payload = f"username={USER}&password={PASS}&grant_type=password"
    r = requests.post(url, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    return r.json().get("access_token") if r.status_code == 200 else None

tk = get_token()

if tk:
    st.success("Conectado")
    headers = {"Authorization": f"Bearer {tk}"}
    
    # Probamos el endpoint de Portafolio Argentina
    # Es mucho más probable que este funcione que los de mercado
    url_portafolio = "https://api.invertironline.com/api/portafolio/bcpp"
    
    res = requests.get(url_portafolio, headers=headers)
    
    if res.status_code == 200:
        st.balloons()
        st.subheader("📊 Tus Activos en Tiempo Real")
        data = res.json()
        
        activos = data.get('activos', [])
        if activos:
            df = pd.DataFrame(activos)
            # Mostramos las columnas que suelen venir en el portafolio
            columnas_interes = ['simbolo', 'cantidad', 'ultimoPrecio', 'valorizado', 'variacionDiaria']
            st.dataframe(df[[c for c in columnas_interes if c in df.columns]])
        else:
            st.info("Portafolio conectado pero parece que no tenés activos en bcpp.")
    else:
        st.error(f"Error 500: IOL tampoco responde el Portafolio.")
else:
    st.error("Error de login.")
    
