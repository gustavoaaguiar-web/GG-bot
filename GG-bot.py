import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de página para móviles
st.set_page_config(page_title="GG-bot | Control", page_icon="🦅", layout="centered")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    .css-1r6slb0 { border: 1px solid #e6e9ef; }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO Y SALDO ---
st.title("🦅 GG-bot | Monitor Intradiario")
col1, col2 = st.columns(2)
with col1:
    st.metric("Saldo IOL (ARS)", "$ 76.71")
with col2:
    st.caption("⚠️ API IOL en mantenimiento. Precios vía Yahoo Finance (Real Time).")

st.divider()

# --- LÓGICA DE DATOS ---
# Tickers argentinos para Yahoo Finance
TICKERS = {
    "GGAL": "GGAL.BA",
    "YPFD": "YPFD.BA",
    "PAMP": "PAMP.BA",
    "ALUA": "ALUA.BA",
    "TXAR": "TXAR.BA",
    "EDN": "EDN.BA"
}

@st.cache_data(ttl=60)
def obtener_pizarra():
    resultados = []
    for nombre, ticker in TICKERS.items():
        try:
            asset = yf.Ticker(ticker)
            info = asset.fast_info
            
            precio_actual = info['last_price']
            precio_cierre = info['regular_market_previous_close']
            variacion = ((precio_actual / precio_cierre) - 1) * 100
            
            # Definir flecha y color
            icono = "🔺" if variacion >= 0 else "🔻"
            
            resultados.append({
                "Especie": nombre,
                "Precio": round(precio_actual, 2),
                "Variación": f"{icono} {variacion:.2f}%",
                "Cierre Ayer": round(precio_cierre, 2)
            })
        except:
            continue
    return pd.DataFrame(resultados)

# --- INTERFAZ DE USUARIO ---
st.subheader("📈 Pizarra de Cotizaciones")

if st.button("🔄 Actualizar Mercado"):
    with st.spinner("Sincronizando precios..."):
        df = obtener_pizarra()
        
        if not df.empty:
            # Mostramos la tabla principal
            st.table(df)
            
            # --- SISTEMA DE ALERTAS RÁPIDAS ---
            st.divider()
            st.subheader("🔔 Estado de Alertas")
            
            # Ejemplo de lógica para alertas automáticas
            for index, row in df.iterrows():
                if row['Especie'] == "GGAL" and row['Precio'] > 7300:
                    st.warning(f"🚨 GGAL superó los $7300 (Actual: ${row['Precio']})")
                if row['Especie'] == "YPFD" and row['Precio'] < 54000:
                    st.error(f"🚨 YPFD cayó por debajo de $54000 (Actual: ${row['Precio']})")
        else:
            st.error("No se pudieron obtener los datos. Verificá la conexión.")

# --- SECCIÓN MANUAL ---
with st.expander("📝 Notas de Estrategia"):
    st.write("""
    1. Revisar los precios aquí (coinciden con la App de Yahoo).
    2. Si el precio toca tu objetivo, entrar a IOL manualmente.
    3. Esperar respuesta de IOL por la API v2.
    """)

st.sidebar.info("Bot configurado para modo: Alerta Intradiaria Manual.")
                
