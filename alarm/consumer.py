from __future__ import annotations

import json
import os
import time
import pika

ALARM_WARNING_QUEUE = "alarm.warning"
ALARM_CRITICAL_QUEUE = "alarm.critical"
ALARM_EXCHANGE = os.getenv("ALARM_EXCHANGE", "alarm-exchange")



def handle_alarm(alarm: dict, priority: str):

    alarm_id
    timestamp
    sensor_id
    sensor_type
    value
    severity
    source_timestamp
    message


def init_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=ALARM_CRITICAL_QUEUE, passive=True)
    channel.queue_declare(queue=ALARM_WARNING_QUEUE, passive=True)

    channel.queue_bind(exchange=ALARM_EXCHANGE, queue=ALARM_CRITICAL_QUEUE, routing_key="alarm.critical")
    channel.queue_bind(exchange=ALARM_EXCHANGE, queue=ALARM_WARNING_QUEUE, routing_key="alarm.warning")

    print("Alarm-Consumer gestartet!")

    try:
        while True:
            method, properties, body = channel.basic_get(
                queue=ALARM_CRITICAL_QUEUE,
                auto_ack=False
            )

            priority = "CRITICAL"

            if method is None:
                method, properties, body = channel.basic_get(
                    queue=ALARM_WARNING_QUEUE,
                    auto_ack=False
                )
                priority = "WARNING"

            if method is None:
                time.sleep(0.2)
                continue

            try:
                alarm = json.loads(body)
                handle_alarm(alarm, priority)

            except json.JSONDecodeError as exc:
                print(f"Alarmnachricht besitzt kein gültiges JSON-Format: {exc}")
                channel.basic_nack(
                    delivery_tag=method.delivery_tag,
                    requeue=False
                )
            except Exception as exc:
                print(f"Fehler bei der Alarmverarbeitung :{exc}")
                channel.basic_nack(
                    delivery_tag=method.delivery_tag,
                    requeue=True
                )

                time.sleep(1)
            else:
                channel.basic_ack(
                    delivery_tag=method.delivery_tag
                )
    except KeyboardInterrupt:
        print("Alarm-Consumer wird beendet.")
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    init_connection()
