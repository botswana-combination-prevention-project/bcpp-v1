import pika
from django.core import serializers
from django.db.models import get_model

class MQConsumerController(object):
    def __init__(self, consumer, producer):
        self.producer = producer
        self.consumer = consumer
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.producer.ipaddress))
        channel = connection.channel()

        channel.exchange_declare(exchange='bhp', type='fanout')

        self.queue_name = self.consumer.name

        channel.queue_declare(queue=self.queue_name, durable=True)

        channel.queue_bind(exchange='bhp',queue=self.queue_name)

        channel.basic_consume(self.receive_message,
                      queue=self.queue_name,
                      no_ack=True)

        def receive_message(ch, method, properties, body):
            IncomingTransaction = get_model('bhp_sync', 'incomingtransaction')
#            transaction = serializers.deserialize("json",body)
            transaction = body
            IncomingTransaction.objects.create ( 
                                               pk = transaction.pk,
                                               tx_name = transaction.tx_name,
                                               tx_pk = transaction.tx_pk,
                                               tx = transaction.tx,
                                               timestamp = transaction.timestamp,
                                               producer = transaction.producer,
                                               action = transaction.action, 
                                               )

            
        def start_consuming():
            self.channel.start_consuming()