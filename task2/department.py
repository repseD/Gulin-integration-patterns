import sys
import pika

dept_name = sys.argv[1] if len(sys.argv) > 1 else "Отдел"
def handle_price(channel, method, properties, body):
    print(f"[{dept_name}] получил: {body.decode()}", flush=True)
    channel.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
channel = connection.channel()
channel.exchange_declare(exchange="price_changes", exchange_type="fanout")
result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange="price_changes", queue=queue_name)
channel.basic_consume(queue=queue_name, on_message_callback=handle_price)
print(f"[{dept_name}] подписан на изменения цены", flush=True)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    
connection.close()