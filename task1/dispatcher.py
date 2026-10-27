import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
channel = connection.channel()
channel.queue_declare(queue="well_repair_requests")
requests = [
    "Скважина 101: заменить насос",
    "Скважина 102: утечка на устье",
    "Скважина 103: ревизия арматуры",
    "Скважина 104: не растёт давление",
    "Скважина 105: замена задвижки",
    "Скважина 106: проверить ШГН",
]
for text in requests:
    channel.basic_publish(exchange="", routing_key="well_repair_requests", body=text)
    print(f"[Диспетчер] отправил заявку: {text}", flush=True)
    time.sleep(2)
connection.close()
print("[Диспетчер] все заявки отправлены", flush=True)