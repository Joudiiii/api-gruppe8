import pika
import sys
import os

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)
channel = connection.channel()

channel.queue_declare(queue="test_crash", durable=True)

action = sys.argv[1]

if action == "send":
    channel.basic_publish(
        exchange="",
        routing_key="test_crash",
        body="Temperature: 25",
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print("Message sent")

else:
    method, properties, message = channel.basic_get(
        queue="test_crash",
        auto_ack=False
    )

    if method:
        print("Message:", message.decode())
        print("Redelivered:", method.redelivered)

        if action == "crash":
            print("Consumer crashes!", flush=True)
            os._exit(1)

        channel.basic_ack(method.delivery_tag)
        print("Message acknowledged (ACK).")

connection.close()
