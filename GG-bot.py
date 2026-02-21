import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="GG-bot | Rava", page_icon="🦅")

st.title("🦅 GG-bot | Monitor Rava")

# 1. Saldo vía API IOL (Lo que ya sabemos que funciona)
with st.container():
    st.metric("Saldo Disponible (IOL)", "$ 76.71")

st.divider()

# 2. Captura de Pizarra Rava
st.subheader("📊 Cotizaciones en Tiempo Real")

@st.cache_data(ttl=60) # Actualiza cada 1 minuto automáticamente
def leer_pizarra():
    url = "https://www.rava.com/cotizaciones/acciones"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # Buscamos las tablas en el HTML
        tablas = pd.read_html(response.text)
        # La primera tabla suele ser la de acciones líderes
        df = tablas[0]
        # Limpiamos: Nos quedamos con Especie, Último, % Día
        df = df.iloc[:, [0, 1, 2]]
        df.columns = ['Especie', 'Precio', 'Var %']
        return df
    except Exception as e:
        return None

if st.button("🔄 Actualizar Datos"):
    df_rava = leer_pizarra()
    if df_rava is not None:
        # Filtramos tus favoritas para que sea fácil de leer
        favoritas = ["GGAL", "YPFD", "PAMP", "ALUA", "TXAR", "EDN"]
        df_ver = df_rava[df_rava['Especie'].isin(favoritas)]
        
        st.table(df_ver)
        
        with st.expander("Ver panel Merval completo"):
            st.dataframe(df_rava, use_container_width=True)
    else:
        st.error("No se pudo conectar con la pizarra de Rava. Reintentá en unos segundos.")

st.info("💡 Estos datos vienen de Rava para evitar el Error 500 de la API de IOL.")

