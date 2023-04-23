"""
Компонент "Интерфейс датчиков"
Приём измерений датчиков, отправка их в шину,
а также отправка в SCADA тех измерений, которые
должны отправляться непосредственно, без обработки
"""

import requests
from flask import Flask, request, jsonify

host_name = "0.0.0.0"
port = 6064
SCADA_SERVICE_ENDPOINT_URI = "http://scada:6069/service_message_from_plc"

app = Flask(__name__)  # create an app instance
CONTENT_HEADER = {"Content-Type": "application/json"}

# получение данных на вход
@app.route("/data_in", methods=['POST'])
def data():
    content = request.json
    delivery_required = False
    msg = ''

    try:

        #TODO помещение сообщения с измерением в очередь

        # и отправка измерений, для которых не нужна
        # обработка в ПП, непосредственно на SCADA
        requests.post(
            "http://scada:6069/data_message_from_plc",
            data=json.dumps(content),
            headers=CONTENT_HEADER,
        )

        
        if content['device'] == 'temperature_device':

            if content['value'] > max_temperature or content['value'] < min_temperature:
                msg = "[Alarm] значения температуры выходят за установленные рамки!"
                delivery_required = True
                # TODO команда защиты

        if content['device'] == 'speed_device':
            if content['value'] > max_speed or content['value'] < min_speed:
                msg = "[Alarm] значения скорости выходят за установленные рамки!"
                delivery_required = True
        if content['device'] == 'power_device':
            if content['value'] > max_power or content['value'] < min_power:
                msg = "[Alarm] значения мощности выходят за установленные рамки!"
                delivery_required = True
        if delivery_required:
            data = {
                "device": content['device'],
                "value": msg
            }
            requests.post(
                SCADA_SERVICE_ENDPOINT_URI,
                data=json.dumps(data),
                headers=CONTENT_HEADER,
            )
    except Exception as _:
        error_message = f"malformed request {request.data}"
        return error_message, 400
    return jsonify({"operation": "data_in", "status": True})

if __name__ == "__main__":
    app.run(port=port, host=host_name)