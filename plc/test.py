# pip install pykafka
from pykafka import KafkaClient

client = KafkaClient(hosts="158.160.98.150:9092")

topic = client.topics["monitor"]

producer = topic.get_producer()
consumer = topic.get_simple_consumer()

# отправить сообщение
# producer.produce(message)
producer.produce(b"1234")

# получить сообщение
# for message in consumer:
#     print(message.value.decode())