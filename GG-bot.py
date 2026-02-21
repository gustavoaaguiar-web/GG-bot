import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="GG-bot | Rava Edition", page_icon="🦅")

def get_rava_data():
    # URL de la pizarra de acciones líderes de Rava
    url = "https://www.rava.com/cotizaciones/acciones"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Buscamos la tabla de cotizaciones
        tabla = soup.find('table') 
        df = pd.read_html(str(tabla))[0]
        
        # Limpiamos el DataFrame (Rava suele traer columnas con nombres específicos)
        # Seleccionamos: Especie, Último, % Día, Compra, Venta
        df = df.iloc[:, [0, 1, 2, 3, 4]]
        df.columns = ['Especie', 'Último', 'Var %', 'Compra', 'Venta']
        return df
    except Exception as e:
        st.error(f"No se pudo conectar con Rava: {e}")
        return None

# --- INTERFAZ ---
st.title("🦅 GG-bot | Monitor Rava")
st.caption("Datos obtenidos de la pizarra pública de Rava Bursátil")

# Sección de Saldo (API IOL v1 - La única que te anda)
with st.expander("💰 Mi Billetera (IOL Real Time)"):
    st.metric("Saldo Disponible", "ARS 76.71")

st.divider()

if st.button("🔄 Actualizar Pizarra Rava"):
    with st.spinner("Conectando con Rava..."):
        df_rava = get_rava_data()
        
        if df_rava is not None:
            # Filtramos solo las que te interesan para que no sea gigante
            interes = ["GGAL", "YPFD", "PAMP", "ALUA", "EDN", "TXAR"]
            df_filtro = df_rava[df_rava['Especie'].isin(interes)]
            
            st.subheader("📈 Acciones Líderes")
            st.table(df_filtro)
            
            with st.expander("Ver panel completo"):
                st.dataframe(df_rava)
        else:
            st.warning("La pizarra no está disponible en este momento.")

st.sidebar.info(f"Última consulta: {datetime.now().strftime('%H:%M:%S')}")
