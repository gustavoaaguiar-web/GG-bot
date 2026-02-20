import streamlit as st
import requests

st.title("🚀 GG-bot: Test de Saldo")

# 1. Obtención de Token (v1)
def test_conexion():
    url_token = "https://api.invertironline.com/token"
    payload = {
        'username': st.secrets["IOL_USER"],
        'password': st.secrets["IOL_PASS"],
        'grant_type': 'password'
    }
    
    st.write("Intentando autenticar...")
    r = requests.post(url_token, data=payload)
    
    if r.status_code == 200:
        token = r.json().get("access_token")
        st.success("✅ Token obtenido con éxito")
        
        # 2. Consulta de Saldo (v1)
        headers = {"Authorization": f"Bearer {token}"}
        r_saldo = requests.get("https://api.invertironline.com/api/estadocuenta", headers=headers)
        
        if r_saldo.status_code == 200:
            st.balloons()
            st.subheader("💰 Resultado del Saldo:")
            st.json(r_saldo.json()) # Esto escupe todo el dato crudo que manda IOL
        else:
            st.error(f"Error al pedir saldo: {r_saldo.status_code}")
            st.write(r_saldo.text)
    else:
        st.error(f"Error de Autenticación: {r.status_code}")
        st.write("Respuesta del servidor:", r.text)

if st.button("Ejecutar Test de Conexión"):
    test_conexion()
