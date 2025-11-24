from flask import Flask, request, jsonify
import logging
import os

# Configuración básica de Flask y Logging
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
PORT = 5001 # Puerto para este servicio 

# Estados del protocolo MSI
# Estados del protocolo MSI
ESTADO_MODIFICADO = 'M' # Copia local modificada, solo un propietario
ESTADO_COMPARTIDO = 'S' # Copia limpia, múltiples propietarios
ESTADO_INVALIDO = 'I'  # El dato en la caché local no es válido

directorio_cache = {}

# Funciones de utilidad para notificar a otros clientes (simulación)
def notificar_invalidacion_a_otros(segmento_hash, cliente_actual):
    info_segmento = directorio_cache.get(segmento_hash, {'propietarios': []})
    clientes_a_invalidar = [c for c in info_segmento['propietarios'] if c != cliente_actual]
    
    if clientes_a_invalidar:
        logging.info(f"invalidacion a otros")
    return clientes_a_invalidar

@app.route('/api/estado/<segmento_hash>', methods=['GET'])
def obtener_estado(segmento_hash):
    info = directorio_cache.get(segmento_hash, {'estado': ESTADO_INVALIDO, 'propietarios': []})
    logging.info(f"Consulta estado: {segmento_hash}") 
    return jsonify(info), 200

@app.route('/api/solicitar_lectura/<segmento_hash>/<cliente_id>', methods=['POST'])
def solicitar_lectura(segmento_hash, cliente_id):
    logging.info(f"C: {cliente_id} solicita lectura")
    info_actual = directorio_cache.get(segmento_hash, {'estado': ESTADO_INVALIDO, 'propietarios': []})
    
    if info_actual['estado'] == ESTADO_MODIFICADO:
        logging.info(f"cambio de M a S (WB)")
    info_actual['estado'] = ESTADO_COMPARTIDO 
    
    if cliente_id not in info_actual['propietarios']:
        info_actual['propietarios'].append(cliente_id)
    directorio_cache[segmento_hash] = info_actual
    
    return jsonify({
        "status": "Acceso de lectura concedido", 
        "nuevo_estado": info_actual['estado'],
        "propietarios": info_actual['propietarios']
    }), 200

@app.route('/api/solicitar_escritura/<segmento_hash>/<cliente_id>', methods=['POST'])
def solicitar_escritura(segmento_hash, cliente_id):
    logging.info(f"C: {cliente_id} solicita escritura")
    
    # notifica e invalida otros clientes
    notificar_invalidacion_a_otros(segmento_hash, cliente_id)
    
    # actualza el directorio a estado modificado
    info_actual = {
        'estado': ESTADO_MODIFICADO, 
        'propietarios': [cliente_id]
    }
    
    directorio_cache[segmento_hash] = info_actual
    
    logging.info(f"nuevo propietario: {cliente_id}")
    
    return jsonify({
        "status": "Acceso de escritura concedido. Otras copias invalidadas", 
        "nuevo_estado": info_actual['estado'],
        "propietarios": info_actual['propietarios']
    }), 200

if __name__ == '__main__':
    logging.info(f"iniciando servicio coherencia")
    app.run(host='0.0.0.0', port=PORT)