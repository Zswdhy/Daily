import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))  # 建立链接

channel = connection.channel()

channel.queue_declare(queue='hello')  # 声明队列


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
