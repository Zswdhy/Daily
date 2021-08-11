import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # 建立链接

channel = connection.channel()

channel.queue_declare(queue='hello')  # 声明队列名称

channel.basic_publish(exchange='', routing_key='hello', body='1-hello world')  # 默认交换机【直接交换机】

print(' [X] Sent "1-hello world" ')

connection.close()
