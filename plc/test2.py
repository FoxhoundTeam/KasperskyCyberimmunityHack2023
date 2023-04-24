# pip install pyopenssl

import json
from OpenSSL import crypto
from base64 import b64encode
from uuid import uuid4
import datetime

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
str_uid = str(uuid4())
body = json.loads(
    {
        "message_id": str_uid,
        "destination": "text", # каждому компоненту дать имя
        "timestamp": datetime.datetime.now().isoformat(),
        "message_type": "text", # каждому типу сообщения дать имя
    })
sign = b64encode(crypto.sign(pkey, body.encode(), "sha256")).decode()
data = {
    "body": body, "signature": sign,
    "source": "machine1" #TODO название машины подставлять
    } 

from pykafka import KafkaClient
client = KafkaClient(hosts="158.160.98.150:9092")
topic = client.topics["monitor"]

producer = topic.get_producer()
consumer = topic.get_simple_consumer()

# отправить сообщение
# producer.produce(message)
# producer.produce(b"1234")
producer.produce(json.dumps(data).encode())

for message in consumer:
    data = json.loads(message.value.decode())
    print(data)
    if(data.get("message_id")==str_uid):
        print("!!!")
