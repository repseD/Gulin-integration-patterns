import sys
import pika

crew_name = sys.argv[1] if len(sys.argv) > 1 else "Бригада"
def handle_request(channel, method, properties, body):
    print(f"[{crew_name}] взял заявку: {body.decode()}", flush=True)
    channel.basic_ack(delivery_tag=method.delivery_tag)
connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
channel = connection.channel()
channel.queue_declare(queue="well_repair_requests")
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="well_repair_requests", on_message_callback=handle_request)

print(f"[{crew_name}] на связи, жду заявки...", flush=True)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()