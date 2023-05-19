import pika
import time
from LogCleaner import lemmatize_word
from UIPathApiCalls import ApiHandler
from S3_algorithm import S3Orchestrator
from DataBaseHandler import Database

class consumer:
    def __init__(self):
        self.orchestrator = ApiHandler()
        self.S3Algorithm = S3Orchestrator()
        self.Database = Database()
        credentials = pika.PlainCredentials('admin', '123456')
        self.parameters = pika.ConnectionParameters('192.168.145.128', 5672, '/', credentials)

    def recive(self,queue_name):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=self.callback)
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        message = body.decode("utf-8")
        queue_name = self.orchestrator.SendLogToOrchestration(message)
        preview = self.orchestrator.get_queue_items(queue_name)
        (terashhold,k) = self.Database.select_from_resault(message, preview)
        self.S3Algorithm.Run_S3_Orchestrator(preview,terashhold,k)
        #print("this message is in callback: ", message)
        #print("this message type in callback: ", type(message))
        #print(lemmatize_word(message.splitlines()[0]))
        #time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)