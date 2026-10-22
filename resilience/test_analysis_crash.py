import os
from analysis import consumer

original = consumer.validate_reading

def crash(message):
    reading = original(message)
    print("Message received:", reading, flush=True)
    print("Consumer crashes before ACK!", flush=True)
    os._exit(1)

consumer.validate_reading = crash
consumer.run_consumer("temperature")
