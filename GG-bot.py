import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="GG-bot | Control", page_icon="🦅", layout="centered")

# --- ESTILOS PARA EL SALDO Y COLORES ---
st.markdown("""
    <style>
    .saldo-box {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FFD700;
        margin-bottom: 20px;
    }
    .val-pos { color: #00FF00; font-weight: bold; }
    .val-neg { color: #FF4B4B; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SECCIÓN DE SALDO ---
st.markdown('<div class="saldo-box"><h3 style="margin:0; color:white;">💰 Saldo Disponible IOL</h3><h1 style="margin:0; color:#FFD700;">ARS 76.71</h1></div>', unsafe_allow_html=True)
st.caption("⚠️ API IOL en mantenimiento. Mostrando último saldo conocido.")

st.divider()

# --- LÓGICA DE PRECIOS (FILTRADA) ---
TICKERS = {
    "GGAL": "GGAL.BA",
    "YPFD": "YPFD.BA",
    "PAMP": "PAMP.BA"
}

@st.cache_data(ttl=60)
def obtener_pizarra():
    resultados = []
    for nombre, ticker in TICKERS.items():
        try:
            asset = yf.Ticker(ticker)
            info = asset.fast_info
            actual = info['last_price']
            cierre = info['regular_market_previous_close']
            var_pct = ((actual / cierre) - 1) * 100
            
            # Lógica de color y flecha
            color = "green" if var_pct >= 0 else "red"
            flecha = "▲" if var_pct >= 0 else "▼"
            
            resultados.append({
                "Especie": nombre,
                "Precio": f"$ {actual:,.2f}",
                "Variación": f"{var_pct:.2f}%",
                "Tendencia": f"{flecha}",
                "Color": color
            })
        except: continue
    return resultados

# --- RENDERIZADO DE PIZARRA ---
st.subheader("📈 Monitor de Mercado")

if st.button("🔄 Actualizar Cotizaciones"):
    datos = obtener_pizarra()
    if datos:
        for d in datos:
            # Creamos una fila visual con columnas
            c1, c2, c3, c4 = st.columns([2, 3, 2, 1])
            with c1: st.write(f"**{d['Especie']}**")
            with c2: st.write(f"{d['Precio']}")
            with c3: 
                # Aplicamos color según la variación
                clase = "val-pos" if d['Color'] == "green" else "val-neg"
                st.markdown(f'<span class="{clase}">{d["Variación"]}</span>', unsafe_allow_html=True)
            with c4:
                st.markdown(f'<span class="{clase}">{d["Tendencia"]}</span>', unsafe_allow_html=True)
            st.divider()
    else:
        st.error("No se pudo conectar con Yahoo Finance.")

# --- ALERTAS RÁPIDAS ---
with st.expander("🔔 Configurar Alertas Rápidas"):
    st.info("Próximamente: Notificaciones push cuando GGAL toque valores clave.")
    
