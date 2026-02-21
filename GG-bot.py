import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="GG-bot | Rava Pro", page_icon="🦅")

st.title("🦅 GG-bot | Monitor Rava")

# 1. Saldo (Dato fijo de tu última conexión exitosa)
st.metric("Saldo Disponible (IOL)", "ARS 76.71")

st.divider()

# 2. Motor de extracción manual de Rava
def leer_rava_manual():
    url = "https://www.rava.com/cotizaciones/acciones"
    # User-Agent completo para parecer un navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos la tabla de cotizaciones por su clase o estructura
        tabla = soup.find('table') 
        if not tabla:
            return None
            
        # Convertimos la tabla de HTML a DataFrame de Pandas
        df = pd.read_html(str(tabla), flavor='bs4')[0]
        
        # Limpieza de columnas (Rava usa: Especie, Último, % Día, etc.)
        df = df.iloc[:, [0, 1, 2]]
        df.columns = ['Especie', 'Precio', 'Var %']
        return df
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

if st.button("🔄 Sincronizar con Rava"):
    with st.spinner("Leyendo pizarra en tiempo real..."):
        df_rava = leer_rava_manual()
        
        if df_rava is not None:
            # Filtramos tus favoritas
            favoritas = ["GGAL", "YPFD", "PAMP", "ALUA", "TXAR", "EDN"]
            df_ver = df_rava[df_rava['Especie'].isin(favoritas)].copy()
            
            if not df_ver.empty:
                st.subheader("📈 Favoritas")
                st.table(df_ver)
            
            with st.expander("Ver todas las Acciones Líderes"):
                st.dataframe(df_rava, use_container_width=True)
        else:
            st.error("Rava rechazó la conexión. Intentá de nuevo en un minuto.")

st.info("💡 Si IOL te habilita la API v2, reemplazaremos este motor por la conexión directa.")
