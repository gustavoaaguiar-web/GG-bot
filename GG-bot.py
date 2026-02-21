import streamlit as st
import requests

st.title("🦅 GG-bot: Buscador de Ruta Correcta")

# Configuración base
USER = st.secrets["IOL_USER"].strip()
PASS = st.secrets["IOL_PASS"].strip()

def get_token():
    url = "https://api.invertironline.com/token"
    payload = f"username={USER}&password={PASS}&grant_type=password"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, data=payload, headers=headers)
    return r.json().get("access_token") if r.status_code == 200 else None

if "tk" not in st.session_state:
    st.session_state["tk"] = get_token()

tk = st.session_state["tk"]

if tk:
    st.success("Conexión Establecida")
    
    # Lista de combinaciones posibles para el panel Merval
    # Probamos variaciones de 'Merval' y de 'bcpp' (mercado local)
    variaciones = [
        "Cotizacion/Paneles/Merval/bcpp",     # Estándar
        "Cotizacion/Paneles/merval/bcpp",     # Minúscula
        "Cotizacion/Paneles/MERVAL/BCPP",     # Todo Mayúscula
        "Cotizacion/Paneles/Merval/Argentina",# Por país
        "Cotizacion/Acciones/Merval/bcpp",    # Usando 'Acciones' en vez de 'Paneles'
        "Cotizacion/Acciones/Lideres/bcpp",   # Variante 'Lideres'
        "titulos/GGAL/bcpp",                 # Directo a un papel
        "titulos/GGAL/BCPP"                  # Directo con mercado en mayúscula
    ]
    
    headers = {"Authorization": f"Bearer {tk}"}
    
    st.write("### 🔍 Escaneando disponibilidad...")
    
    for ruta in variaciones:
        url = f"https://api.invertironline.com/api/{ruta}"
        try:
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                st.success(f"✅ FUNCIONA: {ruta}")
                st.json(r.json()[:1]) # Mostramos solo el primer elemento para confirmar
            elif r.status_code == 500:
                st.warning(f"⚠️ Error 500 en: {ruta} (Ruta existente pero el servidor falló)")
            else:
                st.error(f"❌ Error {r.status_code} en: {ruta}")
        except Exception as e:
            st.write(f"Error de red en {ruta}: {e}")

else:
    st.error("No se pudo obtener el token. Revisá tus credenciales.")
