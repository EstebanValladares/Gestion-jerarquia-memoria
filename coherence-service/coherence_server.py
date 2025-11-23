from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/request_coherence', methods=['POST'])
def request_coherence():
    data = request.json
    hash_id = data.get('hash')
    client_id = data.get('client')
    action = data.get('action')

    return jsonify({
        'status': 'success',
        'hash': hash_id,
        'client': client_id,
        'action': action
    })

@app.route('/health', methods=['GET'])
def health_check():
    return "Coherence Service is up!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)