import streamlit as st
import requests

st.set_page_config(page_title="GG-bot Fix", page_icon="🦅")

# Limpieza automática de espacios en blanco
USER = st.secrets["IOL_USER"].strip()
PASS = st.secrets["IOL_PASS"].strip()

st.title("🦅 GG-bot: Intento de Conexión Forzada")

if st.button("🚀 Probar Conexión Ahora"):
    url = "https://api.invertironline.com/token"
    
    # Payload exacto según tu captura de Postman (Foto 8d66a91f)
    payload = f"username={USER}&password={PASS}&grant_type=password"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    st.write("Enviando credenciales a IOL...")
    
    try:
        r = requests.post(url, data=payload, headers=headers, timeout=15)
        
        if r.status_code == 200:
            st.success("✅ ¡CONECTADO! El servidor aceptó tus credenciales.")
            data = r.json()
            st.session_state["access_token"] = data.get("access_token")
            st.json(data) # Mostramos el éxito
        else:
            st.error(f"❌ Error {r.status_code}: No autorizado")
            st.warning("Causas probables: 1. Contraseña mal escrita en Secrets. 2. Cuenta bloqueada por intentos fallidos. 3. El usuario no es el mail.")
            st.write("Respuesta cruda del servidor:", r.text)
            
    except Exception as e:
        st.error(f"Fallo crítico de red: {e}")
