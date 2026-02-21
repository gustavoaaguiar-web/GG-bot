import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="GG-bot | Rava", page_icon="🦅")

st.title("🦅 GG-bot | Monitor Rava")

# 1. Saldo (API IOL)
st.metric("Saldo Disponible (IOL)", "ARS 76.71")

st.divider()

# 2. Captura de Pizarra Rava
@st.cache_data(ttl=60)
def leer_pizarra():
    url = "https://www.rava.com/cotizaciones/acciones"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # Especificamos 'html5lib' para resolver el error de tu captura
        tablas = pd.read_html(response.text, flavor='html5lib')
        df = tablas[0]
        df = df.iloc[:, [0, 1, 2]]
        df.columns = ['Especie', 'Precio', 'Var %']
        return df
    except Exception as e:
        st.error(f"Error técnico: {e}")
        return None

if st.button("🔄 Actualizar Pizarra Rava"):
    with st.spinner("Conectando con la pizarra..."):
        df_rava = leer_pizarra()
        if df_rava is not None:
            # Filtramos las más importantes
            favoritas = ["GGAL", "YPFD", "PAMP", "ALUA", "TXAR", "EDN"]
            df_ver = df_rava[df_rava['Especie'].isin(favoritas)]
            st.table(df_ver)
        else:
            st.warning("No se pudo obtener la información.")
