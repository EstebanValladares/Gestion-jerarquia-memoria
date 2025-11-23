from kax import acts
from pprint import pprint
import os
import time

# configuracines de inicio 
# configuracines de inicio 
# configuracines de inicio 

BASE_PATH = os.path.dirname(os.path.abspath(__file__)) # directorio actual
USER = os.getenv("USER") or "esteban" # dsuario por defecto

# carpetas de almacenamiento y consumo 
KAX_STORE_DIR = os.path.join(BASE_PATH, "kaxStore")
KAX_FILES_DIR = os.path.join(BASE_PATH, "kaxFiles")

#servidores del documento 
#servidores del documento 
#servidores del documento 

# configuracion de ACTS
acts.setUrl("http://148.247.201.210:5060/api") 

# almacenamiento servidor destino
acts.setStorageUrl("http://148.247.201.210:5070/api") 

# puerto del Broker de servidor de destino
acts.setBrokerPort(1883)

# broker pub/sub servidor de destino
acts.setBrokerUrl("148.247.201.226")

# archivo de prueba 
# archivo de prueba 
# archivo de prueba 

PDF_FILENAME = "f15mb.pdf"
SAVE_FILENAME = "nuevo_f15mb.pdf"
PDF_PATH_IN = os.path.join(KAX_STORE_DIR, PDF_FILENAME)
PDF_PATH_OUT = os.path.join(KAX_FILES_DIR, SAVE_FILENAME)

def kax_pdf():
    if not os.path.exists(PDF_PATH_IN):
        print("el archivo no existe")
        return

    star_time = time.time()
    file_hash = None

    #de disco a memoria
    #de disco a memoria
    #de disco a memoria

    try:
        print("cargando PDF en memoria")
        metadata = acts.loadRes(PDF_PATH_IN) 
        pprint(metadata)

        if (metadata and isinstance(metadata, dict) and 'resources' in metadata and isinstance(metadata['resources'], list) and len(metadata['resources']) > 0 and 'hash' in metadata['resources'][0]):
            file_hash = metadata['resources'][0]['hash']
            print("archivo cargado en memoria con hash")
        else:
            print("no se encontro el hash")
            return
    except Exception as e:
        print(f"error al cargar el archivo {e}")
        return
    
    #memoria a nube
    #memoria a nube
    #memoria a nube

    try:
        acts.uploadToCloudFromMemory(metadata)
        print("PDF subido a la nube")
    except Exception as e:
        print(f"error al subir el archivo a la nube {e}")
        return
    
    # eliminar de memoria compartida 
    # eliminar de memoria compartida 
    # eliminar de memoria compartida 

    try:
        acts.removeShm(file_hash)
        print("archivo eliminado de la memoria compartida local")
    except Exception as e:
        print("error al eliminar el archivo de la memoria")
        # La ejecución puede continuar, es un paso no crítico para el flujo principal.

    # descargar de nube a memoria compartida
    # descargar de nube a memoria compartida
    # descargar de nube a memoria compartida

    try:
        acts.downloadFromCloud(file_hash)
        print("descarga completa de la nube a memoria compartida")
    except Exception as e:
        print(f"error al descargar el archivo de la nube {e}")
        return
    
    # guardar en disco
    # guardar en disco
    # guardar en disco

    try:
        data = acts.getRes(file_hash)
        acts.saveFile("",data, PDF_PATH_OUT)
        print(f"se guardo el archivo")
        acts.removeShmFromCloud(file_hash)
        print("archivo eliminado")
    except Exception as e:
        print(f"error al guardar el archivo {e}")
        return
    
    end_time = time.time()
    tiempo_total = end_time - star_time
    print(f"tiempo de operacion {tiempo_total:.4f} en segundos")

    #comprobar que el archivo se guardo correctamente
    #comprobar que el archivo se guardo correctamente

if __name__ == "__main__":
    if not os.path.exists(KAX_STORE_DIR):
        os.makedirs(KAX_STORE_DIR)
        print(f"Carpeta creada: {KAX_STORE_DIR}")
    if not os.path.exists(KAX_FILES_DIR):
        os.makedirs(KAX_FILES_DIR)
        print(f"Carpeta creada: {KAX_FILES_DIR}")
    
    kax_pdf()