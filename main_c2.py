# main_c2.py (Cliente 2)

from kax import acts
import os
import time
import logging
import requests 

BASE_PATH = os.path.dirname(os.path.abspath(__file__)) 
KAX_STORE_DIR = os.path.join(BASE_PATH, "kaxStore")
KAX_FILES_DIR = os.path.join(BASE_PATH, "kaxFiles")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URL_COHERENCE = "http://coherence-service:5001/api"
CLIENTE_ID = os.getenv("CLIENT_ID") or "C2"

# archivo para el nuevo hash compartido
HASH_FILE = os.path.join(KAX_FILES_DIR, "segmento_y.hash")

# espera y obtiene el hash creado por C1
# espera y obtiene el hash creado por C1
def obtener_hash_y(timeout=30):
    start_time = time.time()
    logging.info(f"[{CLIENTE_ID}] esperando hash de c1")
    
    # Bucle de espera (hasta 30 segundos)
    while not os.path.exists(HASH_FILE) and (time.time() - start_time) < timeout:
        time.sleep(1)
        
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            segmento_hash = f.read().strip()
        logging.info(f"[{CLIENTE_ID}] hash obtenido: {segmento_hash}")
        return segmento_hash
    else:
        logging.error(f"[{CLIENTE_ID}]hash no disponible")
        return None

def interactuar_con_coherencia(segmento_hash, operacion="LECTURA"):
    try:
        if operacion == "LECTURA":
            endpoint = f"{URL_COHERENCE}/solicitar_lectura/{segmento_hash}/{CLIENTE_ID}"
            response = requests.post(endpoint)
        elif operacion == "ESCRITURA":
            endpoint = f"{URL_COHERENCE}/solicitar_escritura/{segmento_hash}/{CLIENTE_ID}"
            response = requests.post(endpoint)
        else:
            return False

        if response.status_code == 200:
            logging.info(f"coherencia ok {operacion}") 
            return True
        else:
            logging.error(f"Error servicio de coherencia: {response.text}")
            return False
            
    except Exception as e:
        logging.error(f"No se pudo contactar al servicio de coherencia: {e}")
        return False

def logica_cliente_2():
    # --- MODIFICACIÓN CLAVE: OBTENER EL HASH REAL ---
    SEGMENTO_Y_HASH = obtener_hash_y()
    
    if not SEGMENTO_Y_HASH:
        return
    # -----------------------------------------------
    
    # 6. C2 genera un segmento de memoria
    logging.info(f"[{CLIENTE_ID}] preparando x2") 
    
    # 7. C2 obtiene los datos.
    logging.info(f"[{CLIENTE_ID}] solicitando lectura") 
    if interactuar_con_coherencia(SEGMENTO_Y_HASH, "LECTURA"):

        logging.info(f"[{CLIENTE_ID}] lectura y en x2 completada") 
    else:
        return

    time.sleep(1)
    
    # 8. C2 modifica los datos
    logging.info(f"[{CLIENTE_ID}] solicitando escritura") 
    if interactuar_con_coherencia(SEGMENTO_Y_HASH, "ESCRITURA"):
        logging.info(f"[{CLIENTE_ID}] modificacion x2/y realizada") 
    
if __name__ == "__main__":
    if not os.path.exists(KAX_STORE_DIR): os.makedirs(KAX_STORE_DIR)
    if not os.path.exists(KAX_FILES_DIR): os.makedirs(KAX_FILES_DIR)
    
    logica_cliente_2()