"""
Компонент "Мажоритарная логика"

Сравнение параметров телеметрии, выдаваемых экземплярами ПП,
по мажоритарному принципу

Принятие решения о целостности данных и выдача на SCADA или ЧПИ оператора

Сравнение команд управления устройствами (включая защиту),
сформированных экземплярами ПП, принятие решения о целостности
данных по мажоритарному принципу и передача на устройство,
с подтверждением в SCADA и ЧМИ оператора
"""

import json
from OpenSSL import crypto
from base64 import b64encode
from uuid import uuid4
import datetime

# import queue
from collections import queue, deque
from pykafka import KafkaClient

CONTENT_HEADER = {"Content-Type": "application/json"}


class MajLogic:

    # msg_queue = queue.Queue(maxsize=20)
    client = KafkaClient(hosts="158.160.98.150:9092")
    topic = client.topics["component_maj_logic"] # топик для всех входящих (и управление, и показания)
    # topic_to_get_control = client.topics["component_maj_logic"]
    # topic_to_get_sensor = client.topics["component_maj_logic"]
    consumer = topic.get_simple_consumer()

    msg_deque = deque(maxlen=20)

    def maj_logic(self):
        # выборка трёх сообщений по uuid
        list_of_uuids = {}
        for msg in msg_deque:
            list_of_uuids[msg.id]
        list_of_uuids = {msg.id for } # создать list из uuid

        # определение типа сообщения
        message_id = "123456"
        msg_type = "control"
        if msg_type == "control":
            # отправка команды непосредственно на устройство
            requests.post(
                "http://scada:6069/data_message_from_plc",
                data=json.dumps({"status":"ok", "uuid": message_id}),
                headers=CONTENT_HEADER,
            )
        elif msg_type == "sensor":
            # отправка подтверждения команды отправителию по REST
            requests.post(
                "http://scada:6069/control_message_from_plc",
                data=json.dumps(content),
                headers=CONTENT_HEADER,
            )
        return

    def exec(self):
        while(True):
            #выгрузка сообщений из kafka в очередь triple voting над очередью
            for itm in consumer:
                message = json.loads(itm.value)
                self.msg_deque.append(message)
                consumer.commit_offsets()
                self.maj_logic()

            time.sleep(0.05) # ожидание, пока сообщений нет          
            
        return

if __name__ == "__main__":
    maj_logic = MajLogic()
    maj_logic.exec()