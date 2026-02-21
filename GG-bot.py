import streamlit as st
from pyhomebroker import HomeBroker
import pandas as pd

st.set_page_config(page_title="GG-bot | Matba Rofex", page_icon="🦅")

st.title("🦅 GG-bot | Monitor Real-Time")

# Saldo (Mantenemos lo que ya funciona de IOL)
st.metric("Saldo Disponible (IOL)", "ARS 76.71")

st.divider()

@st.cache_data(ttl=30)
def obtener_precios_merval():
    try:
        # Inicializamos el conector (usamos opciones públicas)
        hb = HomeBroker(21) # 21 es el ID para datos generales
        # Traemos las cotizaciones de acciones líderes
        pizarra = hb.history.get_quotes(symbols=['GGAL', 'YPFD', 'PAMP', 'ALUA'], market='bcpp')
        return pizarra
    except Exception as e:
        return None

if st.button("🔄 Sincronizar con Mercado"):
    with st.spinner("Conectando con Matba Rofex..."):
        df = obtener_precios_merval()
        
        if df is not None and not df.empty:
            st.subheader("📈 Cotizaciones Líderes")
            # Limpiamos para mostrar lo importante
            df_view = df[['last', 'variation', 'bid_price', 'offer_price']]
            df_view.columns = ['Último', 'Var %', 'Compra', 'Venta']
            st.table(df_view)
        else:
            st.error("No se pudo obtener la pizarra. Intentando método alternativo...")
            # Si falla pyhomebroker, mostramos un link directo de emergencia
            st.info("Podés ver los precios mientras tanto en: [BYMA Datos](https://www.byma.com.ar/cotizaciones/acciones/)")

