import uuid
import json
from confluent_kafka import Consumer
from confluent_kafka import Producer



class KafkaSyncRequest:

    def __init__(self):
        producer_request = Producer({
            'bootstrap.servers': 'mybroker'})
        producer_request.poll(0)
        return

    def produce(self, data, topic):
        
        producer_request.produce(topic, data.encode('utf-8'))

    def recovery_response(self, request_id):
        consumer = Consumer({'bootstrap.servers': 'mybroker',
                            'group.id': 'mygroup',
                            'auto.offset.reset': 'earliest'})

        consumer.subscribe(['response-topic'])

        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            
            msg = msg.value().decode('utf-8')
            msg = json.loads(msg)

            request_id_received = msg.get('request_id')

            if request_id == request_id_received:
                consumer.close()
                return msg
            
            produce(msg, 'response-topic')

if __name__=="__main__":

    request_id = str(uuid.uuid1())
    data_to_produce['request_id'] = request_id

    produce(data_to_produce)
    response = recovery_response(request_id)