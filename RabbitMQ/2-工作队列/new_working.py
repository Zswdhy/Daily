import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)  # 声明持久化队列 durable
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))

    time.sleep(str(body).count('.'))
    print(" [x] Done")

    ch.basic_ack(delivery_tag=method.delivery_tag)  # 发送响应


""" 公平调度，当前消费者执行完毕之后，才会分配新的任务 """
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback,auto_ack=False)

channel.start_consuming()
