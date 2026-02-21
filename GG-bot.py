import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="GG-bot | Final", page_icon="🦅")

st.title("🦅 GG-bot | Monitor Final")

# 1. Saldo de Emergencia (API IOL fallando, mostramos último dato conocido)
st.metric("Saldo Disponible (IOL)", "ARS 76.71")

st.divider()

# 2. Panel de Mercado vía Yahoo Finance
st.subheader("📊 Cotizaciones en Tiempo Real")

# Definimos los tickers ( Yahoo necesita .BA para Argentina)
tickers_ars = ["GGAL.BA", "YPFD.BA", "PAMP.BA", "ALUA.BA", "TXAR.BA"]

def obtener_datos():
    lista_precios = []
    for t in tickers_ars:
        try:
            asset = yf.Ticker(t)
            # fast_info es más rápido y tiene menos riesgo de bloqueo
            info = asset.fast_info
            lista_precios.append({
                "Especie": t.replace(".BA", ""),
                "Último": round(info['last_price'], 2),
                "Var %": f"{info['regular_market_previous_close']:.2f}" # Referencia
            })
        except:
            continue
    return pd.DataFrame(lista_precios)

if st.button("🔄 Actualizar Pizarra"):
    with st.spinner("Sincronizando..."):
        df = obtener_datos()
        if not df.empty:
            st.table(df)
        else:
            st.error("Error al conectar con el servidor de precios.")

st.info("💡 Si el mail a IOL funciona y te dan la API v2, este monitor será 100% exacto.")
