import pika
class RabbitMQ:
    def __init__(self):
            credentials = pika.PlainCredentials('admin', '123456')
            self.parameters = pika.ConnectionParameters('192.168.145.128', 5672, '/', credentials)

    def sendtomq(self, exchange_name, routing_key, msg_body):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.confirm_delivery()
        channel.basic_publish(exchange=exchange_name,
                              routing_key=routing_key,
                              body=msg_body,
                              properties=pika.BasicProperties(content_type='text/plain',
                                                              delivery_mode=pika.DeliveryMode.Transient),
                              mandatory=True
                              )
        connection.close()