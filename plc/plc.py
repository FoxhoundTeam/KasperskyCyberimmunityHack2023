import base64
import hashlib
import json
import os
import random
import subprocess
import time
from urllib.request import urlopen
import requests
from flask import Flask, request, jsonify
from uuid import uuid4
import threading

host_name = "0.0.0.0"
port = 6064

app = Flask(__name__)  # create an app instance


max_speed = 2900
max_power = 19000
max_temperature = 45
min_speed = 333
min_power = 1000
min_temperature = 5

CONTENT_HEADER = {"Content-Type": "application/json"}
SCADA_SERVICE_ENDPOINT_URI = "http://scada:6069/service_message_from_plc"


@app.route("/upload_update", methods=['POST'])
def upload_update():
    """Обновление ПП
    """
    content = request.json
    # содержимое типа
    # { "update_files" : [update_file1, update_file2, update_file3 ] }
    try:
        for itm_name in request.json["update_files"]:
            response = requests.post(
                f"http://update_server:6067/upload_update/{itm_name}",
                headers=CONTENT_HEADER,
            )
            # TODO response = json.loads(response.content.decode('utf8'))
            if response['status'] is True:
                f = open(f"/storage/{itm_name}", "w")
                # TODOjson.dump(content, f)
                f.close()

                response_data = {"status": 'ok'}
                return jsonify(response_data)
            else:
                response_data = {"status": 'error',
                                 "details": "Не удалось получить обновления"}
                return jsonify(response_data)
    except Exception as e:
        error_message = f"malformed request {request.data}"
        return error_message, 400
    return jsonify({"status": 'error', "details": "Неизвестная ошибка"})


@app.route("/upload_settings", methods=['POST'])
def upload_settings():
    """Обновление настроек
    """
    content = request.json
    # содержимое типа
    # {
    #     "max_power_rpm" :
    #     "max_speed_rpm" :
    #     "max_temperature_deg" :
    #     "min_power_mwt":
    #     "min_speed_rpm":
    #     "min_temperature_deg":
    # }

    try:
        f = open("/storage/settings_plc.json", "w")
        # TODO проверка целостности и авторизации

        json.dump(content, f)
        f.close()

        # TODO синхронный запрос через кафку на обновление настроек

        response_data = {"status": 'ok', }
        return jsonify(response_data)
    except Exception as _:
        error_message = f"malformed request {request.data}"
        return error_message, 400
    return jsonify({"operation": "stopped"})


@app.route("/command", methods=['POST'])
def command():
    """
    Команда оператора
    """
    content = request.json
    try:
        if content['device'] == 'plc':
            if content['operation'] == 'reboot':
                with open("/storage/settings_plc.json", "r") as f:
                    data = json.load(f)
                    max_power = data['max_power']
                    max_speed = data['max_speed']
                    max_temperature = data['max_temperature']
                    min_power = data['min_power']
                    min_speed = data['min_speed']
                    min_temperature = data['min_temperature']
                print("Перезагружено")
        else:
            print('Команда отправлена на датчик')
            requests.post(
                "http://sensors:6068/" + content['operation'],
                data=json.dumps(content),
                headers=CONTENT_HEADER,
            )
    except Exception as _:
        print("[error] некорректная команда! ")
        return "Bad command detected", 400
    return jsonify({"operation": "start requested", "status": True})


# получение данных на вход
@app.route("/data_in", methods=['POST'])
def data():
    content = request.json
    delivery_required = False
    msg = ''

    try:

        # код, соответствующий компоненту "Интерфейс датчиков"
        # и отправляющий непосредственные измерения на SCADA
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

# @app.route("/key", methods=['POST'])
# def key():
#     content = request.json
#     global key, timestamp
#     try:
#         key = content['key']
#         timestamp = time.time()
#         print("[KEY] авторизован ключ")
#     except Exception as _:
#         error_message = f"malformed request {request.data}"
#         return error_message, 400
#     return jsonify({"operation": "key_in ", "status": True})


if __name__ == "__main__":
    app.run(port=port, host=host_name)
