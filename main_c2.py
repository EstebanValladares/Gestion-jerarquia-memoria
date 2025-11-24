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
CLIENTE_ID = os.getenv("CLIENT_ID") or "C2" # Obtiene la ID del entorno (de docker-compose)

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
            logging.error(f"Error en servicio de coherencia: {response.text}")
            return False
            
    except Exception as e:
        logging.error(f"No se pudo contactar al servicio de coherencia: {e}")
        return False

def logica_cliente_2():
    SEGMENTO_Y_HASH = "hash_ejemplo_segmento_Y" 
    
    # C2 genera un segmento de memoria
    logging.info(f"[{CLIENTE_ID}] paso 6: preparando x2") 
    
    # C2 obtiene los datos.
    logging.info(f"[{CLIENTE_ID}] paso 7: solicitando lectura") 
    if interactuar_con_coherencia(SEGMENTO_Y_HASH, "LECTURA"):

        logging.info(f"[{CLIENTE_ID}] lectura y en x2 completada") 
    else:
        return

    time.sleep(1)
    
    # C2 modifica los datos
    logging.info(f"[{CLIENTE_ID}] paso 8: solicitando escritura") 
    if interactuar_con_coherencia(SEGMENTO_Y_HASH, "ESCRITURA"):
        logging.info(f"[{CLIENTE_ID}] modificacion x2/y realizada") 
    
if __name__ == "__main__":
    if not os.path.exists(KAX_STORE_DIR): os.makedirs(KAX_STORE_DIR)
    if not os.path.exists(KAX_FILES_DIR): os.makedirs(KAX_FILES_DIR)
    
    logica_cliente_2()