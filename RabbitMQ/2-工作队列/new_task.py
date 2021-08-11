import sys

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare('task_queue', durable=True)  # 声明队列,持久化声明

# sys.argv 获取 命令行的参数  如果不存在参数 默认为  Hello World
message = ''.join(sys.argv[1:]) or 'Hello World'

channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # 消息持久化声明
                      ))

print(f" [X] Sent {message}")
connection.close()
