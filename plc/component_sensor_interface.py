"""
Компонент "Интерфейс датчиков"
Приём измерений датчиков, отправка их в шину,
а также отправка в SCADA тех измерений, которые
должны отправляться непосредственно, без обработки
"""

import requests
from flask import Flask, request, jsonify
import json
from OpenSSL import crypto
from base64 import b64encode
from uuid import uuid4
import datetime

host_name = "0.0.0.0"
port = 6064

app = Flask(__name__)  # create an app instance
CONTENT_HEADER = {"Content-Type": "application/json"}

from pykafka import KafkaClient
client = KafkaClient(hosts="158.160.98.150:9092")

topic_names = [ "pp11_sensors", "pp12_sensors", "pp13_sensors",
                "pp21_sensors", "pp22_sensors", "pp23_sensors"]
component_names = [ "pp11", "pp12", "pp13", "pp21", "pp22", "pp23" ]
topics = [client.topics[t_name] for t_name in topic_names]

key = """-----BEGIN PRIVATE KEY-----
MIIBVgIBADANBgkqhkiG9w0BAQEFAASCAUAwggE8AgEAAkEAnoNh1oK9AxfChWya
wxS1pkiU9MHr0YTEDNR0BY8mMQ3MUh0898I0SNBkcUb/9jLiFn0rOj4ogDOSJwfF
DWzyiwIDAQABAkB0HliotKNTxa8I4LNKnzwmcNs1pW1j0bdwkp3fiKr4mTTeDb0u
rWTpbbNxYoMN9fx63zI4QgaHbKdkALWYcOGhAiEAzFYsYc1Ef9whK4pE/Fhqgvmt
03cmGRcti8FsyVgf5FsCIQDGl0IAl2afkL5ndAQummQga8nyLcAA0DFK4yDErtzB
kQIhAMerTSMkmdL3H9KUAmUzYKErqZgBzdCmvXLbR5pX6pIRAiEAvlSbmmuAnK+h
/Q7RL0Ujb3s/Gk/EtELU61wRvM+GnjECIQDDXNUMy/fDYByAqP0hkzqlDNO0n2Cj
Qxlg1ca/U6AY1w==
-----END PRIVATE KEY-----"""

pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key)

# получение данных на вход
@app.route("/data_in", methods=['POST'])
def data():
    print("/data_in", request)
    content = request.json
    delivery_required = False
    msg = ''

    try:

        # отправка измерений, для которых не нужна
        # обработка в ПП, непосредственно на SCADA
        requests.post(
            "http://scada:6069/data_message_from_plc",
            data=json.dumps(content),
            headers=CONTENT_HEADER,
        )
    except Exception as e:
        pass # после тестирования закоммитить
        #error_message = f"malformed request {request.data}"
        #return error_message, 400

        # помещение сообщений кафку (главным для 2 версий по 3 экземпляра ПП)
    try:
        str_uid = str(uuid4())

        for i in range(6):
            body = {
                    "message_id": str_uid, # метка источника данных
                    "destination": component_names[i], 
                    "timestamp": datetime.datetime.now().isoformat(),
                    "message_type": "sensor",
                }
            body = json.dumps(body)
            sign = b64encode(crypto.sign(pkey, body.encode(), "sha256")).decode()
            data = {
                "body": body,
                "signature": sign,
                "source": "machine1" #TODO название машины подставлять
                } 
            topics[i].get_producer().produce(json.dumps(data).encode())
    except Exception as e:
        error_message = f"malformed request {request.data}"
        return error_message, 400

    return jsonify({"operation": "data_in", "status": True})

if __name__ == "__main__":
    app.run(port=port, host=host_name)