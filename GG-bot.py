import streamlit as st
import requests
import urllib.parse  # Para manejar el símbolo +

st.set_page_config(page_title="GG-bot Fix", page_icon="🦅")

# --- LIMPIEZA Y CODIFICACIÓN ---
# Usamos .strip() para evitar espacios invisibles al pegar
USER = st.secrets["IOL_USER"].strip()
PASS = st.secrets["IOL_PASS"].strip()

# Codificamos la contraseña para que el '+' no se rompa en el camino
PASS_ENCODED = urllib.parse.quote(PASS)

st.title("🦅 GG-bot: Conexión Especial")
st.info(f"Probando conexión con usuario: {USER}")

if st.button("🚀 Intentar Login Seguro"):
    url = "https://api.invertironline.com/token"
    
    # Construimos el payload con la contraseña codificada
    payload = f"username={USER}&password={PASS_ENCODED}&grant_type=password"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    try:
        r = requests.post(url, data=payload, headers=headers, timeout=15)
        
        if r.status_code == 200:
            st.success("✅ ¡LOGRADO! El símbolo '+' fue procesado correctamente.")
            token = r.json().get("access_token")
            
            # Prueba rápida de saldo para confirmar acceso total
            h = {"Authorization": f"Bearer {token}"}
            res_saldo = requests.get("https://api.invertironline.com/api/estadocuenta", headers=h)
            
            if res_saldo.status_code == 200:
                st.balloons()
                st.subheader("💰 Tu Saldo Crudo:")
                st.json(res_saldo.json())
        else:
            st.error(f"❌ Error {r.status_code}")
            st.write("Respuesta del servidor:", r.text)
            st.warning("Si sigue fallando, probá cambiar la clave en IOL por una sin símbolos (+, &, #) para descartar bloqueo del servidor.")
            
    except Exception as e:
        st.error(f"Fallo de red: {e}")
