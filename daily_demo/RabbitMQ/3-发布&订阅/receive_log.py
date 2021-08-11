import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

result = channel.queue_declare('', exclusive=True)  # exclusive 仅接受当前的链接
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)  # 消费者和交换机绑定

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {body.decode('utf-8')} ")


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
