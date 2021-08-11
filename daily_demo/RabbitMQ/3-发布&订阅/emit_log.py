import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')  # 声明扇形交换机

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
""" 发布消息，指定交换机，但不需要指定 routing——key """
channel.basic_publish(exchange='logs', routing_key='', body=message)

print(f" [x] Sent {message} ")
connection.close()
