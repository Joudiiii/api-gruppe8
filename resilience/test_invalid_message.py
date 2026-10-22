
import json
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)
channel = connection.channel()

message = {
    "sensor_id": "test_02",
    "timestamp": "2026-10-20T12:00:00",
    "type": "temperature",
    "value": "FEHLER"
}

channel.basic_publish(
    exchange="sensor-exchange",
    routing_key="sensor.temperature",
    body=json.dumps(message)
)

print("Ungültige Nachricht gesendet!")
connection.close()
