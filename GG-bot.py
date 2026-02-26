import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="GG-bot | API v2", page_icon="🦅")

# --- CREDENCIALES (Usa las mismas que tenés en Secrets) ---
USER = st.secrets["IOL_USER"]
PASS = st.secrets["IOL_PASS"]

def get_token_v2():
    url = "https://api.invertironline.com/token"
    # La v2 usa el mismo sistema de token, pero los endpoints cambian
    payload = f"username={USER}&password={PASS}&grant_type=password"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, data=payload, headers=headers)
    if r.status_code == 200:
        return r.json().get("access_token")
    return None

st.title("🦅 GG-bot | Conexión API v2")

tk = get_token_v2()

if tk:
    st.success("✅ ¡Conectado a la API v2 con éxito!")
    headers = {"Authorization": f"Bearer {tk}"}
    
    # Probamos el endpoint de Portafolio (que en la v1 te daba Error 500)
    # En v2 debería funcionar
    url_portafolio = "https://api.invertironline.com/api/v2/portafolio/argentina"
    
    try:
        res = requests.get(url_portafolio, headers=headers)
        if res.status_code == 200:
            st.subheader("💰 Tu Portafolio Real (v2)")
            data = res.json()
            # Si tenés activos, los mostramos
            if data.get('activos'):
                df = pd.DataFrame(data['activos'])
                st.dataframe(df[['simbolo', 'cantidad', 'ultimoPrecio', 'variacionDiaria']])
            else:
                st.info("No tenés activos actualmente, pero la conexión es EXITOSA.")
                st.metric("Saldo Líquido", f"$ {data.get('saldoTotal', '0.00')}")
        else:
            st.error(f"Error en v2: {res.status_code}")
            st.write("Si sale error aquí, sacamos captura para Macarena.")
    except Exception as e:
        st.error(f"Error de red: {e}")
else:
    st.error("❌ No se pudo obtener el Token. Revisá tus credenciales en Secrets.")
