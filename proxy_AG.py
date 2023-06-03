from flask import Flask, request
import requests
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

# URL del servidor de destino
target_server = "https://tutoacademy-ag-oadjztiq2a-uc.a.run.app"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # Construye la URL de destino
    target_url = target_server + '/' + path

    # Reenvía la solicitud al servidor de destino
    headers = {key: value for (key, value) in request.headers if key != 'Host'}
    response = requests.request(
        method=request.method,
        url=target_url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    # Construye la respuesta del servidor de destino
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    response_headers = [(name, value) for (name, value) in response.raw.headers.items()
                        if name.lower() not in excluded_headers]

    # Envía la respuesta al cliente
    return response.content, response.status_code, response_headers

if __name__ == '__main__':
    print("Running in port 8888")
    http_server = WSGIServer(('', 8888), app)
    http_server.serve_forever()
