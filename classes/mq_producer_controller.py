import pika
#from datetime import datetime
#from django.db.models import get_model
from django.core import serializers

class MQProducerController(object):
    
    def __init__(self):
        self._registry = []
        self._queues = {}
        #initialize rabbit-mq
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='bhp', type='fanout')
        
    def register(self, consumer):
        self._registry.append(consumer)
        self.channel.queue_declare(queue=consumer.name,durable=True)
        
    def send_message(self, outgoing_tx):
       # message = serializers.serialize("json", 
        #                [outgoing_tx,],
        #                ensure_ascii = False) 
        
        self.channel.basic_publish(exchange='bhp',routing_key='',body=outgoing_tx)