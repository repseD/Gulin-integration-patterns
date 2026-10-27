import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
channel = connection.channel()
channel.exchange_declare(exchange="price_changes", exchange_type="fanout")
prices = [
    "Цена за баррель: 82.50 USD",
    "Цена за баррель: 83.10 USD",
    "Цена за баррель: 81.95 USD",
]
time.sleep(10)
for price in prices:
    channel.basic_publish(exchange="price_changes", routing_key="", body=price)
    print(f"[Торговый отдел] опубликовал: {price}", flush=True)
    time.sleep(3)

connection.close()