import streamlit as st
from merval import merval # Importamos la librería específica
import pandas as pd

st.set_page_config(page_title="GG-bot | Merval Lib Test", page_icon="🦅")

st.title("🦅 GG-bot: Test de Biblioteca 'Merval'")
st.write("Probando obtención de datos por fuera de la API v1 de IOL...")

if st.button("🚀 Consultar Panel Merval"):
    try:
        with st.spinner("Obteniendo datos..."):
            # La función get_panel() de esta librería suele traer el panel líder
            df = merval.get_panel() 
            
            if not df.empty:
                st.success("¡Datos obtenidos con éxito!")
                # Filtramos las columnas más importantes para no saturar
                cols = ['especie', 'ultimo', 'variacion', 'compra', 'venta', 'volumen']
                st.dataframe(df[df.columns.intersection(cols)])
            else:
                st.warning("La librería no devolvió datos. Es posible que la fuente esté caída.")
                
    except Exception as e:
        st.error(f"Error al usar la biblioteca: {e}")
        st.info("Nota: Algunas librerías locales requieren que el mercado esté abierto o fallan si la web de origen cambió su estructura.")

st.divider()
st.caption("Esta biblioteca busca datos públicos de Bolsar/BYMA/Rava dependiendo de su versión.")

